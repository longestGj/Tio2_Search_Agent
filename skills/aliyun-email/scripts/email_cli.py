# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 强制 stdout/stderr 为 UTF-8，避免 Windows PowerShell / cmd 的 GBK 控制台把中文输出乱码化
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        # 旧 Python（<3.7）或 stream 不支持 reconfigure 的场景
        pass

import argparse
import hashlib
import re
import smtplib
import imaplib
import email
import ssl
import time
import html
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.header import Header, decode_header, make_header
from email.utils import formataddr, getaddresses, make_msgid, formatdate
from config import get_config
from recv_email import safe_decode
from schedule_queue import (
    add_scheduled_email,
    cancel_scheduled_email,
    list_scheduled_emails,
    run_due_scheduled_emails,
)
from mailbox_read import (
    MailboxDiscoveryError,
    SentFilter,
    discover_sent_mailbox,
    list_sent_messages,
    parse_list_response,
)


def parse_addr_list(value):
    if not value:
        return []
    if isinstance(value, list):
        return [v.strip() for v in value if v and str(v).strip()]
    return [a.strip() for a in str(value).split(",") if a.strip()]


def all_recipients(to_addr, cc=None, bcc=None):
    recipients = parse_addr_list(to_addr)
    recipients.extend(parse_addr_list(cc))
    recipients.extend(parse_addr_list(bcc))
    return recipients


MESSAGE_ID_PATTERN = re.compile(r"^<[^<>\s]+>$")
REFERENCES_PATTERN = re.compile(r"^<[^<>\s]+>(?: +<[^<>\s]+>)*$")


def _validated_thread_headers(in_reply_to=None, references=None):
    if not in_reply_to and not references:
        return None, None
    if not in_reply_to or not references:
        raise ValueError("reply messages require both In-Reply-To and References")
    if not MESSAGE_ID_PATTERN.fullmatch(str(in_reply_to)):
        raise ValueError("invalid In-Reply-To header")
    if not REFERENCES_PATTERN.fullmatch(str(references)):
        raise ValueError("invalid References header")
    return str(in_reply_to), str(references)


def build_message(
    config,
    to_addr,
    subject,
    body,
    attachment_path=None,
    cc=None,
    bcc=None,
    in_reply_to=None,
    references=None,
):
    in_reply_to, references = _validated_thread_headers(in_reply_to, references)
    root = MIMEMultipart('related')
    root['Subject'] = Header(subject, 'utf-8')
    root['From'] = formataddr([config.get('sender_name', 'Ai Long | IKHLAS TITANIUM'), config['user']])
    root['To'] = to_addr
    if config.get('reply_to'):
        root['Reply-To'] = config['reply_to']
    cc_list = parse_addr_list(cc)
    bcc_list = parse_addr_list(bcc)
    if cc_list:
        root['Cc'] = ", ".join(cc_list)
    if bcc_list:
        root['Bcc'] = ", ".join(bcc_list)
    root['Message-id'] = make_msgid()
    root['Date'] = formatdate()
    if in_reply_to:
        root['In-Reply-To'] = in_reply_to
        root['References'] = references

    msg_alternative = MIMEMultipart('alternative')
    root.attach(msg_alternative)

    plain_text = body
    html_text = html.escape(body).replace('\n', '<br>')

    sig_path = config.get('signature_img')
    cid_name = "signature_image_v3"
    has_signature = False
    if sig_path and os.path.exists(sig_path):
        html_text = f"""
        <html>
            <body>
                <div style="font-family: Arial, sans-serif; font-size: 14px;">
                    {html_text}
                </div>
                <br><br>
                <div>
                    <img src="cid:{cid_name}" alt="Signature" style="max-width: 720px; width: 100%; height: auto; display: block;">
                </div>
            </body>
        </html>
        """
        has_signature = True

    msg_alternative.attach(MIMEText(plain_text, 'plain', 'utf-8'))
    msg_alternative.attach(MIMEText(html_text, 'html', 'utf-8'))

    if has_signature:
        with open(sig_path, 'rb') as f:
            img_data = f.read()
        msg_img = MIMEImage(img_data)
        msg_img.add_header('Content-ID', f'<{cid_name}>')
        msg_img.add_header('Content-Disposition', 'inline', filename=os.path.basename(sig_path))
        root.attach(msg_img)

    attachment_paths = (
        attachment_path
        if isinstance(attachment_path, (list, tuple))
        else [attachment_path]
        if attachment_path
        else []
    )
    for path in attachment_paths:
        if not os.path.exists(path):
            print(f"Error: 找不到指定的附件文件: {path}")
            sys.exit(1)
        filename = os.path.basename(path)
        with open(path, 'rb') as f:
            part = MIMEApplication(f.read())
        part.add_header('Content-Disposition', 'attachment', filename=Header(filename, 'utf-8').encode())
        root.attach(part)

    return root


def _normalized_body(value):
    return str(value or "").replace("\r\n", "\n").replace("\r", "\n").rstrip("\n")


def _plain_body(message):
    for part in message.walk():
        if part.get_content_type() != "text/plain":
            continue
        if part.get_content_disposition() == "attachment":
            continue
        payload = part.get_payload(decode=True)
        if payload is None:
            return str(part.get_payload() or "")
        return payload.decode(part.get_content_charset() or "utf-8", errors="replace")
    return ""


def message_matches_draft(message, to_addr, subject, expected_body):
    decoded_subject = str(make_header(decode_header(message.get("Subject", ""))))
    actual_to = {
        address.lower()
        for _name, address in getaddresses(message.get_all("To", []))
        if address
    }
    expected_to = {address.lower() for address in parse_addr_list(to_addr)}
    return (
        decoded_subject == subject
        and actual_to == expected_to
        and _normalized_body(_plain_body(message)) == _normalized_body(expected_body)
    )


def attachment_inventory(message):
    inventory = {}
    for part in message.walk():
        if part.get_content_disposition() != "attachment":
            continue
        filename = str(make_header(decode_header(part.get_filename() or "")))
        inventory[filename] = hashlib.sha256(part.get_payload(decode=True) or b"").hexdigest()
    return inventory

def send_mail_cli(args, account=None, *, config_override=None):
    config = config_override if config_override is not None else get_config(account)
    if not config:
        print("Error: 配置加载失败，请检查 .env。")
        sys.exit(1)
        
    msg = build_message(
        config, args.to, args.subject, args.body, args.attachment,
        cc=getattr(args, "cc", None), bcc=getattr(args, "bcc", None),
        in_reply_to=getattr(args, "in_reply_to", None),
        references=getattr(args, "references", None),
    )

    # 安全连接并发送
    try:
        context = ssl.create_default_context()
        context.set_ciphers('DEFAULT')
        with smtplib.SMTP_SSL(config['smtp_server'], config['smtp_port'], context=context, timeout=15) as client:
            client.login(config['user'], config['password'])
            refused = client.sendmail(
                config['user'],
                all_recipients(args.to, getattr(args, "cc", None), getattr(args, "bcc", None)),
                msg.as_string(),
            )
            extra = ""
            if getattr(args, "cc", None):
                extra += f" | 抄送: {args.cc}"
            print(
                f"Result: SMTP已处理 {args.to}{extra}；拒绝地址数 {len(refused)}。 "
                f"| Message-ID: {msg['Message-id']}"
            )
            return {
                'message_id': msg['Message-id'],
                'accepted': [a for a in all_recipients(args.to, getattr(args, 'cc', None),
                             getattr(args, 'bcc', None)) if a not in refused],
                'refused': {a: value[0] for a, value in refused.items()},
            }
    except Exception as e:
        if config_override is not None:
            raise  # Batch caller records only the safe exception type/status code.
        print(f"Error: 发信失败: {e}")
        sys.exit(1)


def auth_check_cli(account=None):
    """Authenticate to Aliyun SMTP without constructing or sending a message."""
    config = get_config(account)
    if not config:
        print("Error: 配置加载失败，请检查 .env。")
        return False

    try:
        context = ssl.create_default_context()
        context.set_ciphers('DEFAULT')
        with smtplib.SMTP_SSL(
            config['smtp_server'],
            config['smtp_port'],
            context=context,
            timeout=15,
        ) as client:
            client.login(config['user'], config['password'])
        print(f"Success: SMTP authentication succeeded for {config['user']}; no email was sent.")
        return True
    except smtplib.SMTPAuthenticationError:
        print(f"Error: SMTP authentication failed for {config['user']}.")
        return False
    except Exception as e:
        print(f"Error: SMTP authentication check failed for {config['user']}: {e}")
        return False

def save_draft_cli(args, account=None):
    config = get_config(account)
    if not config:
        print("Error: 配置加载失败，请检查 .env。")
        sys.exit(1)

    msg = build_message(
        config, args.to, args.subject, args.body, args.attachment,
        cc=getattr(args, "cc", None), bcc=getattr(args, "bcc", None),
        in_reply_to=getattr(args, "in_reply_to", None),
        references=getattr(args, "references", None),
    )
    draft_folder = "&g0l6Pw-"  # IMAP UTF-7 编码的「草稿」文件夹

    append_ok = False
    conn = None
    try:
        context = ssl.create_default_context()
        conn = imaplib.IMAP4_SSL(config['imap_server'], config['imap_port'], ssl_context=context)
        conn.login(config['user'], config['password'])
        st, data = conn.append(
            draft_folder,
            r'\Draft',
            imaplib.Time2Internaldate(time.time()),
            msg.as_string().encode('utf-8'),
        )
        if st != 'OK':
            raise imaplib.IMAP4.error(f"APPEND returned {st}: {data!r}")
        append_ok = True
        # APPEND 成功 → 草稿已存，剩余 logout/close 阶段阿里云常提前 RST/EOF，按非致命处理
        try:
            conn.logout()
        except Exception:
            pass
        try:
            conn.close()
        except Exception:
            pass
    except Exception as e:
        if not append_ok:
            print(f"Error: 存入草稿箱失败: {e}")
            sys.exit(1)
        # append 已成功，退出阶段 socket 早关属于服务端已知行为
        print(f"Warning: 草稿已存入，但 LOGOUT/CLOSE 阶段连接被服务端关闭（已知非致命，已忽略）: {e}")
    finally:
        # 兜底：contextlib 不再用，确保 socket 在 GC 时不再触发可见异常
        try:
            if conn is not None:
                conn.socket = None
        except Exception:
            pass

    cc_note = f" | 抄送: {args.cc}" if getattr(args, "cc", None) else ""
    print(f"Success: 邮件已成功存入草稿箱！收件人: {args.to}{cc_note} | 主题: {args.subject}")
    print("请在阿里云邮箱网页端的「草稿」文件夹中查看。")


def replace_draft_cli(args, account=None):
    config = get_config(account)
    if not config:
        print("Error: 配置加载失败，请检查 .env。")
        sys.exit(1)

    new_message = build_message(
        config, args.to, args.subject, args.body, args.attachment,
        cc=getattr(args, "cc", None), bcc=getattr(args, "bcc", None),
        in_reply_to=getattr(args, "in_reply_to", None),
        references=getattr(args, "references", None),
    )
    draft_folder = "&g0l6Pw-"
    conn = None
    append_ok = False
    old_uid = None
    try:
        context = ssl.create_default_context()
        conn = imaplib.IMAP4_SSL(
            config["imap_server"], config["imap_port"], ssl_context=context
        )
        conn.login(config["user"], config["password"])
        status, _ = conn.select(draft_folder, readonly=False)
        if status != "OK":
            raise imaplib.IMAP4.error("cannot open Drafts")

        status, data = conn.uid("search", None, "ALL")
        if status != "OK":
            raise imaplib.IMAP4.error("cannot search Drafts")
        matches = []
        for uid in (data[0] or b"").split():
            fetch_status, fetched = conn.uid("fetch", uid, "(BODY.PEEK[])")
            if fetch_status != "OK":
                continue
            raw = next(
                (item[1] for item in fetched if isinstance(item, tuple) and isinstance(item[1], bytes)),
                None,
            )
            if raw is None:
                continue
            candidate = email.message_from_bytes(raw)
            if message_matches_draft(
                candidate, args.to, args.subject, args.expected_old_body
            ):
                matches.append(uid)

        if len(matches) != 1:
            print(
                "Error: 草稿替换已停止：按收件人、主题和旧正文精确匹配到 "
                f"{len(matches)} 封，要求恰好 1 封。"
            )
            sys.exit(1)
        old_uid = matches[0]

        status, data = conn.append(
            draft_folder,
            r"\Draft",
            imaplib.Time2Internaldate(time.time()),
            new_message.as_string().encode("utf-8"),
        )
        if status != "OK":
            raise imaplib.IMAP4.error(f"APPEND returned {status}: {data!r}")
        append_ok = True

        status, data = conn.uid("store", old_uid, "+FLAGS.SILENT", r"(\Deleted)")
        if status != "OK":
            raise imaplib.IMAP4.error(f"STORE returned {status}: {data!r}")
        status, data = conn.uid("expunge", old_uid)
        if status != "OK":
            conn.uid("store", old_uid, "-FLAGS.SILENT", r"(\Deleted)")
            raise imaplib.IMAP4.error(f"UID EXPUNGE returned {status}: {data!r}")
    except SystemExit:
        raise
    except Exception as exc:
        if append_ok:
            print(
                "Error: 新草稿已写入，但旧草稿未能安全删除；草稿箱可能暂时有两个版本。"
            )
        print(f"Error: 替换草稿失败: {exc}")
        sys.exit(1)
    finally:
        try:
            if conn is not None:
                conn.logout()
        except Exception:
            pass

    print(
        "Success: 草稿已精确替换！"
        f"旧草稿 UID: {old_uid.decode('ascii')} | 收件人: {args.to} | 主题: {args.subject} | "
        f"新 Message-ID: {new_message['Message-id']}"
    )
    print("未调用 SMTP，邮件未发送。")


def draft_audit_cli(args, account=None):
    config = get_config(account)
    if not config:
        print("Error: 配置加载失败，请检查 .env。")
        sys.exit(1)
    expected_attachments = {}
    for item in args.expected_attachment or []:
        if "=" not in item:
            print("Error: --expected-attachment 必须使用 filename=sha256 格式。")
            sys.exit(1)
        filename, digest = item.rsplit("=", 1)
        expected_attachments[filename] = digest.lower()

    draft_folder = "&g0l6Pw-"
    matches = []
    try:
        context = ssl.create_default_context()
        with imaplib.IMAP4_SSL(
            config["imap_server"], config["imap_port"], ssl_context=context
        ) as conn:
            conn.login(config["user"], config["password"])
            status, _ = conn.select(draft_folder, readonly=True)
            if status != "OK":
                raise imaplib.IMAP4.error("cannot open Drafts read-only")
            status, data = conn.uid("search", None, "ALL")
            if status != "OK":
                raise imaplib.IMAP4.error("cannot search Drafts")
            for uid in (data[0] or b"").split():
                fetch_status, fetched = conn.uid("fetch", uid, "(BODY.PEEK[])")
                if fetch_status != "OK":
                    continue
                raw = next(
                    (item[1] for item in fetched if isinstance(item, tuple) and isinstance(item[1], bytes)),
                    None,
                )
                if raw is None:
                    continue
                candidate = email.message_from_bytes(raw)
                if message_matches_draft(
                    candidate, args.to, args.subject, args.expected_body
                ):
                    matches.append((uid, candidate))
    except Exception as exc:
        print(f"Error: 草稿只读复核失败: {exc}")
        sys.exit(1)

    if len(matches) != 1:
        print(f"Error: 草稿只读复核命中 {len(matches)} 封，要求恰好 1 封。")
        sys.exit(1)
    uid, candidate = matches[0]
    actual_attachments = attachment_inventory(candidate)
    if actual_attachments != expected_attachments:
        print(
            "Error: 草稿附件与预期不一致。"
            f"实际: {actual_attachments!r} | 预期: {expected_attachments!r}"
        )
        sys.exit(1)
    print(
        "Success: 草稿只读复核通过！"
        f"UID: {uid.decode('ascii')} | Message-ID: {candidate.get('Message-ID', '')} | "
        f"附件: {', '.join(actual_attachments)}"
    )
    print("正文、收件人、主题及附件哈希均匹配；未修改邮箱，未发送邮件。")

def schedule_mail_cli(args, account=None):
    task = add_scheduled_email(
        args.to, args.subject, args.body, args.at, args.attachment,
        cc=getattr(args, "cc", None), bcc=getattr(args, "bcc", None),
        account=account,
    )
    print(f"Success: 已加入定时发送队列")
    print(f"  ID      : {task['id']}")
    print(f"  收件人  : {task['to']}")
    if task.get("cc"):
        print(f"  抄送    : {task['cc']}")
    print(f"  主题    : {task['subject']}")
    print(f"  发送时间: {task['send_at']} (本地时间)")
    print(f"  队列文件: scheduled_emails.json")
    print("请确保本机定时任务会执行: python email_cli.py schedule-run")

    if args.also_draft:
        save_draft_cli(args, account)


def schedule_list_cli(args):
    tasks = list_scheduled_emails(status=args.status)
    if not tasks:
        print("定时队列中没有邮件。")
        return
    print(f"共 {len(tasks)} 条记录:\n")
    for t in tasks:
        print(f"[{t['status']}] ID={t['id']} | {t['send_at']} | To: {t['to']}")
        if t.get("cc"):
            print(f"    Cc: {t['cc']}")
        print(f"    Subject: {t['subject'][:60]}")
        if t.get("error"):
            print(f"    Error: {t['error']}")
        print("-" * 50)


def schedule_cancel_cli(args):
    if cancel_scheduled_email(args.id):
        print(f"Success: 已取消定时任务 {args.id}")
    else:
        print(f"Error: 未找到可取消的 pending 任务: {args.id}")
        sys.exit(1)


def schedule_run_cli(args):
    count = run_due_scheduled_emails(send_mail_cli)
    print(f"定时任务执行完成，本次发送 {count} 封。")

def receive_mail_cli(args, account=None):
    config = get_config(account)
    if not config:
        print("Error: 配置加载失败，请检查 .env。")
        sys.exit(1)
        
    limit = args.limit
    save_dir = args.save_dir

    if save_dir and not os.path.exists(save_dir):
        os.makedirs(save_dir)

    try:
        context = ssl.create_default_context()
        with imaplib.IMAP4_SSL(config['imap_server'], config['imap_port'], ssl_context=context) as conn:
            conn.login(config['user'], config['password'])
            conn.select('INBOX', readonly=True)
            status, data = conn.search(None, 'ALL')
            email_ids = data[0].split()
            
            if not email_ids:
                print("No emails found in INBOX.")
                return
                
            count = min(len(email_ids), limit)
            target_ids = email_ids[-count:]
            print(f"成功获取到最近的 {count} 封邮件：\n")
            
            for idx, num in enumerate(reversed(target_ids)):
                status, fetch_data = conn.fetch(num, '(RFC822)')
                raw_email = fetch_data[0][1]
                msg = email.message_from_bytes(raw_email)
                
                # 获取 UID
                _, uid_data = conn.fetch(num, 'UID')
                uid = uid_data[0].decode('utf-8').split()[2].replace(')', '')
                
                subject = safe_decode(msg['Subject'])
                sender = safe_decode(msg['From'])
                date_str = safe_decode(msg['Date'])
                
                print(f"[{idx+1}] UID: {uid} | 日期: {date_str}")
                print(f"    发件人: {sender}")
                print(f"    主题  : {subject}")
                
                if save_dir:
                    safe_subject = "".join([c if c.isalnum() or c in (' ', '.', '_') else '_' for c in subject])
                    eml_path = os.path.join(save_dir, f"email_{uid}_{safe_subject[:20]}.eml")
                    with open(eml_path, 'wb') as f:
                        f.write(raw_email)
                    print(f"    -> 已保存至: {eml_path}")
                print("-" * 50)
    except Exception as e:
        print(f"Error: 收信失败: {e}")
        sys.exit(1)

def _iso_date(value):
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("date must use YYYY-MM-DD") from exc


def _positive_int(value):
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("value must be a positive integer") from exc
    if parsed < 1:
        raise argparse.ArgumentTypeError("value must be a positive integer")
    return parsed


def _imap_config(account):
    config = get_config(account)
    if not config:
        raise ValueError("email configuration could not be loaded")
    return config


def folder_list_cli(args, account=None):
    try:
        config = _imap_config(account)
        context = ssl.create_default_context()
        with imaplib.IMAP4_SSL(
            config["imap_server"], config["imap_port"], ssl_context=context
        ) as conn:
            conn.login(config["user"], config["password"])
            status, folder_lines = conn.list()
            if status != "OK":
                raise ValueError(f"IMAP LIST failed: {status} {folder_lines!r}")
            sent = discover_sent_mailbox(folder_lines or [])
            mailboxes = [
                parse_list_response(line) for line in (folder_lines or []) if line is not None
            ]
        print(f"Account: {config['user']}")
        for mailbox in mailboxes:
            marker = " [Sent]" if mailbox.name == sent.name else ""
            flags = " ".join(mailbox.flags) or "(none)"
            print(f"- {mailbox.name}{marker} | flags: {flags}")
    except Exception as exc:
        print(f"Error: unable to list IMAP folders: {exc}")
        sys.exit(1)


def _print_sent_messages(messages, account_user, mailbox_name):
    print(f"Account: {account_user}")
    print(f"Sent mailbox: {mailbox_name}")
    print(f"Matched: {len(messages)}")
    for index, message in enumerate(messages, start=1):
        date_value = message.date_raw or "(unparseable/missing)"
        print(f"[{index}] UID: {message.uid} | Date: {date_value}")
        print(f"    From      : {message.from_}")
        print(f"    To        : {message.to}")
        print(f"    Cc        : {message.cc}")
        print(f"    Subject   : {message.subject}")
        print(f"    Message-ID: {message.message_id}")
        if message.eml_path:
            print(f"    EML       : {message.eml_path}")
        print("-" * 50)


def _sent_query_cli(args, account, filters):
    try:
        config = _imap_config(account)
        context = ssl.create_default_context()
        with imaplib.IMAP4_SSL(
            config["imap_server"], config["imap_port"], ssl_context=context
        ) as conn:
            conn.login(config["user"], config["password"])
            status, folder_lines = conn.list()
            if status != "OK":
                raise ValueError(f"IMAP LIST failed: {status} {folder_lines!r}")
            sent_mailbox = discover_sent_mailbox(folder_lines or [])
            messages = list_sent_messages(
                conn,
                sent_mailbox,
                limit=args.limit,
                filters=filters,
                save_dir=getattr(args, "save_dir", None),
            )
        _print_sent_messages(messages, config["user"], sent_mailbox.name)
        return messages
    except (MailboxDiscoveryError, ValueError, imaplib.IMAP4.error, OSError) as exc:
        print(f"Error: unable to query Sent mailbox: {exc}")
        sys.exit(1)


def sent_list_cli(args, account=None):
    return _sent_query_cli(args, account, SentFilter())


def sent_search_cli(args, account=None):
    if args.since and args.before and args.since >= args.before:
        print("Error: --since must be earlier than --before")
        sys.exit(1)
    return _sent_query_cli(
        args,
        account,
        SentFilter(
            since=args.since,
            before=args.before,
            recipient=args.recipient,
            subject=args.subject,
            message_id=args.message_id,
        ),
    )


def _add_mail_args(parser):
    parser.add_argument("--to", required=True, help="主送收件人（多个用逗号分隔）")
    parser.add_argument("--cc", help="抄送（多个邮箱用逗号分隔）")
    parser.add_argument("--bcc", help="密送（多个邮箱用逗号分隔）")
    parser.add_argument("--subject", required=True, help="邮件主题")
    parser.add_argument("--body", required=True, help="邮件正文")
    parser.add_argument(
        "--attachment",
        action="append",
        help="可选：本地附件文件路径；多个附件可重复使用该参数",
    )
    parser.add_argument("--in-reply-to", help="线程回复的客户邮件 Message-ID")
    parser.add_argument("--references", help="线程 References，按顺序用空格分隔 Message-ID")


def main():
    parser = argparse.ArgumentParser(description="阿里云企业邮箱命令行工具 (Aliyun Email CLI)")
    parser.add_argument(
        "--account",
        default=None,
        help="账号标识，加载 .env.<account> 配置文件（如 --account mytio2）。"
             "不加此参数则使用默认 .env。",
    )
    subparsers = parser.add_subparsers(dest="command", required=True, help="可执行的操作命令")

    subparsers.add_parser("auth-check", help="仅验证SMTP登录，不发送邮件")

    # send 子命令
    send_parser = subparsers.add_parser("send", help="发送邮件")
    _add_mail_args(send_parser)

    draft_parser = subparsers.add_parser("draft", help="保存邮件到草稿箱")
    _add_mail_args(draft_parser)

    draft_replace_parser = subparsers.add_parser(
        "draft-replace", help="精确匹配旧草稿后替换；不会发送邮件"
    )
    _add_mail_args(draft_replace_parser)
    draft_replace_parser.add_argument(
        "--expected-old-body", required=True, help="用于精确匹配待替换草稿的旧纯文本正文"
    )

    draft_audit_parser = subparsers.add_parser(
        "draft-audit", help="只读复核一封草稿的正文和附件哈希"
    )
    draft_audit_parser.add_argument("--to", required=True)
    draft_audit_parser.add_argument("--subject", required=True)
    draft_audit_parser.add_argument("--expected-body", required=True)
    draft_audit_parser.add_argument(
        "--expected-attachment",
        action="append",
        help="可重复；格式 filename=sha256",
    )

    sched_parser = subparsers.add_parser("schedule", help="加入本地定时发送队列")
    _add_mail_args(sched_parser)
    sched_parser.add_argument("--at", required=True, help="发送时间，如 2026-06-11 09:00")
    sched_parser.add_argument(
        "--also-draft",
        action="store_true",
        help="同时存入阿里云草稿箱（便于网页端预览；不会启用网页定时）",
    )

    sched_list = subparsers.add_parser("schedule-list", help="查看定时发送队列")
    sched_list.add_argument(
        "--status",
        choices=["pending", "sent", "failed", "cancelled"],
        help="按状态过滤",
    )

    sched_cancel = subparsers.add_parser("schedule-cancel", help="取消 pending 定时任务")
    sched_cancel.add_argument("--id", required=True, help="任务 ID")

    subparsers.add_parser("schedule-run", help="发送所有已到期的定时邮件（供计划任务调用）")

    # receive 子命令
    recv_parser = subparsers.add_parser("receive", help="收取并查看邮件")
    recv_parser.add_argument("--limit", type=int, default=1, help="查看最新邮件的数量 (默认 1)")
    recv_parser.add_argument("--save-dir", help="可选：将拉取的邮件保存为 .eml 文件的本地文件夹路径")

    subparsers.add_parser(
        "folder-list", help="List IMAP folders and identify the Sent mailbox (read-only)"
    )

    sent_list_parser = subparsers.add_parser(
        "sent-list", help="List recent server-side Sent messages (read-only)"
    )
    sent_list_parser.add_argument("--limit", type=_positive_int, default=20)
    sent_list_parser.add_argument("--save-dir", help="Optional directory for matched EML files")

    sent_search_parser = subparsers.add_parser(
        "sent-search", help="Search server-side Sent message metadata (read-only)"
    )
    sent_search_parser.add_argument("--since", type=_iso_date, help="Inclusive date, YYYY-MM-DD")
    sent_search_parser.add_argument("--before", type=_iso_date, help="Exclusive date, YYYY-MM-DD")
    sent_search_parser.add_argument("--recipient", help="Case-insensitive To/Cc substring")
    sent_search_parser.add_argument("--subject", help="Case-insensitive Subject substring")
    sent_search_parser.add_argument("--message-id", help="Exact Message-ID, case-insensitive")
    sent_search_parser.add_argument("--limit", type=_positive_int, default=100)
    sent_search_parser.add_argument("--save-dir", help="Optional directory for matched EML files")

    args = parser.parse_args()
    account = getattr(args, "account", None)

    if args.command == "auth-check":
        if not auth_check_cli(account):
            sys.exit(1)
    elif args.command == "send":
        send_mail_cli(args, account)
    elif args.command == "draft":
        save_draft_cli(args, account)
    elif args.command == "draft-replace":
        replace_draft_cli(args, account)
    elif args.command == "draft-audit":
        draft_audit_cli(args, account)
    elif args.command == "schedule":
        schedule_mail_cli(args, account)
    elif args.command == "schedule-list":
        schedule_list_cli(args)
    elif args.command == "schedule-cancel":
        schedule_cancel_cli(args)
    elif args.command == "schedule-run":
        schedule_run_cli(args)
    elif args.command == "receive":
        receive_mail_cli(args, account)
    elif args.command == "folder-list":
        folder_list_cli(args, account)
    elif args.command == "sent-list":
        sent_list_cli(args, account)
    elif args.command == "sent-search":
        sent_search_cli(args, account)

if __name__ == '__main__':
    main()
