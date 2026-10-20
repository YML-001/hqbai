#!/usr/bin/env python3
# 智慧后勤AI助手原型服务。
# 页面只访问本机接口。DeepSeek 密钥从 .env 读取，不会写进网页。

import json
import re
import ssl
import traceback
import urllib.error
import urllib.request
import zipfile
import xml.etree.ElementTree as ET
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from prototype_data import HOTLINE, SERVICES

ROOT = Path(__file__).resolve().parent
DOC = ROOT / "中南大学后勤服务知识库（公文版）(1).docx"
ENV_PATH = ROOT / ".env"
HOST = "127.0.0.1"
PORT = 8765
BLOCKED = {".env", "server.py", "build_pages.py", "prototype_data.py"}

SERVICE_IDS = {item["id"] for item in SERVICES} | {"none"}


def load_env(path):
    values = {}
    if not path.exists():
        return values
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def load_knowledge(path):
    if not path.exists():
        return ""
    ns = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    with zipfile.ZipFile(path) as package:
        root = ET.fromstring(package.read("word/document.xml"))
    paragraphs = []
    for para in root.iter(ns + "p"):
        parts = []
        for node in para.iter(ns + "t"):
            if node.text:
                parts.append(node.text)
            if node.tail:
                parts.append(node.tail)
        line = "".join(parts).strip()
        if line:
            paragraphs.append(line)
    return "\n".join(paragraphs)


def build_system(knowledge):
    catalog = []
    for item in SERVICES:
        ends = []
        if item["pc"]:
            ends.append("电脑有地址")
        if item["mobile"]:
            ends.append("手机有地址")
        if not ends:
            ends.append("两端都没有单独地址")
        who = "仅学生" if item["student_only"] else item["who"]
        catalog.append(f"- {item['id']}：{item['name']}（{who}；{'，'.join(ends)}）。{item['summary']}")
    catalog_text = "\n".join(catalog)
    return f"""你是中南大学后勤保障部的值班助手，对外名称是「智慧后勤AI助手」。只根据下面的《后勤服务知识库》回答，用简体中文，语气清楚、短句、方便办事。

回答规则：
1. 只用知识库里的事实。不要编造电话、价格、时间和链接。
2. 知识库没有写到的问题，answer 必须以「暂未收录」开头，并写上后勤服务热线 {HOTLINE}。covered 设为 false，serviceId 设为 none。
3. 不要查询或编造个人用量、欠费、房间余额、会议名单。被问到本人账单时，按未收录处理，并说明本期只能告诉缴纳方法。
4. 收费、开放时间要提醒对方以现场公示或当日系统为准。
5. 不要用 Markdown。answer 用普通段落，必要时换行。
6. 同时判断最贴近的一个事项编号。对不上就用 none。不要在 answer 里输出事项编号。

事项编号：
{catalog_text}

只输出一个 JSON 对象，包含三个字段：
- answer：字符串
- covered：布尔值
- serviceId：上面的编号之一，或 none

知识库全文：
{knowledge}
"""


ENV = load_env(ENV_PATH)
KNOWLEDGE = load_knowledge(DOC)
SYSTEM_PROMPT = build_system(KNOWLEDGE)


def extract_json(text):
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?", "", cleaned, flags=re.I).strip()
        cleaned = re.sub(r"```$", "", cleaned).strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, re.S)
        if not match:
            raise
        return json.loads(match.group(0))


def normalize(payload, raw_text):
    if not isinstance(payload, dict):
        payload = {}
    answer = str(payload.get("answer") or raw_text or "").strip()
    service_id = str(payload.get("serviceId") or "none").strip()
    if service_id not in SERVICE_IDS:
        service_id = "none"
    covered = payload.get("covered")
    if not isinstance(covered, bool):
        covered = "暂未收录" not in answer
    if not covered and not answer.startswith("暂未收录"):
        answer = f"暂未收录。{answer}".strip()
        if HOTLINE not in answer:
            answer += f" 如需人工咨询，请拨打后勤服务热线 {HOTLINE}。"
    if not answer:
        answer = f"暂未收录。如需人工咨询，请拨打后勤服务热线 {HOTLINE}。"
        covered = False
        service_id = "none"
    if len(answer) > 1800:
        answer = answer[:1800].rstrip() + "……"
    return {"ok": True, "answer": answer, "covered": covered, "serviceId": service_id, "hotline": HOTLINE}


def llm_settings():
    key = ENV.get("LLM_API_KEY") or ENV.get("DEEPSEEK_API_KEY") or ""
    base = (ENV.get("LLM_API_BASE") or ENV.get("DEEPSEEK_API_BASE") or "https://ark.cn-beijing.volces.com/api/v3").rstrip("/")
    model = ENV.get("LLM_MODEL") or ENV.get("DEEPSEEK_MODEL") or "doubao-seed-2-0-lite-260428"
    return key, base, model


def post_chat(body, key, base):
    request = urllib.request.Request(
        base + "/chat/completions",
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": "Bearer " + key},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=90, context=ssl.create_default_context()) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", "replace")[:500]
        if "ModelNotOpen" in detail:
            raise RuntimeError("模型未开通") from error
        if error.code == 402 or "Insufficient Balance" in detail:
            raise RuntimeError("余额不足") from error
        if error.code == 400 and "response_format" in body:
            retry = dict(body)
            retry.pop("response_format", None)
            return post_chat(retry, key, base)
        raise RuntimeError("接口返回 " + str(error.code)) from error


def ask_model(question, role, port):
    key, base, model = llm_settings()
    if not key:
        raise RuntimeError("未配置密钥")
    if not KNOWLEDGE:
        raise RuntimeError("未读到知识库")
    role_name = {"guest": "游客", "student": "学生", "staff": "教职工"}.get(role, "游客")
    port_name = "电脑" if port == "pc" else "手机"
    body = {
        "model": model,
        "temperature": 0.2,
        "thinking": {"type": "disabled"},
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"提问人是{role_name}，正在使用{port_name}。问题：{question}"},
        ],
    }
    payload = post_chat(body, key, base)
    content = payload["choices"][0]["message"]["content"]
    return normalize(extract_json(content), content)


class Handler(BaseHTTPRequestHandler):
    server_version = "LogisticsPrototype/1.0"

    def log_message(self, fmt, *args):
        print("[原型] " + (fmt % args))

    def send_json(self, data, status=200):
        raw = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path == "/api/health":
            key, _base, model = llm_settings()
            self.send_json({
                "ok": bool(key) and bool(KNOWLEDGE),
                "knowledgeChars": len(KNOWLEDGE),
                "modelReady": bool(key),
                "model": model,
            })
            return
        if path in ("/", ""):
            path = "/index.html"
        relative = path.lstrip("/")
        target = (ROOT / relative).resolve()
        if not str(target).startswith(str(ROOT)) or target.name in BLOCKED or target.name.startswith("."):
            self.send_error(404)
            return
        if not target.is_file():
            self.send_error(404)
            return
        data = target.read_bytes()
        kind = "text/html; charset=utf-8" if target.suffix == ".html" else "application/octet-stream"
        if target.suffix == ".js":
            kind = "text/javascript; charset=utf-8"
        if target.suffix == ".svg":
            kind = "image/svg+xml"
        self.send_response(200)
        self.send_header("Content-Type", kind)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        if self.path.split("?", 1)[0] != "/api/chat":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", "0") or 0)
        if length > 20000:
            self.send_json({"ok": False, "answer": "问题太长了，请缩短后再问。", "covered": False, "serviceId": "none", "hotline": HOTLINE}, 400)
            return
        try:
            incoming = json.loads(self.rfile.read(length).decode("utf-8") or "{}")
        except json.JSONDecodeError:
            self.send_json({"ok": False, "answer": "没有读懂这次请求。", "covered": False, "serviceId": "none", "hotline": HOTLINE}, 400)
            return
        question = str(incoming.get("question") or "").strip()
        role = incoming.get("role") if incoming.get("role") in {"guest", "student", "staff"} else "guest"
        port = incoming.get("port") if incoming.get("port") in {"pc", "mobile"} else "pc"
        if not question:
            self.send_json({"ok": False, "answer": "请先写下你的问题。", "covered": False, "serviceId": "none", "hotline": HOTLINE}, 400)
            return
        question = question[:400]
        try:
            result = ask_model(question, role, port)
            self.send_json(result)
        except Exception as error:
            print("[原型] 问答失败：" + str(error))
            reason = str(error)
            if reason not in {"余额不足", "模型未开通"}:
                traceback.print_exc()
            _key, _base, model = llm_settings()
            if reason == "余额不足":
                answer = f"问答服务已接通，但模型账户余额不足，这次没能生成回答。充值后即可继续提问。你也可以拨打后勤服务热线 {HOTLINE}。"
            elif reason == "模型未开通":
                answer = f"豆包密钥已经接通，但模型 {model} 还没在火山方舟开通。请到开通管理里打开这个模型，并开启安心体验模式后再问。你也可以拨打后勤服务热线 {HOTLINE}。"
            else:
                answer = f"暂时无法连接问答服务，请稍后重试。你也可以拨打后勤服务热线 {HOTLINE}。"
            self.send_json({
                "ok": False,
                "answer": answer,
                "covered": False,
                "serviceId": "none",
                "hotline": HOTLINE,
            })


def main():
    key, _base, model = llm_settings()
    print(f"知识库 {len(KNOWLEDGE)} 字")
    print("密钥已读取，模型 " + model if key else "未找到密钥，请检查 .env")
    print(f"打开 http://{HOST}:{PORT}/")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()


if __name__ == "__main__":
    main()
