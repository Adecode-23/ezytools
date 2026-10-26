```python
import os
import random
import logging
from datetime import datetime, timezone


# ==================================================
# EZYBOT UTILITIES
# ==================================================

logging.basicConfig(
    level=logging.INFO,
    format="[ezybot] %(levelname)s: %(message)s"
)

logger = logging.getLogger("ezybot")

# In-memory warning storage.
# Warnings reset when the bot restarts.
warnings = {}


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
    