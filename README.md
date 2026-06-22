# 🛒 Shopping Bot

A Telegram bot for couples — just type items in a group chat and get a shopping list when you're ready to go.

## Quick Start

1. Create a bot via [BotFather](https://t.me/botfather) and get the token.
2. Create a Telegram group with your partner and add the bot.
3. Find your group chat ID (use [@getidsbot](https://t.me/getidsbot) — the ID will be negative for groups).
4. Copy `.env.example` to `.env` and fill in the values:

```bash
cp .env.example .env
```

```env
BOT_TOKEN=your_bot_token_here
ALLOWED_CHAT_ID=your_group_chat_id_here
```

5. Run with Docker:

```bash
docker compose up
```

## Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome message with help |
| `/add <item>` | Add an item |
| `/list` | Show current items |
| `/shoppinglist` | Get the full list, then clear it |
| `/delete <item>` | Remove an item (prefix matching) |
| `/clear` | Clear the entire list |

| `/help` | Show commands |

## Plain Text

Just type an item name — it gets added automatically.



## Deploying to a VPS

1. SSH into your VPS and clone the repo.
2. Copy `.env` with your bot token and chat ID.
3. Run `docker compose up -d`.

Data persists in the `./data` directory (SQLite database).
