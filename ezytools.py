```python
import os
import random
import logging
from datetime import datetime, timezone
import time
import re
import shlex
# ==================================================
# EZYBOT UTILITIES
# ==================================================

logging.basicConfig(
    level=logging.INFO,
    format="[ezybot] %(levelname)s: %(message)s"
)

logger = logging.getLogger("ezybot")




# ==================================================
# CONFIGURATION
# ==================================================

def get_owner_id():
    """Get the bot owner's user ID from an environment variable."""
    return os.environ.get("EZYBOT_OWNER_ID", "")


def is_owner(user_id):
    """Check whether a user is the configured bot owner."""
    owner_id = get_owner_id()

    return bool(owner_id) and str(user_id) == str(owner_id)


# ==================================================
# LOGGING
# ==================================================

def log(message):
    logger.info(message)


def log_warning(message):
    logger.warning(message)


def log_error(message):
    logger.error(message)


def log_moderation(action, moderator, target, reason="No reason provided"):
    log(
        f"MODERATION | {action} | "
        f"Moderator: {moderator} | "
        f"Target: {target} | "
        f"Reason: {reason}"
    )






# Stored warnings, separated by server and user
_warnings = {}


def _args(msg):
    raw = getattr(msg, "args", "") or ""
    try:
        return shlex.split(raw) if isinstance(raw, str) else list(raw)
    except ValueError:
        return raw.split()


def _reply(msg, text):
    msg.reply(text)


def _server_only(msg):
    if not getattr(msg, "server_id", None):
        _reply(msg, "❌ This command only works in a server")
        return False
    return True


def _duration(value):
    match = re.fullmatch(r"(\d+)([mhd]?)", value.lower())
    if not match:
        return None

    amount = int(match.group(1))
    unit = match.group(2) or "m"
    minutes = amount * {"m": 1, "h": 60, "d": 1440}[unit]

    if not 1 <= minutes <= 40320:
        return None

    return minutes


def _run(msg, action, success):
    try:
        action()
        _reply(msg, success)
    except Exception as exc:
        status = getattr(exc, "status", None)

        if status == 403:
            _reply(msg, "❌ I don't have permission to do that")
        elif status == 404:
            _reply(msg, "❌ Member or ban not found")
        else:
            _reply(msg, f"❌ Action failed: {exc}")


def kick(bot, msg):
    args = _args(msg)

    if not args:
        return _reply(msg, "Usage: /kick <user_id>")
    if not _server_only(msg):
        return

    user_id = args[0]
    _run(msg, lambda: bot.kick(msg.server_id, user_id),
         f"✅ Kicked `{user_id}`")


def ban(bot, msg):
    args = _args(msg)

    if not args:
        return _reply(msg, "Usage: /ban <user_id>")
    if not _server_only(msg):
        return

    user_id = args[0]
    _run(msg, lambda: bot.ban(msg.server_id, user_id),
         f"🔨 Banned `{user_id}`")


def unban(bot, msg):
    args = _args(msg)

    if not args:
        return _reply(msg, "Usage: /unban <user_id>")
    if not _server_only(msg):
        return

    user_id = args[0]
    _run(msg, lambda: bot.unban(msg.server_id, user_id),
         f"✅ Unbanned `{user_id}`")


def mute(bot, msg):
    args = _args(msg)

    if len(args) < 2:
        return _reply(msg, "Usage: /mute <user_id> <duration> [reason]")
    if not _server_only(msg):
        return

    user_id, duration = args[0], args[1]
    minutes = _duration(duration)

    if minutes is None:
        return _reply(msg, "❌ Invalid duration. Try 10m, 2h or 1d")

    reason = " ".join(args[2:]) or "No reason provided"

    _run(
        msg,
        lambda: bot.timeout(msg.server_id, user_id, minutes, reason),
        f"🔇 Timed out `{user_id}` for {duration}. Reason: {reason}"
    )


def unmute(bot, msg):
    args = _args(msg)

    if not args:
        return _reply(msg, "Usage: /unmute <user_id>")
    if not _server_only(msg):
        return

    user_id = args[0]
    _run(
        msg,
        lambda: bot.timeout(msg.server_id, user_id, 0, "Timeout removed"),
        f"🔊 Removed timeout for `{user_id}`"
    )


def warn(bot, msg):
    args = _args(msg)

    if len(args) < 2:
        return _reply(msg, "Usage: /warn <user_id> <reason>")
    if not _server_only(msg):
        return

    user_id = str(args[0])
    reason = " ".join(args[1:])
    key = (str(msg.server_id), user_id)

    _warnings.setdefault(key, []).append(reason)

    _reply(
        msg,
        f"⚠️ Warned `{user_id}`. "
        f"Warnings: {len(_warnings[key])}. Reason: {reason}"
    )


def warnings(bot, msg):
    args = _args(msg)

    if not args:
        return _reply(msg, "Usage: /warnings <user_id>")
    if not _server_only(msg):
        return

    user_id = str(args[0])
    items = _warnings.get((str(msg.server_id), user_id), [])

    if not items:
        return _reply(msg, f"✅ `{user_id}` has no recorded warnings")

    listing = "\n".join(
        f"{number}. {reason}"
        for number, reason in enumerate(items, 1)
    )

    _reply(msg, f"⚠️ Warnings for `{user_id}`:\n{listing}")


def clearwarnings(bot, msg):
    args = _args(msg)

    if not args:
        return _reply(msg, "Usage: /clearwarnings <user_id>")
    if not _server_only(msg):
        return

    user_id = str(args[0])
    key = (str(msg.server_id), user_id)
    removed = len(_warnings.pop(key, []))

    _reply(msg, f"✅ Cleared {removed} warning(s) for `{user_id}`")



def get_latency(start_time):
    return round((time.perf_counter() - start_time) * 1000)

# ==================================================
# MESSAGE HELPERS
# ==================================================

def get_arguments(msg):
    """Return command arguments as a list."""
    return getattr(msg, "argv", msg.content.split())


def get_argument_text(msg):
    """Return everything after the command name."""
    return getattr(msg, "args", "")


def send_message(bot, message, channel_id=None, msg=None):
    """Send a message to a specified channel or the command's channel."""
    if channel_id is None and msg is not None:
        channel_id = msg.channel_id

    if channel_id is None:
        raise ValueError("A channel ID or message object is required")

    return bot.send(channel_id, message)


def get_server_owner_id(bot, msg):
    """Get the owner ID of the server where the command was used."""
    if not msg.server_id:
        return None

    server = bot.server(msg.server_id)
    return server.get("owner_id")


def is_server_owner(bot, msg):
    """Check whether the person using the command owns the server."""
    owner_id = get_server_owner_id(bot, msg)

    if owner_id is None:
        return False

    return str(msg.author_id) == str(owner_id)


def get_reason(arguments, start=1):
    """Get a moderation reason from command arguments."""
    reason = " ".join(arguments[start:]).strip()
    return reason or "No reason provided"


def parse_target_and_reason(arguments):
    """Return a target ID and a reason."""
    if not arguments:
        return None, "No reason provided"

    return arguments[0], get_reason(arguments)


# ==================================================
# DURATION HELPERS
# ==================================================

def parse_duration(value):
    """
    Convert a duration into seconds.

    Examples:
