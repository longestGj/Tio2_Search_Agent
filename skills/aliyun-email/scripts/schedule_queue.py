# -*- coding: utf-8 -*-
"""Local scheduled email queue (SMTP send at due time)."""
import json
import os
import uuid
from datetime import datetime, timedelta

MAX_SCHEDULE_DAYS = 30
QUEUE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scheduled_emails.json")


def _load_queue():
    if not os.path.exists(QUEUE_FILE):
        return []
    with open(QUEUE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, list) else []


def _save_queue(items):
    with open(QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)


def parse_send_at(value):
    """Parse 'YYYY-MM-DD HH:MM' or ISO datetime string (local time)."""
    value = value.strip()
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    raise ValueError(f"无法解析时间: {value}，请使用 YYYY-MM-DD HH:MM")


def validate_send_at(send_at):
    now = datetime.now()
    if send_at <= now:
        raise ValueError("定时发送时间必须晚于当前时间。")
    if send_at > now + timedelta(days=MAX_SCHEDULE_DAYS):
        raise ValueError(f"定时发送时间不能超过 {MAX_SCHEDULE_DAYS} 天（与阿里云网页端一致）。")


def add_scheduled_email(to_addr, subject, body, send_at_str, attachment=None, cc=None, bcc=None, account=None):
    send_at = parse_send_at(send_at_str)
    validate_send_at(send_at)

    task = {
        "id": uuid.uuid4().hex[:12],
        "to": to_addr,
        "cc": cc,
        "bcc": bcc,
        "subject": subject,
        "body": body,
        "attachment": attachment,
        "send_at": send_at.strftime("%Y-%m-%d %H:%M:%S"),
        "status": "pending",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "sent_at": None,
        "error": None,
        "account": account,  # which .env.<account> to use at send time
    }
    queue = _load_queue()
    queue.append(task)
    _save_queue(queue)
    return task


def list_scheduled_emails(status=None):
    queue = _load_queue()
    if status:
        queue = [t for t in queue if t.get("status") == status]
    return sorted(queue, key=lambda t: t.get("send_at", ""))


def cancel_scheduled_email(task_id):
    queue = _load_queue()
    found = False
    for task in queue:
        if task.get("id") == task_id and task.get("status") == "pending":
            task["status"] = "cancelled"
            task["error"] = "cancelled by user"
            found = True
            break
    if not found:
        return False
    _save_queue(queue)
    return True


def run_due_scheduled_emails(send_func):
    """Send all pending tasks whose send_at <= now. send_func(args) performs SMTP send."""
    queue = _load_queue()
    now = datetime.now()
    sent_count = 0

    for task in queue:
        if task.get("status") != "pending":
            continue
        due = parse_send_at(task["send_at"])
        if due > now:
            continue

        class Args:
            pass

        args = Args()
        args.to = task["to"]
        args.subject = task["subject"]
        args.body = task["body"]
        args.attachment = task.get("attachment")
        args.cc = task.get("cc")
        args.bcc = task.get("bcc")

        # Set account env so get_config() picks the right .env.<account>
        saved_env_path = os.environ.get("ALIYUN_ENV_PATH", "")
        if task.get("account"):
            os.environ["ALIYUN_ENV_PATH"] = task["account"]
        else:
            os.environ.pop("ALIYUN_ENV_PATH", None)

        try:
            send_func(args)
            task["status"] = "sent"
            task["sent_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            task["error"] = None
            sent_count += 1
        except SystemExit:
            task["status"] = "failed"
            task["error"] = "send exited with error"
        except Exception as e:
            task["status"] = "failed"
            task["error"] = str(e)
        finally:
            if saved_env_path:
                os.environ["ALIYUN_ENV_PATH"] = saved_env_path
            else:
                os.environ.pop("ALIYUN_ENV_PATH", None)

    _save_queue(queue)
    return sent_count
