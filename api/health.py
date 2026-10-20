# 给预览页确认问答接口是否就绪。
import json
import sys
from http.server import BaseHTTPRequestHandler
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from server import KNOWLEDGE, llm_settings, origin_allowed


class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(204)
        origin = origin_allowed(self.headers.get("Origin", ""))
        if origin:
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        key, _base, model = llm_settings()
        raw = json.dumps({
            "ok": bool(key) and bool(KNOWLEDGE),
            "knowledgeChars": len(KNOWLEDGE),
            "modelReady": bool(key),
            "model": model,
        }, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        origin = origin_allowed(self.headers.get("Origin", ""))
        if origin:
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Vary", "Origin")
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(raw)
