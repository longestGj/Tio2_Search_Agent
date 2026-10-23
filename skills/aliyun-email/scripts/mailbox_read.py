# -*- coding: utf-8 -*-
"""Read-only IMAP mailbox discovery and Sent-message queries."""

from dataclasses import dataclass
from datetime import date, datetime
import email
from email.utils import parsedate_to_datetime
import os
import re

from recv_email import safe_decode


class MailboxDiscoveryError(ValueError):
    """Raised when a Sent mailbox cannot be identified safely."""


@dataclass(frozen=True)
class MailboxInfo:
    flags: tuple[str, ...]
    delimiter: str | None
    name: str


@dataclass(frozen=True)
class SentFilter:
    since: date | None = None
    before: date | None = None
    recipient: str | None = None
    subject: str | None = None
    message_id: str | None = None


@dataclass(frozen=True)
class SentMessage:
    uid: str
    date: datetime | None
    date_raw: str
    from_: str
    to: str
    cc: str
    subject: str
    message_id: str
    eml_path: str | None = None


_LIST_RE = re.compile(
    r'^\((?P<flags>[^)]*)\)\s+(?P<delimiter>NIL|"(?:\\.|[^"])*")\s+(?P<name>.+)$',
    re.IGNORECASE,
)

_COMMON_SENT_NAMES = {
    "sent",
    "sent messages",
    "sent items",
    "已发送",
    "&xfjt0zab-",  # Aliyun modified UTF-7 name for 已发送.
}


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] == '"':
        value = value[1:-1]
        value = value.replace(r'\"', '"').replace(r'\\', '\\')
    return value


def parse_list_response(line: bytes | str) -> MailboxInfo:
    text = line.decode("ascii", errors="replace") if isinstance(line, bytes) else str(line)
    match = _LIST_RE.match(text.strip())
    if not match:
        raise MailboxDiscoveryError(f"invalid IMAP LIST response: {text!r}")
    flags = tuple(part for part in match.group("flags").split() if part)
    delimiter_text = match.group("delimiter")
    delimiter = None if delimiter_text.upper() == "NIL" else _unquote(delimiter_text)
    return MailboxInfo(flags=flags, delimiter=delimiter, name=_unquote(match.group("name")))


def discover_sent_mailbox(lines: list[bytes | str]) -> MailboxInfo:
    mailboxes = [parse_list_response(line) for line in lines if line is not None]
    special_use = [
        mailbox
        for mailbox in mailboxes
        if any(flag.casefold() == r"\sent" for flag in mailbox.flags)
    ]
    if len(special_use) == 1:
        return special_use[0]
    if len(special_use) > 1:
        names = ", ".join(mailbox.name for mailbox in special_use)
        raise MailboxDiscoveryError(f"Sent mailbox is ambiguous: {names}")

    named = [
        mailbox
        for mailbox in mailboxes
        if mailbox.name.strip().casefold() in _COMMON_SENT_NAMES
    ]
    if len(named) == 1:
        return named[0]
    if len(named) > 1:
        names = ", ".join(mailbox.name for mailbox in named)
        raise MailboxDiscoveryError(f"Sent mailbox is ambiguous: {names}")
    raise MailboxDiscoveryError("Sent mailbox not found")


def _message_date(value: str) -> datetime | None:
    if not value:
        return None
    try:
        return parsedate_to_datetime(value)
    except (TypeError, ValueError, OverflowError):
        return None


def _matches(message: SentMessage, filters: SentFilter) -> bool:
    if filters.since or filters.before:
        if message.date is None:
            return False
        message_day = message.date.date()
        if filters.since and message_day < filters.since:
            return False
        if filters.before and message_day >= filters.before:
            return False
    if filters.recipient:
        recipients = f"{message.to}, {message.cc}".casefold()
        if filters.recipient.casefold() not in recipients:
            return False
    if filters.subject and filters.subject.casefold() not in message.subject.casefold():
        return False
    if filters.message_id and filters.message_id.casefold() != message.message_id.casefold():
        return False
    return True


def _raw_message(fetch_data) -> bytes:
    for item in fetch_data or []:
        if isinstance(item, tuple) and len(item) >= 2 and isinstance(item[1], bytes):
            return item[1]
    raise ValueError("IMAP FETCH response did not contain a message")


def list_sent_messages(
    conn,
    mailbox: MailboxInfo | str,
    limit: int,
    filters: SentFilter,
    save_dir: str | None = None,
) -> list[SentMessage]:
    if limit < 1:
        raise ValueError("limit must be at least 1")
    mailbox_name = mailbox.name if isinstance(mailbox, MailboxInfo) else mailbox
    status, data = conn.select(mailbox_name, readonly=True)
    if status != "OK":
        raise ValueError(f"unable to select Sent mailbox: {status} {data!r}")
    status, data = conn.uid("SEARCH", None, "ALL")
    if status != "OK":
        raise ValueError(f"unable to search Sent mailbox: {status} {data!r}")
    uids = data[0].split() if data and data[0] else []
    results: list[SentMessage] = []
    if save_dir:
        os.makedirs(save_dir, exist_ok=True)

    for uid_bytes in reversed(uids):
        uid = uid_bytes.decode("ascii") if isinstance(uid_bytes, bytes) else str(uid_bytes)
        status, fetch_data = conn.uid("FETCH", uid, "(BODY.PEEK[])")
        if status != "OK":
            raise ValueError(f"unable to fetch Sent UID {uid}: {status} {fetch_data!r}")
        raw = _raw_message(fetch_data)
        parsed = email.message_from_bytes(raw)
        date_raw = safe_decode(parsed.get("Date"))
        message = SentMessage(
            uid=uid,
            date=_message_date(date_raw),
            date_raw=date_raw,
            from_=safe_decode(parsed.get("From")),
            to=safe_decode(parsed.get("To")),
            cc=safe_decode(parsed.get("Cc")),
            subject=safe_decode(parsed.get("Subject")),
            message_id=safe_decode(parsed.get("Message-ID")),
        )
        if not _matches(message, filters):
            continue
        if save_dir:
            eml_path = os.path.join(save_dir, f"sent_{uid}.eml")
            with open(eml_path, "wb") as eml_file:
                eml_file.write(raw)
            message = SentMessage(**{**message.__dict__, "eml_path": eml_path})
        results.append(message)
        if len(results) >= limit:
            break
    return results
