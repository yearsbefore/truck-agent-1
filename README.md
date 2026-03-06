<<<<<<< HEAD
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
=======
# truck-agent-1
>>>>>>> 73606bf7df2af0c37422efec2f23676bcf0917b8
