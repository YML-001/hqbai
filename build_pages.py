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
body { background: #F3F7FB; color: #1E323F; font-family: "OPPOSans", "PingFang SC", "HarmonyOS Sans SC", "Microsoft YaHei", sans-serif; }
thead.bg-mist, thead { background: #E3F1F9; color: #006DAD; }
.bg-brand { background-image: linear-gradient(90deg, #2A8DC7, #006DAD); }
.hq-nav-on { background: linear-gradient(90deg, #2A8DC7, #006DAD); color: #fff; font-weight: 600; box-shadow: 0 4px 12px rgba(0,109,173,.25); border-radius: 20px; }
article.rounded-2xl, .rounded-2xl.bg-white, .rounded-2xl.border { box-shadow: 0 1px 5px rgba(45,47,51,.06); }
.hq-stage { min-height: 100vh; display: flex; justify-content: center; align-items: flex-start; padding: 28px 0; background: radial-gradient(1200px 600px at 20% 0%, #DCE9FF 0%, transparent 60%), linear-gradient(180deg, #EAF1FB, #DCE6F2); }
.hq-phone { width: 390px; height: min(844px, calc(100vh - 56px)); border-radius: 40px; background: #F0F6FF; position: relative; overflow: hidden; display: flex; flex-direction: column; box-shadow: 0 0 0 11px #11151D, 0 0 0 12px #3A4150, 0 40px 90px rgba(16,37,104,.35); }
.hq-phone .sky { position: absolute; left: 0; right: 0; top: 0; height: 180px; z-index: 0; background: linear-gradient(180deg, #2F6CFF 0%, #5E9CFF 70px, #B9D5FF 140px, rgba(240,246,255,0) 180px); pointer-events: none; }
.hq-tabbar { flex-shrink: 0; height: 78px; background: #fff; border-radius: 26px 26px 0 0; display: grid; padding: 8px 6px 18px; position: relative; z-index: 5; box-shadow: 0 -6px 24px rgba(4,81,239,.08); }
.hq-tab { display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 3px; font-size: 11px; color: #627079; }
.hq-tab.on { color: #0451EF; font-weight: 600; }
.hq-tab .ti { width: 32px; height: 32px; display: grid; place-items: center; border-radius: 50%; }
.hq-tab.on .ti { background: linear-gradient(135deg, #5BAEFF, #0451EF); color: #fff; box-shadow: 0 4px 10px rgba(4,81,239,.35); }
@media (max-width: 767px) {
  .hq-stage { padding: 0; background: #F0F6FF; }
  .hq-phone { width: 100%; height: 100dvh; border-radius: 0; box-shadow: none; }
}
.num { font-variant-numeric: tabular-nums; }
.listen-ring { position: absolute; inset: -6px; border-radius: 999px; border: 2px solid transparent; pointer-events: none; }
.is-listening .listen-ring { border-color: #3087CC; animation: ring 1.6s ease-out infinite; }
@keyframes ring { from { transform: scale(.94); opacity: .9; } to { transform: scale(1.14); opacity: 0; } }
.hq-composer { position: relative; z-index: 6; overflow: visible; }
.hq-tools { position: relative; z-index: 4; }
.hq-entry-bar { display: flex; flex-wrap: wrap; justify-content: flex-end; gap: 8px; }
.hq-entry-btn {
  display: inline-flex; align-items: center; justify-content: center; gap: 6px;
  min-height: 44px; padding: 0 14px; border-radius: 999px; border: 1px solid #C8E4F4;
  background: #fff; color: #006DAD; font-size: 14px; font-weight: 600; line-height: 1;
  cursor: pointer; white-space: nowrap; box-shadow: 0 1px 4px rgba(0, 109, 173, .12);
}
.hq-entry-btn:hover { border-color: #2A8DC7; background: #E3F1F9; }
.hq-entry-btn.is-on {
  border-color: transparent; color: #fff;
  background: linear-gradient(90deg, #2A8DC7, #006DAD);
  box-shadow: 0 4px 12px rgba(0, 109, 173, .25);
}
.hq-entry-badge {
  min-width: 18px; height: 18px; padding: 0 5px; border-radius: 999px;
  background: #E8801A; color: #fff; font-size: 11px; font-weight: 700;
  line-height: 18px; text-align: center;
}
.hq-entry-btn.is-on .hq-entry-badge { background: #fff; color: #006DAD; }
.hq-panel {
  position: absolute; top: calc(100% + 8px); left: 0; right: 0; z-index: 5;
  max-height: min(260px, 38vh); overflow: auto;
  border: 1px solid #C8E4F4; border-radius: 16px; background: #fff;
  box-shadow: 0 8px 24px rgba(0, 109, 173, .12);
}
.hq-phone .hq-panel { max-height: 220px; }
.hq-panel[hidden] { display: none !important; }
.hq-panel-hd {
  position: sticky; top: 0; z-index: 1; display: flex; align-items: flex-start;
  justify-content: space-between; gap: 12px; padding: 12px 14px;
  background: #fff; border-bottom: 1px solid #E3F1F9;
}
.hq-panel-title { margin: 0; font-size: 15px; font-weight: 700; color: #1E323F; }
.hq-panel-sub { margin: 4px 0 0; font-size: 12px; line-height: 1.5; color: #627079; }
.hq-panel-x {
  flex: 0 0 auto; width: 32px; height: 32px; border: 0; border-radius: 999px;
  background: #E3F1F9; color: #006DAD; cursor: pointer;
}
.hq-note, .hq-hist {
  display: block; width: 100%; margin: 0; text-align: left; border: 0;
  border-bottom: 1px solid #E3F1F9; background: #fff; padding: 12px 14px; cursor: pointer;
}
.hq-note:last-child, .hq-hist:last-child { border-bottom: 0; }
.hq-note.is-unread { background: #F4FAFD; }
.hq-note:hover, .hq-hist:hover { background: #F4FAFD; }
.hq-note-top { display: flex; align-items: flex-start; justify-content: space-between; gap: 8px; }
.hq-note-title, .hq-hist-q { font-size: 14px; font-weight: 600; color: #1E323F; line-height: 1.45; }
.hq-note.is-unread .hq-note-title { color: #006DAD; }
.hq-note.is-unread .hq-note-title::before {
  content: ""; display: inline-block; width: 8px; height: 8px; margin-right: 6px;
  border-radius: 99px; background: #E8801A; box-shadow: 0 0 0 3px rgba(232, 128, 26, .18);
}
.hq-note-pills { display: flex; flex: 0 0 auto; flex-wrap: wrap; justify-content: flex-end; gap: 4px; }
.hq-pill {
  display: inline-flex; align-items: center; min-height: 22px; padding: 0 8px;
  border-radius: 999px; font-size: 12px; font-weight: 600; line-height: 1;
}
.hq-pill.amber { background: #FFF8F0; color: #E8801A; }
.hq-pill.teal, .hq-pill.brand { background: #E3F1F9; color: #006DAD; }
.hq-pill.muted { background: #F3F7FB; color: #627079; }
.hq-note-meta, .hq-hist-a, .hq-note-body { display: block; margin-top: 4px; font-size: 13px; line-height: 1.55; }
.hq-note-meta, .hq-hist-a { color: #627079; }
.hq-note-body { color: #1E323F; }
.hq-phone .hq-entry-bar { display: grid; grid-template-columns: 1fr 1fr; }
.hq-phone .hq-entry-btn { width: 100%; }
.hq-ask-row { display: flex; align-items: flex-end; gap: 8px; }
.hq-ask-row textarea { flex: 1 1 auto; min-width: 0; }
.hq-mic {
  position: relative; isolation: isolate; z-index: 1; align-self: center;
  display: grid; place-items: center;
  width: 44px; height: 44px; flex: 0 0 auto; border: 0; border-radius: 999px; color: #fff;
  background: linear-gradient(145deg, #2A8DC7, #006DAD);
  box-shadow: 0 4px 12px rgba(0, 109, 173, .28); cursor: pointer;
  animation: hq-breathe 2.6s ease-in-out infinite;
}
.hq-mic i { position: relative; z-index: 1; font-size: 16px; }
.hq-mic-ring {
  position: absolute; inset: -2px; border-radius: 999px; pointer-events: none;
  border: 2px solid rgba(42, 141, 199, .55); animation: hq-ripple 2.6s ease-out infinite;
}
.hq-mic-ring.d2 { animation-delay: 1.3s; }
.hq-mic.is-on { animation-duration: 1.05s; box-shadow: 0 6px 16px rgba(0, 109, 173, .45); }
.hq-mic.is-on .hq-mic-ring { animation-duration: 1.15s; border-color: rgba(0, 109, 173, .8); }
.hq-voice-panel {
  margin: 0 0 8px; padding: 8px 12px;
  border: 1px solid #C8E4F4; border-radius: 12px; background: #F4FAFD;
}
.hq-voice-status { margin: 0; flex: 1; min-width: 0; font-size: 14px; font-weight: 600; line-height: 1.4; color: #006DAD; }
.hq-voice-row { display: flex; align-items: center; gap: 8px; }
.hq-voice-hint { margin: 4px 0 0; font-size: 12px; line-height: 1.4; color: #627079; }
.hq-voice-stop {
  margin: 0; min-height: 32px; padding: 0 12px; flex: 0 0 auto; border-radius: 999px;
  border: 1px solid #2A8DC7; background: #E3F1F9; color: #006DAD; font-size: 13px; cursor: pointer;
}
@keyframes hq-breathe { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.06); } }
@keyframes hq-ripple { 0% { transform: scale(1); opacity: .7; } 100% { transform: scale(1.45); opacity: 0; } }
.bubble-user { background: #3087CC; color: #fff; border-radius: 8px 8px 2px 8px; }
.bubble-bot { background: #fff; color: #3C444F; border: 1px solid #C8CAD1; border-radius: 8px 8px 8px 2px; }
main:has(#thread):not(:has(.hq-home)) { overflow: hidden; }
main:has(#thread):not(:has(.hq-home)) > div { min-height: 0; flex: 1; }
@media (min-width: 1024px) {
  main:has(#thread):not(:has(.hq-home)) { display: flex; flex-direction: column; height: 100%; }
  body.hq-pc main:has(.hq-home) { display: flex; flex-direction: column; height: 100%; overflow: hidden; }
  body.hq-pc main:has(.hq-home) > .hq-home { min-height: 0; flex: 1 1 auto; }
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
      brand: { DEFAULT: "#006DAD", dark: "#0451EF", light: "#E3F1F9" },
      ink: "#1E323F",
      teal: { DEFAULT: "#2A8DC7", 50: "#E3F1F9", 700: "#006DAD" },
      amber: { DEFAULT: "#E8801A", 50: "#FFF8F0" },
      mist: "#F3F7FB",
      card: "#FFFFFF",
      inktext: "#1E323F",
      muted: "#627079"
    },
    fontFamily: {
      sans: ["OPPOSans", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "sans-serif"],
      serif: ["OPPOSans", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "sans-serif"]
    },
    borderRadius: { lg: "8px", xl: "12px", "2xl": "16px" }
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
        ("category.html", "办事说明", "fa-map"),
        ("login.html", "登录", "fa-right-to-bracket"),
    ],
    ("pc", "student"): [
        ("home.html", "问答首页", "fa-house"),
        ("services.html", "办事", "fa-table-cells-large"),
        ("utility.html", "水电", "fa-bolt"),
        ("profile.html", "我的", "fa-user"),
    ],
    ("pc", "staff"): [
        ("home.html", "问答首页", "fa-house"),
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
    "not-found.html": "home.html",
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
            cls = "hq-nav-on" if on else "text-inktext hover:bg-white/70"
            links.append(
                f'<a class="flex min-h-11 shrink-0 items-center gap-2 rounded-full px-3 text-sm {cls}" href="{href}">'
                f'<i class="fa-solid {icon} w-4"></i>{label}</a>'
            )
        else:
            cls = "hq-tab on" if on else "hq-tab"
            links.append(
                f'<a class="{cls}" href="{href}"><span class="ti"><i class="fa-solid {icon}"></i></span><span>{label}</span></a>'
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
  var currentQuestion = "";

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
  function reveal() {
    var anchor = thread.lastElementChild || thread;
    var rows = thread.children;
    for (var i = rows.length - 1; i >= 0; i--) {
      if (rows[i].querySelector && rows[i].querySelector(".bubble-user")) { anchor = rows[i]; break; }
    }
    if (anchor && anchor.scrollIntoView) anchor.scrollIntoView({ block: "start", inline: "nearest" });
  }
  function ask(question) {
    currentQuestion = question;
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
    reveal();
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
    if (data.ok !== false && typeof window.hqPushHistory === "function") {
      window.hqPushHistory(currentQuestion, data.answer || "");
    }
    var rail = document.querySelector("#action-rail");
    var item = findService(data.serviceId);
    if (rail) {
      if (!item || data.serviceId === "none") {
        rail.innerHTML = "<p class=\\"text-sm leading-6 text-muted\\">这条回答没有单独的办理入口。需要人工时，请拨打 " + escapeHtml(data.hotline || "0731-88836000") + "。</p>";
      } else {
        rail.innerHTML = '<p class="text-xs text-muted">这一答对应的入口</p><h2 class="mt-1 text-lg font-medium">' + escapeHtml(item.name) + "</h2><p class=\\"mt-2 text-sm leading-6 text-muted\\">" + escapeHtml(item.summary) + "</p>" + extra;
      }
    }
    reveal();
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
  document.querySelectorAll("[data-ask]").forEach(function (el) {
    el.addEventListener("click", function () {
      var question = (el.getAttribute("data-ask") || "").trim();
      if (!question) return;
      error.textContent = "";
      input.value = "";
      ask(question);
    });
  });
  var preset = sessionStorage.getItem("hq-question");
  if (preset) { sessionStorage.removeItem("hq-question"); ask(preset); }
})();
</script>
"""


def composer():
    return """
<form id="ask-form" class="hq-composer shrink-0 border-t border-slate-200 bg-white p-3">
  <label for="question" class="mb-2 block text-xs text-muted">你的问题</label>
  <div class="hq-voice-panel" id="hq-voice-panel" role="status" aria-live="polite" hidden>
    <div class="hq-voice-row">
      <p class="hq-voice-status" id="hq-voice-status">正在听，请说出你的问题</p>
      <button type="button" class="hq-voice-stop" id="hq-mic-stop">说完了</button>
    </div>
    <p class="hq-voice-hint">文字会填进输入框，也可以手写。</p>
  </div>
  <div class="hq-ask-row" id="hq-voice">
    <button type="button" class="hq-mic" id="hq-mic" aria-pressed="false" aria-expanded="false" aria-controls="hq-voice-panel" aria-label="语音提问" title="语音提问">
      <span class="hq-mic-ring" aria-hidden="true"></span>
      <span class="hq-mic-ring d2" aria-hidden="true"></span>
      <i class="fa-solid fa-microphone" aria-hidden="true"></i>
    </button>
    <textarea id="question" rows="2" class="min-h-11 flex-1 resize-none rounded-xl border border-slate-300 px-3 py-2 text-base focus:border-teal" placeholder="例如：宿舍空调不制冷怎么办"></textarea>
    <button id="send" class="h-11 shrink-0 rounded-xl bg-brand px-4 text-sm font-medium text-white" type="submit">发送</button>
  </div>
  <p id="question-error" class="mt-1 min-h-5 text-sm text-red-800" role="alert"></p>
  <p class="text-xs text-muted">回答只依据已审核的后勤服务知识库。</p>
</form>
<script>
(function () {
  var form = document.querySelector("#ask-form");
  var input = document.querySelector("#question");
  var root = document.querySelector("#hq-voice");
  var btn = document.querySelector("#hq-mic");
  var panel = document.querySelector("#hq-voice-panel");
  var status = document.querySelector("#hq-voice-status");
  var stopBtn = document.querySelector("#hq-mic-stop");
  var icon = btn ? btn.querySelector("i") : null;
  if (!form || !input || !root || !btn || !panel || !status || !stopBtn) return;
  var Speech = window.SpeechRecognition || window.webkitSpeechRecognition;
  var hear = null;
  var want = false;

  function show(recording, message) {
    if (message) status.textContent = message;
    root.classList.add("is-open");
    btn.classList.toggle("is-on", !!recording);
    btn.setAttribute("aria-expanded", "true");
    btn.setAttribute("aria-pressed", recording ? "true" : "false");
    btn.setAttribute("aria-label", recording ? "停止聆听" : "语音提问");
    if (icon) icon.className = recording ? "fa-solid fa-microphone-lines" : "fa-solid fa-microphone";
    panel.hidden = false;
    stopBtn.textContent = recording ? "说完了" : "知道了";
  }
  function close() {
    want = false;
    if (hear) { try { hear.stop(); } catch (error) {} }
    root.classList.remove("is-open");
    btn.classList.remove("is-on");
    btn.setAttribute("aria-expanded", "false");
    btn.setAttribute("aria-pressed", "false");
    btn.setAttribute("aria-label", "语音提问");
    if (icon) icon.className = "fa-solid fa-microphone";
    panel.hidden = true;
  }
  function ensure() {
    if (hear || !Speech) return;
    hear = new Speech();
    hear.lang = "zh-CN";
    hear.continuous = true;
    hear.interimResults = true;
    hear.onresult = function (event) {
      if (!want) return;
      var text = "";
      for (var i = 0; i < event.results.length; i++) text += event.results[i][0].transcript;
      if (text) input.value = text;
    };
    hear.onerror = function (event) {
      var code = event.error || "";
      if (code === "aborted" || code === "no-speech") {
        if (code === "no-speech") status.textContent = "没有听到声音，请再说一次或手写。";
        return;
      }
      want = false;
      if (hear) { try { hear.stop(); } catch (error) {} }
        if (code === "not-allowed" || code === "service-not-allowed") {
        show(false, "没有麦克风权限，请在输入框里手写。");
      } else {
        show(false, "麦克风暂时不可用，请在输入框里手写。");
      }
      input.focus();
    };
    hear.onend = function () {
      if (!want) return;
      try { hear.start(); } catch (error) {}
    };
  }
  function start() {
    if (!Speech) {
      want = false;
      show(false, "当前浏览器不能使用麦克风，请手写。");
      input.focus();
      return;
    }
    want = true;
    ensure();
    show(true, "正在听，请说出你的问题");
    try { hear.start(); }
    catch (error) {
      want = false;
      show(false, "麦克风暂时不可用，请在输入框里手写。");
      input.focus();
    }
  }
  btn.addEventListener("click", function () {
    if (!panel.hidden) close();
    else start();
  });
  stopBtn.addEventListener("click", close);
  form.addEventListener("submit", close);
  document.querySelectorAll("[data-ask]").forEach(function (el) {
    el.addEventListener("click", close);
  });
  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && !panel.hidden) close();
  });
})();
</script>"""


def pc_frame(role, current, title, main, right="", listening=False):
    name, sub, _ = PEOPLE[role]
    home = "../../index.html"
    right_html = f'<aside class="hidden h-full flex-col overflow-y-auto border-slate-200 bg-white p-5 lg:flex lg:border-l">{right}</aside>' if right else ""
    cols = "lg:grid-cols-[240px_minmax(0,1fr)_300px]" if right else "lg:grid-cols-[240px_minmax(0,1fr)]"
    body = f"""
<body class="hq-pc min-h-screen bg-mist text-inktext">
<a class="sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-4 focus:z-50 focus:bg-white focus:px-3 focus:py-2" href="#main">跳到主要内容</a>
<header class="sticky top-0 z-20 flex h-14 items-center justify-between px-5 text-white" style="background:linear-gradient(90deg,#1A7DBE 0%,#2A8DC7 100%)">
  <a href="{home}" class="flex items-center gap-3">
    <img src="../../assets/logo.png" alt="" class="h-9 w-9">
    <span><span class="block font-semibold leading-none">中南大学</span><span class="mt-1 block text-[10px] tracking-wide text-white/80">智慧后勤 AI 助手</span></span>
  </a>
  <div class="flex items-center gap-3 text-sm">
    <span class="hidden rounded-full border border-white/30 bg-white/15 px-3 py-1 sm:inline">{name} · {sub}</span>
    <a class="rounded-full border border-white/40 px-3 py-1.5 hover:bg-white/15" href="{home}">返回导航</a>
  </div>
</header>
<div class="lg:grid {cols} lg:h-[calc(100dvh-4rem)]">
  <aside class="border-b border-[#E3F1F9] lg:overflow-y-auto lg:border-b-0" style="background:linear-gradient(180deg,#CFEAFA 0%,#EEF8FE 38%,#FFFFFF 100%)">
    <div class="p-5">{avatar(listening)}</div>
    <nav class="flex gap-2 overflow-x-auto px-3 pb-4 lg:block lg:space-y-1" aria-label="功能">{nav_links("pc", role, current)}</nav>
  </aside>
  <main id="main" class="flex min-h-0 flex-col lg:h-full lg:overflow-y-auto">{main}</main>
  {right_html}
</div>
</body>"""
    return document(title, body)


def mobile_frame(role, current, title, main, footer=""):
    name, sub, _ = PEOPLE[role]
    home = "../../index.html"
    cols = len(NAV[("mobile", role)])
    body = f"""
<body class="hq-stage text-inktext">
<div class="hq-phone">
  <div class="sky"></div>
  <header class="relative z-10 flex h-14 shrink-0 items-center justify-between px-4 text-white">
    <div><p class="text-sm font-semibold leading-none">中南大学</p><p class="mt-1 text-xs text-white/80">{name} · {sub}</p></div>
    <a class="rounded-full border border-white/40 bg-white/15 px-3 py-1.5 text-xs" href="{home}">导航</a>
  </header>
  <main id="main" class="relative z-10 flex min-h-0 flex-1 flex-col overflow-y-auto">{main}</main>
  {footer}
  <nav class="hq-tabbar" style="grid-template-columns:repeat({cols},minmax(0,1fr))" aria-label="主导航">{nav_links("mobile", role, current)}</nav>
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


# 问答首页的消息和历史只在本页展开，不进入侧栏或底栏。
NOTICES = {
    "staff": [
        {
            "id": "weekly",
            "title": "后勤周例会",
            "meta": "2026-10-22 09:00 · 本部后勤楼 3楼",
            "body": "提醒接收人周宁（工号 T20190086）。这场会议目前待提醒。",
            "tag": "待提醒",
            "tone": "amber",
            "unread": True,
        },
        {
            "id": "portal",
            "title": "门户挂载确认会",
            "meta": "2026-10-18 15:00",
            "body": "已按设定时点送出提醒。",
            "tag": "已提醒",
            "tone": "teal",
            "unread": False,
        },
    ],
    "student": [
        {
            "id": "pool",
            "title": "潇湘校区游泳馆开放时间",
            "meta": "公开服务",
            "body": "潇湘校区游泳馆周二至周日开放，周一闭馆。",
            "tag": "服务提示",
            "tone": "brand",
            "unread": True,
        },
        {
            "id": "utility",
            "title": "水电用量暂不能查询",
            "meta": "待接口",
            "body": "水电用量和欠费待接口，暂不提供个人账单。",
            "tag": "待接口",
            "tone": "muted",
            "unread": True,
        },
    ],
    "guest": [
        {
            "id": "public",
            "title": "潇湘校区游泳馆开放时间",
            "meta": "公开服务",
            "body": "潇湘校区游泳馆周二至周日开放，周一闭馆。咨询可拨打后勤服务热线 0731-88836000。",
            "tag": "服务提示",
            "tone": "brand",
            "unread": True,
        },
    ],
}
NOTICE_COPY = {
    "guest": "未登录只看公开服务提示。",
    "student": "公开服务提示。用量和欠费要等水电接口，这里不给出账单。",
    "staff": "周宁的会议提醒。已取消的会议不会出现。",
}
HISTORY_PRESETS = [
    {
        "q": "宿舍水龙头坏了怎么报修？",
        "a": "宿舍水龙头可以报修，也可以拨打后勤服务热线 0731-88836000，全天有人值班。",
    },
    {
        "q": "潇湘校区游泳馆什么时候开放？",
        "a": "潇湘校区游泳馆周二至周日开放，周一闭馆。",
    },
]

HOME_TOOLS_HTML = """
<div class="hq-tools" data-role="home">
  <div class="hq-entry-bar" role="toolbar" aria-label="消息和历史">
    <button type="button" class="hq-entry-btn" id="hq-open-notice" aria-expanded="false" aria-controls="hq-notice-panel" aria-label="消息通知，未读 @@UNREAD@@ 条">
      <i class="fa-solid fa-bell" aria-hidden="true"></i><span>消息通知</span>
      <span class="hq-entry-badge" id="hq-notice-count">@@UNREAD@@</span>
    </button>
    <button type="button" class="hq-entry-btn" id="hq-open-history" aria-expanded="false" aria-controls="hq-history-panel">
      <i class="fa-solid fa-clock-rotate-left" aria-hidden="true"></i><span>历史对话</span>
    </button>
  </div>
  <span id="hq-notice-live" class="sr-only" aria-live="polite"></span>
  <section id="hq-notice-panel" class="hq-panel" hidden aria-labelledby="hq-notice-title">
    <div class="hq-panel-hd">
      <div>
        <p class="hq-panel-title" id="hq-notice-title">消息通知</p>
        <p class="hq-panel-sub">@@NOTICE_SUB@@</p>
      </div>
      <button type="button" class="hq-panel-x" data-hq-close="notice" aria-label="关闭消息通知"><i class="fa-solid fa-xmark" aria-hidden="true"></i></button>
    </div>
    <div id="hq-notice-list"></div>
  </section>
  <section id="hq-history-panel" class="hq-panel" hidden aria-labelledby="hq-history-title">
    <div class="hq-panel-hd">
      <div>
        <p class="hq-panel-title" id="hq-history-title">历史对话</p>
        <p class="hq-panel-sub">点一条，问题和回答会回到本页对话区。</p>
      </div>
      <button type="button" class="hq-panel-x" data-hq-close="history" aria-label="关闭历史对话"><i class="fa-solid fa-xmark" aria-hidden="true"></i></button>
    </div>
    <div id="hq-history-list"></div>
  </section>
</div>
"""

HOME_TOOLS_SCRIPT = r"""
<script>
(function () {
  var role = "@@ROLE@@";
  var notices = @@NOTICES@@;
  var presets = @@HISTORY@@;
  var thread = document.querySelector("#thread");
  var noticeBtn = document.querySelector("#hq-open-notice");
  var historyBtn = document.querySelector("#hq-open-history");
  var noticePanel = document.querySelector("#hq-notice-panel");
  var historyPanel = document.querySelector("#hq-history-panel");
  var noticeList = document.querySelector("#hq-notice-list");
  var historyList = document.querySelector("#hq-history-list");
  var badge = document.querySelector("#hq-notice-count");
  var live = document.querySelector("#hq-notice-live");
  if (!thread || !noticeBtn || !historyBtn || !noticePanel || !historyPanel || !noticeList || !historyList || !badge) return;
  var readKey = "hq-notice-read-" + role;
  var histKey = "hq-history-live-" + role;
  var readIds = loadJson(readKey, []);
  var saved = loadJson(histKey, []);
  var liveRows = saved.filter(function (item) {
    return item && typeof item.q === "string" && typeof item.a === "string" && item.q && item.a;
  }).map(function (item) { return { q: item.q, a: item.a, live: true }; });

  function loadJson(key, fallback) {
    try {
      var parsed = JSON.parse(sessionStorage.getItem(key) || "");
      return Array.isArray(parsed) ? parsed : fallback;
    } catch (error) { return fallback; }
  }
  function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, function (ch) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[ch];
    });
  }
  function isUnread(item) {
    return !!item.unread && readIds.indexOf(item.id) === -1;
  }
  function unreadCount() {
    var count = 0;
    notices.forEach(function (item) { if (isUnread(item)) count += 1; });
    return count;
  }
  function paintBadge(announce) {
    var count = unreadCount();
    badge.hidden = count < 1;
    badge.textContent = String(count);
    noticeBtn.setAttribute("aria-label", count > 0 ? "消息通知，未读 " + count + " 条" : "消息通知，没有未读");
    if (announce && live) live.textContent = count > 0 ? "未读 " + count + " 条" : "没有未读通知";
  }
  function renderNotices(focusId) {
    noticeList.innerHTML = notices.map(function (item) {
      var unread = isUnread(item);
      return '<button type="button" class="hq-note' + (unread ? " is-unread" : "") + '" data-id="' + escapeHtml(item.id) + '">' +
        '<span class="hq-note-top"><span class="hq-note-title">' + escapeHtml(item.title) + "</span>" +
        '<span class="hq-note-pills"><span class="hq-pill ' + escapeHtml(item.tone || "muted") + '">' + escapeHtml(item.tag) + "</span>" +
        '<span class="hq-pill ' + (unread ? "amber" : "muted") + '">' + (unread ? "未读" : "已读") + "</span></span></span>" +
        '<span class="hq-note-meta">' + escapeHtml(item.meta) + "</span>" +
        '<span class="hq-note-body">' + escapeHtml(item.body) + "</span></button>";
    }).join("");
    noticeList.querySelectorAll(".hq-note").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var id = btn.getAttribute("data-id");
        if (id && readIds.indexOf(id) === -1) {
          readIds.push(id);
          try { sessionStorage.setItem(readKey, JSON.stringify(readIds)); } catch (error) {}
        }
        renderNotices(id);
        paintBadge(true);
      });
    });
    if (focusId) {
      var again = noticeList.querySelector('[data-id="' + focusId + '"]');
      if (again) again.focus();
    }
  }
  function preview(text) {
    var line = String(text).replace(/\s+/g, " ").trim();
    return line.length > 46 ? line.slice(0, 46) + "…" : line;
  }
  function allHistory() {
    return liveRows.concat(presets);
  }
  function renderHistory() {
    historyList.innerHTML = allHistory().map(function (item, index) {
      return '<button type="button" class="hq-hist" data-index="' + index + '">' +
        '<span class="hq-note-top"><span class="hq-hist-q">' + escapeHtml(item.q) + "</span>" +
        '<span class="hq-pill ' + (item.live ? "teal" : "muted") + '">' + (item.live ? "本次会话" : "演示") + "</span></span>" +
        '<span class="hq-hist-a">' + escapeHtml(preview(item.a)) + "</span></button>";
    }).join("");
    historyList.querySelectorAll(".hq-hist").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var item = allHistory()[Number(btn.getAttribute("data-index"))];
        if (item) fillThread(item.q, item.a);
      });
    });
  }
  function fillThread(question, answer) {
    thread.innerHTML = "";
    var user = document.createElement("div");
    user.className = "flex justify-end";
    user.innerHTML = '<div class="bubble-user max-w-[86%] px-4 py-3 text-sm leading-6">' + escapeHtml(question) + "</div>";
    var bot = document.createElement("div");
    bot.className = "flex justify-start";
    bot.innerHTML = '<div class="bubble-bot max-w-[92%] px-4 py-3 text-sm leading-6">' +
      '<p class="mb-2 text-xs font-medium text-teal"><i class="fa-solid fa-clock-rotate-left mr-1" aria-hidden="true"></i>历史对话</p>' +
      '<div class="whitespace-pre-wrap">' + escapeHtml(answer) + "</div></div>";
    thread.appendChild(user);
    thread.appendChild(bot);
    setOpen("");
    if (user.scrollIntoView) user.scrollIntoView({ block: "nearest", inline: "nearest" });
  }
  function setOpen(which) {
    noticePanel.hidden = which !== "notice";
    historyPanel.hidden = which !== "history";
    noticeBtn.classList.toggle("is-on", which === "notice");
    historyBtn.classList.toggle("is-on", which === "history");
    noticeBtn.setAttribute("aria-expanded", which === "notice" ? "true" : "false");
    historyBtn.setAttribute("aria-expanded", which === "history" ? "true" : "false");
  }
  noticeBtn.addEventListener("click", function () {
    setOpen(noticePanel.hidden ? "notice" : "");
  });
  historyBtn.addEventListener("click", function () {
    setOpen(historyPanel.hidden ? "history" : "");
  });
  document.querySelectorAll("[data-hq-close]").forEach(function (el) {
    el.addEventListener("click", function () { setOpen(""); });
  });
  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") setOpen("");
  });
  window.hqPushHistory = function (question, answer) {
    question = String(question || "").trim();
    answer = String(answer || "").trim();
    if (!question || !answer) return;
    liveRows.unshift({ q: question, a: answer, live: true });
    if (liveRows.length > 20) liveRows.length = 20;
    try { sessionStorage.setItem(histKey, JSON.stringify(liveRows)); } catch (error) {}
    renderHistory();
  };
  renderNotices();
  renderHistory();
  paintBadge(false);
})();
</script>
"""


def home_tools(role):
    notices = NOTICES[role]
    unread = sum(1 for item in notices if item["unread"])
    html = render(HOME_TOOLS_HTML, UNREAD=str(unread), NOTICE_SUB=escape(NOTICE_COPY[role]))
    script = render(
        HOME_TOOLS_SCRIPT,
        ROLE=role,
        NOTICES=json.dumps(notices, ensure_ascii=False),
        HISTORY=json.dumps(HISTORY_PRESETS, ensure_ascii=False),
    )
    return html, script


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
    tools, tools_script = home_tools(role)
    if port == "mobile":
        icons = []
        for item in SERVICES:
            if item["id"] == "announcement":
                continue
            if item["student_only"] and role != "student":
                continue
            href = "login.html" if role == "guest" else (action_href(item, role, "mobile")[0] or "services.html")
            icons.append(
                f'<a class="flex flex-col items-center gap-2 text-xs text-ink" href="{href}">'
                f'<span class="flex h-12 w-12 items-center justify-center rounded-2xl bg-teal-50 text-lg text-brand"><i class="fa-solid {item["icon"]}"></i></span>{item["name"]}</a>'
            )
        return f"""
<div class="hq-home">
  <div class="hq-tools-slot shrink-0 px-4 pt-3">{tools}</div>
  <div class="px-4 pb-2">
    <div class="rounded-2xl bg-white/95 p-4 shadow-[0_8px_24px_rgba(4,81,239,.08)]">
      <p class="text-xs font-medium text-brand">后勤值班台</p>
      <h1 class="mt-1 text-2xl font-semibold leading-snug text-ink">{welcome}</h1>
      <p class="mt-2 text-sm leading-6 text-muted">可以问报修、水电、班车、食堂、宿舍和场馆。</p>
      <div class="mt-3 flex flex-wrap gap-2">{suggestion_buttons()}</div>
    </div>
  </div>
  <div id="thread" class="space-y-3 px-4 py-2" aria-live="polite"></div>
  {composer()}
  <div class="mx-4 mb-3 mt-2 rounded-2xl bg-white p-4 shadow-[0_4px_16px_rgba(4,81,239,.05)]">
    <p class="mb-3 text-base font-semibold">办事入口</p>
    <div class="grid grid-cols-4 gap-y-4">{''.join(icons)}</div>
  </div>
</div>
{tools_script}
"""
    return f"""
<div class="hq-home flex min-h-full flex-1 flex-col">
  <div class="hq-tools-slot shrink-0 px-5 pt-4 lg:px-6 lg:pt-5">{tools}</div>
  <div class="shrink-0 px-5 pb-4 pt-3 lg:px-6 lg:pb-5">
    <div class="rounded-2xl bg-white p-5 shadow-[0_1px_5px_rgba(45,47,51,.06)]">
      <p class="text-xs font-medium text-brand">后勤值班台</p>
      <h1 class="mt-2 text-3xl font-semibold text-ink">{welcome}</h1>
      <p class="mt-3 max-w-xl text-sm leading-6 text-muted">可以问报修、水电、班车、食堂、宿舍和场馆。回答来自 2026 年 9 月 17 日截止的后勤服务知识库。</p>
      <div class="mt-4 flex flex-wrap gap-2">{suggestion_buttons()}</div>
    </div>
  </div>
  <div id="thread" class="space-y-3 px-5 pb-4 lg:min-h-0 lg:flex-1 lg:overflow-y-auto lg:px-6" aria-live="polite"></div>
  <div class="mt-auto shrink-0">{composer()}</div>
</div>
{tools_script}
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
    location.href = "home.html";
  });
})();
</script>
"""


def listening_main():
    return """
<div class="mx-auto max-w-lg p-6">
  <p class="rounded-xl border border-[#C8E4F4] bg-[#E3F1F9] px-4 py-3 text-sm leading-6 text-[#006DAD]">语音提问在问答首页输入框的左侧。点麦克风说话，识别结果会填进输入框；没有麦克风时仍可手写。</p>
  <h1 class="mt-5 font-serif text-3xl text-ink">正在听</h1>
  <p class="mt-2 text-sm leading-6 text-muted">浏览器若允许麦克风，会把识别出的话填进下面。你也可以直接改字。日常使用请回到问答首页，麦克风在输入框左边。</p>
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
    location.href = "home.html";
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
  <a class="mt-4 inline-flex min-h-11 items-center text-sm text-teal" href="home.html">返回问答首页，试一个后勤问题</a>
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


def profile_main(role, port="pc"):
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
    body = "".join(f'<div class="flex items-center justify-between gap-4 border-b border-[#E6EEF4] py-3 last:border-0"><dt class="text-sm text-muted">{k}</dt><dd class="text-right text-sm">{v}</dd></div>' for k, v in rows)
    if port == "mobile":
        name = "林夏" if role == "student" else "周宁"
        meta = "计算机学院 · 学号 820240118" if role == "student" else "后勤保障部 · 工号 T20190086"
        chips = "学生 · 2024 级" if role == "student" else "教职工 · 在岗"
        return f"""
<div class="px-4 pb-6">
  <div class="mt-2 flex items-center gap-3 text-white">
    <span class="flex h-14 w-14 items-center justify-center rounded-full bg-white/90 text-lg font-semibold text-brand">{name[:1]}</span>
    <div><p class="text-xl font-semibold">{name}</p><p class="text-sm text-white/85">{meta}</p><p class="mt-1 inline-flex rounded-full bg-white/20 px-2 py-0.5 text-xs">{chips}</p></div>
  </div>
  <div class="relative z-10 mt-4 rounded-2xl bg-white p-4 shadow-[0_8px_24px_rgba(4,81,239,.08)]">
    <dl>{body}</dl>
    <p class="mt-3 text-xs leading-5 text-muted">{note}</p>
  </div>
  <div class="mt-4">{extra}</div>
  <a class="mt-4 block text-center text-sm text-muted" href="../guest/home.html">退出演示身份</a>
</div>
"""
    return f"""
<div class="p-5 lg:p-8">
  <div class="rounded-2xl bg-white p-5 shadow-[0_1px_5px_rgba(45,47,51,.06)]">
    <div class="mb-4 flex items-center justify-between border-b border-[#E3F1F9] pb-3">
      <h1 class="text-lg font-bold">我的身份</h1>
      <span class="rounded-full bg-teal-50 px-3 py-1 text-xs text-brand">{'学生' if role == 'student' else '教职工'}</span>
    </div>
    <p class="text-sm leading-6 text-muted">{note}</p>
    <dl class="mt-2">{body}</dl>
    {extra}
    <a class="mt-4 inline-flex text-sm text-brand" href="../guest/home.html">退出演示身份</a>
  </div>
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
        cls = "hq-nav-on" if on else "text-inktext hover:bg-white/70"
        links.append(f'<a class="flex min-h-11 items-center gap-3 rounded-full px-3 text-sm {cls}" href="{href}"><i class="fa-solid {icon} w-4"></i>{label}</a>')
    body = f"""
<body class="min-h-screen bg-mist text-inktext">
<div class="min-h-screen md:grid md:grid-cols-[220px_minmax(0,1fr)]">
  <aside class="text-inktext md:min-h-screen" style="background:linear-gradient(180deg,#CFEAFA 0%,#EEF8FE 38%,#FFFFFF 100%)">
    <a href="../index.html" class="block px-5 py-5">
      <span class="flex h-10 w-10 items-center justify-center rounded-full bg-brand"><img src="../assets/logo.png" alt="" class="h-8 w-8"></span>
      <span class="mt-3 block font-semibold">中南大学</span>
      <span class="mt-1 block text-xs text-muted">智慧后勤 AI 助手</span>
    </a>
    <nav class="flex gap-2 overflow-x-auto px-3 pb-4 md:block md:space-y-1" aria-label="后台">{''.join(links)}</nav>
  </aside>
  <div class="min-w-0">
    <header class="flex h-14 items-center justify-between px-5 text-white" style="background:linear-gradient(90deg,#1A7DBE,#2A8DC7)">
      <h1 class="text-lg font-semibold">{escape(title)}</h1>
      <div class="flex items-center gap-3 text-sm"><span class="rounded-full border border-white/30 bg-white/15 px-3 py-1">审核人 周宁</span><a class="rounded-full border border-white/40 px-3 py-1" href="../index.html">返回导航</a></div>
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
    icons = ["fa-comments", "fa-book", "fa-clipboard-check", "fa-bell"]
    stats = "".join(
        f'<article class="relative overflow-hidden rounded-xl bg-white p-4 shadow-[0_1px_5px_rgba(45,47,51,.06)]"><p class="text-sm text-muted">{k}</p><p class="num mt-2 text-3xl font-extrabold text-ink">{v}</p><p class="mt-1 text-xs text-muted">{s}</p><span class="absolute right-4 top-4 flex h-10 w-10 items-center justify-center rounded-xl bg-teal-50 text-brand"><i class="fa-solid {ic}"></i></span></article>'
        for (k, v, s), ic in zip(cards, icons)
    )
    return f"""
<div class="mb-3 flex flex-wrap items-center justify-between gap-3">
  <div><h2 class="text-base font-bold">后勤运行总览</h2><p class="text-xs text-muted">数据为演示口径 · 周宁今天有 1 条知识待审核</p></div>
  <div class="flex gap-2 text-sm"><span class="rounded bg-teal-50 px-3 py-1 font-semibold text-brand">本周</span><span class="rounded px-3 py-1 text-muted">本月</span><span class="rounded px-3 py-1 text-muted">本年</span></div>
</div>
<section class="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">{stats}</section>
<section class="mt-3 grid gap-3 lg:grid-cols-5">
  <article class="rounded-xl bg-white p-5 shadow-[0_1px_5px_rgba(45,47,51,.06)] lg:col-span-3">
    <div class="mb-3 flex items-center justify-between border-b border-[#E3F1F9] pb-2"><h2 class="font-bold">近七日公开问答</h2><span class="text-xs text-muted">演示数据</span></div>
    <div class="flex items-end gap-3" role="img" aria-label="近七日问答量依次升高后略有回落">{chart}</div>
  </article>
  <article class="rounded-xl bg-white p-5 shadow-[0_1px_5px_rgba(45,47,51,.06)] lg:col-span-2">
    <h2 class="border-b border-[#E3F1F9] pb-2 font-bold">下一场提醒</h2>
    <p class="mt-4 text-2xl font-semibold text-ink">后勤周例会</p>
    <p class="num mt-2 text-sm text-muted">10 月 22 日 09:00 · 会前 1 小时</p>
    <a class="mt-4 inline-flex text-sm font-medium text-brand" href="meeting-detail.html">查看会议</a>
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
<div id="banner" hidden class="mb-3 rounded-lg bg-teal-50 px-4 py-2 text-sm text-teal-700"></div>
<div class="mb-3 flex flex-wrap items-center gap-2 rounded-xl bg-white px-4 py-3 shadow-[0_1px_5px_rgba(45,47,51,.06)]">
  <span class="text-sm text-muted">状态</span>
  <span class="rounded bg-teal-50 px-3 py-1 text-sm text-brand">全部</span>
  <span class="rounded px-3 py-1 text-sm text-muted">已发布</span>
  <span class="rounded px-3 py-1 text-sm text-muted">待审核</span>
  <span class="rounded px-3 py-1 text-sm text-muted">草稿</span>
  <span class="ml-auto flex gap-2"><a class="inline-flex h-8 items-center rounded bg-brand px-3 text-sm text-white" href="knowledge-edit.html">起草知识</a><a class="inline-flex h-8 items-center rounded border border-[#D8DBE4] bg-white px-3 text-sm text-brand" href="knowledge-review.html">处理待审核</a></span>
</div>
<div class="overflow-x-auto rounded-xl bg-white shadow-[0_1px_5px_rgba(45,47,51,.06)]">
  <table class="w-full min-w-[640px] text-left text-sm">
    <thead class="bg-mist text-muted"><tr><th class="px-4 py-3 font-medium">标题</th><th class="px-4 py-3 font-medium">状态</th><th class="px-4 py-3 font-medium">可见性</th><th class="px-4 py-3 text-right font-medium">日期</th></tr></thead>
    <tbody class="divide-y divide-slate-100">{''.join(body)}    </tbody>
  </table>
</div>
<div class="mt-3 flex items-center justify-between text-sm text-muted"><span>共 4 条知识</span><span class="flex items-center gap-1"><span class="grid h-8 min-w-8 place-items-center rounded bg-brand px-2 text-white">1</span><span class="grid h-8 min-w-8 place-items-center rounded bg-[#F2F5F8] px-2">10 条/页</span></span></div>
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

    def add_pc(group, role, filename, card_title, desc, icon, main, right="", listening=False, script="", catalog=True):
        html = pc_frame(role, filename, card_title, main + script, right, listening)
        rel = f"pc/{role}/{filename}"
        if catalog:
            emit(group, rel, card_title, desc, icon, html)
        else:
            write_file(rel, html)

    def add_mobile(group, role, filename, card_title, desc, icon, main, script="", catalog=True):
        html = mobile_frame(role, filename, card_title, main + script)
        rel = f"mobile/{role}/{filename}"
        if catalog:
            emit(group, rel, card_title, desc, icon, html)
        else:
            write_file(rel, html)

    for port, adder, group_prefix in (("pc", add_pc, "电脑端"), ("mobile", add_mobile, "移动端")):
        g = f"{group_prefix} · 游客"
        home = home_main("guest", port)
        if port == "pc":
            adder(g, "guest", "home.html", "问答首页", "迎宾、热门问题，回答留在本页", "fa-house", home + chat_js("guest", "pc"), rail_home("guest"))
            adder(g, "guest", "chat.html", "对话", "发送问题并得到知识库回答", "fa-comments", chat_main() + chat_js("guest", "pc"), '<div id="action-rail"><p class="text-sm leading-6 text-muted">回答之后，这里出现对应的办事入口。游客会先去登录。</p></div>', catalog=False)
        else:
            adder(g, "guest", "home.html", "问答首页", "手机上提问，回答留在本页", "fa-house", home + chat_js("guest", "mobile"))
            adder(g, "guest", "chat.html", "对话", "手机上的真实问答", "fa-comments", mobile_chat_main() + chat_js("guest", "mobile"), catalog=False)
        adder(g, "guest", "not-found.html", "暂未收录", "知识库没有写到时的版式", "fa-circle-info", not_found_main())
        adder(g, "guest", "category.html", "办事说明", "四类公开说明，办理前要登录", "fa-map", category_main())
        adder(g, "guest", "login.html", "统一认证", "演示学生或教职工身份", "fa-right-to-bracket", login_main(port))
        adder(g, "guest", "listening.html", "聆听说明", "麦克风在输入框左侧", "fa-microphone", listening_main() + LISTEN_SCRIPT, listening=True) if port == "pc" else adder(g, "guest", "listening.html", "聆听说明", "麦克风在输入框左侧", "fa-microphone", listening_main() + LISTEN_SCRIPT)

    add_pc("电脑端 · 学生", "student", "home.html", "学生首页", "登录后的欢迎，回答留在本页", "fa-house", home_main("student", "pc") + chat_js("student", "pc"), rail_home("student"))
    add_pc("电脑端 · 学生", "student", "chat.html", "学生对话", "回答后按电脑规则给入口", "fa-comments", chat_main() + chat_js("student", "pc"), '<div id="action-rail"><p class="text-sm leading-6 text-muted">水电缴费会引导到二维码。其余电脑地址可以直接去办理。</p></div>', catalog=False)
    add_pc("电脑端 · 学生", "student", "services.html", "学生办事", "八个电脑地址，外加缴费二维码", "fa-table-cells-large", services_main("student", "pc"))
    add_pc("电脑端 · 学生", "student", "jump.html", "离开确认", "确认后打开这一端的正式地址", "fa-arrow-up-right-from-square", jump_main() + jump_js("student", "pc"))
    add_pc("电脑端 · 学生", "student", "qrcode.html", "缴费二维码", "电脑上看见手机缴费码", "fa-qrcode", qrcode_main() + QR_SCRIPT)
    add_pc("电脑端 · 学生", "student", "utility.html", "水电指引", "怎么缴、到哪里缴，用量待接口", "fa-bolt", utility_main("pc", "student"))
    add_pc("电脑端 · 学生", "student", "profile.html", "学生身份", "只读的院系和住宿", "fa-user", profile_main("student"))
    add_pc("电脑端 · 学生", "student", "listening.html", "聆听说明", "麦克风在输入框左侧", "fa-microphone", listening_main() + LISTEN_SCRIPT, listening=True)

    add_pc("电脑端 · 教职工", "staff", "home.html", "教职工首页", "周宁的值班欢迎，回答留在本页", "fa-house", home_main("staff", "pc") + chat_js("staff", "pc"), rail_home("staff"))
    add_pc("电脑端 · 教职工", "staff", "chat.html", "教职工对话", "不出现学生缴费入口", "fa-comments", chat_main() + chat_js("staff", "pc"), '<div id="action-rail"><p class="text-sm leading-6 text-muted">教职工可以办报修、监督、场馆和仅电脑事项，不能缴学生水电。</p></div>', catalog=False)
    add_pc("电脑端 · 教职工", "staff", "services.html", "教职工办事", "没有水电缴费二维码", "fa-table-cells-large", services_main("staff", "pc"))
    add_pc("电脑端 · 教职工", "staff", "jump.html", "离开确认", "打开教职工可用的电脑地址", "fa-arrow-up-right-from-square", jump_main() + jump_js("staff", "pc"))
    add_pc("电脑端 · 教职工", "staff", "profile.html", "教职工身份", "部门、工号和在岗情况", "fa-user", profile_main("staff"))
    add_pc("电脑端 · 教职工", "staff", "listening.html", "聆听说明", "麦克风在输入框左侧", "fa-microphone", listening_main() + LISTEN_SCRIPT, listening=True)

    add_mobile("移动端 · 学生", "student", "home.html", "学生首页", "手机欢迎，回答留在本页", "fa-house", home_main("student", "mobile") + chat_js("student", "mobile"))
    add_mobile("移动端 · 学生", "student", "chat.html", "学生对话", "手机上直接去缴纳或改用电脑", "fa-comments", mobile_chat_main() + chat_js("student", "mobile"), catalog=False)
    add_mobile("移动端 · 学生", "student", "listening.html", "聆听说明", "麦克风在输入框左侧", "fa-microphone", listening_main() + LISTEN_SCRIPT)
    add_mobile("移动端 · 学生", "student", "services.html", "学生办事", "四个手机地址可办，五项改用电脑", "fa-table-cells-large", services_main("student", "mobile"))
    add_mobile("移动端 · 学生", "student", "utility.html", "去缴纳", "手机上的缴费步骤和入口", "fa-bolt", utility_main("mobile", "student"))
    add_mobile("移动端 · 学生", "student", "jump.html", "离开确认", "打开手机端正式地址", "fa-arrow-up-right-from-square", jump_main() + jump_js("student", "mobile"))
    add_mobile("移动端 · 学生", "student", "guide.html", "电脑办理说明", "班车、宾馆、报刊、失物和公告", "fa-desktop", guide_main() + guide_js)
    add_mobile("移动端 · 学生", "student", "profile.html", "学生身份", "手机上的只读资料", "fa-user", profile_main("student", "mobile"))

    add_mobile("移动端 · 教职工", "staff", "home.html", "教职工首页", "手机上提问，回答留在本页", "fa-house", home_main("staff", "mobile") + chat_js("staff", "mobile"))
    add_mobile("移动端 · 教职工", "staff", "chat.html", "教职工对话", "手机上也不出现缴费", "fa-comments", mobile_chat_main() + chat_js("staff", "mobile"), catalog=False)
    add_mobile("移动端 · 教职工", "staff", "services.html", "教职工办事", "只能办报修、监督和游泳馆", "fa-table-cells-large", services_main("staff", "mobile"))
    add_mobile("移动端 · 教职工", "staff", "jump.html", "离开确认", "打开教职工的手机地址", "fa-arrow-up-right-from-square", jump_main() + jump_js("staff", "mobile"))
    add_mobile("移动端 · 教职工", "staff", "guide.html", "电脑办理说明", "仅电脑事项的地址说明", "fa-desktop", guide_main() + guide_js)
    add_mobile("移动端 · 教职工", "staff", "profile.html", "教职工身份", "工号与会议提醒入口", "fa-user", profile_main("staff", "mobile"))

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


INDEX_CSS = """
:root { --p:#006DAD; --p2:#2A8DC7; --pl:#E3F1F9; --m:#0451EF; --t1:#1E323F; --t2:#627079; --t3:#979FA6; --line:#E6EEF4; --bg:#F3F7FB; --red:#F43F51; --green:#0E9F63; --orange:#E8801A; }
body.hq { font-family:"OPPOSans",-apple-system,"PingFang SC","HarmonyOS Sans SC","Microsoft YaHei",sans-serif; color:var(--t1); background:var(--bg); font-size:14px; line-height:1.6; }
.hq a { color:inherit; text-decoration:none; }
.hq-nav { position:sticky; top:0; z-index:20; height:60px; display:flex; align-items:center; gap:28px; padding:0 40px; background:rgba(255,255,255,.88); backdrop-filter:blur(12px); border-bottom:1px solid var(--line); }
.hq-nav .brand { display:flex; align-items:center; gap:10px; font-weight:800; font-size:16px; }
.hq-nav .mark { width:32px; height:32px; border-radius:8px; background:linear-gradient(135deg,var(--p2),var(--p)); color:#fff; display:grid; place-items:center; font-weight:800; }
.hq-nav .links { display:flex; gap:22px; margin-left:auto; color:var(--t2); flex-wrap:wrap; }
.hq-nav .links a:hover { color:var(--p); }
.hq-hero { position:relative; color:#fff; padding:64px 40px 120px; overflow:hidden; background:linear-gradient(115deg,rgba(0,70,130,.95) 0%,rgba(4,81,239,.82) 55%,rgba(42,141,199,.65) 100%),url(https://images.unsplash.com/photo-1541339907198-e08756dedf3f?auto=format&fit=crop&w=1800&h=700&q=70) center/cover; }
.hq-hero .wrap { max-width:1240px; margin:0 auto; }
.hq-hero .tagline { display:inline-flex; gap:8px; align-items:center; background:rgba(255,255,255,.16); border:1px solid rgba(255,255,255,.3); border-radius:16px; padding:4px 14px; font-size:13px; }
.hq-hero h1 { font-size:44px; letter-spacing:3px; margin:18px 0 10px; line-height:1.25; }
.hq-hero p { font-size:16px; opacity:.9; max-width:760px; }
.hq-hero .loop { display:flex; gap:10px; margin-top:26px; flex-wrap:wrap; }
.hq-hero .loop span { background:rgba(255,255,255,.14); border-radius:20px; padding:6px 16px; }
.hq-kpis { max-width:1240px; margin:-72px auto 0; position:relative; z-index:2; display:grid; grid-template-columns:repeat(5,1fr); gap:14px; padding:0 40px; }
.hq-kpi { background:#fff; border-radius:16px; padding:18px 20px; box-shadow:0 12px 30px rgba(0,60,110,.08); }
.hq-kpi b { display:block; font-size:30px; font-weight:800; color:var(--p); font-variant-numeric:tabular-nums; }
.hq-kpi span { color:var(--t2); font-size:13px; }
.hq-sec { max-width:1240px; margin:0 auto; padding:56px 40px 0; }
.hq-st { display:flex; align-items:flex-end; justify-content:space-between; margin-bottom:20px; gap:16px; }
.hq-st h2 { font-size:26px; display:flex; align-items:center; gap:10px; }
.hq-st h2 i { font-style:normal; font-size:13px; color:#fff; background:linear-gradient(135deg,var(--p2),var(--p)); border-radius:8px; padding:2px 8px; }
.hq-st p { color:var(--t2); margin-top:4px; }
.hq-roles { display:grid; grid-template-columns:repeat(3,1fr); gap:16px; }
.hq-role { background:#fff; border-radius:18px; overflow:hidden; box-shadow:0 6px 20px rgba(0,60,110,.06); display:flex; flex-direction:column; }
.hq-role .top { padding:22px; color:#fff; }
.hq-role .top h3 { font-size:20px; margin-top:12px; }
.hq-role .top small { opacity:.85; }
.hq-role .bd { padding:18px 22px 22px; }
.hq-role ul { list-style:none; display:grid; gap:8px; color:var(--t2); margin-bottom:16px; }
.hq-go { display:flex; flex-wrap:wrap; gap:10px; }
.hq-btn { height:38px; padding:0 16px; border-radius:19px; display:inline-flex; align-items:center; gap:6px; font-weight:600; font-size:13px; background:linear-gradient(90deg,var(--p2),var(--p)); color:#fff; }
.hq-btn.ghost { background:#fff; color:var(--p); border:1px solid #CFE3F1; }
.hq-mods { display:grid; grid-template-columns:repeat(2,1fr); gap:18px; }
.hq-mod { background:#fff; border-radius:18px; overflow:hidden; box-shadow:0 6px 20px rgba(0,60,110,.06); }
.hq-mod .hd { display:flex; align-items:center; gap:12px; padding:16px 20px; border-bottom:1px solid var(--line); }
.hq-mod .hd .ic { width:38px; height:38px; border-radius:11px; display:grid; place-items:center; background:var(--pl); color:var(--p); }
.hq-mod .hd b { font-size:17px; } .hq-mod .hd small { display:block; color:var(--t2); font-size:12px; }
.hq-mod .hd .cnt { margin-left:auto; font-size:12px; color:var(--t2); background:var(--bg); padding:3px 10px; border-radius:10px; }
.hq-plist { display:grid; grid-template-columns:1fr 1fr; gap:2px 16px; padding:8px 12px 16px; }
.hq-pl { display:flex; align-items:center; gap:8px; padding:8px; border-radius:8px; font-size:13px; }
.hq-pl:hover { background:var(--bg); }
.hq-pl .nm { flex:1; min-width:0; } .hq-pl .r { font-size:11px; color:var(--t3); }
.hq-card { background:#fff; border-radius:18px; padding:20px 22px; box-shadow:0 6px 20px rgba(0,60,110,.06); }
.hq-matrix { max-height:640px; overflow:auto; border-radius:12px; border:1px solid var(--line); }
.hq-matrix table { width:100%; border-collapse:collapse; }
.hq-matrix th { position:sticky; top:0; background:var(--pl); text-align:left; padding:10px 12px; font-weight:600; white-space:nowrap; }
.hq-matrix td { padding:9px 12px; border-bottom:1px solid var(--line); color:var(--t2); }
.hq-feats { display:grid; grid-template-columns:repeat(2,1fr); gap:14px; }
.hq-feat { background:#fff; border-radius:14px; padding:16px 18px; box-shadow:0 4px 14px rgba(0,60,110,.05); }
.hq-flows { display:grid; grid-template-columns:1fr 1fr; gap:14px; }
.hq-flow { background:#fff; border-radius:16px; padding:18px 20px; box-shadow:0 4px 14px rgba(0,60,110,.05); }
.hq-flow h3 { font-size:16px; margin-bottom:10px; }
.hq-flow li { color:var(--t2); margin-left:18px; }
.hq-foot { text-align:center; color:var(--t3); font-size:12px; padding:48px 0 40px; }
@media (max-width:900px) {
  .hq-nav { padding:0 16px; height:auto; min-height:60px; flex-wrap:wrap; }
  .hq-kpis, .hq-roles, .hq-mods, .hq-feats, .hq-flows, .hq-plist { grid-template-columns:1fr 1fr; }
  .hq-hero { padding:40px 16px 90px; } .hq-hero h1 { font-size:32px; }
  .hq-sec, .hq-kpis { padding-left:16px; padding-right:16px; }
}
"""


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
        if rel.endswith("/chat.html"):
            continue
        if group != current:
            if bucket:
                groups.append((current, bucket))
            current = group
            bucket = []
        bucket.append((rel, title, desc, icon))
    if bucket:
        groups.append((current, bucket))
    mods = []
    for name, items in groups:
        links = "".join(
            f'<a class="hq-pl" href="{rel}"><i class="fa-solid {icon}"></i><span class="nm">{title}</span><span class="r">{desc}</span></a>'
            for rel, title, desc, icon in items
        )
        mods.append(
            f'<article class="hq-mod"><div class="hd"><span class="ic"><i class="fa-solid {items[0][3]}"></i></span>'
            f'<div><b>{name}</b><small>点击页面名称进入</small></div><span class="cnt">{len(items)} 页</span></div>'
            f'<div class="hq-plist">{links}</div></article>'
        )
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
<style>{INDEX_CSS}</style>
<body class="hq">
<nav class="hq-nav"><a class="brand" href="index.html"><span class="mark">后</span>中南大学智慧后勤AI助手 · 原型导航</a>
  <div class="links"><a href="#roles">角色与端口</a><a href="#pages">页面导航</a><a href="#matrix">权限矩阵</a><a href="#features">功能清单</a><a href="#flows">业务流程</a></div></nav>
<header class="hq-hero"><div class="wrap">
  <span class="tagline" id="health">正在检查问答服务</span>
  <h1>智慧后勤AI助手</h1>
  <p>公开问题用知识库回答，能办理的事项按电脑或手机跳回原系统，会议由管理员录入后按工号提醒。个人水电账单本期不查。</p>
  <div class="loop"><span>智能问答</span><span>办事跳转</span><span>会议提醒</span><span>知识审核</span></div>
</div></header>
<div class="hq-kpis">
  <div class="hq-kpi"><b>59</b><span>原型页面</span></div>
  <div class="hq-kpi"><b>2</b><span>终端：电脑 + 手机</span></div>
  <div class="hq-kpi"><b>5</b><span>使用角色</span></div>
  <div class="hq-kpi"><b>4</b><span>核心流程</span></div>
  <div class="hq-kpi"><b>8</b><span>电脑端正式地址</span></div>
</div>
<section class="hq-sec" id="roles"><div class="hq-st"><div><h2><i>01</i>角色与端口</h2><p>演示时按这张卡片讲。知识维护人李衡，审核人周宁。</p></div></div>
<div class="hq-roles">
  <article class="hq-role"><div class="top" style="background:linear-gradient(135deg,#7AA7BE,#627079)"><h3>游客</h3><small>不登录 · 只看公开说明</small></div><div class="bd"><ul><li>查阅已公开的办事问答</li><li>办理前进入统一身份认证</li><li>不开放个人账单和会议提醒</li></ul><div class="hq-go"><a class="hq-btn" href="pc/guest/home.html">电脑端</a><a class="hq-btn ghost" href="mobile/guest/home.html">手机端</a></div></div></article>
  <article class="hq-role"><div class="top" style="background:linear-gradient(135deg,#3E8BFF,#0451EF)"><h3>学生 · 林夏</h3><small>计算机学院 · 麓南校区升华公寓</small></div><div class="bd"><ul><li>公开问答，并按学生身份办事</li><li>水电缴费只在手机办理</li><li>电脑上对缴费出示二维码</li></ul><div class="hq-go"><a class="hq-btn" href="pc/student/home.html">电脑端</a><a class="hq-btn ghost" href="mobile/student/home.html">手机端</a></div></div></article>
  <article class="hq-role"><div class="top" style="background:linear-gradient(135deg,#2A8DC7,#006DAD)"><h3>教职工 · 周宁</h3><small>后勤保障部 · 工号 T20190086</small></div><div class="bd"><ul><li>公开问答和已开放的办事入口</li><li>不出现学生水电缴费</li><li>在提醒名单内可回看会议</li></ul><div class="hq-go"><a class="hq-btn" href="pc/staff/home.html">电脑端</a><a class="hq-btn ghost" href="mobile/staff/home.html">手机端</a></div></div></article>
  <article class="hq-role"><div class="top" style="background:linear-gradient(135deg,#F7A64A,#E8801A)"><h3>提醒接收人</h3><small>按工号接收，正式通道是学校 ITS</small></div><div class="bd"><ul><li>回看已推送的会议提醒</li><li>默认会前 1 小时，只提醒一次</li><li>取消的会议不再推送</li></ul><div class="hq-go"><a class="hq-btn" href="pc/recipient/inbox.html">电脑端</a><a class="hq-btn ghost" href="mobile/recipient/inbox.html">手机端</a></div></div></article>
  <article class="hq-role"><div class="top" style="background:linear-gradient(135deg,#1A7DBE,#006DAD)"><h3>业务管理员</h3><small>后勤领导指定 · 维护与审核分开</small></div><div class="bd"><ul><li>维护知识、分类、功能清单</li><li>知识须审核后前台才能引用</li><li>会议保存即生效，不做审批</li></ul><div class="hq-go"><a class="hq-btn" href="admin/dashboard.html">进入后台</a><a class="hq-btn ghost" href="admin/login.html">登录页</a></div></div></article>
</div></section>
<section class="hq-sec" id="pages"><div class="hq-st"><div><h2><i>02</i>页面导航</h2><p>每行两个功能模块，点击页面名称进入对应界面</p></div></div>
<div class="hq-mods">{''.join(mods)}</div></section>
<section class="hq-sec" id="matrix"><div class="hq-st"><div><h2><i>03</i>角色权限矩阵</h2><p>格子里写的是能做的事，不单靠颜色区分。</p></div></div>
<div class="hq-card"><div class="hq-matrix">{matrix}</div></div></section>
<section class="hq-sec" id="features"><div class="hq-st"><div><h2><i>04</i>功能清单</h2><p>地址以《服务链接》的电脑段、手机段为准。部分电脑地址打开时可能是 404，页面会标成待复核。</p></div></div>
<div class="hq-feats">
  <article class="hq-feat"><h3>两端都有地址</h3><p>网上报修、服务监督、游泳馆预定。电脑和手机各用各的链接。</p></article>
  <article class="hq-feat"><h3>只有手机地址</h3><p>水电缴费，只对学生开放。电脑访问时说明原因并出示二维码。</p></article>
  <article class="hq-feat"><h3>只有电脑地址</h3><p>水电费服务说明、班车查询、校园宾馆、报刊订阅、失物招领。</p></article>
  <article class="hq-feat"><h3>没有单独地址</h3><p>校园公告。两端都只说明，请看后勤保障部官网 {OFFICIAL_SITE}。</p></article>
</div></section>
<section class="hq-sec" id="flows"><div class="hq-st"><div><h2><i>05</i>业务流程</h2><p>问答、跳转、会议提醒和知识审核</p></div></div>
<div class="hq-flows">{flows}</div></section>
<footer class="hq-foot">热线 {HOTLINE} 来自后勤服务知识库。收费和开放时间以现场公示为准。知识采集截止 2026 年 9 月 17 日。</footer>
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
