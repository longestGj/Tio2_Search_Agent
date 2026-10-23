# -*- coding: utf-8 -*-
import os

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANONICAL_ENV = r"D:\\05CursorForTio2\\01ForTradeofTio2\\05Agent邮箱\\.env"


def load_env(account=None):
    """Load .env for the specified account.

    If account is None → uses default .env search order.
    If account is set → loads <SKILL_ROOT>/.env.<account>  (e.g. .env.account2)
    Also checks ALIYUN_ENV_PATH env var — can be a full path OR an account name.
    """
    # Env-var override: full path wins; bare name → resolve to .env.<name>
    env_path_override = os.environ.get("ALIYUN_ENV_PATH")
    if env_path_override:
        if os.path.exists(env_path_override):
            return _do_load_env(env_path_override)
        # Treat as account name and resolve to SKILL_ROOT/.env.<name>
        resolved = os.path.join(SKILL_ROOT, f".env.{env_path_override}")
        if os.path.exists(resolved):
            return _do_load_env(resolved)
        # Also try canonical dir
        canonical_dir = os.path.dirname(CANONICAL_ENV)
        resolved2 = os.path.join(canonical_dir, f".env.{env_path_override}")
        if os.path.exists(resolved2):
            return _do_load_env(resolved2)
        print(f"警告: ALIYUN_ENV_PATH='{env_path_override}' 对应文件不存在。")
        return False

    if account:
        account_env = os.path.join(SKILL_ROOT, f".env.{account}")
        if os.path.exists(account_env):
            return _do_load_env(account_env)
        # Fallback: also check canonical dir
        canonical_dir = os.path.dirname(CANONICAL_ENV)
        account_env2 = os.path.join(canonical_dir, f".env.{account}")
        if os.path.exists(account_env2):
            return _do_load_env(account_env2)
        print(f"警告: 账号 '{account}' 的配置文件不存在: {account_env}")
        return False

    search_paths = [
        os.path.join(os.getcwd(), ".env"),
        os.path.join(SKILL_ROOT, ".env"),
        os.path.join(os.path.dirname(__file__), ".env"),
        CANONICAL_ENV,
    ]
    env_path = next((p for p in search_paths if os.path.exists(p)), None)
    if not env_path:
        print("警告: 未找到 .env。请配置邮箱项目或 skill 目录下的 .env。")
        return False
    return _do_load_env(env_path)


def _do_load_env(env_path):
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, val = line.split("=", 1)
                os.environ[key.strip()] = val.strip()
    return True


def get_config(account=None):
    if not load_env(account):
        return None
    user = os.environ.get("ALIYUN_EMAIL_USER")
    password = os.environ.get("ALIYUN_EMAIL_PASS")
    receiver = os.environ.get("ALIYUN_TEST_RECEIVER")
    if not user or "your_username" in user:
        print("错误: 请在 .env 中填写真实的阿里云邮箱账号。")
        return None
    if not password or "your_client" in password:
        print("错误: 请在 .env 中填写客户端专属密码。")
        return None
    if not receiver or "receiver@example.com" in receiver:
        receiver = user
    # Per-account overrides via env vars (set in .env.<account>)
    sig_img = os.environ.get("ALIYUN_SIGNATURE_IMG") or os.path.join(SKILL_ROOT, "assets", "signature_ikhlas_titanium_email.png")
    sender_name = os.environ.get("ALIYUN_SENDER_NAME") or "Ai Long | IKHLAS TITANIUM"
    return {
        "user": user,
        "password": password,
        "receiver": receiver,
        "smtp_server": "smtp.qiye.aliyun.com",
        "imap_server": "imap.qiye.aliyun.com",
        "smtp_port": 465,
        "imap_port": 993,
        "signature_img": sig_img,
        "sender_name": sender_name,
    }
