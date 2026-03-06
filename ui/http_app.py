import json
import os
import threading
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from agent.core import create_agent


_AGENT = create_agent()
_AGENT_LOCK = threading.Lock()
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_INDEX_PATH = os.path.join(_BASE_DIR, "static", "index.html")


def _json_response(handler: BaseHTTPRequestHandler, payload: dict, status: int = 200) -> None:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


class ChatHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path not in ("/", "/index.html"):
            self.send_error(HTTPStatus.NOT_FOUND, "Not Found")
            return

        if not os.path.exists(_INDEX_PATH):
            self.send_error(HTTPStatus.INTERNAL_SERVER_ERROR, "index.html missing")
            return

        with open(_INDEX_PATH, "rb") as f:
            body = f.read()

        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:
        if self.path == "/api/chat":
            self._handle_chat()
            return
        if self.path == "/api/reset":
            self._handle_reset()
            return
        self.send_error(HTTPStatus.NOT_FOUND, "Not Found")

    def _read_json(self) -> dict:
        content_len = int(self.headers.get("Content-Length", "0"))
        if content_len <= 0:
            return {}
        raw = self.rfile.read(content_len)
        try:
            return json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            return {}

    def _handle_chat(self) -> None:
        payload = self._read_json()
        message = str(payload.get("message", "")).strip()
        if not message:
            _json_response(self, {"error": "message is required"}, status=400)
            return

        try:
            with _AGENT_LOCK:
                result = _AGENT.invoke({"input": message})
            answer = result.get("output", "Sorry, no response was returned.")
            _json_response(self, {"answer": answer})
        except Exception as exc:
            _json_response(self, {"error": f"Agent error: {exc}"}, status=500)

    def _handle_reset(self) -> None:
        try:
            with _AGENT_LOCK:
                _AGENT.memory.clear()
            _json_response(self, {"ok": True})
        except Exception as exc:
            _json_response(self, {"error": f"Reset error: {exc}"}, status=500)

    def log_message(self, format: str, *args) -> None:
        return


def run_server(host: str = "127.0.0.1", port: int = 8501) -> None:
    server = ThreadingHTTPServer((host, port), ChatHandler)
    print(f"Truck Agent Web UI running on http://{host}:{port}")
    server.serve_forever()

