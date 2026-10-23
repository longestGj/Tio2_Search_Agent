# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import imaplib
import email
from email.header import decode_header
import ssl
from config import get_config

def safe_decode(header_value):
    """安全解码邮件头字段"""
    if not header_value:
        return ""
    decoded_fragments = decode_header(header_value)
    result = []
    for text, encoding in decoded_fragments:
        if isinstance(text, bytes):
            result.append(text.decode(encoding or 'utf-8', errors='ignore'))
        else:
            result.append(text)
    return "".join(result)

def receive_test_email():
    # 1. 加载配置
    config = get_config()
    if not config:
        print("配置加载失败，请检查 .env 文件。")
        return False
        
    print(f"正在连接收信服务器 {config['imap_server']}:{config['imap_port']} ...")

    # 2. 建立加密连接
    try:
        context = ssl.create_default_context()
        with imaplib.IMAP4_SSL(config['imap_server'], config['imap_port'], ssl_context=context) as conn:
            print("连接服务器成功，正在进行登录认证...")
            conn.login(config['user'], config['password'])
            print("登录成功！正在检索收件箱...")

            # 选择收件箱 (只读模式以防止影响已读/未读状态)
            conn.select('INBOX', readonly=True)

            # 搜索所有邮件
            status, data = conn.search(None, 'ALL')
            email_ids = data[0].split()
            
            if not email_ids:
                print("您的收件箱里目前没有任何邮件！")
                return True

            print(f"收件箱内共有 {len(email_ids)} 封邮件。")
            
            # 取最后一封最新的邮件进行解析
            latest_id = email_ids[-1]
            print(f"正在拉取最新的一封邮件 (ID: {latest_id.decode()}) 原文进行解析...")
            
            status, fetch_data = conn.fetch(latest_id, '(RFC822)')
            raw_email = fetch_data[0][1]
            msg = email.message_from_bytes(raw_email)

            # 解码发件人和主题
            subject = safe_decode(msg['Subject'])
            sender = safe_decode(msg['From'])
            date_str = safe_decode(msg['Date'])

            print("\n" + "="*50)
            print("【最新邮件拉取成功】")
            print(f"发件人 : {sender}")
            print(f"主题   : {subject}")
            print(f"时间   : {date_str}")
            print("="*50 + "\n")
            print("收信 (IMAP) 功能验证完美通过！")
            return True

    except Exception as e:
        print(f"\n[收信失败] 连接或读取邮件异常: {e}")
        print("建议排查: 邮箱后台是否开启了 IMAP 协议权限。")
        
    return False

if __name__ == '__main__':
    receive_test_email()
