"""Telegram shopping-list bot — add items, get a list, clear it."""

import logging

from dotenv import load_dotenv
import telebot

import database as db

load_dotenv()

import os

BOT_TOKEN: str = os.environ.get("BOT_TOKEN", "")
ALLOWED_CHAT_ID: str = os.environ.get("ALLOWED_CHAT_ID", "")

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(BOT_TOKEN)


# ── Authorization ──────────────────────────────────────────────────────────

def _is_allowed(message) -> bool:
    return str(message.chat.id) == ALLOWED_CHAT_ID


def _check_auth(message) -> bool:
    if _is_allowed(message):
        return True
    logger.warning("Unauthorized chat %s — ignoring", message.chat.id)
    bot.send_message(message.chat.id, "🔒 Sorry, this bot isn't set up for this chat.")
    return False


# ── Helpers ────────────────────────────────────────────────────────────────

def _format_list(items: list) -> str:
    lines = []
    for row in items:
        lines.append(f"• {row['item_name']}")
    return "\n".join(lines) if lines else "No items in the list yet."


# ── Commands ───────────────────────────────────────────────────────────────

@bot.message_handler(commands=["start", "help"])
def cmd_start(message):
    if not _check_auth(message):
        return
    bot.reply_to(
        message,
        "🛒 *Shopping bot ready!*\n\n"
        "Just type an item and I'll add it automatically.\n\n"
        "Commands:\n"
        "  /add item        — add an item\n"
        "  /list            — show current items\n"
        "  /shoppinglist    — get list & clear\n"
        "  /delete item     — remove an item\n"
        "  /help            — show this message",
        parse_mode="Markdown",
    )


@bot.message_handler(commands=["add"])
def cmd_add(message):
    if not _check_auth(message):
        return
    args = message.text.split(maxsplit=1)
    if len(args) < 2 or not args[1].strip():
        bot.reply_to(message, "Usage: /add <item>")
        return
    item_name = args[1].strip()
    db.add_item(item_name)
    bot.reply_to(message, f"Added *{item_name}* ✓", parse_mode="Markdown")


@bot.message_handler(commands=["list"])
def cmd_list(message):
    if not _check_auth(message):
        return
    items = db.get_items()
    if not items:
        bot.reply_to(message, "📭 The list is empty.")
        return
    bot.reply_to(message, _format_list(items), parse_mode="Markdown")


@bot.message_handler(commands=["shoppinglist"])
def cmd_shoppinglist(message):
    if not _check_auth(message):
        return
    items = db.get_items()
    if not items:
        bot.reply_to(message, "📭 Nothing to buy — the list is empty!")
        return
    bot.reply_to(message, f"🛒 *Your shopping list:*\n\n{_format_list(items)}", parse_mode="Markdown")
    deleted = db.delete_all_items()
    logger.info("Shopping list cleared (%d items removed)", deleted)
    bot.send_message(message.chat.id, "✅ List cleared — enjoy the shopping!")


@bot.message_handler(commands=["delete"])
def cmd_delete(message):
    if not _check_auth(message):
        return
    args = message.text.split(maxsplit=1)
    if len(args) < 2 or not args[1].strip():
        bot.reply_to(message, "Usage: /delete <item>")
        return
    item_name = args[1].strip().lower()
    deleted = db.delete_item(item_name)
    if deleted:
        bot.reply_to(message, f"Deleted *{item_name}* ✓", parse_mode="Markdown")
    else:
        bot.reply_to(message, f"'{item_name}' not found in the list.")


# ── Plain text handler (implicit /add) ─────────────────────────────────────

@bot.message_handler(func=lambda m: True, content_types=["text"])
def handle_plain_text(message):
    if not _check_auth(message):
        return
    item_name = message.text.strip()
    if not item_name:
        return
    db.add_item(item_name)
    bot.reply_to(message, f"Added *{item_name}* ✓", parse_mode="Markdown")


# ── Entry point ────────────────────────────────────────────────────────────

def main():
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN not set — exiting")
        return

    db.init_db()
    logger.info("Bot starting (allowed chat: %s)", ALLOWED_CHAT_ID)
    bot.infinity_polling()


if __name__ == "__main__":
    main()
