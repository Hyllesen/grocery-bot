# TODO

## Goal
Enhance the shopping bot with fuzzy prefix matching on `/delete`, remove category functionality entirely, add `/clear` command, and add help fallback for unknown commands.

## Tasks

### 1. Remove category functionality
- [x] Remove `categories.py` — the file is no longer needed
- [x] Update `database.py` — remove the `category` column from the `items` table schema
- [x] Update `database.py` — remove `move_item` function (no longer needed)
- [x] Update `bot.py` — remove the `/move` command handler
- [x] Update `bot.py` — remove all category references from the `/add` confirmation messages (e.g., "Added 'chicken' to 🥩 Meat ✓")

### 2. Implement fuzzy prefix matching on `/delete`
- [x] Update `database.py` — add a `search_items_by_prefix(prefix)` function that queries `SELECT * FROM items WHERE item_name LIKE ?` with `prefix + '%'`
- [x] Update `bot.py` — rewrite `cmd_delete` to use prefix matching: if 1 match, delete it; if 2+ matches, reply with suggestions ("Did you mean X, Y, or Z to be deleted?"); if 0 matches, reply with "not found"

### 3. Add `/clear` command
- [x] Update `bot.py` — add `cmd_clear` handler that calls `db.delete_all_items()` and confirms the list is empty

### 4. Handle unknown commands
- [x] Update `bot.py` — add a `/commands` handler (or reuse existing `/help`) that lists all available commands
- [x] Update `bot.py` — add a generic message handler that intercepts messages starting with `/` that don't match any known command, and replies with the available commands list
- [x] Update `README.md` — remove `/move` and `/add <item> <category>` entries, update description to remove "categorized"

## Notes
- The `items` table schema change (removing `category`) will require a migration for existing databases. Since this is a small app, we can either:
  - Drop the column and let SQLite handle it (ALTER TABLE DROP COLUMN), or
  - Add a migration flag so users can run it once
- The `/delete` fuzzy matching should be case-insensitive (item names are stored lowercase already)
