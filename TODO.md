# TODO

## Goal
Build a Dockerized Python Telegram bot that lets a couple chat grocery items into a shared shopping list, auto-categorized, with a command to retrieve and clear the list.

## Tasks

### 1. Project Setup
- [x] Initialize Python project (virtual env, `pyproject.toml`, `requirements.txt`)
- [x] Install `python-telebot` (or `aiogram`) as the Telegram bot framework
- [x] Set up `Dockerfile` and `docker-compose.yml` for containerized deployment
- [x] Create `.env` template and `.gitignore`

### 2. Data Layer
- [x] Set up SQLite database with a single `items` table (id, item_name, category, created_at)
- [x] Write a `database.py` module with `add_item`, `get_items`, `delete_items`, `move_item` functions

### 3. Category Mapping
- [x] Create a keyword-to-category mapping dictionary in `categories.py` with ~10 predefined categories and ~30-50 common grocery/household keyword mappings
- [x] Write `guess_category(item_name)` function that returns the best category match or "Other"

### 4. Bot Commands
- [x] Implement `/start` — welcome message with usage instructions
- [x] Implement `/add <item>` or `/add <item> <category>` to add items
- [x] Implement `/list` to show all current items grouped by category
- [x] Implement `/shoppinglist` to output the full list grouped by category, then clear all items
- [x] Implement `/delete <item>` to remove a specific item
- [x] Implement `/move <item> <category>` to recategorize an item

### 5. Message Handling (No Command)
- [x] Handle plain text messages as implicit `/add` — auto-categorize and confirm with the user (e.g., "Added 'toothpaste' to 🚿 Bathroom ✓")

### 6. Docker & Deployment
- [x] Test locally with Docker (`docker compose up`)
- [x] Ensure `.env` with `BOT_TOKEN` and `ADMIN_CHAT_ID` is handled (restrict bot to specific group chat)
- [x] Add `docker-compose.yml` with volume mount for SQLite persistence

### 7. README
- [x] Write `README.md` with setup instructions, commands reference, and deployment steps

## Notes
- Bot framework: `python-telebot` (synchronous, simple for this use case)
- Database: SQLite (lightweight, single file, works well in Docker with volume mount)
- Authorization: Restrict to a specific chat ID (the group chat with the bot)
- Categories: Produce, Dairy, Meat, Bakery, Pantry, Drinks, Bathroom, Household, Snacks, Other
