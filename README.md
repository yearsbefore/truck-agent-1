
# Truck Engineering AI Agent

An AI Agent built with LangChain + OpenRouter for truck engineering tasks.
Supports database queries, CATIA control, and regulation compliance checking.

## Quick Start

### Mac
```bash
bash start.sh
```

### Windows
Double-click `start.bat`

The script automatically handles: creating the virtual environment, installing dependencies, and initializing the database.

---

## Manual Setup (if scripts fail)

```bash
python3 -m venv venv
venv/bin/pip install -r requirements.txt   # Mac
venv/bin/python database/init_db.py
venv/bin/streamlit run ui/app.py
```

---

## Configuration

Copy `.env.example` to `.env` and fill in your API key:

```
OPENROUTER_API_KEY=sk-or-your-key-here
MODEL_NAME=meta-llama/llama-3.3-70b-instruct:free
CATIA_MODE=mock


## Project Structure

```
truck_agent/
├── .env                    # Your config (do not commit to Git)
├── .env.example            # Config template
├── requirements.txt
├── start.sh                # One-click start (Mac)
├── start.bat               # One-click start (Windows)
├── main.py
│
├── agent/
│   ├── core.py             # Agent assembly (LLM + Tools)
│   └── prompts.py          # System prompt
│
├── tools/
│   ├── db_tool.py          # Tool 1: Database query
│   ├── catia_tool.py       # Tool 2: CATIA control
│   └── regulation_tool.py  # Tool 3: Regulation check
│
├── database/
│   ├── init_db.py          # Database initialization script
│   └── trucks.db           # SQLite database (auto-generated)
│
└── ui/
    └── app.py              # Streamlit interface
```

---

## CATIA Integration

Default mode is `mock` (simulates operations, no CATIA required).

To connect real CATIA:
1. Ensure CATIA is installed and running (Windows only)
2. Set `CATIA_MODE=real` in `.env`
3. Install pywin32: `pip install pywin32`

# Truck Agent Project

This repository contains the code for the **Truck Engineering AI Agent** project.

The project is developed collaboratively using **GitHub and Git branches** to avoid code conflicts.

---

# Collaboration Workflow (Branch-Based Development)

To ensure smooth collaboration between multiple developers, we follow a **branch-based workflow**.

The `main` branch always contains the **stable version of the project**.  
All development should be done in **separate branches**.

---

# 1. Clone the Repository (First Time Only)

Each collaborator should first clone the repository to their local computer.

```bash
git clone https://github.com/yearsbefore/truck-agent-1.git
cd truck-agent-1
```

---

# 2. Update the Latest Code

Before starting work, always pull the latest version of the project.

```bash
git pull origin main
```

This ensures your local code is synchronized with the remote repository.

---

# 3. Create a New Development Branch

Each new feature should be developed in a **separate branch**.

Example:

```bash
git checkout -b feature-agent
```

Branch naming suggestions:

```
feature-agent
feature-ui
feature-database
feature-rag
bugfix-memory
```

Avoid unclear names like:

```
test
newbranch
temp
```

---

# 4. Develop and Commit Code

After making changes, add and commit your work.

```bash
git add .
git commit -m "Add agent module"
```

Use clear commit messages describing what you changed.

Examples:

```
Add truck recommendation logic
Fix database connection bug
Improve UI layout
```

---

# 5. Push the Branch to GitHub

Upload your branch to the remote repository.

```bash
git push origin feature-agent
```

Now the branch will appear on GitHub.

---

# 6. Create a Pull Request

Go to the repository page:

```
https://github.com/yearsbefore/truck-agent-1
```

GitHub will show a button:

```
Compare & pull request
```

Create a **Pull Request** from your branch to `main`.

Example:

```
feature-agent → main
```

---

# 7. Merge the Branch

After reviewing the changes, the branch can be merged into `main`.

Click:

```
Merge pull request
```

The new code will now become part of the main project.

---

# 8. Start the Next Task

Before starting a new feature, switch back to `main` and update it.

```bash
git checkout main
git pull origin main
```

Then create a new branch:

```bash
git checkout -b feature-new-module
```

---

# Recommended Daily Workflow

A simple workflow for daily development:

Before coding:

```bash
git pull origin main
```

Create a branch:

```bash
git checkout -b feature-xxx
```

After coding:

```bash
git add .
git commit -m "describe your change"
git push origin feature-xxx
```

Create a **Pull Request** on GitHub to merge into `main`.

---

# Best Practices

To avoid conflicts:

1. Always pull the latest code before starting work.
2. Do not develop directly on the `main` branch.
3. Use meaningful branch names.
4. Write clear commit messages.
5. Avoid modifying the same part of the same file simultaneously.


