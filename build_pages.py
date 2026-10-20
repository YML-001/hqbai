#!/usr/bin/env python3
# 生成智慧后勤AI助手的独立 HTML 原型。样式写在每个页面里。

import json
from html import escape
from pathlib import Path

from prototype_data import HOTLINE, OFFICIAL_SITE, SERVICES

# 线上预览站调用的问答接口。本机打开页面时仍走当前域名。
PUBLIC_API = ""

ROOT = Path(__file__).resolve().parent
CAMPUS = "https://images.unsplash.com/photo-1562774053-701939374585?auto=format&fit=crop&w=1600&q=80"
POOL = "https://images.unsplash.com/photo-1576013551627-0cc20b96c2a7?auto=format&fit=crop&w=1400&q=80"
BUS = "https://images.unsplash.com/photo-1544620341-11cb2cd7c5b2?auto=format&fit=crop&w=1400&q=80"
DORM = "https://images.unsplash.com/photo-1555854877-bab0e564b8d5?auto=format&fit=crop&w=1400&q=80"

WRITTEN = []
CARDS = []


def write_file(rel, html):
    if "@@" in html:
        raise SystemExit("页面还有未替换的占位：" + rel)
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    WRITTEN.append(rel)


def emit(group, rel, title, desc, icon, html):
    CARDS.append((group, rel, title, desc, icon))
    write_file(rel, html)


def render(template, **kwargs):
    for key, value in kwargs.items():
        template = template.replace("@@" + key + "@@", value)
    return template


STYLE = """
:focus-visible { outline: 2px solid #146C74; outline-offset: 2px; }
body { background: #E3F1F9; color: #3C444F; font-family: "OPPOSans", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif; }
thead.bg-mist { background: #D6EAF9; color: #3087CC; }
.num { font-variant-numeric: tabular-nums; }
.listen-ring { position: absolute; inset: -6px; border-radius: 999px; border: 2px solid transparent; pointer-events: none; }
.is-listening .listen-ring { border-color: #3087CC; animation: ring 1.6s ease-out infinite; }
@keyframes ring { from { transform: scale(.94); opacity: .9; } to { transform: scale(1.14); opacity: 0; } }
.bubble-user { background: #3087CC; color: #fff; border-radius: 8px 8px 2px 8px; }
.bubble-bot { background: #fff; color: #3C444F; border: 1px solid #C8CAD1; border-radius: 8px 8px 8px 2px; }
main:has(#thread) { overflow: hidden; }
main:has(#thread) > div { min-height: 0; flex: 1; }
@media (min-width: 1024px) {
  main:has(#thread) { display: flex; flex-direction: column; height: 100%; }
}
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: .01ms !important; animation-iteration-count: 1 !important; transition-duration: .01ms !important; }
}
"""

HEAD = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>@@TITLE@@ · 智慧后勤AI助手</title>
<script src="https://cdn.tailwindcss.com"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%233087CC'/%3E%3Ctext x='16' y='22' text-anchor='middle' font-size='16' fill='white' font-family='PingFang SC'%3E后%3C/text%3E%3C/svg%3E">
<script>
tailwind.config = {
  theme: { extend: {
    colors: {
      brand: { DEFAULT: "#3087CC", dark: "#006DAD", light: "#E3F1F9" },
      ink: "#3C444F",
      teal: { DEFAULT: "#3087CC", 50: "#E3F1F9", 700: "#006DAD" },
      amber: { DEFAULT: "#F29100", 50: "#FFF5E5" },
      mist: "#E3F1F9",
      card: "#FFFFFF",
      inktext: "#3C444F",
      muted: "#696F7D"
    },
    fontFamily: {
      sans: ["OPPOSans", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "sans-serif"],
      serif: ["OPPOSans", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "sans-serif"]
    },
    borderRadius: { lg: "8px", xl: "8px", "2xl": "8px" }
  } }
}
</script>
<style>@@STYLE@@</style>
</head>
"""


def document(title, body):
    return render(HEAD, TITLE=escape(title), STYLE=STYLE) + body + "\n</html>\n"


def avatar(listening=False, size="h-24 w-24"):
    state = "is-listening" if listening else ""
    label = "聆听" if listening else "迎宾"
    return f"""
<div class="text-center">
  <div class="relative mx-auto {size} {state}">
    <span class="listen-ring"></span>
    <svg viewBox="0 0 160 200" class="h-full w-full" role="img" aria-label="后勤值班人员{label}形象">
      <circle cx="80" cy="86" r="74" fill="#E7F4F5"/>
      <path d="M18 200c8-42 28-62 62-62s54 20 62 62" fill="#10243A"/>
      <path d="M62 132l18 22 18-22" fill="none" stroke="#146C74" stroke-width="4" stroke-linejoin="round"/>
      <ellipse cx="80" cy="78" rx="30" ry="34" fill="#F4D7C8"/>
      <path d="M50 76c2-36 22-48 30-48 10 0 30 12 30 48-8-16-18-22-30-22S58 60 50 76z" fill="#1C2834"/>
      <circle cx="69" cy="80" r="2.2" fill="#1C2834"/>
      <circle cx="91" cy="80" r="2.2" fill="#1C2834"/>
      <path d="M70 96c4 5 16 5 20 0" fill="none" stroke="#9A5A48" stroke-width="1.8" stroke-linecap="round"/>
      <rect x="98" y="158" width="26" height="16" rx="2" fill="#B86E2A"/>
      <text x="111" y="169" text-anchor="middle" font-size="8" fill="#10243A">值班</text>
    </svg>
  </div>
  <p class="mt-2 text-xs text-muted">{label}</p>
</div>"""


PEOPLE = {
    "guest": ("游客", "未登录", "你好，我是后勤值班助手。"),
    "student": ("林夏", "学生 · 计算机学院", "林夏同学，今天想办哪一件事？"),
    "staff": ("周宁", "教职工 · 后勤保障部", "周宁老师，需要查哪一项后勤服务？"),
}

NAV = {
    ("pc", "guest"): [
        ("home.html", "问答首页", "fa-house"),
        ("chat.html", "对话", "fa-comments"),
        ("category.html", "办事说明", "fa-map"),
        ("listening.html", "聆听", "fa-microphone"),
        ("login.html", "登录", "fa-right-to-bracket"),
    ],
    ("pc", "student"): [
        ("home.html", "问答首页", "fa-house"),
        ("chat.html", "对话", "fa-comments"),
        ("listening.html", "聆听", "fa-microphone"),
        ("services.html", "办事", "fa-table-cells-large"),
        ("utility.html", "水电", "fa-bolt"),
        ("profile.html", "我的", "fa-user"),
    ],
    ("pc", "staff"): [
        ("home.html", "问答首页", "fa-house"),
        ("chat.html", "对话", "fa-comments"),
        ("listening.html", "聆听", "fa-microphone"),
        ("services.html", "办事", "fa-table-cells-large"),
        ("profile.html", "我的", "fa-user"),
    ],
    ("mobile", "guest"): [
        ("home.html", "问答", "fa-comments"),
        ("category.html", "说明", "fa-map"),
        ("login.html", "登录", "fa-right-to-bracket"),
    ],
    ("mobile", "student"): [
        ("home.html", "问答", "fa-comments"),
        ("services.html", "办事", "fa-table-cells-large"),
        ("utility.html", "水电", "fa-bolt"),
        ("profile.html", "我的", "fa-user"),
    ],
    ("mobile", "staff"): [
        ("home.html", "问答", "fa-comments"),
        ("services.html", "办事", "fa-table-cells-large"),
        ("profile.html", "我的", "fa-user"),
    ],
}

ACTIVE = {
    "chat.html": "home.html",
    "listening.html": "home.html",
    "not-found.html": "chat.html",
    "jump.html": "services.html",
    "qrcode.html": "utility.html",
    "guide.html": "services.html",
    "detail.html": "inbox.html",
}


def nav_links(port, role, current):
    items = NAV[(port, role)]
    known = {href for href, _, _ in items}
    current_key = current if current in known else ACTIVE.get(current, current)
    links = []
    for href, label, icon in items:
        on = href == current_key
        if port == "pc":
            cls = "bg-teal-50 font-medium text-teal" if on else "text-inktext hover:bg-mist"
            links.append(
                f'<a class="flex min-h-11 shrink-0 items-center gap-2 rounded-lg px-3 text-sm {cls}" href="{href}">'
                f'<i class="fa-solid {icon} w-4"></i>{label}</a>'
            )
        else:
            cls = "text-teal" if on else "text-muted"
            links.append(
                f'<a class="flex min-h-14 flex-col items-center justify-center gap-1 text-xs {cls}" href="{href}">'
                f'<i class="fa-solid {icon}"></i><span>{label}</span></a>'
            )
    return "\n".join(links)


def public_services():
    data = []
    for item in SERVICES:
        data.append({
            "id": item["id"],
            "name": item["name"],
            "summary": item["summary"],
            "detail": item["detail"],
            "pc": item["pc"],
            "mobile": item["mobile"],
            "pc_review": item["pc_review"],
            "student_only": item["student_only"],
        })
    return json.dumps(data, ensure_ascii=False)


def badge(text, tone="teal"):
    tones = {
        "teal": "bg-teal-50 text-teal-700",
        "amber": "bg-amber-50 text-amber",
        "ink": "bg-mist text-inktext",
        "danger": "bg-red-50 text-red-800",
    }
    return f'<span class="inline-flex items-center rounded-full px-2 py-0.5 text-xs {tones[tone]}">{text}</span>'


def port_badges(item, port):
    bits = []
    if item["pc"] and item["mobile"]:
        bits.append(badge("两端可办"))
    elif item["pc"] and not item["mobile"]:
        bits.append(badge("仅电脑", "amber"))
    elif item["mobile"] and not item["pc"]:
        bits.append(badge("仅手机", "amber"))
    else:
        bits.append(badge("仅说明", "ink"))
    if port == "pc" and item["pc_review"]:
        bits.append(badge("地址待复核", "danger"))
    if item["student_only"]:
        bits.append(badge("学生", "ink"))
    return " ".join(bits)


def action_href(item, role, port):
    if item["student_only"] and role != "student":
        return None, ""
    url = item["pc"] if port == "pc" else item["mobile"]
    if url:
        return f'jump.html?service={item["id"]}', "去办理"
    if port == "pc" and item["id"] == "utility-pay" and role == "student":
        return "qrcode.html", "查看二维码"
    if port == "mobile" and item["pc"] and not item["mobile"]:
        return f'guide.html?service={item["id"]}', "电脑办理说明"
    if item["id"] == "announcement":
        if port == "mobile":
            return "guide.html?service=announcement", "查看出处"
        return "services.html#announcement", "查看出处"
    return None, ""


def service_cards(role, port):
    cards = []
    for item in SERVICES:
        if item["student_only"] and role != "student" and item["id"] == "utility-pay":
            continue
        href, label = action_href(item, role, port)
        button = ""
        if href and not (item["id"] == "announcement" and port == "pc"):
            button = (
                f'<a class="mt-4 inline-flex min-h-11 items-center rounded-lg bg-brand px-4 text-sm text-white hover:bg-brand-dark" href="{href}">'
                f'{label}</a>'
            )
        anchor = ' id="announcement"' if item["id"] == "announcement" else ""
        cards.append(f"""
<article{anchor} class="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
  <div class="flex items-start justify-between gap-3">
    <span class="flex h-11 w-11 items-center justify-center rounded-xl bg-teal-50 text-teal"><i class="fa-solid {item["icon"]}"></i></span>
    <div class="flex flex-wrap justify-end gap-1">{port_badges(item, port)}</div>
  </div>
  <h2 class="mt-4 text-lg font-medium">{item["name"]}</h2>
  <p class="mt-2 text-sm leading-6 text-muted">{escape(item["summary"])}</p>
  {button}
</article>""")
    return "\n".join(cards)


SUGGESTIONS = [
    ("宿舍水龙头坏了怎么报修？", "报修"),
    ("学生水电费怎么缴纳？", "水电"),
    ("校区间班车怎么查询时刻？", "班车"),
    ("潇湘校区游泳馆什么时候开放？", "游泳馆"),
]


def suggestion_buttons():
    return "\n".join(
        f'<button type="button" data-ask="{escape(q)}" class="min-h-11 rounded-full border border-slate-200 bg-white px-4 text-left text-sm hover:border-teal">{label}</button>'
        for q, label in SUGGESTIONS
    )


HOME_SCRIPT = """
<script>
document.querySelectorAll("[data-ask]").forEach(function (el) {
  el.addEventListener("click", function () {
    sessionStorage.setItem("hq-question", el.getAttribute("data-ask"));
    location.href = "chat.html";
  });
});
var form = document.querySelector("#ask-form");
if (form) {
  form.addEventListener("submit", function (event) {
    event.preventDefault();
    var input = document.querySelector("#question");
    var error = document.querySelector("#question-error");
    var question = input.value.trim();
    if (!question) {
      error.textContent = "请先写下你的问题。";
      input.focus();
      return;
    }
    sessionStorage.setItem("hq-question", question);
    location.href = "chat.html";
  });
}
</script>
"""

CHAT_SCRIPT = """
<script>
(function () {
  var ROLE = "@@ROLE@@";
  var PORT = "@@PORT@@";
  var SERVICES = @@SERVICES@@;
  var API_ORIGIN = "@@PUBLIC_API@@";
  function apiUrl(path) {
    if (location.hostname === "127.0.0.1" || location.hostname === "localhost") return path;
    return API_ORIGIN ? API_ORIGIN.replace(/\/$/, "") + path : path;
  }
  var thread = document.querySelector("#thread");
  var form = document.querySelector("#ask-form");
  var input = document.querySelector("#question");
  var error = document.querySelector("#question-error");
  var send = document.querySelector("#send");

  function findService(id) {
    for (var i = 0; i < SERVICES.length; i++) if (SERVICES[i].id === id) return SERVICES[i];
    return null;
  }
  function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, function (ch) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[ch];
    });
  }
  function actionFor(id) {
    var item = findService(id);
    if (!item || id === "none") return null;
    if (ROLE === "guest") {
      if (id === "announcement") return { kind: "note", text: "校园公告没有单独办理地址，请查看后勤保障部官网的通知公告。" };
      return { kind: "link", href: "login.html", label: "登录后办理" };
    }
    if (item.student_only && ROLE !== "student") return { kind: "note", text: "水电缴费面向在校学生。教职工账号不提供缴费和账单。" };
    var url = PORT === "pc" ? item.pc : item.mobile;
    if (url) return { kind: "link", href: "jump.html?service=" + encodeURIComponent(id), label: "去办理" };
    if (PORT === "pc" && id === "utility-pay") return { kind: "link", href: "qrcode.html", label: "查看手机办理二维码" };
    if (PORT === "mobile" && item.pc) return { kind: "link", href: "guide.html?service=" + encodeURIComponent(id), label: "查看电脑办理说明" };
    if (id === "announcement") {
      return { kind: "link", href: PORT === "mobile" ? "guide.html?service=announcement" : "services.html#announcement", label: "查看出处说明" };
    }
    return null;
  }
  function ask(question) {
    var empty = document.querySelector("#empty-thread");
    if (empty) empty.remove();
    var user = document.createElement("div");
    user.className = "flex justify-end";
    user.innerHTML = '<div class="bubble-user max-w-[86%] px-4 py-3 text-sm leading-6">' + escapeHtml(question) + "</div>";
    thread.appendChild(user);
    var pending = document.createElement("div");
    pending.className = "flex justify-start";
    pending.innerHTML = '<div class="bubble-bot max-w-[86%] px-4 py-3 text-sm text-muted">正在查阅后勤服务知识库…</div>';
    thread.appendChild(pending);
    thread.scrollTop = thread.scrollHeight;
    send.disabled = true;
    fetch(apiUrl("/api/chat"), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: question, role: ROLE, port: PORT })
    }).then(function (response) { return response.json(); }).then(function (data) {
      pending.remove();
      paint(data);
    }).catch(function () {
      pending.remove();
      paint({ ok: false, answer: "暂时无法连接问答服务，请稍后重试。你也可以拨打后勤服务热线 0731-88836000。", covered: false, serviceId: "none" });
    }).finally(function () { send.disabled = false; input.focus(); });
  }
  function paint(data) {
    var action = actionFor(data.serviceId);
    var tag = data.ok === false
      ? '<p class="mb-2 text-xs font-medium text-[#8A5A12]"><i class="fa-solid fa-circle-info mr-1" aria-hidden="true"></i>暂时无法生成回答</p>'
      : (data.covered === false
        ? '<p class="mb-2 text-xs font-medium text-[#8A5A12]"><i class="fa-solid fa-circle-info mr-1" aria-hidden="true"></i>暂未收录</p>'
        : '<p class="mb-2 text-xs font-medium text-teal"><i class="fa-solid fa-book-open mr-1" aria-hidden="true"></i>来自后勤服务知识库</p>');
    var extra = "";
    if (action && action.kind === "link") {
      extra = '<a class="mt-3 inline-flex min-h-11 items-center rounded-lg bg-brand px-4 text-sm text-white" href="' + action.href + '">' + escapeHtml(action.label) + "</a>";
    } else if (action && action.kind === "note") {
      extra = '<p class="mt-3 text-sm leading-6 text-muted">' + escapeHtml(action.text) + "</p>";
    }
    var node = document.createElement("div");
    node.className = "flex justify-start";
    node.innerHTML = '<div class="bubble-bot max-w-[92%] px-4 py-3 text-sm leading-6">' + tag +
      '<div class="whitespace-pre-wrap">' + escapeHtml(data.answer || "") + "</div>" + extra +
      '<div class="mt-3"><button type="button" class="speak min-h-11 text-sm text-teal"><i class="fa-solid fa-volume-high mr-1" aria-hidden="true"></i>朗读这段回答</button></div></div>';
    node.querySelector(".speak").addEventListener("click", function () { speak(data.answer || ""); });
    thread.appendChild(node);
    var rail = document.querySelector("#action-rail");
    var item = findService(data.serviceId);
    if (rail) {
      if (!item || data.serviceId === "none") {
        rail.innerHTML = "<p class=\\"text-sm leading-6 text-muted\\">这条回答没有单独的办理入口。需要人工时，请拨打 " + escapeHtml(data.hotline || "0731-88836000") + "。</p>";
      } else {
        rail.innerHTML = '<p class="text-xs text-muted">这一答对应的入口</p><h2 class="mt-1 text-lg font-medium">' + escapeHtml(item.name) + "</h2><p class=\\"mt-2 text-sm leading-6 text-muted\\">" + escapeHtml(item.summary) + "</p>" + extra;
      }
    }
    thread.scrollTop = thread.scrollHeight;
  }
  function speak(text) {
    if (!window.speechSynthesis) {
      error.textContent = "当前浏览器不能朗读，请直接阅读文字。";
      return;
    }
    window.speechSynthesis.cancel();
    var utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = "zh-CN";
    window.speechSynthesis.speak(utterance);
  }
  form.addEventListener("submit", function (event) {
    event.preventDefault();
    var question = input.value.trim();
    if (!question) { error.textContent = "请先写下你的问题。"; input.focus(); return; }
    error.textContent = "";
    input.value = "";
    ask(question);
  });
  input.addEventListener("keydown", function (event) {
    if (event.key === "Enter" && !event.shiftKey) { event.preventDefault(); form.requestSubmit(); }
  });
  var preset = sessionStorage.getItem("hq-question");
  if (preset) { sessionStorage.removeItem("hq-question"); ask(preset); }
})();
</script>
"""


def composer(listening_href="listening.html"):
    return f"""
<form id="ask-form" class="border-t border-slate-200 bg-white p-3">
  <label for="question" class="mb-2 block text-xs text-muted">你的问题</label>
  <div class="flex items-end gap-2">
    <a href="{listening_href}" class="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl border border-slate-200 text-teal" aria-label="改用语音"><i class="fa-solid fa-microphone"></i></a>
    <textarea id="question" rows="2" class="min-h-11 flex-1 resize-none rounded-xl border border-slate-300 px-3 py-2 text-base focus:border-teal" placeholder="例如：宿舍空调不制冷怎么办"></textarea>
    <button id="send" class="h-11 shrink-0 rounded-xl bg-brand px-4 text-sm font-medium text-white" type="submit">发送</button>
  </div>
  <p id="question-error" class="mt-1 min-h-5 text-sm text-red-800" role="alert"></p>
  <p class="text-xs text-muted">回答只依据已审核的后勤服务知识库。</p>
</form>"""


def pc_frame(role, current, title, main, right="", listening=False):
    name, sub, _ = PEOPLE[role]
    home = "../../index.html"
    right_html = f'<aside class="hidden h-full flex-col overflow-y-auto border-slate-200 bg-white p-5 lg:flex lg:border-l">{right}</aside>' if right else ""
    cols = "lg:grid-cols-[240px_minmax(0,1fr)_300px]" if right else "lg:grid-cols-[240px_minmax(0,1fr)]"
    body = f"""
<body class="min-h-screen bg-mist text-inktext">
<a class="sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-4 focus:z-50 focus:bg-white focus:px-3 focus:py-2" href="#main">跳到主要内容</a>
<header class="sticky top-0 z-20 flex h-16 items-center justify-between border-b border-[#C8CAD1] bg-white px-5 text-inktext">
  <a href="{home}" class="flex items-center gap-3">
    <span class="flex h-9 w-9 items-center justify-center rounded-lg bg-brand text-sm font-semibold text-white">后</span>
    <span><span class="block font-semibold leading-none">中南大学</span><span class="mt-1 block text-xs text-muted">智慧后勤AI助手</span></span>
  </a>
  <div class="flex items-center gap-3 text-sm">
    <span class="hidden text-muted sm:inline">{name} · {sub}</span>
    <a class="rounded-lg border border-[#C8CAD1] px-3 py-2 text-brand hover:bg-teal-50" href="{home}">返回导航</a>
  </div>
</header>
<div class="lg:grid {cols} lg:h-[calc(100dvh-4rem)]">
  <aside class="border-b border-slate-200 bg-white lg:overflow-y-auto lg:border-b-0 lg:border-r">
    <div class="p-5">{avatar(listening)}</div>
    <nav class="flex gap-2 overflow-x-auto px-3 pb-4 lg:block lg:space-y-1" aria-label="功能">{nav_links("pc", role, current)}</nav>
  </aside>
  <main id="main" class="min-h-0 lg:overflow-y-auto">{main}</main>
  {right_html}
</div>
</body>"""
    return document(title, body)


def mobile_frame(role, current, title, main, footer=""):
    name, sub, _ = PEOPLE[role]
    home = "../../index.html"
    cols = len(NAV[("mobile", role)])
    body = f"""
<body class="bg-mist text-inktext">
<div class="mx-auto flex h-dvh w-full flex-col bg-mist md:my-6 md:h-[min(844px,calc(100dvh-3rem))] md:w-[420px] md:overflow-hidden md:rounded-2xl md:border md:border-[#C8CAD1] md:bg-white md:shadow-[0_8px_24px_rgba(48,135,204,.12)]">
  <header class="flex h-14 shrink-0 items-center justify-between border-b border-[#C8CAD1] bg-white px-4">
    <div><p class="text-sm font-semibold leading-none text-ink">中南大学</p><p class="mt-1 text-xs text-muted">{name} · {sub}</p></div>
    <a class="rounded-lg bg-teal-50 px-3 py-2 text-xs text-brand" href="{home}">导航</a>
  </header>
  <main id="main" class="flex min-h-0 flex-1 flex-col overflow-y-auto">{main}</main>
  {footer}
  <nav class="grid shrink-0 border-t border-slate-200 bg-white" style="grid-template-columns:repeat({cols},minmax(0,1fr))" aria-label="主导航">{nav_links("mobile", role, current)}</nav>
</div>
</body>"""
    return document(title, body)


def rail_shortcuts(role, port="pc"):
    tiles = []
    for item in SERVICES:
        if item["id"] == "announcement":
            continue
        if item["student_only"] and role != "student":
            continue
        if role == "guest":
            href = "login.html"
        else:
            href, _label = action_href(item, role, port)
            if not href:
                continue
        tiles.append(
            f'<a class="flex min-h-11 items-center gap-2 rounded-lg border border-[#C8CAD1] bg-[#F5F7FA] px-3 text-sm text-ink hover:border-brand hover:bg-teal-50" href="{href}">'
            f'<i class="fa-solid {item["icon"]} w-4 text-brand"></i><span class="min-w-0 truncate">{item["name"]}</span></a>'
        )
    note = "登录后才能办理。" if role == "guest" else "从这里直接进入对应事项。"
    return f"""
<div class="mt-auto pt-4">
  <p class="text-sm font-semibold text-ink">办事入口</p>
  <p class="mt-1 text-xs leading-5 text-muted">{note}</p>
  <div class="mt-3 grid grid-cols-2 gap-2">{''.join(tiles)}</div>
</div>
"""


def rail_home(role):
    return f"""
<div>
<p class="text-xs font-medium text-brand">值班说明</p>
<h2 class="mt-2 text-xl font-semibold text-ink">先问清楚，再决定要不要跳走</h2>
<p class="mt-3 text-sm leading-6 text-muted">能在知识库里回答的，直接告诉你。要办理的，按你现在用的电脑或手机，打开对应的原系统。</p>
<img class="mt-5 h-28 w-full rounded-lg object-cover" src="{CAMPUS}" width="600" height="220" alt="大学校园里的教学楼">
<p class="mt-3 text-sm leading-6">后勤服务热线 <span class="num font-medium">{HOTLINE}</span><br>全天值班。综合服务大厅在岳麓山校区甘棠村 1 栋。</p>
</div>
{rail_shortcuts(role, "pc")}
"""


def home_main(role, port):
    _, _, welcome = PEOPLE[role]
    photo = f'<img class="mb-4 h-36 w-full rounded-2xl object-cover" src="{DORM if role == "student" else CAMPUS}" width="800" height="280" alt="校园建筑与宿舍楼">' if port == "mobile" else ""
    mobile_entries = rail_shortcuts(role, "mobile").replace("mt-auto", "mx-4 mb-5", 1) if port == "mobile" else ""
    return f"""
<div class="p-5 lg:p-8">
  {photo}
  <p class="text-xs tracking-widest text-teal">后勤值班台</p>
  <h1 class="mt-2 font-serif text-3xl text-ink lg:text-4xl">{welcome}</h1>
  <p class="mt-3 max-w-xl text-sm leading-6 text-muted">可以问报修、水电、班车、食堂、宿舍和场馆。回答来自 2026 年 9 月 17 日截止的后勤服务知识库。</p>
  <div class="mt-5 flex flex-wrap gap-2">{suggestion_buttons()}</div>
</div>
{composer()}
{mobile_entries}
"""


def empty_thread():
    return f"""
<div id="empty-thread" class="m-4 rounded-2xl border border-dashed border-slate-300 bg-white p-5">
  <h1 class="font-serif text-2xl text-ink">把问题发给值班助手</h1>
  <p class="mt-2 text-sm leading-6 text-muted">发送后会查阅知识库。知识库没有的内容，会直接说暂未收录。</p>
  <div class="mt-4 flex flex-wrap gap-2">{suggestion_buttons()}</div>
</div>
<div id="thread" class="flex-1 space-y-3 overflow-y-auto px-4 pb-4" aria-live="polite"></div>
"""


def chat_main():
    return f'<div class="flex h-full min-h-[70dvh] flex-col lg:h-full">{empty_thread()}{composer()}</div>'


def mobile_chat_main():
    return f'<div class="flex min-h-0 flex-1 flex-col">{empty_thread()}{composer()}</div>'


LISTEN_SCRIPT = """
<script>
(function () {
  var box = document.querySelector("#heard");
  var recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (recognition) {
    var hear = new recognition();
    hear.lang = "zh-CN";
    hear.onresult = function (event) {
      box.value = event.results[0][0].transcript;
    };
    hear.onerror = function () {};
    try { hear.start(); } catch (error) {}
  }
  document.querySelector("#send-listen").addEventListener("click", function () {
    var question = box.value.trim();
    var error = document.querySelector("#listen-error");
    if (!question) { error.textContent = "还没有听到问题，请输入后再发送。"; box.focus(); return; }
    sessionStorage.setItem("hq-question", question);
    location.href = "chat.html";
  });
})();
</script>
"""


def listening_main():
    return """
<div class="mx-auto max-w-lg p-6">
  <h1 class="font-serif text-3xl text-ink">正在听</h1>
  <p class="mt-2 text-sm leading-6 text-muted">浏览器若允许麦克风，会把识别出的话填进下面。你也可以直接改字。</p>
  <label for="heard" class="mt-5 block text-sm">听到的问题</label>
  <textarea id="heard" rows="3" class="mt-2 w-full rounded-xl border border-slate-300 px-3 py-3 text-base">宿舍水龙头坏了怎么报修？</textarea>
  <p id="listen-error" class="mt-2 min-h-5 text-sm text-red-800" role="alert"></p>
  <button id="send-listen" type="button" class="mt-2 min-h-11 rounded-xl bg-brand px-5 text-sm font-medium text-white">停止并发送</button>
</div>
"""


def category_main():
    blocks = [
        ("报修", "fa-screwdriver-wrench", "宿舍家具、门锁、空调，以及公共区域的泥木水电，都属于日常零星维修。可拨打 " + HOTLINE + "，登录后也能进入网上报修。", "宿舍水龙头坏了怎么报修？"),
        ("水电缴纳", "fa-bolt", "学生在手机上缴费，路径是后勤公众号的服务中心。电脑不能直接缴，登录后会看到二维码。本人用量和欠费本期不能查。参考电价 0.619 元/度，水价 3.56 元/吨，以平台显示为准。", "学生水电费怎么缴纳？"),
        ("班车", "fa-bus", "工作日有校区通勤班车。时刻以班车查询系统当日公布为准。书面清单只提供电脑地址，手机上会提示改用电脑。", "校区间班车怎么查询时刻？"),
        ("其他办事", "fa-ellipsis", "游泳馆、服务监督两端都能办。宾馆、报刊、失物招领目前按电脑地址提供。校园公告没有单独链接，请看后勤保障部官网通知。", "潇湘校区游泳馆什么时候开放？"),
    ]
    cards = []
    for title, icon, text, question in blocks:
        cards.append(f"""
<article class="rounded-2xl border border-slate-200 bg-white p-5">
  <span class="flex h-11 w-11 items-center justify-center rounded-xl bg-teal-50 text-teal"><i class="fa-solid {icon}"></i></span>
  <h2 class="mt-4 text-lg font-medium">{title}</h2>
  <p class="mt-2 text-sm leading-6 text-muted">{text}</p>
  <button type="button" data-ask="{escape(question)}" class="mt-4 min-h-11 rounded-lg border border-slate-300 px-4 text-sm">就此提问</button>
</article>""")
    return f"""
<div class="p-5 lg:p-8">
  <h1 class="font-serif text-3xl text-ink">公开办事说明</h1>
  <p class="mt-2 max-w-2xl text-sm leading-6 text-muted">游客只能看已公开的说明。办理前需要通过中南大学统一身份认证，原型里用演示身份进入。</p>
  <div class="mt-6 grid gap-4 md:grid-cols-2">{''.join(cards)}</div>
</div>
<script>
document.querySelectorAll("[data-ask]").forEach(function (el) {{
  el.addEventListener("click", function () {{
    sessionStorage.setItem("hq-question", el.getAttribute("data-ask"));
    location.href = "chat.html";
  }});
}});
</script>
"""


def login_main(port):
    student = "../student/home.html"
    staff = "../staff/home.html"
    return f"""
<div class="mx-auto max-w-xl p-6">
  <p class="text-xs tracking-widest text-teal">中南大学统一身份认证</p>
  <h1 class="mt-2 font-serif text-3xl text-ink">登录后才能办理</h1>
  <p class="mt-3 text-sm leading-6 text-muted">正式环境跳转到学校统一身份认证，本系统不另外收集学号或工号。下面两个按钮只用于原型演示。</p>
  <div class="mt-6 space-y-3">
    <a class="flex min-h-14 items-center justify-between rounded-2xl bg-brand px-5 text-white" href="{student}">以学生林夏进入 <i class="fa-solid fa-arrow-right"></i></a>
    <a class="flex min-h-14 items-center justify-between rounded-2xl border border-slate-300 bg-white px-5" href="{staff}">以教职工周宁进入 <i class="fa-solid fa-arrow-right"></i></a>
  </div>
  <p class="mt-4 text-xs leading-5 text-muted">游客仍可返回问答，查看公开说明。个人账单和会议提醒不对游客开放。</p>
</div>
"""


def not_found_main():
    return f"""
<div class="mx-auto max-w-2xl p-6">
  <p class="text-xs text-muted">版式示例 · 问题</p>
  <h1 class="mt-2 font-serif text-3xl text-ink">图书馆的座位怎么预约？</h1>
  <div class="bubble-bot mt-6 p-5 text-sm leading-7">
    <p class="mb-2 text-xs font-medium text-[#8A5A12]"><i class="fa-solid fa-circle-info mr-1"></i>暂未收录</p>
    <p>暂未收录。座位预约不属于后勤服务知识库。如需人工确认是不是后勤的事，请拨打后勤服务热线 {HOTLINE}，全天有人值班。</p>
  </div>
  <a class="mt-4 inline-flex min-h-11 items-center text-sm text-teal" href="chat.html">返回对话，试一个后勤问题</a>
</div>
"""


def services_main(role, port):
    title = "可办的事" if port == "mobile" else "办事清单"
    note = "手机清单只有报修、服务监督、游泳馆" + ("和水电缴费。" if role == "student" else "。") + "其余有电脑地址的事项，在这里只给出说明。"
    if port == "pc":
        note = "电脑可以打开书面清单里的八个地址。水电缴费没有电脑办理页，学生会看到二维码。"
        if role == "staff":
            note = "教职工可以打开报修、监督、游泳馆，以及班车、宾馆、报刊、失物和水电说明。不提供学生水电缴费。"
    return f"""
<div class="p-5 lg:p-8">
  <h1 class="font-serif text-3xl text-ink">{title}</h1>
  <p class="mt-2 max-w-2xl text-sm leading-6 text-muted">{note} 标成「地址待复核」的电脑链接，按书面清单保留，打开时可能暂时找不到页面。</p>
  <div class="mt-6 grid gap-4 md:grid-cols-2">{service_cards(role, port)}</div>
</div>
"""


JUMP_SCRIPT = """
<script>
(function () {
  var ROLE = "@@ROLE@@";
  var PORT = "@@PORT@@";
  var SERVICES = @@SERVICES@@;
  var params = new URLSearchParams(location.search);
  var id = params.get("service") || "repair";
  var item = null;
  for (var i = 0; i < SERVICES.length; i++) if (SERVICES[i].id === id) item = SERVICES[i];
  if (!item) return;
  var url = PORT === "pc" ? item.pc : item.mobile;
  document.querySelector("#jump-name").textContent = item.name;
  document.querySelector("#jump-detail").textContent = item.detail;
  var review = document.querySelector("#jump-review");
  var go = document.querySelector("#jump-go");
  var blocked = document.querySelector("#jump-blocked");
  if (item.student_only && ROLE !== "student") {
    blocked.hidden = false;
    blocked.textContent = "水电缴费只对学生开放。";
    go.hidden = true;
    return;
  }
  if (!url) {
    blocked.hidden = false;
    blocked.textContent = PORT === "pc" ? "这件事没有电脑办理地址。" : "这件事没有手机办理地址，请改用电脑。";
    go.hidden = true;
    return;
  }
  go.href = url;
  go.hidden = false;
  if (PORT === "pc" && item.pc_review) review.hidden = false;
})();
</script>
"""


def jump_main():
    return """
<div class="mx-auto max-w-xl p-6">
  <p class="text-xs tracking-widest text-teal">即将离开助手</p>
  <h1 id="jump-name" class="mt-2 font-serif text-3xl text-ink">网上报修</h1>
  <p id="jump-detail" class="mt-4 text-sm leading-7 text-muted">办理过程在原来的业务系统里完成，助手不保存你的单据。</p>
  <p id="jump-review" hidden class="mt-4 rounded-xl bg-red-50 px-4 py-3 text-sm text-red-900">这份书面地址目前可能无法打开，业务部门复核前仍按清单提供。</p>
  <p id="jump-blocked" hidden class="mt-4 rounded-xl bg-amber-50 px-4 py-3 text-sm"></p>
  <div class="mt-6 flex flex-wrap gap-3">
    <a id="jump-go" class="inline-flex min-h-11 items-center rounded-xl bg-brand px-5 text-sm text-white" target="_blank" rel="noopener" href="http://zhhq.csu.edu.cn/stu/repairHome.html">继续前往</a>
    <a class="inline-flex min-h-11 items-center rounded-xl border border-slate-300 bg-white px-5 text-sm" href="services.html">留在助手</a>
  </div>
</div>
"""


def utility_main(port, role):
    pay = ""
    if role == "student" and port == "mobile":
        pay = '<a class="inline-flex min-h-11 items-center rounded-xl bg-brand px-5 text-sm text-white" href="jump.html?service=utility-pay">去缴纳</a>'
    elif role == "student":
        pay = '<a class="inline-flex min-h-11 items-center rounded-xl bg-brand px-5 text-sm text-white" href="qrcode.html">在电脑上查看二维码</a>'
    info = ""
    if port == "pc":
        info = '<a class="inline-flex min-h-11 items-center rounded-xl border border-slate-300 bg-white px-5 text-sm" href="jump.html?service=utility-info">打开水电说明页</a>'
    else:
        info = '<a class="inline-flex min-h-11 items-center rounded-xl border border-slate-300 bg-white px-5 text-sm" href="guide.html?service=utility-info">电脑上的说明页</a>'
    return f"""
<div class="p-5 lg:p-8">
  <h1 class="font-serif text-3xl text-ink">水电怎么缴</h1>
  <p class="mt-2 max-w-2xl text-sm leading-6 text-muted">本期只引导去哪里缴。本人用量、欠费和房间账单等水电接口确认后再做。</p>
  <ol class="mt-6 space-y-3 text-sm leading-6">
    <li class="rounded-2xl bg-white p-4"><span class="num text-teal">01</span> 打开「中南大学后勤保障部」公众号，进入服务中心、服务平台、水电缴费。</li>
    <li class="rounded-2xl bg-white p-4"><span class="num text-teal">02</span> 注册手机号，再用统一身份认证关联学工信息。</li>
    <li class="rounded-2xl bg-white p-4"><span class="num text-teal">03</span> 按校区、区域、楼栋、楼层、房间绑定账户，输入金额。成功后即时到账。</li>
  </ol>
  <div class="mt-4 rounded-2xl border border-slate-200 bg-white p-4 text-sm leading-6">
    <p>参考单价：电 0.619 元/度，水 3.56 元/吨。这是平台示例，以缴费页面为准。</p>
    <p class="mt-2">岳麓山校区窗口：能源管理中心办公楼一楼，电话 88836337。上午 8:00—12:00，下午 14:30—18:00。</p>
  </div>
  <div class="mt-4 flex flex-wrap gap-3">{pay}{info}</div>
  <button type="button" disabled class="mt-4 flex min-h-11 cursor-not-allowed items-center gap-2 rounded-xl bg-slate-200 px-4 text-sm text-slate-600" aria-disabled="true">
    <i class="fa-solid fa-lock"></i> 查询本人用量和欠费 · 待接口确认
  </button>
</div>
"""


QR_SCRIPT = """
<script src="https://cdn.jsdelivr.net/npm/qrcode@1.5.4/build/qrcode.min.js"></script>
<script>
var url = "https://znu-hip.csu.edu.cn/saas_wap/";
var canvas = document.querySelector("#qr");
if (window.QRCode) {
  QRCode.toCanvas(canvas, url, { width: 196, margin: 1, color: { dark: "#10243A", light: "#F8FBFC" } });
}
</script>
"""


def qrcode_main():
    return """
<div class="mx-auto max-w-xl p-6 text-center">
  <p class="text-xs tracking-widest text-teal">仅手机可办</p>
  <h1 class="mt-2 font-serif text-3xl text-ink">请用手机缴纳水电</h1>
  <p class="mt-3 text-sm leading-6 text-muted">学生水费、电费没有电脑办理页。用手机扫下面的码，打开缴费页面。助手不保存账单。</p>
  <div class="mx-auto mt-6 w-fit rounded-3xl bg-white p-4 shadow-sm"><canvas id="qr" width="196" height="196" aria-label="水电缴费二维码"></canvas></div>
  <p class="mt-4 break-all text-sm"><a class="text-teal" href="https://znu-hip.csu.edu.cn/saas_wap/">https://znu-hip.csu.edu.cn/saas_wap/</a></p>
  <p class="mt-3 text-sm text-muted">若二维码没有画出来，可以把地址复制到手机浏览器。</p>
  <button type="button" disabled class="mx-auto mt-4 flex min-h-11 cursor-not-allowed items-center gap-2 rounded-xl bg-slate-200 px-4 text-sm text-slate-600" aria-disabled="true"><i class="fa-solid fa-lock"></i> 查询本人用量 · 待接口确认</button>
</div>
"""


GUIDE_SCRIPT = """
<script>
(function () {
  var SERVICES = @@SERVICES@@;
  var params = new URLSearchParams(location.search);
  var id = params.get("service") || "shuttle";
  var item = null;
  for (var i = 0; i < SERVICES.length; i++) if (SERVICES[i].id === id) item = SERVICES[i];
  if (!item) return;
  document.querySelector("#guide-name").textContent = item.name;
  document.querySelector("#guide-detail").textContent = item.detail;
  var address = document.querySelector("#guide-address");
  var copy = document.querySelector("#copy-address");
  if (item.pc) {
    address.hidden = false;
    address.querySelector("input").value = item.pc;
    copy.hidden = false;
    copy.addEventListener("click", function () {
      var done = document.querySelector("#copy-done");
      if (navigator.clipboard) {
        navigator.clipboard.writeText(item.pc).then(function () { done.textContent = "已复制，请到电脑上打开。"; });
      } else {
        address.querySelector("input").select();
        done.textContent = "请长按地址并复制。";
      }
    });
  }
})();
</script>
"""


def guide_main():
    return f"""
<div class="p-5">
  <p class="text-xs tracking-widest text-teal">请改用电脑</p>
  <h1 id="guide-name" class="mt-2 font-serif text-3xl text-ink">班车查询</h1>
  <p id="guide-detail" class="mt-3 text-sm leading-7 text-muted">书面清单只提供了电脑地址，手机上不直接打开。</p>
  <div id="guide-address" class="mt-4">
    <label for="pc-url" class="text-xs text-muted">电脑地址</label>
    <input id="pc-url" readonly class="mt-1 w-full rounded-xl border border-slate-300 bg-white px-3 py-3 text-sm" value="https://wxxy.csu.edu.cn/site/shuttleBus/index?bus_id=2">
  </div>
  <button id="copy-address" type="button" class="mt-3 min-h-11 rounded-xl bg-brand px-4 text-sm text-white">复制电脑地址</button>
  <p id="copy-done" class="mt-2 min-h-5 text-sm text-teal" role="status"></p>
  <a class="mt-4 inline-flex min-h-11 items-center text-sm text-teal" href="services.html">返回办事</a>
  <section class="mt-8">
    <h2 class="text-sm font-medium">同样只在电脑办理的事项</h2>
    <ul class="mt-3 space-y-2 text-sm leading-6 text-muted">
      <li><a class="text-teal" href="guide.html?service=utility-info">水电费服务</a></li>
      <li><a class="text-teal" href="guide.html?service=shuttle">班车查询</a></li>
      <li><a class="text-teal" href="guide.html?service=hotel">校园宾馆</a></li>
      <li><a class="text-teal" href="guide.html?service=newspaper">报刊订阅</a></li>
      <li><a class="text-teal" href="guide.html?service=lost">失物招领</a></li>
      <li><a class="text-teal" href="guide.html?service=announcement">校园公告（两端都没有单独地址）</a></li>
    </ul>
  </section>
</div>
"""


def profile_main(role):
    if role == "student":
        rows = [
            ("姓名", "林夏"),
            ("学号", "820240118"),
            ("身份", "学生"),
            ("院系", "计算机学院"),
            ("年级", "2024 级"),
            ("校区 / 宿舍", "麓南校区升华学生公寓 7 栋 314"),
        ]
        note = "住宿信息来自学校共享的学生住宿数据，只能查看。水电账户的绑定在水电系统里，这里不重复建一份。"
        extra = ""
    else:
        rows = [
            ("姓名", "周宁"),
            ("工号", "T20190086"),
            ("身份", "教职工"),
            ("部门", "后勤保障部"),
            ("在岗情况", "在岗"),
        ]
        note = "部门、工号和在岗情况来自人事共享数据，只能查看。会议提醒按工号投递，不使用手机号作为默认通道。"
        extra = '<a class="mt-4 inline-flex min-h-11 items-center rounded-xl border border-slate-300 bg-white px-4 text-sm" href="../recipient/inbox.html">查看我的会议提醒</a>'
    body = "".join(f'<div class="flex items-baseline justify-between gap-4 border-t border-slate-100 py-3"><dt class="text-sm text-muted">{k}</dt><dd class="text-right text-sm font-medium">{v}</dd></div>' for k, v in rows)
    return f"""
<div class="mx-auto max-w-xl p-5 lg:p-8">
  <h1 class="font-serif text-3xl text-ink">我的身份</h1>
  <p class="mt-2 text-sm leading-6 text-muted">{note}</p>
  <dl class="mt-4 rounded-2xl bg-white px-4">{body}</dl>
  {extra}
  <a class="mt-4 block text-sm text-muted" href="../guest/home.html">退出演示身份</a>
</div>
"""


def inbox_main(port):
    detail = "detail.html"
    pad = "p-5 lg:p-8" if port == "pc" else "p-4"
    return f"""
<div class="{pad}">
  <p class="text-xs tracking-widest text-teal">学校 ITS 已按工号推送</p>
  <h1 class="mt-2 font-serif text-3xl text-ink">会议提醒</h1>
  <p class="mt-2 text-sm leading-6 text-muted">正式通道是学校消息。这一页展示接收人看到的内容，方便演示。同一会议只提醒一次。</p>
  <div class="mt-5 space-y-3">
    <a class="block rounded-2xl bg-white p-4 shadow-sm" href="{detail}">
      <div class="flex items-center justify-between gap-3"><h2 class="font-medium">后勤周例会</h2>{badge("待提醒", "amber")}</div>
      <p class="mt-2 text-sm text-muted num">2026-10-22 09:00 · 本部后勤楼 3 楼会议室</p>
      <p class="mt-1 text-sm">会前 1 小时提醒周宁、赵衡、陈茉</p>
    </a>
    <article class="rounded-2xl bg-white p-4">
      <div class="flex items-center justify-between"><h2 class="font-medium">门户挂载确认会</h2>{badge("已提醒")}</div>
      <p class="mt-2 text-sm text-muted num">2026-10-18 15:00 · 已按设定时点送出</p>
    </article>
    <article class="rounded-2xl bg-white p-4 opacity-70">
      <div class="flex items-center justify-between"><h2 class="font-medium">水电接口协调会</h2>{badge("已取消", "ink")}</div>
      <p class="mt-2 text-sm text-muted">取消后不再提醒。</p>
    </article>
  </div>
</div>
"""


def detail_main():
    return f"""
<div class="mx-auto max-w-xl p-5 lg:p-8">
  <a class="text-sm text-teal" href="inbox.html">返回提醒</a>
  <div class="mt-3">{badge("待提醒", "amber")}</div>
  <h1 class="mt-3 font-serif text-3xl text-ink">后勤周例会</h1>
  <dl class="mt-5 space-y-3 rounded-2xl bg-white p-5 text-sm">
    <div class="flex justify-between gap-4"><dt class="text-muted">开始</dt><dd class="num">2026-10-22 09:00</dd></div>
    <div class="flex justify-between gap-4"><dt class="text-muted">地点</dt><dd>本部后勤楼 3 楼会议室</dd></div>
    <div class="flex justify-between gap-4"><dt class="text-muted">提醒</dt><dd>会前 60 分钟，只送一次</dd></div>
    <div class="flex justify-between gap-4"><dt class="text-muted">接收人</dt><dd class="text-right">周宁、赵衡、陈茉<br>按工号经 ITS 送达</dd></div>
  </dl>
  <p class="mt-4 text-sm leading-6 text-muted">这是接收到的提醒内容。会议没有审批，管理员保存后就会按时间推送。</p>
</div>
"""


ADMIN_NAV = [
    ("dashboard.html", "总览", "fa-gauge"),
    ("knowledge-list.html", "知识库", "fa-book"),
    ("knowledge-review.html", "审核", "fa-clipboard-check"),
    ("categories.html", "快捷分类", "fa-grip"),
    ("catalog-list.html", "功能清单", "fa-list"),
    ("meeting-list.html", "会议", "fa-calendar"),
    ("recipients.html", "提醒名单", "fa-users"),
    ("avatar.html", "形象与语音", "fa-user"),
    ("logs.html", "操作日志", "fa-clock-rotate-left"),
]
ADMIN_PARENT = {
    "knowledge-edit.html": "knowledge-list.html",
    "knowledge-review.html": "knowledge-review.html",
    "catalog-edit.html": "catalog-list.html",
    "meeting-edit.html": "meeting-list.html",
    "meeting-detail.html": "meeting-list.html",
}


def admin_frame(current, title, main, script=""):
    parent = ADMIN_PARENT.get(current, current)
    links = []
    for href, label, icon in ADMIN_NAV:
        on = href == parent
        cls = "bg-teal-50 font-medium text-brand" if on else "text-muted hover:bg-mist"
        links.append(f'<a class="flex min-h-11 items-center gap-3 rounded-lg px-3 text-sm {cls}" href="{href}"><i class="fa-solid {icon} w-4"></i>{label}</a>')
    body = f"""
<body class="min-h-screen bg-mist text-inktext">
<div class="min-h-screen md:grid md:grid-cols-[220px_minmax(0,1fr)]">
  <aside class="border-r border-[#C8CAD1] bg-white text-inktext md:min-h-screen">
    <a href="../index.html" class="block px-5 py-5">
      <span class="flex h-9 w-9 items-center justify-center rounded-lg bg-brand text-sm font-semibold text-white">后</span>
      <span class="mt-3 block font-semibold">中南大学</span>
      <span class="mt-1 block text-xs text-muted">后勤业务管理</span>
    </a>
    <nav class="flex gap-2 overflow-x-auto px-3 pb-4 md:block md:space-y-1" aria-label="后台">{''.join(links)}</nav>
  </aside>
  <div class="min-w-0">
    <header class="flex h-16 items-center justify-between border-b border-slate-200 bg-white px-5">
      <h1 class="text-lg font-medium">{escape(title)}</h1>
      <div class="flex items-center gap-3 text-sm text-muted"><span>审核人 周宁</span><a class="text-teal" href="../index.html">返回导航</a></div>
    </header>
    <main id="main" class="p-5">{main}</main>
  </div>
</div>
{script}
</body>"""
    return document(title, body)


def admin_login():
    body = """
<body class="flex min-h-screen items-center justify-center bg-mist px-4 text-inktext">
<main class="w-full max-w-md rounded-2xl border border-[#C8CAD1] bg-white p-8">
  <p class="text-xs tracking-widest text-teal">后勤领导指定的管理员</p>
  <h1 class="mt-2 font-serif text-3xl text-ink">进入管理后台</h1>
  <p class="mt-3 text-sm leading-6 text-muted">正式环境走统一身份认证。原型直接进入，用来演示知识、清单和会议。</p>
  <a class="mt-6 flex min-h-12 items-center justify-center rounded-xl bg-brand font-medium text-white" href="dashboard.html">进入后台</a>
  <a class="mt-3 block text-center text-sm text-muted" href="../index.html">返回导航</a>
</main>
</body>"""
    return document("管理员登录", body)


def dashboard_main():
    bars = [40, 55, 48, 72, 63, 80, 58]
    days = ["一", "二", "三", "四", "五", "六", "日"]
    chart = "".join(
        f'<div class="flex flex-1 flex-col items-center gap-2"><div class="flex h-32 w-full items-end"><div class="w-full rounded-t bg-teal" style="height:{h}%"></div></div><span class="text-xs text-muted">{d}</span></div>'
        for h, d in zip(bars, days)
    )
    cards = [
        ("今日问答", "128", "演示数据"),
        ("已发布知识", "1", "后勤服务知识库"),
        ("待审核", "1", "宿舍报修范围补充"),
        ("即将提醒", "1", "后勤周例会"),
    ]
    stats = "".join(
        f'<article class="rounded-2xl border border-slate-200 bg-white p-5"><p class="text-sm text-muted">{k}</p><p class="num mt-2 text-3xl font-semibold">{v}</p><p class="mt-1 text-xs text-muted">{s}</p></article>'
        for k, v, s in cards
    )
    return f"""
<p class="text-sm text-muted">周宁，今天有 1 条知识待审核，1 场会议还没到提醒时间。</p>
<section class="mt-4 grid gap-3 sm:grid-cols-2 xl:grid-cols-4">{stats}</section>
<section class="mt-4 grid gap-4 lg:grid-cols-5">
  <article class="rounded-2xl border border-slate-200 bg-white p-5 lg:col-span-3">
    <h2 class="font-medium">近七日公开问答</h2>
    <p class="text-xs text-muted">演示数据，正式环境来自操作日志。</p>
    <div class="mt-4 flex items-end gap-3" role="img" aria-label="近七日问答量依次升高后略有回落">{chart}</div>
  </article>
  <article class="rounded-2xl border border-slate-200 bg-white p-5 lg:col-span-2">
    <h2 class="font-medium">下一场提醒</h2>
    <p class="mt-3 font-serif text-2xl text-ink">后勤周例会</p>
    <p class="num mt-2 text-sm text-muted">10 月 22 日 09:00 · 会前 1 小时</p>
    <a class="mt-4 inline-flex min-h-11 items-center text-sm text-teal" href="meeting-detail.html">查看会议</a>
  </article>
</section>
"""


def knowledge_list():
    rows = [
        ("kb", "中南大学后勤服务知识库（公文版）", "已发布", "公开", "2026-09-17", "teal"),
        ("repair-note", "宿舍报修范围补充", "待审核", "公开", "2026-10-19", "amber"),
        ("draft", "假期服务时间口径", "草稿", "内部", "2026-10-18", "ink"),
        ("old", "2025 年班车临时通知", "已下线", "公开", "2026-10-01", "danger"),
    ]
    body = []
    for key, name, status, vis, date, tone in rows:
        body.append(f"""<tr data-id="{key}">
          <td class="px-4 py-3">{name}</td>
          <td class="status px-4 py-3">{badge(status, tone)}</td>
          <td class="px-4 py-3">{vis}</td>
          <td class="num px-4 py-3 text-right">{date}</td>
        </tr>""")
    return f"""
<div id="banner" hidden class="mb-4 rounded-xl bg-teal-50 px-4 py-3 text-sm text-teal-700"></div>
<div class="mb-4 flex flex-wrap gap-3">
  <a class="inline-flex min-h-11 items-center rounded-xl bg-brand px-4 text-sm text-white" href="knowledge-edit.html">起草知识</a>
  <a class="inline-flex min-h-11 items-center rounded-xl border border-slate-300 bg-white px-4 text-sm" href="knowledge-review.html">处理待审核</a>
</div>
<div class="overflow-x-auto rounded-2xl border border-slate-200 bg-white">
  <table class="w-full min-w-[640px] text-left text-sm">
    <thead class="bg-mist text-muted"><tr><th class="px-4 py-3 font-medium">标题</th><th class="px-4 py-3 font-medium">状态</th><th class="px-4 py-3 font-medium">可见性</th><th class="px-4 py-3 text-right font-medium">日期</th></tr></thead>
    <tbody class="divide-y divide-slate-100">{''.join(body)}</tbody>
  </table>
</div>
<script>
var done = new URLSearchParams(location.search).get("done");
var banner = document.querySelector("#banner");
var status = document.querySelector('[data-id="repair-note"] .status');
if (done === "pass") {{ banner.hidden = false; banner.textContent = "审核已通过。宿舍报修范围补充改为已发布，前台可以引用。"; status.innerHTML = '{badge("已发布", "teal")}'; }}
if (done === "back") {{ banner.hidden = false; banner.textContent = "已退回给维护人修改。前台暂时不会引用这条知识。"; status.innerHTML = '{badge("退回修改", "danger")}'; }}
if (done === "draft") {{ banner.hidden = false; banner.textContent = "草稿已保存。提交审核之后才会进入待审。"; }}
</script>
"""


def knowledge_edit():
    return """
<form id="knowledge-form" class="max-w-2xl space-y-4 rounded-2xl bg-white p-5">
  <div>
    <label for="title" class="text-sm">标题 <span class="text-red-800">*</span></label>
    <input id="title" value="假期服务时间口径" class="mt-1 h-11 w-full rounded-lg border border-slate-300 px-3">
    <p id="title-error" class="mt-1 text-sm text-red-800"></p>
  </div>
  <div>
    <label for="body" class="text-sm">正文</label>
    <textarea id="body" rows="5" class="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2">寒暑假的食堂、宿舍、班车和收发室，以当期《后勤保障部关于寒（暑）假有关工作安排的通知》为准。</textarea>
  </div>
  <fieldset>
    <legend class="text-sm">可见性</legend>
    <label class="mt-2 flex min-h-11 items-center gap-2 text-sm"><input type="radio" name="vis" value="内部" checked> 内部，游客和普通登录用户看不到</label>
    <label class="flex min-h-11 items-center gap-2 text-sm"><input type="radio" name="vis" value="公开"> 公开</label>
  </fieldset>
  <button class="min-h-11 rounded-xl bg-brand px-5 text-sm text-white" type="submit">保存草稿</button>
</form>
<script>
document.querySelector("#knowledge-form").addEventListener("submit", function (event) {
  event.preventDefault();
  var title = document.querySelector("#title");
  var error = document.querySelector("#title-error");
  if (!title.value.trim()) { error.textContent = "请填写标题。"; title.focus(); return; }
  location.href = "knowledge-list.html?done=draft";
});
</script>
"""


def knowledge_review():
    return """
<article class="max-w-2xl rounded-2xl bg-white p-5">
  <div class="flex flex-wrap gap-2"><span class="rounded-full bg-amber-50 px-2 py-0.5 text-xs text-amber">待审核</span><span class="rounded-full bg-mist px-2 py-0.5 text-xs">公开</span></div>
  <h2 class="mt-3 text-xl font-medium">宿舍报修范围补充</h2>
  <p class="mt-2 text-sm text-muted">维护人 李衡 · 2026-10-19 提交</p>
  <p class="mt-4 text-sm leading-7">公共区域的泥、木、水、电属于零星维修，走网上报修或热线 0731-88836000。宿舍空调租赁故障，先到「永润智慧校园」办理点，不和零星维修混在一张单里。</p>
  <div class="mt-6 flex flex-wrap gap-3">
    <a class="inline-flex min-h-11 items-center rounded-xl bg-brand px-5 text-sm text-white" href="knowledge-list.html?done=pass">通过并发布</a>
    <a class="inline-flex min-h-11 items-center rounded-xl border border-red-200 px-5 text-sm text-red-800" href="knowledge-list.html?done=back">退回修改</a>
  </div>
  <p class="mt-4 text-xs leading-5 text-muted">通过后前台才能引用。下线是发布之后的另一步，下线后前台不再使用。</p>
</article>
"""


def categories_main():
    return """
<p class="max-w-2xl text-sm leading-6 text-muted">首批四类按方案上线。后台可以增删，前台快捷入口跟着变。对话本身仍能回答知识库里的食堂、宿舍和场馆。</p>
<ul id="cats" class="mt-4 max-w-xl divide-y divide-slate-100 rounded-2xl bg-white">
  <li class="flex min-h-14 items-center justify-between px-4"><span>报修</span><span class="text-xs text-muted">对应维修与修缮</span></li>
  <li class="flex min-h-14 items-center justify-between px-4"><span>水电缴纳</span><span class="text-xs text-muted">对应水电与能源</span></li>
  <li class="flex min-h-14 items-center justify-between px-4"><span>班车</span><span class="text-xs text-muted">对应交通出行</span></li>
  <li class="flex min-h-14 items-center justify-between px-4"><span>其他办事</span><span class="text-xs text-muted">场馆、监督、住宿说明</span></li>
</ul>
<form id="add-cat" class="mt-4 flex max-w-xl flex-wrap gap-2">
  <label for="cat-name" class="sr-only">新分类名称</label>
  <input id="cat-name" class="h-11 min-w-0 flex-1 rounded-lg border border-slate-300 px-3" placeholder="例如：餐饮">
  <button class="h-11 rounded-lg bg-brand px-4 text-sm text-white" type="submit">添加分类</button>
</form>
<p id="cat-error" class="mt-2 text-sm text-red-800" role="alert"></p>
<script>
document.querySelector("#add-cat").addEventListener("submit", function (event) {
  event.preventDefault();
  var input = document.querySelector("#cat-name");
  var error = document.querySelector("#cat-error");
  var name = input.value.trim();
  if (!name) { error.textContent = "请填写分类名称。"; input.focus(); return; }
  error.textContent = "";
  var li = document.createElement("li");
  li.className = "flex min-h-14 items-center justify-between px-4";
  li.innerHTML = "<span></span><span class=\\"text-xs text-teal\\">刚刚添加，演示不写入服务器</span>";
  li.querySelector("span").textContent = name;
  document.querySelector("#cats").appendChild(li);
  input.value = "";
});
</script>
"""


def catalog_rows():
    rows = []
    for item in SERVICES:
        if item["pc"] and item["mobile"]:
            terminal = "两端"
        elif item["pc"]:
            terminal = "仅电脑"
        elif item["mobile"]:
            terminal = "仅手机"
        else:
            terminal = "无地址"
        url = item["pc"] or item["mobile"] or "—"
        review = "待复核" if item["pc_review"] else "按清单"
        rows.append(f"<tr><td class=\"px-4 py-3\">{item['name']}</td><td class=\"px-4 py-3\">{item['who']}</td><td class=\"px-4 py-3\">{terminal}</td><td class=\"px-4 py-3\">{review}</td><td class=\"max-w-xs truncate px-4 py-3 text-xs text-muted\">{escape(url)}</td></tr>")
    return "".join(rows)


def catalog_list():
    return f"""
<div id="banner" hidden class="mb-4 rounded-xl bg-teal-50 px-4 py-3 text-sm text-teal-700">功能清单已保存。前台按适用对象和终端决定能不能打开。</div>
<div class="mb-4"><a class="inline-flex min-h-11 items-center rounded-xl bg-brand px-4 text-sm text-white" href="catalog-edit.html">编辑班车查询</a></div>
<div class="overflow-x-auto rounded-2xl border border-slate-200 bg-white">
  <table class="w-full min-w-[760px] text-left text-sm">
    <thead class="bg-mist text-muted"><tr><th class="px-4 py-3 font-medium">名称</th><th class="px-4 py-3 font-medium">适用对象</th><th class="px-4 py-3 font-medium">终端</th><th class="px-4 py-3 font-medium">地址</th><th class="px-4 py-3 font-medium">链接</th></tr></thead>
    <tbody class="divide-y divide-slate-100">{catalog_rows()}</tbody>
  </table>
</div>
<script>if (new URLSearchParams(location.search).get("done") === "saved") document.querySelector("#banner").hidden = false;</script>
"""


def catalog_edit():
    return """
<form id="catalog-form" class="grid max-w-2xl gap-4 rounded-2xl bg-white p-5 md:grid-cols-2">
  <div class="md:col-span-2"><label for="name" class="text-sm">功能名称 <span class="text-red-800">*</span></label><input id="name" value="班车查询" class="mt-1 h-11 w-full rounded-lg border border-slate-300 px-3"><p id="name-error" class="mt-1 text-sm text-red-800"></p></div>
  <div><label for="who" class="text-sm">适用对象</label><select id="who" class="mt-1 h-11 w-full rounded-lg border border-slate-300 px-3"><option>全部登录用户</option><option>学生</option><option>教职工</option></select></div>
  <div><label for="terminal" class="text-sm">终端</label><select id="terminal" class="mt-1 h-11 w-full rounded-lg border border-slate-300 px-3"><option selected>仅电脑</option><option>仅手机</option><option>两端</option></select></div>
  <div class="md:col-span-2"><label for="url" class="text-sm">访问地址</label><input id="url" value="https://wxxy.csu.edu.cn/site/shuttleBus/index?bus_id=2" class="mt-1 h-11 w-full rounded-lg border border-slate-300 px-3"></div>
  <div class="md:col-span-2"><label for="triggers" class="text-sm">触发说法</label><input id="triggers" value="班车、通勤车、校车时刻" class="mt-1 h-11 w-full rounded-lg border border-slate-300 px-3"></div>
  <div class="md:col-span-2"><label for="note" class="text-sm">补充说明</label><textarea id="note" rows="3" class="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2">手机端没有单独地址。请告诉用户改用电脑，并展示这条地址。</textarea></div>
  <div class="md:col-span-2"><button class="min-h-11 rounded-xl bg-brand px-5 text-sm text-white" type="submit">保存</button></div>
</form>
<script>
document.querySelector("#catalog-form").addEventListener("submit", function (event) {
  event.preventDefault();
  var name = document.querySelector("#name");
  if (!name.value.trim()) { document.querySelector("#name-error").textContent = "请填写功能名称。"; name.focus(); return; }
  location.href = "catalog-list.html?done=saved";
});
</script>
"""


def meeting_list():
    return """
<div id="banner" hidden class="mb-4 rounded-xl bg-teal-50 px-4 py-3 text-sm text-teal-700"></div>
<div class="mb-4"><a class="inline-flex min-h-11 items-center rounded-xl bg-brand px-4 text-sm text-white" href="meeting-edit.html">录入会议</a></div>
<div class="overflow-x-auto rounded-2xl border border-slate-200 bg-white">
  <table class="w-full min-w-[680px] text-left text-sm">
    <thead class="bg-mist text-muted"><tr><th class="px-4 py-3 font-medium">主题</th><th class="px-4 py-3 font-medium">开始</th><th class="px-4 py-3 font-medium">提醒</th><th class="px-4 py-3 font-medium">状态</th></tr></thead>
    <tbody id="meetings" class="divide-y divide-slate-100">
      <tr><td class="px-4 py-3"><a class="text-teal" href="meeting-detail.html">后勤周例会</a></td><td class="num px-4 py-3">10-22 09:00</td><td class="px-4 py-3">会前 60 分钟</td><td class="px-4 py-3">待提醒</td></tr>
      <tr><td class="px-4 py-3">门户挂载确认会</td><td class="num px-4 py-3">10-18 15:00</td><td class="px-4 py-3">会前 60 分钟</td><td class="px-4 py-3">已提醒</td></tr>
      <tr><td class="px-4 py-3">水电接口协调会</td><td class="num px-4 py-3">10-23 10:00</td><td class="px-4 py-3">—</td><td class="px-4 py-3">已取消</td></tr>
    </tbody>
  </table>
</div>
<p class="mt-3 text-xs text-muted">会议保存后即生效，本期不设审批。取消后的会议不再提醒。</p>
<script>
var params = new URLSearchParams(location.search);
if (params.get("done") === "saved") {
  var banner = document.querySelector("#banner");
  banner.hidden = false;
  banner.textContent = "会议已保存，无需审批。系统会在设定时点经 ITS 按工号提醒一次。";
  var tr = document.createElement("tr");
  var title = params.get("title") || "新会议";
  tr.innerHTML = "<td class=\\"px-4 py-3\\"></td><td class=\\"num px-4 py-3\\">刚刚录入</td><td class=\\"px-4 py-3\\">按表单设置</td><td class=\\"px-4 py-3\\">待提醒</td>";
  tr.querySelector("td").textContent = title;
  document.querySelector("#meetings").prepend(tr);
}
</script>
"""


def meeting_edit():
    return """
<form id="meeting-form" class="max-w-2xl space-y-4 rounded-2xl bg-white p-5">
  <div><label for="topic" class="text-sm">会议主题 <span class="text-red-800">*</span></label><input id="topic" class="mt-1 h-11 w-full rounded-lg border border-slate-300 px-3" placeholder="例如：节能工作布置会"><p id="topic-error" class="mt-1 text-sm text-red-800"></p></div>
  <div class="grid gap-4 md:grid-cols-2">
    <div><label for="when" class="text-sm">开始时间 <span class="text-red-800">*</span></label><input id="when" type="datetime-local" class="mt-1 h-11 w-full rounded-lg border border-slate-300 px-3"><p id="when-error" class="mt-1 text-sm text-red-800"></p></div>
    <div><label for="place" class="text-sm">地点 <span class="text-red-800">*</span></label><input id="place" class="mt-1 h-11 w-full rounded-lg border border-slate-300 px-3" placeholder="本部后勤楼"><p id="place-error" class="mt-1 text-sm text-red-800"></p></div>
  </div>
  <div><label for="ahead" class="text-sm">提前提醒（分钟）</label><input id="ahead" type="number" min="5" value="60" class="num mt-1 h-11 w-40 rounded-lg border border-slate-300 px-3"><p class="mt-1 text-xs text-muted">默认会前 1 小时，可按这一场改短。</p></div>
  <div>
    <label for="dept" class="text-sm">按部门筛选名单</label>
    <select id="dept" class="mt-1 h-11 rounded-lg border border-slate-300 px-3"><option value="all">全部</option><option value="后勤保障部">后勤保障部</option><option value="能源管理中心">能源管理中心</option><option value="生活服务中心">生活服务中心</option></select>
  </div>
  <fieldset>
    <legend class="text-sm">参会人（须有工号）</legend>
    <label class="mt-2 flex min-h-11 items-center gap-2 text-sm" data-dept="后勤保障部"><input type="checkbox" name="person" value="周宁" checked> 周宁 · T20190086 · 后勤保障部</label>
    <label class="flex min-h-11 items-center gap-2 text-sm" data-dept="能源管理中心"><input type="checkbox" name="person" value="赵衡"> 赵衡 · T20180021 · 能源管理中心</label>
    <label class="flex min-h-11 items-center gap-2 text-sm" data-dept="生活服务中心"><input type="checkbox" name="person" value="陈茉"> 陈茉 · T20210044 · 生活服务中心</label>
    <p id="person-error" class="mt-1 text-sm text-red-800"></p>
  </fieldset>
  <button class="min-h-11 rounded-xl bg-brand px-5 text-sm text-white" type="submit">保存并生效</button>
</form>
<script>
document.querySelector("#dept").addEventListener("change", function () {
  var value = this.value;
  document.querySelectorAll("[data-dept]").forEach(function (row) {
    row.hidden = value !== "all" && row.getAttribute("data-dept") !== value;
  });
});
document.querySelector("#meeting-form").addEventListener("submit", function (event) {
  event.preventDefault();
  var ok = true;
  [["#topic", "#topic-error", "请填写会议主题。"], ["#when", "#when-error", "请选择开始时间。"], ["#place", "#place-error", "请填写地点。"]].forEach(function (pair) {
    var field = document.querySelector(pair[0]);
    var error = document.querySelector(pair[1]);
    if (!field.value.trim()) { error.textContent = pair[2]; ok = false; } else error.textContent = "";
  });
  var chosen = document.querySelectorAll('input[name="person"]:checked');
  var personError = document.querySelector("#person-error");
  if (!chosen.length) { personError.textContent = "请至少选择一位有工号的参会人。"; ok = false; } else personError.textContent = "";
  if (!ok) return;
  location.href = "meeting-list.html?done=saved&title=" + encodeURIComponent(document.querySelector("#topic").value.trim());
});
</script>
"""


def meeting_detail_admin():
    return """
<a class="text-sm text-teal" href="meeting-list.html">返回会议</a>
<article class="mt-3 max-w-2xl rounded-2xl bg-white p-5">
  <h2 class="font-serif text-2xl text-ink">后勤周例会</h2>
  <dl class="mt-4 space-y-2 text-sm">
    <div class="flex justify-between"><dt class="text-muted">开始</dt><dd class="num">2026-10-22 09:00</dd></div>
    <div class="flex justify-between"><dt class="text-muted">地点</dt><dd>本部后勤楼 3 楼会议室</dd></div>
    <div class="flex justify-between"><dt class="text-muted">状态</dt><dd>待提醒 · 无审批</dd></div>
    <div class="flex justify-between"><dt class="text-muted">通道</dt><dd>ITS，按工号，只提醒一次</dd></div>
  </dl>
  <p class="mt-4 text-sm leading-6">参会人：周宁（T20190086）、赵衡（T20180021）、陈茉（T20210044）。</p>
</article>
"""


def recipients_main():
    people = [
        ("周宁", "T20190086", "后勤保障部", "在岗"),
        ("赵衡", "T20180021", "能源管理中心", "在岗"),
        ("陈茉", "T20210044", "生活服务中心", "在岗"),
    ]
    rows = "".join(f"<tr><td class=\"px-4 py-3\">{a}</td><td class=\"num px-4 py-3\">{b}</td><td class=\"px-4 py-3\">{c}</td><td class=\"px-4 py-3\">{d}</td></tr>" for a, b, c, d in people)
    return f"""
<p class="max-w-2xl text-sm leading-6 text-muted">名单来自已配置的教职工信息。推送以工号为准，没有工号的人不会进入名单，手机号不作为本期默认通道。</p>
<div class="mt-4 overflow-x-auto rounded-2xl border border-slate-200 bg-white">
  <table class="w-full min-w-[560px] text-left text-sm">
    <thead class="bg-mist text-muted"><tr><th class="px-4 py-3 font-medium">姓名</th><th class="px-4 py-3 font-medium">工号</th><th class="px-4 py-3 font-medium">部门</th><th class="px-4 py-3 font-medium">在岗</th></tr></thead>
    <tbody class="divide-y divide-slate-100">{rows}</tbody>
  </table>
</div>
"""


def avatar_admin():
    return f"""
<div class="grid gap-4 lg:grid-cols-2">
  <article class="rounded-2xl bg-white p-5">{avatar(False, "h-40 w-40")}<p class="mt-3 text-center text-sm">迎宾。胸牌只写「值班」，不印系统名称。</p></article>
  <article class="rounded-2xl bg-white p-5">{avatar(True, "h-40 w-40")}<p class="mt-3 text-center text-sm">聆听。琥珀色圆圈表示正在听。</p></article>
</div>
<form class="mt-4 max-w-xl" id="voice-form">
  <label for="welcome" class="text-sm">欢迎语</label>
  <textarea id="welcome" rows="3" class="mt-1 w-full rounded-xl border border-slate-300 px-3 py-2">同学你好，我是后勤值班助手。</textarea>
  <button class="mt-3 min-h-11 rounded-xl bg-brand px-4 text-sm font-medium text-white" type="submit">朗读欢迎语</button>
  <p id="voice-error" class="mt-2 text-sm text-red-800" role="alert"></p>
</form>
<p class="mt-4 max-w-xl text-xs leading-5 text-muted">形象按后勤服务人员设计，着装稳重。稿子由后勤指定一人、两轮内确认。播报文字与屏幕上的欢迎语一致。正式名称确定前，形象上不印系统名字。</p>
<script>
document.querySelector("#voice-form").addEventListener("submit", function (event) {{
  event.preventDefault();
  var text = document.querySelector("#welcome").value.trim();
  var error = document.querySelector("#voice-error");
  if (!text) {{ error.textContent = "请先写欢迎语。"; return; }}
  if (!window.speechSynthesis) {{ error.textContent = "当前浏览器不能朗读。"; return; }}
  error.textContent = "";
  window.speechSynthesis.cancel();
  var utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = "zh-CN";
  window.speechSynthesis.speak(utterance);
}});
</script>
"""


def logs_main():
    rows = [
        ("2026-10-19 16:40", "李衡", "提交审核", "宿舍报修范围补充"),
        ("2026-10-19 11:05", "周宁", "保存会议", "后勤周例会"),
        ("2026-10-01 08:20", "周宁", "下线知识", "2025 年班车临时通知"),
        ("2026-09-17 09:12", "周宁", "发布知识", "后勤服务知识库（公文版）"),
    ]
    body = "".join(f"<tr><td class=\"num px-4 py-3\">{a}</td><td class=\"px-4 py-3\">{b}</td><td class=\"px-4 py-3\">{c}</td><td class=\"px-4 py-3\">{d}</td></tr>" for a, b, c, d in rows)
    return f"""
<div class="overflow-x-auto rounded-2xl border border-slate-200 bg-white">
  <table class="w-full min-w-[680px] text-left text-sm">
    <thead class="bg-mist text-muted"><tr><th class="px-4 py-3 font-medium">时间</th><th class="px-4 py-3 font-medium">操作人</th><th class="px-4 py-3 font-medium">动作</th><th class="px-4 py-3 font-medium">对象</th></tr></thead>
    <tbody class="divide-y divide-slate-100">{body}</tbody>
  </table>
</div>
<p class="mt-3 text-xs text-muted">演示记录。正式环境写入 MySQL，并按学校规范备份至少 14 天。</p>
"""


def build_front():
    services_json = public_services()
    chat_script = render(CHAT_SCRIPT, ROLE="{role}", PORT="{port}", SERVICES=services_json)
    # ROLE/PORT filled per page below; SERVICES already inserted.
    # render replaced @@SERVICES@@. ROLE still needs per page. I used {role} wrongly.
    # Fix: CHAT_SCRIPT still has @@ROLE@@ if I didn't include them in this render.
    # I passed ROLE="{role}" which replaced @@ROLE@@ with the literal {role}. That's a bug.
    # Redo properly inside the loop.
    del chat_script

    def chat_js(role, port):
        return render(CHAT_SCRIPT, ROLE=role, PORT=port, SERVICES=services_json, PUBLIC_API=PUBLIC_API)

    def jump_js(role, port):
        return render(JUMP_SCRIPT, ROLE=role, PORT=port, SERVICES=services_json)

    guide_js = render(GUIDE_SCRIPT, SERVICES=services_json)

    specs = []

    def add_pc(group, role, filename, card_title, desc, icon, main, right="", listening=False, script=""):
        html = pc_frame(role, filename, card_title, main + script, right, listening)
        emit(group, f"pc/{role}/{filename}", card_title, desc, icon, html)

    def add_mobile(group, role, filename, card_title, desc, icon, main, script=""):
        html = mobile_frame(role, filename, card_title, main + script)
        emit(group, f"mobile/{role}/{filename}", card_title, desc, icon, html)

    for port, adder, group_prefix in (("pc", add_pc, "电脑端"), ("mobile", add_mobile, "移动端")):
        g = f"{group_prefix} · 游客"
        home = home_main("guest", port)
        if port == "pc":
            adder(g, "guest", "home.html", "问答首页", "迎宾、热门问题和输入", "fa-house", home + HOME_SCRIPT, rail_home("guest"))
            adder(g, "guest", "chat.html", "对话", "发送问题并得到知识库回答", "fa-comments", chat_main() + chat_js("guest", "pc"), '<div id="action-rail"><p class="text-sm leading-6 text-muted">回答之后，这里出现对应的办事入口。游客会先去登录。</p></div>')
        else:
            adder(g, "guest", "home.html", "问答首页", "手机上的迎宾和快捷问题", "fa-house", home + HOME_SCRIPT)
            adder(g, "guest", "chat.html", "对话", "手机上的真实问答", "fa-comments", mobile_chat_main() + chat_js("guest", "mobile"))
        adder(g, "guest", "not-found.html", "暂未收录", "知识库没有写到时的版式", "fa-circle-info", not_found_main())
        adder(g, "guest", "category.html", "办事说明", "四类公开说明，办理前要登录", "fa-map", category_main())
        adder(g, "guest", "login.html", "统一认证", "演示学生或教职工身份", "fa-right-to-bracket", login_main(port))
        adder(g, "guest", "listening.html", "聆听", "麦克风或手写问题后发送", "fa-microphone", listening_main() + LISTEN_SCRIPT, listening=True) if port == "pc" else adder(g, "guest", "listening.html", "聆听", "手机上的聆听状态", "fa-microphone", listening_main() + LISTEN_SCRIPT)

    add_pc("电脑端 · 学生", "student", "home.html", "学生首页", "登录后的欢迎和住宿身份", "fa-house", home_main("student", "pc") + HOME_SCRIPT, rail_home("student"))
    add_pc("电脑端 · 学生", "student", "chat.html", "学生对话", "回答后按电脑规则给入口", "fa-comments", chat_main() + chat_js("student", "pc"), '<div id="action-rail"><p class="text-sm leading-6 text-muted">水电缴费会引导到二维码。其余电脑地址可以直接去办理。</p></div>')
    add_pc("电脑端 · 学生", "student", "services.html", "学生办事", "八个电脑地址，外加缴费二维码", "fa-table-cells-large", services_main("student", "pc"))
    add_pc("电脑端 · 学生", "student", "jump.html", "离开确认", "确认后打开这一端的正式地址", "fa-arrow-up-right-from-square", jump_main() + jump_js("student", "pc"))
    add_pc("电脑端 · 学生", "student", "qrcode.html", "缴费二维码", "电脑上看见手机缴费码", "fa-qrcode", qrcode_main() + QR_SCRIPT)
    add_pc("电脑端 · 学生", "student", "utility.html", "水电指引", "怎么缴、到哪里缴，用量待接口", "fa-bolt", utility_main("pc", "student"))
    add_pc("电脑端 · 学生", "student", "profile.html", "学生身份", "只读的院系和住宿", "fa-user", profile_main("student"))
    add_pc("电脑端 · 学生", "student", "listening.html", "学生聆听", "听完送入学生对话", "fa-microphone", listening_main() + LISTEN_SCRIPT, listening=True)

    add_pc("电脑端 · 教职工", "staff", "home.html", "教职工首页", "周宁的值班欢迎", "fa-house", home_main("staff", "pc") + HOME_SCRIPT, rail_home("staff"))
    add_pc("电脑端 · 教职工", "staff", "chat.html", "教职工对话", "不出现学生缴费入口", "fa-comments", chat_main() + chat_js("staff", "pc"), '<div id="action-rail"><p class="text-sm leading-6 text-muted">教职工可以办报修、监督、场馆和仅电脑事项，不能缴学生水电。</p></div>')
    add_pc("电脑端 · 教职工", "staff", "services.html", "教职工办事", "没有水电缴费二维码", "fa-table-cells-large", services_main("staff", "pc"))
    add_pc("电脑端 · 教职工", "staff", "jump.html", "离开确认", "打开教职工可用的电脑地址", "fa-arrow-up-right-from-square", jump_main() + jump_js("staff", "pc"))
    add_pc("电脑端 · 教职工", "staff", "profile.html", "教职工身份", "部门、工号和在岗情况", "fa-user", profile_main("staff"))
    add_pc("电脑端 · 教职工", "staff", "listening.html", "教职工聆听", "听完送入教职工对话", "fa-microphone", listening_main() + LISTEN_SCRIPT, listening=True)

    add_mobile("移动端 · 学生", "student", "home.html", "学生首页", "手机欢迎和快捷问题", "fa-house", home_main("student", "mobile") + HOME_SCRIPT)
    add_mobile("移动端 · 学生", "student", "chat.html", "学生对话", "手机上直接去缴纳或改用电脑", "fa-comments", mobile_chat_main() + chat_js("student", "mobile"))
    add_mobile("移动端 · 学生", "student", "listening.html", "学生聆听", "手机聆听后发送", "fa-microphone", listening_main() + LISTEN_SCRIPT)
    add_mobile("移动端 · 学生", "student", "services.html", "学生办事", "四个手机地址可办，五项改用电脑", "fa-table-cells-large", services_main("student", "mobile"))
    add_mobile("移动端 · 学生", "student", "utility.html", "去缴纳", "手机上的缴费步骤和入口", "fa-bolt", utility_main("mobile", "student"))
    add_mobile("移动端 · 学生", "student", "jump.html", "离开确认", "打开手机端正式地址", "fa-arrow-up-right-from-square", jump_main() + jump_js("student", "mobile"))
    add_mobile("移动端 · 学生", "student", "guide.html", "电脑办理说明", "班车、宾馆、报刊、失物和公告", "fa-desktop", guide_main() + guide_js)
    add_mobile("移动端 · 学生", "student", "profile.html", "学生身份", "手机上的只读资料", "fa-user", profile_main("student"))

    add_mobile("移动端 · 教职工", "staff", "home.html", "教职工首页", "手机上的教职工欢迎", "fa-house", home_main("staff", "mobile") + HOME_SCRIPT)
    add_mobile("移动端 · 教职工", "staff", "chat.html", "教职工对话", "手机上也不出现缴费", "fa-comments", mobile_chat_main() + chat_js("staff", "mobile"))
    add_mobile("移动端 · 教职工", "staff", "services.html", "教职工办事", "只能办报修、监督和游泳馆", "fa-table-cells-large", services_main("staff", "mobile"))
    add_mobile("移动端 · 教职工", "staff", "jump.html", "离开确认", "打开教职工的手机地址", "fa-arrow-up-right-from-square", jump_main() + jump_js("staff", "mobile"))
    add_mobile("移动端 · 教职工", "staff", "guide.html", "电脑办理说明", "仅电脑事项的地址说明", "fa-desktop", guide_main() + guide_js)
    add_mobile("移动端 · 教职工", "staff", "profile.html", "教职工身份", "工号与会议提醒入口", "fa-user", profile_main("staff"))

    # The guest listening call above used a ternary that still passes listening= to mobile.
    # add_mobile does not accept listening. I need to fix the guest loop. See below.


def build_recipient_and_admin():
    emit("电脑端 · 提醒接收人", "pc/recipient/inbox.html", "提醒列表", "ITS 推送之后可以回看", "fa-bell", pc_simple("提醒列表", inbox_main("pc")))
    emit("电脑端 · 提醒接收人", "pc/recipient/detail.html", "提醒详情", "一场会议的时间、地点和接收人", "fa-calendar-day", pc_simple("提醒详情", detail_main()))
    emit("移动端 · 提醒接收人", "mobile/recipient/inbox.html", "提醒列表", "手机上的会议提醒", "fa-bell", mobile_simple("提醒列表", inbox_main("mobile")))
    emit("移动端 · 提醒接收人", "mobile/recipient/detail.html", "提醒详情", "手机上的单场会议", "fa-calendar-day", mobile_simple("提醒详情", detail_main()))

    emit("管理后台", "admin/login.html", "管理员登录", "进入知识、清单和会议维护", "fa-right-to-bracket", admin_login())
    emit("管理后台", "admin/dashboard.html", "运行总览", "待审知识、即将召开的会议", "fa-gauge", admin_frame("dashboard.html", "运行总览", dashboard_main()))
    emit("管理后台", "admin/knowledge-list.html", "知识列表", "已发布的知识库和审核状态", "fa-book", admin_frame("knowledge-list.html", "知识列表", knowledge_list()))
    emit("管理后台", "admin/knowledge-edit.html", "编辑知识", "保存草稿，公开与内部分开", "fa-pen", admin_frame("knowledge-edit.html", "编辑知识", knowledge_edit()))
    emit("管理后台", "admin/knowledge-review.html", "审核知识", "通过后发布，或退回修改", "fa-clipboard-check", admin_frame("knowledge-review.html", "审核知识", knowledge_review()))
    emit("管理后台", "admin/categories.html", "快捷分类", "报修、水电、班车、其他办事", "fa-grip", admin_frame("categories.html", "快捷分类", categories_main()))
    emit("管理后台", "admin/catalog-list.html", "功能清单", "按终端列出正式地址", "fa-list", admin_frame("catalog-list.html", "功能清单", catalog_list()))
    emit("管理后台", "admin/catalog-edit.html", "编辑入口", "名称、对象、地址、终端和触发说法", "fa-pen-to-square", admin_frame("catalog-edit.html", "编辑入口", catalog_edit()))
    emit("管理后台", "admin/meeting-list.html", "会议列表", "保存即生效，取消后不再提醒", "fa-calendar", admin_frame("meeting-list.html", "会议列表", meeting_list()))
    emit("管理后台", "admin/meeting-edit.html", "录入会议", "选择有工号的参会人", "fa-calendar-plus", admin_frame("meeting-edit.html", "录入会议", meeting_edit()))
    emit("管理后台", "admin/meeting-detail.html", "会议详情", "提醒时点和接收工号", "fa-calendar-day", admin_frame("meeting-detail.html", "会议详情", meeting_detail_admin()))
    emit("管理后台", "admin/recipients.html", "提醒名单", "工号、姓名和部门", "fa-users", admin_frame("recipients.html", "提醒名单", recipients_main()))
    emit("管理后台", "admin/avatar.html", "形象与语音", "迎宾、聆听和欢迎语试听", "fa-user", admin_frame("avatar.html", "形象与语音", avatar_admin()))
    emit("管理后台", "admin/logs.html", "操作日志", "发布、审核、下线和会议保存", "fa-clock-rotate-left", admin_frame("logs.html", "操作日志", logs_main()))


def pc_simple(title, main):
    body = f"""
<body class="min-h-screen bg-mist text-inktext">
<header class="flex h-16 items-center justify-between border-b border-[#C8CAD1] bg-white px-5">
  <a href="../../index.html" class="font-semibold text-ink">中南大学 · 会议提醒</a>
  <a class="rounded-lg border border-[#C8CAD1] px-3 py-2 text-sm text-brand" href="../../index.html">返回导航</a>
</header>
<main id="main" class="mx-auto max-w-3xl">{main}</main>
</body>"""
    return document(title, body)


def mobile_simple(title, main):
    body = f"""
<body class="bg-mist">
<div class="mx-auto flex min-h-dvh w-full flex-col bg-white md:my-6 md:min-h-[844px] md:w-[420px] md:rounded-2xl md:border md:border-[#C8CAD1]">
  <header class="flex h-14 items-center justify-between border-b border-[#C8CAD1] bg-white px-4"><span class="text-sm font-semibold">会议提醒</span><a class="text-xs text-brand" href="../../index.html">导航</a></header>
  <main id="main" class="flex-1">{main}</main>
</div>
</body>"""
    return document(title, body)


def build_index():
    order = [
        "电脑端 · 游客", "电脑端 · 学生", "电脑端 · 教职工", "电脑端 · 提醒接收人",
        "移动端 · 游客", "移动端 · 学生", "移动端 · 教职工", "移动端 · 提醒接收人",
        "管理后台",
    ]
    rank = {name: index for index, name in enumerate(order)}
    ordered = sorted(CARDS, key=lambda item: (rank.get(item[0], 99),))
    groups = []
    current = None
    bucket = []
    for group, rel, title, desc, icon in ordered:
        if group != current:
            if bucket:
                groups.append((current, bucket))
            current = group
            bucket = []
        bucket.append((rel, title, desc, icon))
    if bucket:
        groups.append((current, bucket))
    sections = []
    for name, items in groups:
        if len(items) % 2:
            raise SystemExit("入口不是成对的：" + name)
        cards = []
        for rel, title, desc, icon in items:
            cards.append(f"""
<a class="flex min-h-28 flex-col gap-2 rounded-2xl border border-slate-200 bg-white p-4 transition hover:border-teal" href="{rel}">
  <span class="flex h-10 w-10 items-center justify-center rounded-xl bg-teal-50 text-teal"><i class="fa-solid {icon}"></i></span>
  <span class="font-medium leading-snug">{title}</span>
  <span class="text-sm leading-5 text-muted">{desc}</span>
</a>""")
        sections.append(f'<section class="mt-10"><h3 class="font-serif text-2xl text-ink">{name}</h3><div class="mt-4 grid grid-cols-2 gap-3">{"".join(cards)}</div></section>')

    matrix = """
<div class="mt-4 overflow-x-auto rounded-2xl border border-slate-200 bg-white">
<table class="w-full min-w-[880px] text-left text-sm">
<caption class="px-4 py-3 text-left text-xs text-muted">横向滑动可以看完所有列。格子里写的是能做的事，不单靠颜色区分。</caption>
<thead class="bg-mist text-muted"><tr>
<th class="sticky left-0 bg-mist px-3 py-3 font-medium">事项</th><th class="px-3 py-3 font-medium">游客</th><th class="px-3 py-3 font-medium">学生</th><th class="px-3 py-3 font-medium">教职工</th><th class="px-3 py-3 font-medium">提醒接收人</th><th class="px-3 py-3 font-medium">知识维护</th><th class="px-3 py-3 font-medium">知识审核</th><th class="px-3 py-3 font-medium">会议管理</th>
</tr></thead>
<tbody class="divide-y divide-slate-100">
<tr><th class="sticky left-0 bg-white px-3 py-3 font-medium">公开问答</th><td class="px-3 py-3">可看</td><td class="px-3 py-3">可看</td><td class="px-3 py-3">可看</td><td class="px-3 py-3">可看</td><td class="px-3 py-3">起草</td><td class="px-3 py-3">审核后发布</td><td class="px-3 py-3">不涉及</td></tr>
<tr><th class="sticky left-0 bg-white px-3 py-3 font-medium">暂未收录</th><td class="px-3 py-3">给热线</td><td class="px-3 py-3">给热线</td><td class="px-3 py-3">给热线</td><td class="px-3 py-3">给热线</td><td class="px-3 py-3">不代替正文</td><td class="px-3 py-3">不代替正文</td><td class="px-3 py-3">不涉及</td></tr>
<tr><th class="sticky left-0 bg-white px-3 py-3 font-medium">报修、监督、游泳馆</th><td class="px-3 py-3">只看说明</td><td class="px-3 py-3">两端可办</td><td class="px-3 py-3">两端可办</td><td class="px-3 py-3">不涉及</td><td class="px-3 py-3">不涉及</td><td class="px-3 py-3">不涉及</td><td class="px-3 py-3">不涉及</td></tr>
<tr><th class="sticky left-0 bg-white px-3 py-3 font-medium">水电费服务说明</th><td class="px-3 py-3">只看说明</td><td class="px-3 py-3">电脑可办</td><td class="px-3 py-3">电脑可办</td><td class="px-3 py-3">不涉及</td><td class="px-3 py-3">不涉及</td><td class="px-3 py-3">不涉及</td><td class="px-3 py-3">不涉及</td></tr>
<tr><th class="sticky left-0 bg-white px-3 py-3 font-medium">水电缴费</th><td class="px-3 py-3">不可办</td><td class="px-3 py-3">手机可办，电脑看二维码</td><td class="px-3 py-3">不开放</td><td class="px-3 py-3">不涉及</td><td class="px-3 py-3">不涉及</td><td class="px-3 py-3">不涉及</td><td class="px-3 py-3">不涉及</td></tr>
<tr><th class="sticky left-0 bg-white px-3 py-3 font-medium">班车、宾馆、报刊、失物</th><td class="px-3 py-3">只看说明</td><td class="px-3 py-3">电脑可办</td><td class="px-3 py-3">电脑可办</td><td class="px-3 py-3">不涉及</td><td class="px-3 py-3">维护地址</td><td class="px-3 py-3">不涉及</td><td class="px-3 py-3">不涉及</td></tr>
<tr><th class="sticky left-0 bg-white px-3 py-3 font-medium">校园公告</th><td class="px-3 py-3">只看说明</td><td class="px-3 py-3">只看说明</td><td class="px-3 py-3">只看说明</td><td class="px-3 py-3">不涉及</td><td class="px-3 py-3">不涉及</td><td class="px-3 py-3">不涉及</td><td class="px-3 py-3">不涉及</td></tr>
<tr><th class="sticky left-0 bg-white px-3 py-3 font-medium">本人用量和欠费</th><td class="px-3 py-3">不开放</td><td class="px-3 py-3">待接口</td><td class="px-3 py-3">不开放</td><td class="px-3 py-3">不开放</td><td class="px-3 py-3">不涉及</td><td class="px-3 py-3">不涉及</td><td class="px-3 py-3">不涉及</td></tr>
<tr><th class="sticky left-0 bg-white px-3 py-3 font-medium">会议提醒</th><td class="px-3 py-3">不开放</td><td class="px-3 py-3">不开放</td><td class="px-3 py-3">仅被点名的工号</td><td class="px-3 py-3">可回看</td><td class="px-3 py-3">不涉及</td><td class="px-3 py-3">不涉及</td><td class="px-3 py-3">录入即生效</td></tr>
</tbody></table></div>
"""
    flows = """
<div class="mt-4 grid grid-cols-2 gap-3">
  <article class="rounded-2xl bg-white p-4"><h3 class="font-medium">问答</h3><ol class="mt-3 space-y-2 text-sm leading-6 text-muted"><li>1. 打开页面，可以不登录。</li><li>2. 提问后只查已审核知识库。</li><li>3. 查到了就回答，并给出这一端的入口。</li><li>4. 没查到就说暂未收录，并给出热线。</li></ol></article>
  <article class="rounded-2xl bg-white p-4"><h3 class="font-medium">办事跳转</h3><ol class="mt-3 space-y-2 text-sm leading-6 text-muted"><li>1. 先看清单里有没有当前端口的地址。</li><li>2. 有地址就确认后离开助手。</li><li>3. 水电缴费在电脑上只出二维码。</li><li>4. 仅电脑事项在手机上展示地址。没有地址就只说明。</li></ol></article>
  <article class="rounded-2xl bg-white p-4"><h3 class="font-medium">会议提醒</h3><ol class="mt-3 space-y-2 text-sm leading-6 text-muted"><li>1. 录入主题、时间、地点和有工号的人。</li><li>2. 保存即生效，本期不审批。</li><li>3. 默认会前 1 小时，可按单场改短。</li><li>4. 经 ITS 按工号推送一次。取消后不再推送。</li></ol></article>
  <article class="rounded-2xl bg-white p-4"><h3 class="font-medium">知识审核</h3><ol class="mt-3 space-y-2 text-sm leading-6 text-muted"><li>1. 维护人起草，公开和内部分开标记。</li><li>2. 提交后由另一人审核。</li><li>3. 通过才发布，前台才能引用。</li><li>4. 退回就修改。已发布的可以下线。</li></ol></article>
</div>
"""
    body = f"""
<body class="bg-[#F5F7FA] text-inktext">
<a class="sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-4 focus:bg-white focus:px-3 focus:py-2" href="#main">跳到主要内容</a>
<main id="main" class="mx-auto max-w-6xl px-5 pb-10">
  <section class="px-4 py-14 text-center">
    <div class="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-brand text-2xl font-semibold text-white shadow-[0_10px_24px_rgba(48,135,204,.28)]">后</div>
    <h1 class="mt-5 text-3xl font-semibold tracking-wide text-ink">智慧后勤AI助手 · 原型页面导航</h1>
    <p class="mx-auto mt-4 max-w-3xl text-sm leading-7 text-muted">后勤保障部的办事原型。公开问题用知识库回答，能办理的事项按电脑或手机跳回原系统，会议由管理员录入后按工号提醒。</p>
    <p class="mt-2 text-sm font-medium text-ink">电脑端、移动端、管理后台，按角色分开。</p>
    <div class="mt-5 flex flex-wrap justify-center gap-2">
      <span class="inline-flex h-9 items-center rounded-full bg-teal-50 px-4 text-sm text-brand">中南蓝 · 学工视觉</span>
      <span id="health" class="inline-flex h-9 items-center rounded-full border border-[#C8CAD1] bg-white px-4 text-sm text-muted">正在检查问答服务</span>
    </div>
    <div class="mt-8 flex justify-center gap-12">
      <p><b class="block text-4xl font-semibold text-brand num">59</b><span class="text-sm text-muted">HTML 页面</span></p>
      <p><b class="block text-4xl font-semibold text-brand num">2</b><span class="text-sm text-muted">终端形态</span></p>
      <p><b class="block text-4xl font-semibold text-brand num">5</b><span class="text-sm text-muted">使用角色</span></p>
      <p><b class="block text-4xl font-semibold text-brand num">4</b><span class="text-sm text-muted">核心流程</span></p>
    </div>
  </section>
  <p class="rounded-lg border border-[#95C6E3] bg-teal-50 px-4 py-3 text-sm leading-6 text-[#006DAD]">这些页面可点击跳转。真实问答需要本机运行 python3 server.py。密钥放在 .env，不写进页面。</p>

  <section class="mt-12">
    <h2 class="font-serif text-3xl text-ink">01 角色和权限</h2>
    <p class="mt-2 max-w-3xl text-sm leading-6 text-muted">演示时可以按这张表讲。知识维护人用李衡，审核人用周宁，避免自己审自己。周宁同时在会议提醒名单里。</p>
    {matrix}
    <div class="mt-4 grid grid-cols-2 gap-3">
      <article class="rounded-2xl bg-white p-4"><h3 class="font-medium">林夏 · 学生</h3><p class="mt-2 text-sm leading-6 text-muted">计算机学院 2024 级。住宿演示数据为麓南校区升华学生公寓 7 栋 314，与知识库里的公寓位置一致。</p></article>
      <article class="rounded-2xl bg-white p-4"><h3 class="font-medium">周宁 · 教职工</h3><p class="mt-2 text-sm leading-6 text-muted">后勤保障部，工号 T20190086，在岗。可以收会议提醒，也可以审核知识。</p></article>
    </div>
  </section>

  <section class="mt-12">
    <h2 class="font-serif text-3xl text-ink">02 功能清单和端口</h2>
    <p class="mt-2 text-sm leading-6 text-muted">地址以《服务链接》的电脑段、手机段为准。游泳馆、水电费服务、宾馆、报刊这四个电脑地址打开时可能是 404，页面上会标成待复核。</p>
    <div class="mt-4 grid grid-cols-2 gap-3">
      <article class="rounded-2xl bg-white p-4"><h3 class="font-medium">两端都有地址</h3><ul class="mt-3 space-y-2 text-sm leading-6"><li>网上报修</li><li>服务监督</li><li>游泳馆预定</li></ul><p class="mt-3 text-xs text-muted">电脑和手机各用各的链接。</p></article>
      <article class="rounded-2xl bg-white p-4"><h3 class="font-medium">只有手机地址</h3><p class="mt-3 text-sm leading-6">水电缴费，只对学生开放。电脑访问时说明原因并出示二维码。</p></article>
      <article class="rounded-2xl bg-white p-4"><h3 class="font-medium">只有电脑地址</h3><ul class="mt-3 space-y-2 text-sm leading-6"><li>水电费服务（说明，不是缴费）</li><li>班车查询</li><li>校园宾馆、报刊订阅、失物招领</li></ul></article>
      <article class="rounded-2xl bg-white p-4"><h3 class="font-medium">没有单独地址</h3><p class="mt-3 text-sm leading-6">校园公告。两端都只说明，请看后勤保障部官网 <span class="break-all">{OFFICIAL_SITE}</span> 和公众号信息中心。</p></article>
    </div>
  </section>

  <section class="mt-12">
    <h2 class="font-serif text-3xl text-ink">03 四条流程</h2>
    {flows}
  </section>

  <section class="mt-12">
    <h2 class="font-serif text-3xl text-ink">04 进入页面</h2>
    <p class="mt-2 text-sm leading-6 text-muted">每行两个入口。真实问答请用 <span class="num">python3 server.py</span> 打开本页，再从对话页提问。密钥放在本机 .env，不写在页面里。</p>
    {''.join(sections)}
  </section>
</main>
<footer class="mx-auto max-w-6xl px-5 py-8 text-xs leading-5 text-muted">热线 {HOTLINE} 来自后勤服务知识库。收费和开放时间以现场公示为准。知识采集截止 2026 年 9 月 17 日。</footer>
<script>
var apiOrigin = "{PUBLIC_API}";
function apiUrl(path) {{
  if (location.hostname === "127.0.0.1" || location.hostname === "localhost") return path;
  return apiOrigin ? apiOrigin.replace(/\\/$/, "") + path : path;
}}
fetch(apiUrl("/api/health")).then(function (r) {{ return r.json(); }}).then(function (data) {{
  var el = document.querySelector("#health");
  el.textContent = data.ok ? ("密钥已读取 · 知识库 " + data.knowledgeChars + " 字") : "问答服务还没准备好";
}}).catch(function () {{
  document.querySelector("#health").textContent = "请先运行 python3 server.py";
}});
</script>
</body>
"""
    write_file("index.html", document("原型导航", body))


def main():
    build_front()
    build_recipient_and_admin()
    build_index()
    if len(WRITTEN) != 59:
        raise SystemExit("页面数量是 %s，应为 59" % len(WRITTEN))
    print("已生成 %s 个页面" % len(WRITTEN))


if __name__ == "__main__":
    main()
