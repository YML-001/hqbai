# Vercel 上的问答接口。密钥从环境变量读取，不放进网页。
import json
import sys
from http.server import BaseHTTPRequestHandler
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from prototype_data import HOTLINE
from server import ask_model, client_ip, origin_allowed, too_many


def failure_text(error):
    reason = str(error)
    if reason == "余额不足":
        return f"问答服务已接通，但模型账户余额不足，这次没能生成回答。充值后即可继续提问。你也可以拨打后勤服务热线 {HOTLINE}。"
    if reason == "模型未开通":
        return f"豆包模型还没开通。请到火山方舟开通后再问。你也可以拨打后勤服务热线 {HOTLINE}。"
    return f"暂时无法连接问答服务，请稍后重试。你也可以拨打后勤服务热线 {HOTLINE}。"


class handler(BaseHTTPRequestHandler):
    def _cors(self):
        origin = origin_allowed(self.headers.get("Origin", ""))
        if origin:
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Vary", "Origin")
            self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _json(self, data, status=200):
        raw = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self._cors()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(raw)

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0") or 0)
        try:
            incoming = json.loads(self.rfile.read(length).decode("utf-8") or "{}")
        except json.JSONDecodeError:
            self._json({"ok": False, "answer": "没有读懂这次请求。", "covered": False, "serviceId": "none", "hotline": HOTLINE}, 400)
            return
        question = str(incoming.get("question") or "").strip()[:400]
        role = incoming.get("role") if incoming.get("role") in {"guest", "student", "staff"} else "guest"
        port = incoming.get("port") if incoming.get("port") in {"pc", "mobile"} else "pc"
        if not question:
            self._json({"ok": False, "answer": "请先写下你的问题。", "covered": False, "serviceId": "none", "hotline": HOTLINE}, 400)
            return
        if too_many(client_ip(self.headers)):
            self._json({"ok": False, "answer": f"提问有点频繁，请稍后再试。你也可以拨打后勤服务热线 {HOTLINE}。", "covered": False, "serviceId": "none", "hotline": HOTLINE}, 429)
            return
        try:
            self._json(ask_model(question, role, port))
        except Exception as error:
            self._json({"ok": False, "answer": failure_text(error), "covered": False, "serviceId": "none", "hotline": HOTLINE})
