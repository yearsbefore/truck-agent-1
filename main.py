import os

from dotenv import load_dotenv

from ui.http_app import run_server


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    load_dotenv()
    run_server(host="127.0.0.1", port=8501)

