import os
import random
import logging
from datetime import datetime, timezone
import time
import re
import shlex
import time

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


# ==================================================
# MODERATION
# ==================================================

# Stored warnings, separated by server and user.
# Note: these are stored in memory and reset when the bot restarts.
_warnings = {}


def _args(msg):
    """Get command arguments, respecting quoted text when possible."""
    raw = getattr(msg, "args", "") or ""

    try:
        return shlex.split(raw) if isinstance(raw, str) else list(raw)
    except ValueError:
        return raw.split()


def _reply(msg, text):
    msg.reply(text)


def _server_only(msg):
    """Ensure the command was used inside a server."""
    if not getattr(msg, "server_id", None):
        _reply(msg, "❌ This command only works in a server.")
        return False
    return True


def _duration(value):
    """Convert 10m, 2h, or 1d to minutes, with a 28-day maximum."""
    match = re.fullmatch(r"(\d+)([mhd]?)", str(value).lower())

    if not match:
        return None

    amount = int(match.group(1))
    unit = match.group(2) or "m"
    minutes = amount * {"m": 1, "h": 60, "d": 1440}[unit]

    if not 1 <= minutes <= 40320:
        return None

    return minutes


def _run(msg, action, success):
    """Run a moderation action and provide a readable response."""
    try:
        action()
        _reply(msg, success)
    except Exception as exc:
        status = getattr(exc, "status", None)

        if status == 403:
            _reply(msg, "❌ I don't have permission to do that.")
        elif status == 404:
            _reply(msg, "❌ Member or ban not found.")
        else:
            log_error(f"Moderation action failed: {exc}")
            _reply(msg, f"❌ Action failed: {exc}")


def kick(bot, msg):
    """Kick a user. Usage: /kick <user_id>."""
    args = _args(msg)

    if not args:
        return _reply(msg, "Usage: /kick <user_id>")
    if not _server_only(msg):
        return

    user_id = get_target(bot, msg)

    if not user_id:
        return _reply(
              msg,
              "❌ User not found. Use a mention, username, or ID."
          )
    _run(
        msg,
        lambda: bot.kick(msg.server_id, user_id),
        f"✅ Kicked `{user_id}`."
    )


def ban(bot, msg):
    """Ban a user. Usage: /ban <user_id>."""
    args = _args(msg)

    if not args:
        return _reply(msg, "Usage: /ban <user_id>")
    if not _server_only(msg):
        return

    user_id = get_target(bot, msg)

    if not user_id:
        return _reply(
            msg,
            "❌ User not found. Use a mention, username, or ID."
        )
    _run(
        msg,
        lambda: bot.ban(msg.server_id, user_id),
        f"🔨 Banned `{user_id}`."
    )


def unban(bot, msg):
    """Unban a user. Usage: /unban <user_id>."""
    args = _args(msg)

    if not args:
        return _reply(msg, "Usage: /unban <user_id>")
    if not _server_only(msg):
        return

    user_id = args[0]
    _run(
        msg,
        lambda: bot.unban(msg.server_id, user_id),
        f"✅ Unbanned `{user_id}`."
    )


def mute(bot, msg):
    """Timeout a user. Usage: /mute <user_id> <duration> [reason]."""
    args = _args(msg)

    if len(args) < 2:
        return _reply(
            msg,
            "Usage: /mute <user_id> <duration> [reason]\n"
            "Example: /mute 12345 30m spamming"
        )
    if not _server_only(msg):
        return

    user_id, duration = args[0], args[1]
    minutes = _duration(duration)

    if minutes is None:
        return _reply(
            msg,
            "❌ Invalid duration. Use 10m, 2h, 1d, or a number of minutes "
            "(maximum 28 days)."
        )

    reason = " ".join(args[2:]) or "No reason provided"

    _run(
        msg,
        lambda: bot.timeout(msg.server_id, user_id, minutes, reason),
        f"🔇 Timed out `{user_id}` for {duration}. Reason: {reason}"
    )


def unmute(bot, msg):
    """Remove a timeout. Usage: /unmute <user_id>."""
    args = _args(msg)

    if not args:
        return _reply(msg, "Usage: /unmute <user_id>")
    if not _server_only(msg):
        return

    user_id = args[0]
    _run(
        msg,
        lambda: bot.timeout(msg.server_id, user_id, 0, "Timeout removed"),
        f"🔊 Removed timeout for `{user_id}`."
    )


def warn(bot, msg):
    """Record a warning. Usage: /warn <user_id> <reason>."""
    args = _args(msg)

    if len(args) < 2:
        return _reply(msg, "Usage: /warn <user_id> <reason>")
    if not _server_only(msg):
        return

    user_id = str(args[0])
    reason = " ".join(args[1:])
    key = (str(msg.server_id), user_id)

    _warnings.setdefault(key, []).append(reason)
    count = len(_warnings[key])

    log_moderation("WARN", msg.author_id, user_id, reason)
    _reply(
        msg,
        f"⚠️ Warned `{user_id}`. Warnings: {count}. Reason: {reason}"
    )


def warnings(bot, msg):
    """Show recorded warnings. Usage: /warnings <user_id>."""
    args = _args(msg)

    if not args:
        return _reply(msg, "Usage: /warnings <user_id>")
    if not _server_only(msg):
        return

    user_id = str(args[0])
    items = _warnings.get((str(msg.server_id), user_id), [])

    if not items:
        return _reply(msg, f"✅ `{user_id}` has no recorded warnings.")

    listing = "\n".join(
        f"{number}. {reason}"
        for number, reason in enumerate(items, start=1)
    )
    _reply(msg, f"⚠️ Warnings for `{user_id}`:\n{listing}")


def clearwarnings(bot, msg):
    """Clear recorded warnings. Usage: /clearwarnings <user_id>."""
    args = _args(msg)

    if not args:
        return _reply(msg, "Usage: /clearwarnings <user_id>")
    if not _server_only(msg):
        return

    user_id = str(args[0])
    key = (str(msg.server_id), user_id)
    removed = len(_warnings.pop(key, []))

    log_moderation("CLEAR WARNINGS", msg.author_id, user_id)
    _reply(msg, f"✅ Cleared {removed} warning(s) for `{user_id}`.")


# ==================================================
# PERFORMANCE
# ==================================================

def get_latency(start_time):
    """Return elapsed time in milliseconds since start_time."""
    return round((time.perf_counter() - start_time) * 1000)


# ==================================================
# MESSAGE HELPERS
# ==================================================

def get_arguments(msg):
    """Return command arguments as a list."""
    argv = getattr(msg, "argv", None)

    if argv is not None:
        return list(argv)

    content = getattr(msg, "content", "") or ""
    return content.split()


def get_argument_text(msg):
    """Return everything after the command name."""
    return getattr(msg, "args", "") or ""


def send_message(bot, message, channel_id=None, msg=None):
    """Send a message to a channel or the command's channel."""
    if channel_id is None and msg is not None:
        channel_id = msg.channel_id

    if channel_id is None:
        raise ValueError("A channel ID or message object is required.")

    return bot.send(channel_id, message)


# ==================================================
# SERVER HELPERS
# ==================================================

def get_server_owner_id(bot, msg):
    """Get the owner ID of the server where the command was used."""
    if not getattr(msg, "server_id", None):
        return None

    server = bot.server(msg.server_id)
    return server.get("owner_id")


def is_server_owner(bot, msg):
    """Check whether the person using the command owns the server."""
    owner_id = get_server_owner_id(bot, msg)

    if owner_id is None:
        return False

    return str(msg.author_id) == str(owner_id)


# ==================================================
# ARGUMENT AND REASON HELPERS
# ==================================================

def get_reason(arguments, start=1):
    """Get a moderation reason from a list of command arguments."""
    reason = " ".join(arguments[start:]).strip()
    return reason or "No reason provided"


def parse_target_and_reason(arguments):
    """Return a target user ID and reason from command arguments."""
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
        parse_duration("30s") -> 30
        parse_duration("10m") -> 600
        parse_duration("2h")  -> 7200
        parse_duration("1d")  -> 86400
    """
    match = re.fullmatch(r"(\d+)([smhd]?)", str(value).lower().strip())

    if not match:
        return None

    amount = int(match.group(1))
    unit = match.group(2) or "s"
    seconds = amount * {"s": 1, "m": 60, "h": 3600, "d": 86400}[unit]

    return seconds if amount > 0 else None


def format_duration(seconds):
    """Format a duration in seconds into a readable string."""
    seconds = max(0, int(seconds))

    units = (
        ("day", 86400),
        ("hour", 3600),
        ("minute", 60),
        ("second", 1),
    )

    parts = []

    for name, size in units:
        amount, seconds = divmod(seconds, size)

        if amount:
            label = name if amount == 1 else f"{name}s"
            parts.append(f"{amount} {label}")

    return ", ".join(parts) if parts else "0 seconds"

#//////Other//////


def embed(title, description=None, color=0x5865F2, fields=None, footer=None):
    """Create a reusable embed dictionary for Yapper messages."""
    result = {
        "title": str(title),
        "color": color,
    }

    if description:
        result["description"] = str(description)

    if fields:
        result["fields"] = fields

    if footer:
        result["footer"] = {"text": str(footer)}

    return result


def send_embed(msg, title, description=None, color=0x5865F2,
               fields=None, footer="Ezybot"):
    """Create and send an embed as a reply to a message."""
    msg.reply(
        " ",
        embeds=[embed(title, description, color, fields, footer)]
    )

def dm(bot, user_id, message):
    """Open a DM and send a message."""
    try:
        channel_id = bot.dm(user_id)
        bot.send(channel_id, str(message))
        return True

    except Exception as e:
        log_error(f"Failed to DM user {user_id}: {e}")
        return False

def require_owner(bot, msg):
    """Return True if the server owner is running the command."""
    if not is_server_owner(bot, msg):
        msg.reply("❌ Only the server owner can use this command.")
        return False
    return True

def get_target(bot, msg):
    """Extract a target user ID from the first command argument."""
    import re

    args = _args(msg)

    if not args:
        return None

    target = args[0]

    # Support mentions such as <@123456> and <@!123456>
    match = re.fullmatch(r"<@!?([^<>]+)>", target)

    if match:
        return match.group(1)

    # Otherwise, assume the argument is a raw user ID
    return target


def _get_name(data, *keys):
    """Find the first available name field in an API response."""
    if not data:
        return None

    for key in keys:
        value = data.get(key)

        if value and isinstance(value, str):
            return value

    return None


def format_name(name, item_id=None, show_id=False):
    """Format a name, optionally displaying its ID alongside it."""
    name = str(name or "Unknown")

    if show_id and item_id:
        return f"{name} ({item_id})"

    return name


def get_server_name(bot, server_id):
    """Resolve a server ID to its name."""
    try:
        server = bot.server(server_id)
        return _get_name(server, "name") or str(server_id)
    except Exception:
        return str(server_id)


def get_user_name(bot, user_id):
    """Resolve a user ID to their username."""
    try:
        user = bot.user(user_id)
        return _get_name(
            user, "username", "display_name", "name"
        ) or str(user_id)
    except Exception:
        return str(user_id)


def get_role_name(bot, server_id, role_id):
    """Resolve a role ID to its name."""
    try:
        for role in bot.roles(server_id):
            if str(role.get("id")) == str(role_id):
                return _get_name(role, "name") or str(role_id)

        return str(role_id)
    except Exception:
        return str(role_id)


def server_label(bot, server_id, show_id=False):
    """Return a readable server name, optionally with its ID."""
    name = get_server_name(bot, server_id)
    return format_name(name, server_id, show_id)


def user_label(bot, user_id, show_id=False):
    """Return a readable username, optionally with its ID."""
    name = get_user_name(bot, user_id)
    return format_name(name, user_id, show_id)


def role_label(bot, server_id, role_id, show_id=False):
    """Return a readable role name, optionally with its ID."""
    name = get_role_name(bot, server_id, role_id)
    return format_name(name, role_id, show_id)

def success_embed(msg, title, description=None):
    """Send a standard green success embed."""
    send_embed(
        msg,
        title=f"✅ {title}",
        description=description,
        color=0x57F287
    )

def error_embed(msg, title, description=None):
    """Send a standard red error embed."""
    send_embed(
        msg,
        title=f"❌ {title}",
        description=description,
        color=0xED4245
    )



# ==================================================
# COOLDOWNS
# ==================================================

_cooldowns = {}


def cooldown(user_id, command, seconds=5):
    """Return remaining cooldown seconds, or 0 if ready."""
    now = time.monotonic()

    if seconds < 0:
        raise ValueError("Cooldown duration cannot be negative")

    key = (str(user_id), str(command))
    expires = _cooldowns.get(key, 0)

    if now < expires:
        return round(expires - now, 1)

    _cooldowns[key] = now + seconds

    # Remove expired cooldowns to prevent unlimited dictionary growth
    if len(_cooldowns) > 1000:
        _cleanup_cooldowns(now)

    return 0


def _cleanup_cooldowns(now):
    """Remove expired cooldown entries."""
    expired = [
        key for key, expires in _cooldowns.items()
        if expires <= now
    ]

    for key in expired:
        del _cooldowns[key]