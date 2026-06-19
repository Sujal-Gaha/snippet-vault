# Snippet Vault

A minimal, beautiful, and self-hosted Streamlit application for uploading, searching, and managing code snippets and terminal commands for future use.

## Features

- **Store Code & Commands:** Categorize entries as either code snippets or terminal commands.
- **Syntax Highlighting:** Choose language formatting (Python, SQL, Shell, YAML, JSON, CSS, JavaScript, HTML, Plain Text).
- **Tagging System:** Organize snippets with searchable tags.
- **Search & Filters:** Real-time search across titles, content, descriptions, and tags. Filter by tags or types.
- **Flexible Storage:** Supports both a lightweight SQLite database and a production-ready MySQL backend.
- **Dark-themed UI:** Modern, clean Nordic dark design.

## Configuration (.env)

Copy the example configuration to `.env` and adjust the variables:

```bash
cp example.env .env
```

Available variables:

- `DB_TYPE`: `sqlite` (default) or `mysql`
- `SQLITE_DB_PATH`: Path to SQLite database file (defaults to `snippets.db`)
- `MYSQL_HOST`: MySQL database host
- `MYSQL_PORT`: MySQL port (defaults to `3306`)
- `MYSQL_DATABASE`: MySQL database name
- `MYSQL_USER`: MySQL user
- `MYSQL_PASSWORD`: MySQL password
- `MYSQL_ROOT_PASSWORD`: MySQL root password (required for initialization in container)

## Quickstart

### 1. Recommended Setup: Running with Docker Compose (MySQL Backend)

To launch both the Streamlit web application and the MySQL database in an isolated container network:

1. Copy the environment configuration template:

   ```bash
   cp example.env .env
   ```

   Modify `.env` to set `DB_TYPE=mysql` (along with any custom usernames or passwords if needed).

2. Build and start the containerized services:

   ```bash
   docker compose up --build -d
   ```

3. The application will start up automatically and is accessible at `http://localhost:1234`.

---

### 2. Alternative Setup: Local Python Virtual Environment (SQLite Backend)

For a lightweight, local SQLite database run:

1. Set up a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Copy the configuration template:

   ```bash
   cp example.env .env
   ```

4. Run the application:

   ```bash
   streamlit run app.py
   ```

The app will start and automatically open in your browser at `http://localhost:1234`.
