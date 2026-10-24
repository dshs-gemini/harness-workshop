#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""하네스 엔지니어링 교원연수 HTML 슬라이드 덱 조립기.

입력 : _workspace/deck/02_writer_M1..M5,M6,M7,MW_slides.md  (슬라이드 1-68)
출력 : output/하네스엔지니어링_교원연수_슬라이드.html (외부 의존 없는 단일 파일)
사용 : python3 output/build_deck.py
원고를 고친 뒤 이 스크립트를 다시 실행하면 한 번에 재조립된다.
원고의 '가정'·'검수 반영' 등 첫 슬라이드 이전 블록과 슬라이드 뒤의 검산 블록은 무시한다.

구성: (1) 공용 파서·인라인·블록 렌더 함수(교재판 build_handout.py가 import, 동작 변경 금지)
      (2) 발표용 렌더 층(디자인 v2): 조각 추출 pieces() -> 레이아웃 템플릿(L_*) -> 슬라이드별 도식 OVERRIDES(인라인 SVG)
      (3) CSS 토큰·컴포넌트, JS(키보드·노트·목차·맞춤 계산 fit)
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "_workspace" / "deck"
OUT = ROOT / "output" / "하네스엔지니어링_교원연수_슬라이드.html"
FILES = ["M1", "M2", "M3", "M4", "M5", "M6", "M7", "MW"]

# 설계서 모듈표(슬라이드 번호 범위, 모듈 이름)
MODULES = [
    (1, 6, "M1", "도입 · Claude Code 첫 대화"),
    (7, 11, "M2", "잘 시키는 법: 프롬프트 · 컨텍스트 · 플랜 모드"),
    (12, 19, "M3", "CLAUDE.md · 스킬 · 권한"),
    (20, 25, "M4", "하네스 입문"),
    (26, 33, "M5", "하네스가 만든 파일 읽고 고치기"),
    (34, 52, "M6", "Firebase 기능 지도와 콘솔 설정"),
    (53, 64, "M7", "프로젝트: 우리 교과 단원 수업 패키지 만들기"),
    (65, 68, "MW", "마무리"),
]
FIELD_RE = re.compile(r"^- (유형|본문|도식|프롬프트|예상 결과|막힐 때|노트):[ \t]*(.*)$")
SLIDE_RE = re.compile(r"^## \[슬라이드 (\d+)\]\s*(.*)$")
CHECK_RE = re.compile(r"(`?)\[확인필요([^\]]*)\]\1")
CAPTURE_RE = re.compile(r"`?\[(화면 캡처 자리[^\]]*|설문 링크/QR[^\]]*)\]`?")


# ----------------------------------------------------------------- 파서
def parse_file(path):
    slides = []
    cur = None
    field = None
    in_fence = False
    for raw in path.read_text(encoding="utf-8").split("\n"):
        line = raw.rstrip()
        m = SLIDE_RE.match(line)
        if m:
            cur = {"n": int(m.group(1)), "title": m.group(2).strip(), "f": {}, "file": path.name}
            slides.append(cur)
            field = None
            in_fence = False
            continue
        if cur is None:
            continue
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        if not in_fence and (line.startswith("---") or re.match(r"^#{1,3} ", line)):
            cur = None
            field = None
            continue
        fm = FIELD_RE.match(line) if not in_fence else None
        if fm:
            field = fm.group(1)
            cur["f"][field] = [fm.group(2)] if fm.group(2) else []
        elif field is not None:
            cur["f"][field].append(line[2:] if line.startswith("  ") else line)
    return slides


def field_text(slide, key):
    lines = list(slide["f"].get(key, []))
    while lines and not lines[-1].strip():
        lines.pop()
    while lines and not lines[0].strip():
        lines.pop(0)
    txt = "\n".join(lines)
    if re.fullmatch(r"\((?:해당 )?없음[^)\n]*\)|\(Claude Code 사용 없음[^)\n]*\)|\(없음\)", txt.strip()):
        return ""
    if re.fullmatch(r"\([^)\n]*(?:해당 없음|해당 없다)[^)\n]*\)", txt.strip()):
        return ""
    return txt


# ----------------------------------------------------------------- 인라인
def inline(text, tokens=None):
    """원고 인라인 문법을 HTML로. [확인필요]는 작은 배지, 백틱은 code."""
    store = []

    def keep(h):
        store.append(h)
        return "\x00%d\x00" % (len(store) - 1)

    def chk(m):
        detail = m.group(2).lstrip(":： ").strip()
        title = html.escape(detail or "원고에 [확인필요]로 남은 항목", quote=True)
        if tokens is not None:
            tokens.append(detail)
        return keep('<span class="chk" title="%s">확인 필요</span>' % title)

    def cap(m):
        label = m.group(1)
        if label.startswith("설문"):
            return keep('<span class="ph">%s</span>' % html.escape(label))
        return keep('<span class="ph">%s</span>' % html.escape(label))

    text = CHECK_RE.sub(chk, text)
    text = CAPTURE_RE.sub(cap, text)

    def code(m):
        body = m.group(1)
        if "→" in body and "[" in body:
            parts = [p.strip() for p in body.split("→")]
            chips = '<span class="arr">→</span>'.join(
                '<span class="chip">%s</span>' % html.escape(p.strip("[] ")) for p in parts
            )
            return keep('<span class="flowline">%s</span>' % chips)
        return keep("<code>%s</code>" % html.escape(body))

    text = re.sub(r"`([^`\n]+)`", code, text)
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    return re.sub(r"\x00(\d+)\x00", lambda m: store[int(m.group(1))], text)


# ----------------------------------------------------------------- 블록
LIST_RE = re.compile(r"^(\s*)([-*]|\d+\.)\s+(.*)$")


def render_fence(lines, ctx, title=None):
    """코드 펜스를 컴포넌트로. ctx: prompt|result|plain"""
    if lines and lines[0].startswith("[file-box]"):
        title = lines[0][len("[file-box]"):].strip()
        lines = lines[1:]
    body = "\n".join(lines)
    esc = html.escape(body)
    if ctx == "prompt":
        return ('<div class="prompt-box"><button class="copy" type="button">복사</button>'
                "<pre><code>%s</code></pre></div>" % esc)
    if title is not None:
        return ('<div class="file-box"><div class="fb-title">%s</div><button class="copy" type="button">복사</button>'
                "<pre><code>%s</code></pre></div>" % (html.escape(title), esc))
    cls = "terminal" if ctx == "result" else "code-block"
    return '<div class="%s"><pre><code>%s</code></pre></div>' % (cls, esc)


def render_table(rows, tokens):
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    cells = [r for r in cells if not all(re.fullmatch(r":?-{2,}:?", c) for c in r if c) or not any(r)]
    cells = [r for r in cells if not all(re.fullmatch(r":?-+:?", c) for c in r)]
    if not cells:
        return ""
    head, rest = cells[0], cells[1:]
    out = ["<table><thead><tr>"]
    out += ["<th>%s</th>" % inline(c, tokens) for c in head]
    out.append("</tr></thead><tbody>")
    for r in rest:
        out.append("<tr>" + "".join("<td>%s</td>" % inline(c, tokens) for c in r) + "</tr>")
    out.append("</tbody></table>")
    return "".join(out)


def render_list(items, tokens):
    """items: [(indent, kind, text)] -> 중첩 ul/ol"""
    out = []
    stack = []  # (indent, tag)
    for indent, marker, text in items:
        tag = "ol" if marker[0].isdigit() else "ul"
        while stack and indent < stack[-1][0]:
            out.append("</li></%s>" % stack.pop()[1])
        if stack and indent == stack[-1][0]:
            if stack[-1][1] != tag:
                out.append("</li></%s>" % stack.pop()[1])
                out.append("<%s><li>" % tag)
                stack.append((indent, tag))
            else:
                out.append("</li><li>")
        elif not stack or indent > stack[-1][0]:
            out.append("<%s><li>" % tag)
            stack.append((indent, tag))
        out.append(inline(text, tokens))
    while stack:
        out.append("</li></%s>" % stack.pop()[1])
    return "".join(out)


def render_blocks(text, tokens, ctx="plain"):
    """원고용 미니 마크다운 -> HTML. 반환: (html, 코드펜스 목록)"""
    lines = text.split("\n")
    out = []
    i = 0
    pending_title = None
    para = []

    def flush():
        nonlocal para
        if para:
            out.append("<p>%s</p>" % "<br>".join(inline(p.strip(), tokens) for p in para))
            para = []

    while i < len(lines):
        ln = lines[i]
        s = ln.strip()
        if s.startswith("```"):
            flush()
            ind = len(ln) - len(ln.lstrip())
            j = i + 1
            body = []
            while j < len(lines) and not lines[j].strip().startswith("```"):
                body.append(lines[j][ind:] if lines[j][:ind].strip() == "" else lines[j].lstrip())
                j += 1
            for b in body:
                if CHECK_RE.search(b):
                    tokens.append(CHECK_RE.search(b).group(2).lstrip(":： ").strip())
            out.append(render_fence(body, ctx, pending_title))
            pending_title = None
            i = j + 1
            continue
        if s.startswith("|"):
            flush()
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(lines[i])
                i += 1
            out.append(render_table(rows, tokens))
            continue
        lm = LIST_RE.match(ln)
        if lm:
            flush()
            items = []
            while i < len(lines):
                lm = LIST_RE.match(lines[i])
                if lm:
                    items.append([len(lm.group(1)), lm.group(2), lm.group(3)])
                    i += 1
                elif lines[i].strip() and lines[i].startswith(" ") and items and not lines[i].strip().startswith(("```", "|")):
                    items[-1][2] += " " + lines[i].strip()  # 이어지는 줄
                    i += 1
                else:
                    break
            out.append(render_list([tuple(x) for x in items], tokens))
            continue
        fb = re.match(r'^file-box\s+"(.+)"\s*$', s)
        if fb:
            flush()
            pending_title = fb.group(1)
            i += 1
            continue
        if not s:
            flush()
        else:
            para.append(ln)
        i += 1
    flush()
    return "".join(out)


def split_diagram(text):
    """도식: 첫 목록·표·펜스 앞 설명 문장(노트로)과 실제 그릴 내용으로 나눈다."""
    lines = text.split("\n")
    for k, ln in enumerate(lines):
        s = ln.strip()
        if LIST_RE.match(ln) or s.startswith("|") or s.startswith("```"):
            return "\n".join(lines[:k]).strip(), "\n".join(lines[k:])
    return text.strip(), ""


# ----------------------------------------------------------------- 슬라이드
def module_of(n):
    for a, b, code, name in MODULES:
        if a <= n <= b:
            return code, name
    return "", ""


def parse_type(raw):
    raw = raw.strip()
    word = re.match(r"(개념|실습|점검|정리|데모)", raw)
    base = word.group(1) if word else "개념"
    rest = raw[len(base):]
    tags = []
    if base == "데모":
        base = "개념"
        tags.append("강사 시연")
    for part in re.split(r"·", rest):
        part = re.sub(r"[`*()]", "", part).strip()
        for sub in [p.strip() for p in part.split(",")]:
            if sub and sub not in tags and sub != "강사 시연":
                tags.append(sub)
    tags = [t for t in tags if t]
    return base, tags


def minutes_of(note):
    ms = re.findall(r"\((\d+(?:\.\d+)?)분", note)
    return float(ms[-1]) if ms else 0


# =====================================================================
# 발표용 렌더 층 (디자인 v2)
# 위의 파서·인라인·블록 함수(parse_file, field_text, inline, render_*, split_diagram,
# module_of, parse_type, minutes_of)는 교재판(build_handout.py)과 공용이다. 동작을 바꾸지 않는다.
# 아래는 발표용 덱에서만 쓰는 층이다: 슬라이드 조각 추출 -> 레이아웃 템플릿 선택 -> 도식(인라인 SVG).
# =====================================================================
CURRICULUM = SRC / "01_designer_curriculum.md"
TRACK_OF = {"M1": "t1", "M2": "t1", "M3": "t1", "M4": "t2", "M5": "t2",
            "M6": "fb", "M7": "t2", "MW": "wrap"}
TRACK_LABEL = {"t1": "Track 1 · Claude Code 기본", "t2": "Track 2 · 하네스 엔지니어링",
               "fb": "Firebase 기능 지도", "wrap": "마무리"}
SHORT = {"M1": "첫 대화", "M2": "프롬프트", "M3": "CLAUDE.md·스킬", "M4": "하네스 입문",
         "M5": "하네스 파일 고치기", "M6": "Firebase 지도",
         "M7": "수업 패키지 프로젝트", "MW": "마무리"}
BREAK_SLIDE = 33
OPENERS = {7, 12, 20, 26, 34, 53, 65}  # 모듈 첫 슬라이드(M1은 표지가 대신한다)
KIND_GLYPH = {"개념": "개념", "실습": "실습", "점검": "점검", "정리": "정리"}


# 설계서(수정하지 않음)의 M4·M5·M7 목표는 옛 구성 기준이라, 새 원고 구성에 맞춘 목표로 덮어쓴다.
GOALS_NEW = {
    "M3": "CLAUDE.md로 반복 규칙을 남기고, 나만의 스킬(/quiz)을 만들어 재사용할 수 있다.",
    "M4": "하네스(revfactory/harness) 플러그인을 설치하고, 말로 요청해 '만드는 쪽 + 검수하는 쪽' 팀을 만들어 실행할 수 있다.",
    "M5": "하네스가 만든 `.claude/` 파일을 열어 읽고, 말로 고쳐 다시 실행해 결과를 비교할 수 있다.",
    "M6": "Firebase 6개 항목을 언제 쓰는지 고르고, 콘솔에서 인증과 데이터베이스를 직접 설정할 수 있다. 접근 규칙은 Claude Code가 만든다.",
    "M7": "자기 교과 단원의 명세를 쓰고 하네스로 수업 슬라이드와 학생 워크북 웹앱을 만들어 Firebase Hosting 주소로 확인할 수 있다.",
}


def load_goals_deck():
    goals = {}
    if not CURRICULUM.exists():
        return goals
    for ln in CURRICULUM.read_text(encoding="utf-8").split("\n"):
        if re.match(r"^\|\s*M\d", ln):
            c = [x.strip() for x in ln.strip().strip("|").split("|")]
            if len(c) >= 8:
                goals[c[0]] = c[6]
    return goals


def pieces(s):
    """원고 한 장을 발표용 조각으로. 처리 규칙은 이전 조립기(v1)와 같다."""
    n = s["n"]
    kind, tags = parse_type(field_text(s, "유형"))
    raw_note = field_text(s, "노트")
    mins = minutes_of(raw_note)
    s["min"] = mins
    body_tokens, note_tokens = [], []
    body_raw = field_text(s, "본문")
    diag_raw = field_text(s, "도식")
    prompt_raw = field_text(s, "프롬프트")
    result_raw = field_text(s, "예상 결과")
    stuck_raw = field_text(s, "막힐 때")
    if "콘솔 직접 조작" in "\n".join(s["f"].get("프롬프트", [])):
        tags.append("콘솔 직접 조작")
    diag_intro, diag_rest = split_diagram(diag_raw) if diag_raw else ("", "")
    if "☐" in body_raw:
        out_l = []
        for l in body_raw.split("\n"):
            if l.count("☐") > 1:
                ind = l[: len(l) - len(l.lstrip())]
                out_l += [ind + "- ☐ " + x.strip() for x in re.split(r"\s*·?\s*☐\s*", l.lstrip("- ").strip()) if x.strip()]
            else:
                out_l.append(l)
        body_raw = "\n".join(out_l)
    # 목록 기호가 없는 본문은 줄마다 문단으로 나눈다(발표용 표시만; 문장은 그대로)
    if body_raw and not re.search(r"^\s*([-*]|\d+\.)\s", body_raw, re.M) and "|" not in body_raw and "```" not in body_raw:
        body_disp = "\n\n".join(l for l in body_raw.split("\n") if l.strip())
    else:
        body_disp = body_raw
    body_html = render_blocks(body_disp, body_tokens)
    diag_rest = re.sub(r"^(\s*[-*]\s+)(?:표\(원본 그대로\):?|`\.(?:flow|steps|grid2)`[^:\n]{0,20}:)\s*", r"\1", diag_rest, flags=re.M)
    diag_html = render_blocks(diag_rest, body_tokens) if diag_rest else ""
    prompt_html = render_blocks(prompt_raw, body_tokens, "prompt") if prompt_raw else ""
    result_html = render_blocks(result_raw, body_tokens, "result") if result_raw else ""
    stuck_html = render_blocks(stuck_raw, body_tokens) if stuck_raw else ""
    if stuck_raw and not re.search(r"^\s*[-*]\s", stuck_raw, re.M) and re.search(r"\(2\)", stuck_raw):
        parts = [p.strip() for p in re.split(r"(?:^|\s)\(\d\)\s*", stuck_raw) if p.strip()]
        stuck_html = "<ul>" + "".join("<li>%s</li>" % inline(p, body_tokens) for p in parts) + "</ul>"
    note_html = render_blocks(raw_note, note_tokens)
    extra = ""
    if diag_intro:
        extra += '<div class="nx"><b>도식 설명(강사용)</b> %s</div>' % inline(diag_intro.replace("\n", " "), note_tokens)
    if body_tokens:
        items = "".join("<li>%s</li>" % html.escape(t or "상세 없음") for t in body_tokens)
        extra += '<div class="nx"><b>이 슬라이드의 확인 필요 항목</b><ul>%s</ul></div>' % items
    if stuck_html:
        extra += '<div class="nx"><b>막힐 때</b>%s</div>' % stuck_html
    return {
        "n": n, "kind": kind, "tags": tags, "mins": mins,
        "body_raw": body_raw, "diag_raw": diag_raw, "diag_intro": diag_intro, "diag_rest": diag_rest,
        "prompt_raw": prompt_raw, "result_raw": result_raw, "stuck_raw": stuck_raw,
        "body": decorate(body_html), "diag": decorate(diag_html), "prompt": decorate(prompt_html),
        "result": decorate(result_html), "stuck": decorate(stuck_html),
        "note": note_html + extra, "has_check": bool(body_tokens or note_tokens), "tokens": body_tokens,
    }


# ----------------------------------------------------------------- 발표용 장식(코드 구문 대비 등)
def _syn_line(ln, kind):
    if kind == "md":
        if re.fullmatch(r"-{3}", ln.strip()):
            return '<span class="sy-fm">%s</span>' % ln
        m = re.match(r"^(\s*)([A-Za-z][\w-]*)(:)(.*)$", ln)
        if m:
            return '%s<span class="sy-key">%s</span>%s%s' % m.groups()
        if re.match(r"^#{1,3} ", ln):
            return '<span class="sy-head">%s</span>' % ln
        return ln
    if kind == "json":
        ln = re.sub(r"(&quot;|\")([\w-]+)(&quot;|\")(\s*:)", r'<span class="sy-key">\1\2\3</span>\4', ln)
        return ln
    if kind == "rules":
        ln = re.sub(r"\b(rules_version|service|match|allow|if)\b", r'<span class="sy-key">\1</span>', ln)
        return ln
    return ln


def syntax(code_inner, kind):
    return "\n".join(_syn_line(l, kind) for l in code_inner.split("\n"))


def decorate(h):
    """render_blocks 결과를 발표용으로 다듬는다(교재판과 무관한 표시 층)."""
    if not h:
        return h

    # 경로 한 줄로 시작하는 터미널 블록 -> 파일 상자
    def term_to_file(m):
        body = m.group(1)
        first, _, rest = body.partition("\n")
        if re.fullmatch(r"[.\w/-]+\.(json|md|py|rules|draft)", first.strip()):
            return ('<div class="file-box"><div class="fb-title">%s</div><button class="copy" type="button">복사</button>'
                    "<pre><code>%s</code></pre></div>" % (first.strip(), rest))
        return m.group(0)
    h = re.sub(r'<div class="terminal"><pre><code>(.*?)</code></pre></div>', term_to_file, h, flags=re.S)

    def fb(m):
        title, code = m.group(1), m.group(2)
        kind = "md"
        if title.endswith(".json"):
            kind = "json"
        return m.group(0).replace("<code>%s</code>" % code, "<code>%s</code>" % syntax(code, kind))
    h = re.sub(r'<div class="file-box"><div class="fb-title">(.*?)</div><button class="copy" type="button">복사</button><pre><code>(.*?)</code></pre></div>', fb, h, flags=re.S)

    def rules(m):
        code = m.group(1)
        if "rules_version" in code or "service cloud.firestore" in code:
            return m.group(0).replace("<code>%s</code>" % code, "<code>%s</code>" % syntax(code, "rules"))
        return m.group(0)
    h = re.sub(r'<div class="code-block"><pre><code>(.*?)</code></pre></div>', rules, h, flags=re.S)
    # 코드 블록에도 복사 버튼(복사 대상은 첫 code)
    h = h.replace('<div class="code-block"><pre>', '<div class="code-block"><button class="copy" type="button">복사</button><pre>')
    return h


# ----------------------------------------------------------------- 공용 조각
def esc(t):
    return html.escape(t, quote=False)


def lbl(text, cls=""):
    return '<div class="lbl %s">%s</div>' % (cls, text)


def chk_badge():
    return '<span class="chk hd-chk" title="이 슬라이드(본문 또는 노트)에 원고의 [확인필요]가 남아 있습니다">확인 필요</span>'


def has_fence(h):
    return any(c in h for c in ('class="prompt-box"', 'class="file-box"', 'class="terminal"', 'class="code-block"'))


def code_len(raw):
    return sum(len(b) for b in re.findall(r"```(.*?)```", raw, re.S))


def li_texts(raw):
    """원고 목록의 최상위 항목 문장(인라인 문법 그대로)."""
    out = []
    for ln in raw.split("\n"):
        m = re.match(r"^([-*]|\d+\.)\s+(.*)$", ln)
        if m:
            out.append(m.group(2).strip())
        elif ln.startswith(" ") and out and ln.strip():
            out[-1] += " " + ln.strip()
    return out


def steps_html(raw, tokens):
    """본문 목록을 실습 단계 타임라인으로. 문장에 번호가 이미 있으면 그대로 쓴다."""
    lines = [l for l in raw.split("\n") if l.strip()]
    items, asides = [], []
    if re.search(r"^\s*([-*]|\d+\.)\s", raw, re.M):
        for t in li_texts(raw):
            items.append(t)
    else:
        for l in lines:
            (asides if l.strip().startswith("(") else items).append(l.strip())
    out = []
    for i, t in enumerate(items, 1):
        m = re.match(r"^(?:(\d+)\.\s+|([①②③④⑤⑥⑦⑧⑨])\s*|(\d)단계:\s*)(.*)$", t)
        num, txt = str(i), t
        if m:
            num = m.group(1) or m.group(3) or str("①②③④⑤⑥⑦⑧⑨".index(m.group(2)) + 1)
            txt = m.group(4)
        out.append('<li><span class="sn">%s</span><div class="st">%s</div></li>' % (num, inline(txt, tokens)))
    h = '<ol class="tl">%s</ol>' % "".join(out)
    if asides:
        h += "".join('<p class="aside">%s</p>' % inline(a, tokens) for a in asides)
    return h


def band(result=None, stuck=None, cls=""):
    cells = []
    if result:
        cells.append('<div class="cell res ovc">%s<div class="cb">%s</div></div>' % (lbl("예상 결과", "l-res"), result))
    if stuck:
        cells.append('<div class="cell stk ovc">%s<div class="cb">%s</div></div>' % (lbl("막힐 때", "l-stk"), stuck))
    if not cells:
        return ""
    return '<div class="band %s n%d">%s</div>' % (cls, len(cells), "".join(cells))


# ----------------------------------------------------------------- 레이아웃 템플릿
def L_statement(p):
    """개념·정리: 글머리만 있는 슬라이드. 큰 타이포 + 선 구분, 세로 가운데."""
    return '<div class="body stmt ovc"><div class="col ovc">%s</div></div>' % p["body"]


def L_summary(p):
    """정리: 핵심 항목을 번호와 큰 글자로."""
    return '<div class="body summ ovc"><div class="col ovc">%s</div></div>' % p["body"]


def L_question(p, visual=""):
    side = '<div class="col q-side ovc">%s</div>' % visual if visual else ""
    return '<div class="body quest ovc %s"><div class="col q-main ovc"><div class="qmark" aria-hidden="true">?</div>%s</div>%s</div>' % (
        "has-side" if visual else "", p["body"], side)


def L_split(p, visual, ratio="r46", left=None):
    return '<div class="body split %s ovc"><div class="col ovc">%s</div><div class="col vis ovc">%s</div></div>' % (
        ratio, left if left is not None else p["body"], visual)


def L_stack(p, visual):
    return '<div class="body stack ovc"><div class="lead ovc">%s</div><div class="vis ovc">%s</div></div>' % (p["body"], visual)


def density(p):
    prose = len(BOX_RE.sub("", p["result"])) if p["result"] else 0
    return 1.4 * code_len(p["prompt_raw"]) + code_len(p["result_raw"]) + 0.8 * (len(p["body_raw"]) + len(p["stuck_raw"]) + prose * 0.35)


def L_practice(p, left_extra="", main=None, result_in_main=None, steps=None):
    """실습: 왼쪽 단계 타임라인, 오른쪽 프롬프트·결과 화면.
    예상 결과 글(.resbox)과 막힐 때(.stkbox)는 .mov로 표시해, 화면에서 맞춤 계산(JS)이 덜 찬 열로 옮긴다.
    코드가 아주 많은 실습(heavy)은 왼쪽을 프롬프트 큰 열로, 오른쪽에 단계·결과 미리보기(2단)를 둔다."""
    st = steps if steps is not None else steps_html(p["body_raw"], [])
    if main is None:
        main = ""
        if p["prompt"]:
            main += '<div class="grp%s">%s</div>' % ("" if has_fence(p["prompt"]) else " prose", p["prompt"])
        if p["diag"]:
            main += '<div class="grp diag">%s</div>' % p["diag"]
    res_code = has_fence(p["result"]) if result_in_main is None else result_in_main
    res_prose, res_boxes = split_result(p["result"]) if res_code else (p["result"], "")
    if res_boxes.count("\n") > 18:
        res_boxes = res_boxes.replace('<div class="file-box">', '<div class="file-box cols2">', 1)
    resbox = ('<div class="resbox mov">%s%s</div>' % (lbl("예상 결과", "l-res"), res_prose)) if res_prose.strip() else ""
    stk = ('<div class="stkbox mov">%s%s</div>' % (lbl("막힐 때", "l-stk"), p["stuck"])) if p["stuck"] else ""
    if res_code and p["prompt"] and density(p) > 900:
        st = st.replace('<ol class="tl">', '<ol class="tl tl-c">')
        return ('<div class="body prac heavy ovc"><div class="col ovc">%s%s</div>'
                '<div class="col ovc"><div class="hst mov top">%s</div><div class="grp rescode">%s%s</div>%s</div></div>'
                % (main, stk, lbl("단계", "l-step") + st, lbl("예상 결과 · 파일 미리보기", "l-res"), res_boxes, resbox))
    right = main
    left = st + left_extra + resbox + stk
    if res_code and res_boxes:
        rc = "rescode" if res_boxes.count("\n") > 10 else "resshort"
        right += '<div class="grp %s">%s%s</div>' % (rc, lbl("예상 결과 · 화면", "l-res"), res_boxes)
    return ('<div class="body prac ovc"><div class="col steps ovc">%s%s</div><div class="col main ovc">%s</div></div>'
            % (lbl("단계", "l-step"), left, right))


BOX_RE = re.compile(r'<div class="(?:file-box|terminal|code-block)">.*?</code></pre></div>', re.S)


def split_result(h):
    boxes = BOX_RE.findall(h)
    prose = BOX_RE.sub("", h)
    return prose, "".join(boxes)


def L_table(p, table_html=None, after=""):
    return '<div class="body tbl ovc"><div class="lead ovc">%s</div><div class="tw ovc">%s</div>%s</div>' % (
        p["body"], table_html if table_html is not None else p["diag"], after)


def rail(code, mname, p, goal, mins_mod, rng):
    num = code[1:] if code.startswith("M") and code != "MW" else ""
    big = ('<span class="rk">M</span><span class="rn">%s</span>' % num) if num else '<span class="rn rw">%s</span>' % esc(mname)
    meta = '<dl><dt>시간</dt><dd>%s분</dd><dt>슬라이드</dt><dd>%s</dd></dl>' % (("%g" % mins_mod), rng)
    g = ('<div class="rg">%s<p>%s</p></div>' % (lbl("학습 목표"), inline(goal))) if goal and goal != "—" else ""
    return ('<aside class="rail"><div class="rlab">%s</div><div class="rbig">%s</div>%s%s%s</aside>'
            % ("모듈" if num else "MW", big, ('<div class="rname">%s</div>' % esc(mname)) if num else "", meta, g))


def default_layout(p):
    k = p["kind"]
    if k == "실습" or p["prompt"]:
        return L_practice(p)
    if k == "점검":
        return L_question(p, ('<div class="panel">%s</div>' % p["diag"]) if p["diag"] else ""), "", 36
    if p["diag"]:
        if p["diag"].startswith("<table") and p["diag"].count("<table") == 1:
            return L_table(p) + band(p["result"], p["stuck"])
        return L_split(p, '<div class="panel">%s</div>' % p["diag"]) + band(p["result"], p["stuck"])
    if p["result"] or p["stuck"]:
        return (L_summary(p) if k == "정리" else L_statement(p)) + band(p["result"], p["stuck"]), "", 34
    return (L_summary(p), "", 36) if k == "정리" else (L_statement(p), "", 36)


# ----------------------------------------------------------------- 슬라이드 한 장
GOALS = {}
MOD_MIN = {}


def footer(n, total, code):
    segs = []
    for a, b, c, _ in MODULES:
        cnt = b - a + 1
        if n > b:
            st, fill = "past", 100
        elif n < a:
            st, fill = "fut", 0
        else:
            st, fill = "cur", (n - a + 1) / cnt * 100
        segs.append('<i class="%s" style="flex:%d"><b style="width:%.1f%%"></b></i>' % (st, cnt, fill))
    return ('<footer class="ft"><span class="ft-tr">%s</span><span class="ft-bar">%s</span>'
            '<span class="ft-num"><b>%d</b> / %d</span></footer>' % (TRACK_LABEL[TRACK_OF[code]], "".join(segs), n, total))


TABLE_RE = re.compile(r"<table>(.*?)</table>", re.S)


def mark_nowrap_tables(h):
    """셀 글이 짧은 표는 줄바꿈을 막는다(괄호 하나 때문에 첫 열이 꺾이는 것 방지).
    모든 셀이 짧으면 표 전체(nw), 첫 열만 짧으면 첫 열(nw1)에 적용한다. 자리가 모자라면 JS 맞춤이 글자를 줄인다."""
    def one(m):
        rows = re.findall(r"<tr>(.*?)</tr>", m.group(1), re.S)
        cells = [re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", r, re.S) for r in rows]
        txt = [[html.unescape(re.sub(r"<[^>]+>", "", c)).strip() for c in r] for r in cells if r]
        if not txt:
            return m.group(0)
        first = max(len(r[0]) for r in txt)
        allmax = max(len(c) for r in txt for c in r)
        if allmax <= 30:
            return '<table class="nw">' + m.group(1) + "</table>"
        if first <= 26:
            return '<table class="nw1">' + m.group(1) + "</table>"
        return m.group(0)
    return TABLE_RE.sub(one, h)


def build_slide(s, total):
    n = s["n"]
    code, mname = module_of(n)
    p = pieces(s)
    p["code"], p["mname"], p["title"] = code, mname, s["title"]
    kind = p["kind"]
    custom = OVERRIDES.get(n)
    res = custom(p) if custom else default_layout(p)
    layout, fsmax = "", 32
    if isinstance(res, tuple):
        res = tuple(res)
        layout = res[1] if len(res) > 1 else ""
        fsmax = res[2] if len(res) > 2 else 32
        res = res[0]
    inner = mark_nowrap_tables(res)
    tags = "".join('<span class="tag">%s</span>' % esc(t) for t in p["tags"])
    if p["has_check"]:
        tags += chk_badge()
    hd = ('<header class="hd"><span class="hd-mod"><b>%s</b>%s</span><span class="hd-meta">'
          '<span class="kind k-%s">%s</span>%s</span></header>' % (code, esc(mname), kind, kind, tags))
    opener = n in OPENERS
    rl = ""
    if opener:
        a, b = [(x[0], x[1]) for x in MODULES if x[2] == code][0]
        rl = rail(code, mname, p, GOALS.get(code, ""), MOD_MIN.get(code, 0), "%d–%d" % (a, b))
    cls = "slide k-%s%s%s" % (kind, " opener" if opener else "", (" " + layout) if layout else "")
    note = '<div class="nmeta">슬라이드 %d · %s · 소요 %s분</div>%s' % (n, esc(code + " " + mname), ("%g" % p["mins"]) if p["mins"] else "-", p["note"])
    return (
        '<section class="%s" id="s%d" data-n="%d" data-kind="%s" data-min="%g" data-module="%s" data-track="%s" data-fsmax="%d">'
        '%s%s<h2 class="title">%s</h2>%s%s<div class="notes">%s</div></section>'
        % (cls, n, n, kind, p["mins"], code, TRACK_OF[code], fsmax, rl, hd, inline(s["title"]), inner,
           footer(n, total, code), note)
    )


# ----------------------------------------------------------------- 도식 도구(인라인 SVG)
def tw(s, fs):
    """글자 폭 추정(시스템 한글 고딕 기준). 상자 크기 계산용."""
    w = 0.0
    for ch in s:
        o = ord(ch)
        if 0xAC00 <= o <= 0xD7A3 or 0x3130 <= o <= 0x318F:
            w += 0.92
        elif ch == " ":
            w += 0.27
        elif ch in ".,:;·'\"()[]{}|!`":
            w += 0.3
        elif ch in "-_/~=+<>*":
            w += 0.5
        elif ch.isupper():
            w += 0.66
        elif ch.isdigit():
            w += 0.58
        elif o < 128:
            w += 0.55
        else:
            w += 0.95
    return w * fs


def x(t):
    return html.escape(t, quote=True)


class D:
    """좌표를 직접 정하는 작은 SVG 작성기. viewBox 너비 = 화면 배치 너비로 잡아 글자 크기가 그대로 나온다."""

    def __init__(self, w, h, label="", cls=""):
        self.w, self.h, self.label, self.cls = w, h, label, cls
        self.e = []

    def add(self, s):
        self.e.append(s)
        return self

    def rect(self, x0, y0, w, h, cls="n", rx=6):
        return self.add('<rect x="%g" y="%g" width="%g" height="%g" rx="%g" class="%s"/>' % (x0, y0, w, h, rx, cls))

    def circle(self, cx, cy, r, cls="n"):
        return self.add('<circle cx="%g" cy="%g" r="%g" class="%s"/>' % (cx, cy, r, cls))

    def text(self, x0, y0, s, fs=22, cls="", anchor="middle", lh=1.28, raw=False):
        """y0 = 글 덩어리의 세로 가운데. 줄바꿈은 \\n."""
        lines = s.split("\n")
        n = len(lines)
        out = []
        for i, ln in enumerate(lines):
            yy = y0 + (i - (n - 1) / 2.0) * fs * lh
            out.append('<text x="%g" y="%g" font-size="%g" text-anchor="%s" dominant-baseline="central" class="%s">%s</text>'
                       % (x0, yy, fs, anchor, cls, ln if raw else x(ln)))
        return self.add("".join(out))

    def node(self, x0, y0, w, h, s, cls="n", fs=22, tcls="m", sub=None, sfs=20, scls="t3", rx=6):
        self.rect(x0, y0, w, h, cls, rx)
        if sub:
            nl = s.count("\n") + 1
            sl = sub.count("\n") + 1
            tot = nl * fs * 1.25 + sl * sfs * 1.25 + 4
            top = y0 + h / 2.0 - tot / 2.0
            self.text(x0 + w / 2.0, top + nl * fs * 1.25 / 2.0, s, fs, tcls, lh=1.25)
            self.text(x0 + w / 2.0, top + nl * fs * 1.25 + 4 + sl * sfs * 1.25 / 2.0, sub, sfs, scls, lh=1.25)
        else:
            self.text(x0 + w / 2.0, y0 + h / 2.0, s, fs, tcls, lh=1.25)
        return self

    def line(self, pts, cls="ln", head="ink", dash=False):
        d = "M" + " L".join("%g %g" % p for p in pts)
        mk = (' marker-end="url(#ah-%s)"' % head) if head else ""
        return self.add('<path d="%s" class="%s"%s/>' % (d, cls, mk))

    def path(self, d, cls="ln", head="ink"):
        mk = (' marker-end="url(#ah-%s)"' % head) if head else ""
        return self.add('<path d="%s" class="%s"%s/>' % (d, cls, mk))

    def arrow(self, x1, y1, x2, y2, cls="ln", head="ink", label=None, fs=20, lcls="t3", ldx=0, ldy=-16, anchor="middle"):
        self.line([(x1, y1), (x2, y2)], cls, head)
        if label:
            self.text((x1 + x2) / 2.0 + ldx, (y1 + y2) / 2.0 + ldy, label, fs, lcls, anchor=anchor)
        return self

    def svg(self, style=""):
        return ('<svg class="dg %s" viewBox="0 0 %g %g" role="img" aria-label="%s"%s>%s</svg>'
                % (self.cls, self.w, self.h, x(self.label), (' style="%s"' % style) if style else "", "".join(self.e)))


def box_w(s, fs, pad=22, minw=0):
    return max(minw, max(tw(l, fs) for l in s.split("\n")) + 2 * pad)


def hflow(d, x0, y, items, h=64, fs=22, gap=56, cls=None, labels=None, head="ink", lcls="ln", widths=None, tcls="m"):
    """가로 흐름: 상자 자동 폭 + 화살표. 반환: 상자 좌표 목록."""
    pos = []
    cx = x0
    for i, it in enumerate(items):
        w = widths[i] if widths else box_w(it, fs)
        c = cls[i] if isinstance(cls, (list, tuple)) else (cls or "n")
        tc = "tw b" if c in ("na", "ntf", "nk") else tcls
        d.node(cx, y, w, h, it, c, fs, tc)
        pos.append((cx, y, w, h))
        if i < len(items) - 1:
            lab = labels[i] if labels else None
            d.arrow(cx + w + 6, y + h / 2.0, cx + w + gap - 6, y + h / 2.0, lcls, head, lab)
        cx += w + gap
    return pos


def hflow_width(items, fs=22, gap=56, pad=22):
    return sum(box_w(i, fs, pad) for i in items) + gap * (len(items) - 1)


# 작은 상징(아이콘): 선 위주, 토큰 색
def ic_folder(x0, y0, s=40, cls="ln"):
    k = s / 40.0
    return ('<path class="%s" d="M%g %g h%g l%g %g h%g v%g h%g z" style="stroke-linejoin:round"/>'
            % (cls, x0 + 2 * k, y0 + 8 * k, 13 * k, 4 * k, 5 * k, 19 * k, 23 * k, -36 * k))


def ic_stamp(d, cx, cy, r=34, txt="승인"):
    d.circle(cx, cy, r, "naw")
    d.add('<circle cx="%g" cy="%g" r="%g" fill="none" stroke="var(--accent)" stroke-width="1.5"/>' % (cx, cy, r - 6))
    d.add('<g transform="rotate(-12 %g %g)">' % (cx, cy))
    d.text(cx, cy, txt, r * 0.56, "ta b")
    d.add("</g>")
    return d


def ic_person(d, cx, cy, s=1.0, cls="fi3"):
    d.add('<circle cx="%g" cy="%g" r="%g" class="%s"/>' % (cx, cy - 14 * s, 9 * s, cls))
    d.add('<path class="%s" d="M%g %g q%g %g %g 0 v%g h%g z"/>' % (cls, cx - 16 * s, cy + 20 * s, 16 * s, -34 * s, 32 * s, 0, -32 * s))
    return d


def ic_doc(d, x0, y0, w=44, h=54, cls="n"):
    f = 12
    d.add('<path class="%s" d="M%g %g h%g l%g %g v%g h%g z"/>' % (cls, x0, y0, w - f, f, f, h - f, -w))
    d.add('<path class="ln" style="stroke-width:1.5" d="M%g %g v%g h%g"/>' % (x0 + w - f, y0, f, f))
    return d


SVG_DEFS = (
    '<svg id="svgdefs" aria-hidden="true" focusable="false"><defs>'
    + "".join('<marker id="ah-%s" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="9" markerHeight="9" markerUnits="userSpaceOnUse" orient="auto-start-reverse">'
              '<path d="M0 0 L10 5 L0 10 z"/></marker>' % c for c in ("ink", "acc", "teal", "mute", "blue", "ochre", "paper"))
    + "</defs></svg>"
)


# ----------------------------------------------------------------- 스타일(디자인 토큰 -> 컴포넌트 -> 템플릿)
CSS = r"""
:root{
  /* 색: 종이·잉크(따뜻한 중립) */
  --paper:#f8f2e4; --paper-hi:#fcf8ef; --paper-2:#f2e9d5; --paper-3:#e8dcc2;
  --ink:#2a2314; --ink-2:#4b412d; --ink-3:#74664a; --ink-4:#a69576;
  --rule:#ddd0b4; --rule-2:#c6b48e;
  /* 색: 역할 */
  --accent:#b0402c; --accent-2:#8d3020; --accent-wash:#f3e0d4;
  --teal:#356e67; --teal-2:#285650; --teal-wash:#deeae4;
  --blue:#2f5f98; --blue-2:#244a77; --blue-wash:#e1e7ef;
  --ochre:#8a6420; --ochre-2:#6e4f17; --ochre-wash:#f1e4c4;
  --night:#231d14; --night-2:#2f271b; --night-rule:#4a3f2c; --on-night:#efe5cf; --on-night-2:#b3a483;
  --sy-key:#eaa283; --sy-head:#f0c987; --sy-fm:#8f8268; --sy-file:#9fd0c4;
  /* 글꼴: 시스템 한글 스택과 모노 스택만 */
  --font:"Apple SD Gothic Neo","Malgun Gothic","Noto Sans KR","Noto Sans CJK KR","Nanum Gothic","Segoe UI",system-ui,sans-serif;
  --mono:ui-monospace,"SF Mono",Menlo,Consolas,"D2Coding","Noto Sans Mono","Liberation Mono",monospace;
  /* 타입 스케일(무대 1280x720 기준 px) */
  --t-cover:86px; --t-chapter:150px; --t-title:46px; --t-lead:36px; --t-body:28px; --t-small:24px; --t-aux:21px; --t-label:15px;
  /* 간격 스케일 */
  --s1:4px; --s2:8px; --s3:12px; --s4:16px; --s5:24px; --s6:32px; --s7:48px; --s8:64px;
  --pad-x:64px; --rail:248px;
  /* 선·모서리 규칙: 상자는 거의 각지게, 선은 머리카락 선 + 강조 굵은 선 두 가지 */
  --r-s:3px; --r-m:6px; --r-l:10px;
  --hair:1px solid var(--rule); --rule-ink:2px solid var(--ink);
  --tone:var(--blue); --tone-2:var(--blue-2); --tone-wash:var(--blue-wash);
}
.slide[data-track="t1"]{--tone:var(--blue);--tone-2:var(--blue-2);--tone-wash:var(--blue-wash)}
.slide[data-track="t2"]{--tone:var(--teal);--tone-2:var(--teal-2);--tone-wash:var(--teal-wash)}
.slide[data-track="fb"]{--tone:var(--ochre);--tone-2:var(--ochre-2);--tone-wash:var(--ochre-wash)}
.slide[data-track="wrap"]{--tone:var(--accent);--tone-2:var(--accent-2);--tone-wash:var(--accent-wash)}
*{box-sizing:border-box}
html,body{margin:0;height:100%;background:#17130d;overflow:hidden;font-family:var(--font);color:var(--ink);
  -webkit-font-smoothing:antialiased;font-kerning:normal;word-break:keep-all;overflow-wrap:break-word}
#viewport{position:fixed;inset:0;display:flex;align-items:center;justify-content:center}
#stage{width:1280px;height:720px;position:relative;transform-origin:center center;flex:none;background:var(--paper);overflow:hidden;box-shadow:0 10px 50px rgba(0,0,0,.5)}

/* ---------- 슬라이드 뼈대 ---------- */
.slide{--fs:30px;--fp:24px;--fr:22px;--fk:22px;--ft:var(--t-title);
  position:absolute;inset:0;background:var(--paper);visibility:hidden;opacity:0;font-size:var(--fs);line-height:1.42;
  padding:0 var(--pad-x);display:flex;flex-direction:column;transition:opacity .18s ease,visibility 0s linear .18s}
.slide.on{visibility:visible;opacity:1;transition:opacity .18s ease}
@media (prefers-reduced-motion:reduce){.slide,.slide.on{transition:none}}
.hd{display:flex;align-items:center;justify-content:space-between;gap:var(--s4);height:56px;padding-top:20px;flex:none;
  font-size:var(--t-label);line-height:1;color:var(--ink-3);white-space:nowrap}
.hd-mod{font-weight:600;letter-spacing:.01em;display:flex;align-items:center;min-width:0;overflow:hidden;text-overflow:ellipsis}
.hd-mod b{display:inline-block;padding:4px 7px 3px;margin-right:10px;background:var(--tone);color:#fff;border-radius:var(--r-s);font-weight:800;letter-spacing:.04em;font-variant-numeric:tabular-nums}
.hd-meta{display:flex;align-items:center;gap:10px}
.kind{display:inline-flex;align-items:center;gap:6px;padding:4px 10px 3px;border-radius:var(--r-s);font-weight:800;letter-spacing:.06em;border:1.5px solid currentColor}
.kind:before{content:"";width:7px;height:7px;background:currentColor}
.k-개념.kind{color:var(--ink-2)}
.k-개념.kind:before{border-radius:50%}
.k-실습.kind{background:var(--accent);border-color:var(--accent);color:#fff}
.k-점검.kind{color:var(--ochre-2);background:var(--ochre-wash);border-color:var(--ochre)}
.k-점검.kind:before{transform:rotate(45deg);width:6px;height:6px}
.k-정리.kind{background:var(--ink);border-color:var(--ink);color:var(--paper)}
.tag{color:var(--ink-3);font-weight:600}
.tag:before{content:"·";margin-right:10px;color:var(--ink-4)}
.chk{display:inline-block;padding:.14em .5em .1em 1.25em;margin:0 .15em;position:relative;border-radius:var(--r-s);
  font:700 max(14px,.5em)/1.3 var(--font);letter-spacing:.02em;background:var(--ochre-wash);color:var(--ochre-2);
  box-shadow:inset 0 0 0 1px rgba(138,100,32,.38);vertical-align:.18em;white-space:nowrap}
.chk:before{content:"";position:absolute;left:.5em;top:50%;width:.42em;height:.42em;margin-top:-.21em;border-radius:50%;border:1.5px solid var(--ochre)}
.hd-chk{font-size:14px;vertical-align:baseline}
.title{margin:8px 0 0;font-size:var(--ft);line-height:1.16;font-weight:800;letter-spacing:-.028em;flex:none;color:var(--ink);text-wrap:balance;max-width:1100px}
.title code{font-size:.8em}
.body{flex:1;min-height:0;display:flex;gap:var(--s7);margin-top:24px;margin-bottom:var(--s4);overflow:hidden}
.col{min-width:0;min-height:0;overflow:hidden;display:flex;flex-direction:column;gap:var(--s3)}
.ft{flex:none;height:40px;display:flex;align-items:center;gap:var(--s5);font-size:13px;color:var(--ink-3);border-top:var(--hair);letter-spacing:.02em}
.ft-tr{font-weight:700;min-width:190px}
.ft-bar{flex:1;display:flex;gap:3px;height:4px}
.ft-bar i{position:relative;background:var(--paper-3);overflow:hidden}
.ft-bar i.past{background:var(--ink-4)}
.ft-bar i b{position:absolute;left:0;top:0;bottom:0;background:var(--tone)}
.ft-num{font-variant-numeric:tabular-nums;min-width:56px;text-align:right}
.ft-num b{color:var(--ink);font-weight:800}
.slide>*{position:relative;z-index:1}
.notes{display:none}

/* ---------- 본문 타이포 ---------- */
p{margin:0}
strong{font-weight:800;color:var(--ink);background:linear-gradient(transparent 64%,var(--tone-wash) 64%)}
ul,ol{margin:0;padding:0;list-style:none}
li{position:relative;padding-left:1.05em;margin:.18em 0}
ul>li:before{content:"";position:absolute;left:.08em;top:.6em;width:.3em;height:.3em;background:var(--tone)}
ol{counter-reset:c}
ol>li{counter-increment:c;padding-left:1.6em}
ol>li:before{content:counter(c);position:absolute;left:0;top:.08em;width:1.22em;height:1.22em;border-radius:50%;
  border:2px solid var(--tone);color:var(--tone-2);font-size:.74em;font-weight:800;text-align:center;line-height:1.08em;font-variant-numeric:tabular-nums}
li ul,li ol{font-size:.86em;margin-top:.15em}
li li:before{background:var(--ink-4)}
code{font-family:var(--mono);font-size:.86em;background:var(--paper-3);padding:.04em .32em;border-radius:var(--r-s);color:var(--accent-2);
  word-break:normal;overflow-wrap:anywhere;font-variant-ligatures:none;font-feature-settings:"liga" 0,"calt" 0}
pre{margin:0;white-space:pre-wrap;word-break:normal;overflow-wrap:anywhere;font-family:var(--mono);font-variant-ligatures:none;font-feature-settings:"liga" 0,"calt" 0}
pre code{background:none;padding:0;color:inherit;font-size:inherit;border-radius:0}
.lbl{display:flex;align-items:center;gap:8px;font-size:14px;font-weight:800;letter-spacing:.1em;color:var(--ink-3);margin:0 0 var(--s2);line-height:1.2}
.lbl:before{content:"";width:9px;height:9px;background:currentColor}
.l-res{color:var(--teal)} .l-stk{color:var(--accent)} .l-in{color:var(--accent)} .l-step{color:var(--ink-3)}
.aside{font-size:.8em;color:var(--ink-3);margin-top:var(--s3)}
.ph{display:inline-flex;align-items:center;gap:.5em;padding:.35em .9em;border:1.5px dashed var(--ink-4);border-radius:var(--r-m);
  color:var(--ink-3);font-size:max(20px,.72em);font-weight:700;line-height:1.3;
  background:repeating-linear-gradient(135deg,transparent 0 9px,rgba(166,149,118,.12) 9px 18px)}
li:has(>.ph:only-child){padding-left:0}
li:has(>.ph:only-child):before{display:none}

/* ---------- 코드·프롬프트 패널 ---------- */
.prompt-box,.file-box,.terminal,.code-block{position:relative;background:var(--night);color:var(--on-night);border-radius:var(--r-m);
  padding:42px 20px 16px;font-size:var(--fp);line-height:1.46;margin:0 0 var(--s3)}
.prompt-box:before,.terminal:before,.code-block:before{position:absolute;left:20px;top:13px;font:800 13px/1 var(--font);letter-spacing:.12em;color:var(--on-night-2)}
.prompt-box:before{content:"입력";color:#f0a58c}
.terminal:before{content:"화면 예시"}
.code-block:before{content:"코드"}
.prompt-box:after,.file-box:after,.terminal:after,.code-block:after{content:"";position:absolute;left:0;right:0;top:34px;border-top:1px solid var(--night-rule)}
.prompt-box{box-shadow:inset 4px 0 0 var(--accent)}
.file-box{box-shadow:inset 4px 0 0 var(--teal)}
.file-box .fb-title{position:absolute;left:20px;top:11px;right:90px;font:700 14px/1.2 var(--mono);color:var(--sy-file);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.terminal pre{color:#d8ecd0}
.sy-key{color:var(--sy-key)} .sy-head{color:var(--sy-head);font-weight:700} .sy-fm{color:var(--sy-fm)}
.copy{position:absolute;top:7px;right:10px;font:700 13px/1 var(--font);padding:5px 11px;border-radius:var(--r-s);border:1px solid var(--night-rule);
  background:transparent;color:var(--on-night-2);cursor:pointer;letter-spacing:.06em}
.copy:hover{color:var(--on-night);border-color:var(--on-night-2)}
.copy.done{background:var(--teal);border-color:var(--teal);color:#fff}
.copy:focus-visible,.tile:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
.rescode .prompt-box,.rescode .file-box,.rescode .terminal,.rescode .code-block{font-size:var(--fr)}
.grp>p{font-size:.78em;color:var(--ink-3);margin:0 0 var(--s2)}
.grp.prose>p{font-size:.9em;color:var(--ink-2)}
.grp.prose>ol,.grp.prose>ul{font-size:1em}
.grp.prose>ol>li{margin:.15em 0 .45em}
.grp>ul,.grp>ol{font-size:.82em;margin-bottom:var(--s2)}
.flowline{display:inline-flex;flex-wrap:wrap;align-items:center;gap:.2em;vertical-align:baseline}
.chip{display:inline-block;padding:0 .45em;border:1.5px solid var(--tone);background:var(--tone-wash);border-radius:var(--r-s);font-size:.9em}
.arr{color:var(--accent);font-weight:800;margin:0 .1em}

/* ---------- 표 ---------- */
table{border-collapse:collapse;width:100%;font-size:.86em;line-height:1.32;font-variant-numeric:tabular-nums}
th{text-align:left;font-size:.84em;font-weight:800;letter-spacing:.04em;color:var(--ink-3);padding:.3em .6em .4em;border-bottom:var(--rule-ink);vertical-align:bottom}
td{padding:.42em .6em;border-bottom:var(--hair);vertical-align:top}
td:first-child{font-weight:700}
tbody tr:last-child td{border-bottom:1.5px solid var(--ink-3)}
td code{font-size:.82em;white-space:nowrap;word-break:normal}
table.nw th,table.nw td{white-space:nowrap}
table.nw1 th:first-child,table.nw1 td:first-child{white-space:nowrap}
.ptbl table.nw,.ptbl table.nw1{table-layout:auto}
.ptbl table.nw th:first-child,.ptbl table.nw td:first-child,.ptbl table.nw1 th:first-child,.ptbl table.nw1 td:first-child{width:auto}

/* ---------- 아래 띠: 예상 결과 · 막힐 때 ---------- */
.band{flex:none;display:grid;grid-template-columns:1fr 1.35fr;gap:0 var(--s7);border-top:1.5px solid var(--ink);padding-top:var(--s3);margin-bottom:var(--s3);
  font-size:var(--fk);line-height:1.4;max-height:250px}
.band.n1{grid-template-columns:1fr}
.cell{min-width:0;overflow:hidden}
.cell p{margin:0 0 .2em}
.band.n1 .stk ul{display:grid;grid-template-columns:1fr 1fr;gap:0 var(--s7)}
.band.n1 .stk ul:has(>li:only-child){display:block}
.cell li{margin:.1em 0}
.stk li:before{background:var(--accent)}
.res li:before{background:var(--teal)}
.nostuck .cell.stk,.nostuck .stkbox{display:none}
.nostuck .band.n2{grid-template-columns:1fr}
.nostuck .band.n1{display:none}

/* ---------- 템플릿: 진술(개념) ---------- */
.stmt .col{flex:1;justify-content:safe center;gap:0}
.stmt ul{counter-reset:k}
.stmt .col>ul>li,.stmt .col>ol>li{counter-increment:k;padding:.5em 0 .52em 2.1em;margin:0;border-top:var(--hair);font-weight:500}
.stmt .col>ul>li:first-child,.stmt .col>ol>li:first-child{border-top:var(--rule-ink)}
.stmt .col>ul>li:last-child,.stmt .col>ol>li:last-child{border-bottom:var(--hair)}
.stmt .col>ul>li:before,.stmt .col>ol>li:before{content:counter(k,decimal-leading-zero);left:0;top:.82em;width:auto;height:auto;background:none;border:0;border-radius:0;
  font-size:.56em;font-weight:800;color:var(--tone);letter-spacing:.04em;line-height:1;font-variant-numeric:tabular-nums}
.stmt .col>p{color:var(--ink-2);margin:.3em 0}
.stmt .col>p:first-child{font-size:1.24em;font-weight:800;color:var(--ink);letter-spacing:-.02em;line-height:1.28;margin-bottom:.5em}

/* ---------- 템플릿: 정리 ---------- */
.summ .col{flex:1;justify-content:safe center;gap:0}
.summ .col>ul{counter-reset:k;display:flex;flex-direction:column}
.summ .col>ul>li{counter-increment:k;position:relative;padding:.42em 0 .42em 2.1em;margin:0;border-top:var(--hair);font-weight:600;letter-spacing:-.01em}
.summ .col>ul>li:first-child{border-top:var(--rule-ink)}
.summ .col>ul>li:before{content:counter(k);position:absolute;left:0;top:.3em;width:auto;height:auto;background:none;font-size:1.3em;font-weight:800;color:var(--tone);line-height:1;font-variant-numeric:tabular-nums;letter-spacing:-.03em}
.summ .col>ul>li>ul{font-weight:500}
.summ .col>p{margin:.2em 0}
.summ .col>p:first-child{font-size:1.2em;font-weight:800;letter-spacing:-.02em}

/* ---------- 템플릿: 질문(점검) ---------- */
.quest{position:relative}
.quest .q-main{flex:1;justify-content:safe center;position:relative;border-left:6px solid var(--ochre);padding-left:28px}
.quest.has-side .q-main{flex:0 0 44%}
.quest .q-side{flex:1;justify-content:safe center}
.qmark{display:none;position:absolute;right:-.06em;top:50%;transform:translateY(-54%);font-size:330px;line-height:1;font-weight:800;color:var(--ochre-wash);z-index:-1;letter-spacing:-.05em}
.quest.has-side .qmark{right:auto;left:-.04em;opacity:.8}
.quest .q-main>ul>li:first-child,.quest .q-main>p:first-of-type{font-size:1.28em;font-weight:800;letter-spacing:-.025em;line-height:1.3;padding-left:0;margin-bottom:.55em}
.quest .q-main>ul>li:first-child:before{display:none}
.quest .q-main>ul>li{color:var(--ink-2)}
.quest .q-main>ul>li:before{background:var(--ochre)}

/* ---------- 템플릿: 분할(서술 + 시각물) ---------- */
.split>.col:first-child{flex:0 0 38%;justify-content:safe center}
.split.r30>.col:first-child{flex:0 0 31%}
.split.r50>.col:first-child{flex:0 0 47%}
.split>.vis{flex:1;justify-content:safe center}
.split>.col:first-child>ul>li{margin:.1em 0 .55em}
.split>.col:first-child>p:first-child{font-size:1.14em;font-weight:800;letter-spacing:-.02em;line-height:1.3;margin-bottom:.4em}
.split>.col:first-child>p+p{color:var(--ink-2);margin-top:.35em}
.panel{border-top:var(--rule-ink);padding-top:var(--s4);font-size:.9em}
.panel>ul>li,.panel>ol>li{margin:.1em 0 .45em}
.panel>p{margin:.3em 0}
.panel table{font-size:.92em}
.panel>*+table,.panel>table+*{margin-top:var(--s4)}
.stack{flex-direction:column;gap:var(--s5)}
.stack>.lead{flex:none}
.stack>.vis{flex:1;min-height:0;display:flex;flex-direction:column;justify-content:safe center}
.stack>.lead>p:first-child{font-size:1.1em;font-weight:800;letter-spacing:-.02em}
.stack>.lead>p.sub2{font-size:.86em;color:var(--ink-3);font-weight:600;margin-top:.3em}

/* ---------- 템플릿: 실습 ---------- */
.prac>.col.steps{flex:0 0 37%}
.prac>.col.main{flex:1}
.tl{counter-reset:none;display:flex;flex-direction:column;gap:0}
.tl>li{display:grid;grid-template-columns:1.55em 1fr;gap:0 .55em;padding:0 0 .7em;margin:0;position:relative}
.tl>li:before{content:"";position:absolute;left:.72em;top:1.3em;bottom:.1em;width:2px;background:var(--rule);border:0;border-radius:0;height:auto}
.tl>li:last-child:before{display:none}
.tl .sn{width:1.36em;height:1.36em;border-radius:50%;background:var(--accent);color:#fff;font-size:.82em;font-weight:800;display:flex;align-items:center;justify-content:center;margin-top:.12em;font-variant-numeric:tabular-nums}
.tl .st{min-width:0}
.tl .st>ul{font-size:.86em}
.tl-h{flex-direction:row;gap:var(--s6)}
.tl-h>li{flex:1;padding:0}
.tl-h>li:before{display:none}
.prac.heavy{gap:var(--s6)}
.prac.heavy>.col:first-child{flex:0 0 51%}
.prac.heavy>.col:last-child{flex:1}
.prac.heavy .prompt-box{flex:none}
.tl-c>li{padding-bottom:.35em}
.heavy .rescode .cols2 pre{column-count:2;column-gap:28px;column-rule:1px solid var(--night-rule)}
.heavy .resbox{margin-top:var(--s2);margin-bottom:var(--s3)}
.prac .grp{min-width:0}
.prac .diag ol>li:before{border-color:var(--accent);color:var(--accent-2)}
.prac .diag>ol>li{margin:.05em 0 .4em}
.prac .diag table{font-size:.84em}

/* ---------- 템플릿: 표 중심 ---------- */
.tbl{flex-direction:column;gap:var(--s5)}
.tbl>.lead{flex:none}
.tbl>.lead>ul{display:flex;flex-direction:column;gap:.1em}
.tbl>.tw{flex:1;min-height:0}
.tbl table{font-size:.9em}

/* ---------- 모듈 첫 슬라이드: 왼쪽 레일 ---------- */
.slide.opener{padding-left:calc(var(--rail) + 56px)}
.rail{position:absolute!important;left:0;top:0;bottom:0;width:var(--rail);background:var(--tone);color:#fbf5e8;padding:30px 28px 28px;display:flex;flex-direction:column;z-index:2}
.rlab{font-size:14px;font-weight:800;letter-spacing:.22em;opacity:.75}
.rbig{display:flex;align-items:flex-start;margin:6px 0 2px;line-height:.86;font-weight:800;letter-spacing:-.05em;font-variant-numeric:tabular-nums}
.rk{font-size:46px;margin-top:12px;opacity:.7;letter-spacing:0}
.rn{font-size:var(--t-chapter)}
.rw{font-size:64px;letter-spacing:-.04em;margin-top:10px}
.rname{font-size:24px;font-weight:800;line-height:1.28;letter-spacing:-.02em;margin-top:6px}
.rail dl{display:grid;grid-template-columns:auto 1fr;gap:6px 14px;margin:20px 0 0;padding-top:14px;border-top:1px solid rgba(255,255,255,.35);font-size:20px;line-height:1.2}
.rail dt{opacity:.72}.rail dd{margin:0;font-weight:700;font-variant-numeric:tabular-nums}
.rg{margin-top:auto;padding-top:14px;border-top:1px solid rgba(255,255,255,.35)}
.rg .lbl{color:#fbf5e8;opacity:.75}
.rg p{font-size:20px;line-height:1.42}
.rg code{background:rgba(255,255,255,.16);color:#fff}
.rail strong{background:none;color:#fff}

/* ---------- 도식(인라인 SVG) ---------- */
.dg{display:block;width:100%;height:auto;overflow:visible;font-family:var(--font)}
.dg text{fill:var(--ink);font-family:var(--font)}
.dg .mono{font-family:var(--mono)}
.dg .num{font-variant-numeric:tabular-nums;font-weight:600}
.dg .b{font-weight:800}.dg .m{font-weight:600}
.dg .t2{fill:var(--ink-2)}.dg .t3{fill:var(--ink-3)}.dg .tw{fill:#fff}.dg .tp{fill:var(--paper)}
.dg .tt{fill:var(--tone-2)}.dg .ta{fill:var(--accent-2)}.dg .tteal{fill:var(--teal-2)}.dg .tb{fill:var(--blue-2)}.dg .to{fill:var(--ochre-2)}
.dg .n{fill:var(--paper-hi);stroke:var(--rule-2);stroke-width:1.5}
.dg .n2{fill:var(--paper-2);stroke:none}
.dg .nt{fill:var(--tone-wash);stroke:var(--tone);stroke-width:1.5}
.dg .ntf{fill:var(--tone);stroke:none}
.dg .na{fill:var(--accent);stroke:none}
.dg .naw{fill:var(--accent-wash);stroke:var(--accent);stroke-width:1.5}
.dg .nteal{fill:var(--teal-wash);stroke:var(--teal);stroke-width:1.5}
.dg .nblue{fill:var(--blue-wash);stroke:var(--blue);stroke-width:1.5}
.dg .noch{fill:var(--ochre-wash);stroke:var(--ochre);stroke-width:1.5}
.dg .nk{fill:var(--ink);stroke:none}
.dg .nd{fill:none;stroke:var(--ink-4);stroke-width:1.5;stroke-dasharray:6 5}
.dg .nm{fill:var(--paper-2);stroke:var(--rule-2);stroke-width:1.5;stroke-dasharray:6 5}
.dg .ln{fill:none;stroke:var(--ink-3);stroke-width:2}
.dg .ln.acc{stroke:var(--accent)} .dg .ln.teal{stroke:var(--teal)} .dg .ln.tone{stroke:var(--tone)} .dg .ln.mute{stroke:var(--ink-4);stroke-dasharray:5 5}
.dg .ln.thick{stroke-width:3}
.dg .rule{stroke:var(--rule);stroke-width:1.5}
.dg .fa{fill:var(--accent)} .dg .ft2{fill:var(--tone)} .dg .fi{fill:var(--ink)} .dg .fi3{fill:var(--ink-3)} .dg .fw{fill:var(--paper-hi)} .dg .fteal{fill:var(--teal)}
#svgdefs{position:absolute;width:0;height:0;overflow:hidden}
#ah-ink path{fill:var(--ink-3)} #ah-acc path{fill:var(--accent)} #ah-teal path{fill:var(--teal)} #ah-mute path{fill:var(--ink-4)}
#ah-blue path{fill:var(--blue)} #ah-ochre path{fill:var(--ochre)} #ah-paper path{fill:#efe5cf}

/* ---------- 카드(쓰는 곳에만) ---------- */
.cards{display:grid;gap:var(--s5)}
.card{border-top:var(--rule-ink);padding-top:var(--s3);min-width:0}
.card h4{margin:0 0 .3em;font-size:1em;font-weight:800;letter-spacing:-.015em;line-height:1.25}
.card .ey{font-size:14px;font-weight:800;letter-spacing:.12em;color:var(--tone);margin-bottom:6px}
.card.good{border-top-color:var(--teal)} .card.good .ey{color:var(--teal)}
.card.bad{border-top-color:var(--accent)} .card.bad .ey{color:var(--accent)}
.card.mute{border-top-color:var(--ink-4);color:var(--ink-3)}
.card p{margin:.2em 0}
.warn{display:flex;gap:.6em;align-items:baseline;padding:.45em .8em;border-left:4px solid var(--accent);background:var(--accent-wash);font-size:.86em;font-weight:600}
.warn:before{content:"주의";font-size:14px;font-weight:800;letter-spacing:.12em;color:var(--accent);flex:none}
.quote{font-size:1.5em;font-weight:800;letter-spacing:-.03em;line-height:1.2;padding-left:.6em;border-left:6px solid var(--accent)}
.quote small{display:block;font-size:.48em;font-weight:600;color:var(--ink-3);letter-spacing:.02em;margin-top:.35em}
.deep{border:1.5px dashed var(--ink-4);padding:.5em .8em;font-size:.82em;color:var(--ink-2);border-radius:var(--r-m)}
.deep:before{content:"심화 선택";display:block;font-size:14px;font-weight:800;letter-spacing:.12em;color:var(--ink-3);margin-bottom:4px}
.box{display:inline-block;border:2px solid var(--ink);min-width:1.1em;height:1.1em;vertical-align:-.15em;margin-right:.35em}
.stamp{display:inline-flex;align-items:center;justify-content:center;width:2.6em;height:2.6em;border-radius:50%;border:3px solid var(--accent);color:var(--accent);
  font-weight:800;font-size:.7em;transform:rotate(-12deg);letter-spacing:.02em;flex:none;box-shadow:inset 0 0 0 3px var(--paper),inset 0 0 0 4.5px var(--accent)}


/* ---------- 슬라이드별 도식 보조 ---------- */
.c2{grid-template-columns:1fr 1fr;gap:var(--s7)}
.c3{grid-template-columns:repeat(3,1fr)}
.c4{grid-template-columns:repeat(4,1fr)}
.c-req{grid-template-columns:1fr;gap:var(--s5)}
.c-req .q{font-size:1.05em;font-weight:600;line-height:1.5}
.c-req .bad .q{color:var(--ink-3)}
mark{background:none;color:inherit;padding:0 .1em;border-bottom:4px solid;border-radius:0}
mark.m1,.mlegend .m1{border-color:var(--blue)} mark.m2,.mlegend .m2{border-color:var(--teal)}
mark.m3,.mlegend .m3{border-color:var(--ochre)} mark.m4,.mlegend .m4{border-color:var(--accent)}
.mlegend{display:flex;gap:var(--s5);margin-top:var(--s3);font-size:.78em;font-weight:800;color:var(--ink-2)}
.mlegend span{border-bottom:4px solid;padding-bottom:2px}
.vis-in{margin-top:var(--s4)}
.modes td:last-child code{background:var(--night);color:var(--on-night);white-space:nowrap;font-size:.8em;padding:.15em .5em}
.modes td:first-child{white-space:nowrap}
.checks{counter-reset:none;display:flex;flex-direction:column;font-size:.74em}
.checks>li{display:flex;gap:.6em;align-items:flex-start;padding:.38em 0;margin:0;border-top:var(--hair)}
.checks>li:before{display:none}
.checks .box{flex:none;margin-top:.1em}
.tally{display:flex;align-items:center;gap:.6em;margin-top:var(--s4);font-size:.8em;font-weight:800;color:var(--ochre-2)}
.tally i{display:inline-block;width:3.2em;height:1.4em;border-bottom:3px solid var(--ochre)}
.caps2{display:grid;grid-template-columns:1fr 1fr;gap:var(--s8);font-size:.9em;border-top:var(--hair);padding-top:var(--s4);flex:none}
.caps2 p:last-child{font-weight:700}
.card svg.dg{margin-top:var(--s3)}
.def{font-size:1.02em;font-weight:700;line-height:1.38}
.q-s{font-size:1.05em;margin:var(--s5) 0}
.stat{border-top:var(--hair);padding-top:var(--s3)}
.sv{display:flex;align-items:baseline;gap:.3em;font-weight:800;letter-spacing:-.03em;font-variant-numeric:tabular-nums;line-height:1}
.sv span{font-size:1.5em;color:var(--ink-3)} .sv i{font-style:normal;color:var(--ink-4);font-size:1.1em} .sv b{font-size:2.2em;color:var(--accent)}
.sl{font-size:.74em;color:var(--ink-2);margin-top:.4em;font-weight:600}
.cav{display:inline-block;margin-left:.4em;padding:.1em .5em;background:var(--ochre-wash);color:var(--ochre-2);border-radius:var(--r-s);font-weight:700}


.pillars{display:grid;grid-template-columns:repeat(3,1fr);gap:var(--s5);align-items:stretch}
.pillar{border-top:8px solid var(--tone);border-bottom:var(--rule-ink);background:var(--paper-hi);padding:14px 18px 16px;display:flex;flex-direction:column;gap:6px;font-size:.78em;min-width:0}
.pillar .pk{font-size:2.2em;font-weight:800;line-height:1;color:var(--tone);letter-spacing:-.03em}
.pillar h4{margin:0;font-size:1.22em;font-weight:800;letter-spacing:-.02em}
.pillar .pr{font-weight:800;color:var(--tone-2)}
.pillar code{font-size:.78em;align-self:flex-start;word-break:break-all}
.pillar .pa{margin-top:auto;padding-top:8px;border-top:var(--hair);font-weight:600}
.pillar .pe{color:var(--ink-3);font-size:.9em}
.pillar.faint{background:transparent;border-top-style:double;border-top-width:8px}
.pillar.faint .pe{font-style:normal;opacity:.75}
.anat{display:grid;grid-template-columns:1fr;font-size:.8em;border-top:var(--rule-ink)}
.anat .af{font:600 .8em/1.6 var(--mono);color:var(--ink-4);padding-left:.3em}
.anat .ar{display:grid;grid-template-columns:9.2em 1fr;gap:var(--s4);padding:.32em 0;border-bottom:var(--hair);align-items:baseline}
.anat .ak code{background:none;color:var(--accent-2);font-weight:700;font-size:.92em;padding:0}
.anat .ab{font-weight:800;color:var(--ink-2)}
.req{display:inline-block;font-size:14px;font-weight:800;letter-spacing:.08em;color:#fff;background:var(--accent);padding:2px 6px;border-radius:var(--r-s);margin-right:.5em;vertical-align:.15em}
.ana{margin-top:var(--s3);font-size:.82em;color:var(--ink-2);font-weight:600;padding-left:.8em;border-left:4px solid var(--tone)}
.c-pr .card{font-size:.74em;display:flex;flex-direction:column;gap:8px}
.c-pr .card h4{font-size:1.15em}
.cmp{display:grid;grid-template-columns:auto 1fr;gap:.5em;align-items:baseline;padding:.4em .5em;border-left:4px solid}
.cmp.no{border-color:var(--accent);background:var(--accent-wash)}
.cmp.ok{border-color:var(--teal);background:var(--teal-wash)}
.cmp span{font-weight:800;font-size:.86em}
.cmp.no span{color:var(--accent-2)} .cmp.ok span{color:var(--teal-2)}
.cmp code{background:none;padding:0;color:var(--ink);font-size:.86em}
.cmp p{margin:0}
.file-box.tree{font-size:.7em;margin:0;padding-top:12px}
.file-box.tree:after{display:none}
.tree .fb-title{position:static;white-space:normal;margin-bottom:8px;font-size:.9em}
.pats{display:grid;grid-template-columns:repeat(3,1fr);gap:var(--s5)}
.pat{border-top:var(--rule-ink);padding-top:10px;min-width:0;display:flex;flex-direction:column;gap:10px}
.pat .ph-h{display:flex;align-items:baseline;gap:8px;flex-wrap:wrap}
.pat .pn{font-size:1.1em;font-weight:800;color:var(--tone);font-variant-numeric:tabular-nums}
.pat b{font-size:1em;font-weight:800;letter-spacing:-.02em}
.pat small{font-size:.66em;color:var(--ink-3);font-weight:600}
.pat p{font-size:.8em;color:var(--ink-2);line-height:1.38}
.pat svg{max-width:300px;align-self:center}
.comp{flex:none;border-top:var(--hair);padding-top:12px}
.cases{display:flex;flex-direction:column;gap:var(--s4)}
.case{border-left:5px solid var(--ochre);padding:.3em 0 .3em .8em;font-size:.76em}
.case .cl{font-size:14px;font-weight:800;letter-spacing:.12em;color:var(--ochre-2)}
.case p{font-weight:600;margin:.15em 0}
.case .ans{font-size:.82em;color:var(--ink-3);font-weight:700;display:flex;align-items:center;gap:.5em}
.case .ans i{display:inline-block;width:8em;border-bottom:2px solid var(--ink-4);height:1em}
.gatebox{display:grid;grid-template-columns:1fr auto 1fr;gap:var(--s5);font-size:.8em}
.gatebox ul>li{margin:.15em 0 .45em}
.gatebox .good li:before{background:var(--teal)} .gatebox .bad li:before{background:var(--accent)}
.gate{display:flex;flex-direction:column;align-items:center;gap:8px;padding-top:6px}
.gate .gl{flex:1;width:0;border-left:2px dashed var(--accent)}
.gate .gt{font-size:15px;font-weight:800;letter-spacing:.12em;color:var(--accent)}
.stamp.big{font-size:1.05em}
.stamped{display:flex;gap:var(--s6);align-items:flex-start}
.qs{font-size:.8em;display:flex;flex-direction:column;gap:.2em}
.qs>li{padding:.35em 0 .4em 1.8em;border-top:var(--hair);margin:0}
.qs>li:before{border-color:var(--ochre);color:var(--ochre-2);top:.4em}


.console>.col:first-child{flex:0 0 36%}
.console.wide-l>.col:first-child{flex:0 0 44%}
.console>.col:first-child>ul>li{margin:.1em 0 .5em}
.resbox{border-left:4px solid var(--teal);background:var(--teal-wash);padding:.45em .75em;font-size:var(--fk);line-height:1.4;margin-top:var(--s4)}
.resbox p{margin:0 0 .25em}
.stkbox{border-left:4px solid var(--accent);padding:.35em 0 .35em .75em;font-size:var(--fk);line-height:1.4;margin-top:var(--s4)}
.stkbox li{margin:.1em 0 .3em}
.stkbox li:before{background:var(--accent)}
.stkbox .lbl,.resbox .lbl{margin-bottom:4px}
.console .resbox{font-size:var(--fk)}
.resbox .lbl{margin-bottom:4px}
.csteps>ol{counter-reset:c}
.csteps>ol>li{padding:.1em 0 .5em 2.1em;margin:0 0 .25em;border-bottom:var(--hair)}
.prac .csteps>ol>li:before{width:1.5em;height:1.5em;line-height:1.36em;font-size:.8em;background:var(--accent);border-color:var(--accent);color:#fff}
.csteps>ol>li>ul{font-size:.84em;color:var(--ink-2)}
.csteps>ol>li>ul>li:before{background:var(--ink-4)}
.csteps>ul{margin-top:var(--s3)}
.csteps table{margin-top:var(--s3)}
.csteps>p{font-size:.82em;color:var(--ink-3);margin:var(--s3) 0 var(--s2)}
.fmap{display:grid;grid-template-columns:repeat(4,1fr);gap:var(--s3)}
.fmap.c3{grid-template-columns:repeat(3,1fr)}
.fm{background:var(--paper-hi);border-top:5px solid var(--tone);padding:10px 14px 12px;display:flex;flex-direction:column;gap:3px;min-width:0;font-size:.74em;line-height:1.3}
.fm.demo{background:transparent;border:1.5px dashed var(--ink-4);border-top:5px solid var(--ink-4)}
.fm-a{color:var(--ink-3);font-weight:600}
.fm-n{font-size:1.18em;font-weight:800;letter-spacing:-.02em;color:var(--ink)}
.fm-x{color:var(--ink-2)}
.fm-x:before{content:"예  ";font-size:.8em;font-weight:800;color:var(--ink-4)}
.fm-p{margin-top:auto;align-self:flex-start;font-size:15px;font-weight:800;letter-spacing:.04em;padding:3px 8px;border-radius:var(--r-s)}
.fm-p.spark{color:var(--teal-2);box-shadow:inset 0 0 0 1.5px var(--teal)}
.fm-p.blaze{background:var(--accent);color:#fff}
.fm-p.none{color:var(--ink-3);box-shadow:inset 0 0 0 1.5px var(--ink-4)}
.fmleg{display:flex;gap:var(--s6);margin-top:var(--s4);font-size:.66em;font-weight:700;color:var(--ink-2)}
.fmleg span{display:flex;align-items:center;gap:8px}
.fmleg span:before{content:"";width:26px;height:16px;border-top:5px solid var(--tone);background:var(--paper-hi)}
.fmleg .demo:before{border:1.5px dashed var(--ink-4);border-top:5px solid var(--ink-4);background:none}
.con51{gap:var(--s4)}
.con51>.vis{flex:none}
.con51 .row2{flex:1;min-height:0;display:flex;gap:var(--s7)}
.con51 .row2>.col:first-child{flex:0 0 46%}
.con51 .row2>.col{flex:1}
.con51 .row2>.col:first-child>ul>li{margin:.05em 0 .35em}
.cards.use{flex:none}
.ckcs{align-items:stretch}.ckc{display:flex;gap:.7em;align-items:flex-start;background:var(--paper-hi);padding:var(--s4);font-size:1.05em;line-height:1.4}.ckc .box{flex:none;margin-top:.15em}.ckc p{margin:0}
.use .card p,.cards.c3 .card p{font-size:.92em}
.card.mute .ey{color:var(--ink-3)}
.uk{display:grid;grid-template-columns:4.6em 1fr;gap:.2em .6em;margin-top:var(--s4);padding-top:var(--s3);border-top:var(--hair);font-size:.86em}
.uk span{font-size:15px;font-weight:800;letter-spacing:.06em;padding:4px 0;color:var(--teal-2)}
.uk.nouse span{color:var(--ink-3)}
.uk p{grid-column:2;margin:0 0 .2em}
.uk.nouse p{color:var(--ink-3)}
.verdict{margin-top:var(--s4);font-size:.82em}
.vr{display:flex;align-items:center;justify-content:space-between;gap:var(--s4);padding:.32em 0;border-bottom:var(--hair)}
.vr b{flex:none;font-size:.9em;padding:.12em .7em;border-radius:99px;color:#fff}
.vr b.ok{background:var(--teal)} .vr b.no{background:var(--accent)}
.plans{display:grid;grid-template-columns:1fr 1fr;gap:var(--s4);margin-bottom:var(--s4);margin-left:28%}
.pl{padding:10px 14px;border-top:5px solid;display:flex;flex-direction:column;gap:2px;font-size:.8em;line-height:1.25}
.pl b{font-size:1.2em;font-weight:800}
.pl small{font-size:.78em;color:var(--ink-3);font-weight:600}
.pl.spark{border-color:var(--teal);background:var(--teal-wash)} .pl.blaze{border-color:var(--accent);background:var(--accent-wash)}
.ptbl table{font-size:.8em;table-layout:fixed}
.ptbl th:first-child,.ptbl td:first-child{width:28%}
.ptbl td.na{color:var(--ink-4);font-weight:600}
.qgrid{display:flex;flex-direction:column;gap:var(--s4)}
.qc{border-left:5px solid var(--ochre);padding:.2em 0 .3em .8em}
.qq{font-size:1.05em;font-weight:800;letter-spacing:-.02em}
.qo{display:flex;gap:var(--s5);font-size:.74em;color:var(--ink-2);margin-top:.2em;font-weight:600}
.qo span{display:flex;align-items:center}
.blanks{display:flex;flex-direction:column;gap:var(--s4);position:relative;padding:12px 16px 12px 0}
.bl{display:flex;align-items:flex-end;gap:var(--s4);font-size:1.1em}
.bl b{color:var(--ochre-2)}
.bl i{flex:1;border-bottom:2.5px solid var(--ink-4);height:1.2em}
.blanks .stamp{align-self:flex-end;margin-top:var(--s3)}
.sits{display:flex;flex-direction:column;gap:var(--s2);font-size:.78em;margin-top:var(--s4)}
.sits>li{padding:.25em 0 .35em 1.7em;border-top:var(--hair);margin:0}
.sits>li:before{border-color:var(--accent);color:var(--accent-2);top:.35em}
.sits .sa{font-size:.78em;color:var(--ink-3);font-weight:700;display:flex;gap:.5em;align-items:center}
.sits .sa i{display:inline-block;width:6em;border-bottom:2px solid var(--ink-4);height:1em}
.chkt td:first-child{font-weight:500}
.chkt td{white-space:normal}
.chkt .box{width:.9em;min-width:.9em;height:.9em;border-width:2px}
.info{font-size:.78em;color:var(--ink-2);border-left:4px solid var(--ink-3);padding:.3em .8em;background:var(--paper-2)}
.capt{font-size:.8em;color:var(--ink-2);margin-top:var(--s3);border-top:var(--hair);padding-top:var(--s3)}
.ws{display:flex;flex-direction:column;font-size:.78em}
.ws>li{display:flex;flex-direction:column;padding:.22em 0 .28em 1.7em;margin:0;border-top:var(--hair)}
.ws>li i{display:block;height:.9em;border-bottom:1.5px dashed var(--ink-4);margin-top:.15em}
.ws>li:before{top:.3em}
.me{display:flex;flex-direction:column;align-items:center;gap:10px;font-size:.8em;color:var(--accent-2)}
.stamped .checks{flex:1;font-size:.8em}
.recap{border:var(--rule-ink);border-width:2px;padding:0;display:flex;flex-direction:column;font-size:.86em;background:var(--paper-hi)}
.rc{padding:14px 18px;border-top:var(--hair)}
.rc:first-child{border-top:0}
.r7{display:flex;flex-wrap:wrap;gap:6px 8px}
.r7>li{display:inline-flex;align-items:center;gap:.4em;padding:.15em .6em .15em .35em;margin:0;border:1.5px solid var(--tone);border-radius:var(--r-s);font-size:.84em;font-weight:700}
.r7>li:before{position:static;width:1.3em;height:1.3em;line-height:1.1em;font-size:.7em;flex:none}
.rt{font-size:.82em;line-height:1.4;color:var(--ink-2)}
.rcg{display:grid;grid-template-columns:1.1fr 1fr 1fr;border:2px solid var(--ink);background:var(--paper-hi);font-size:.8em}
.rcg .rc{border-top:0;border-left:var(--hair)}.rcg .rc:first-child{border-left:0}
.rcl{display:flex;flex-direction:column;gap:2px;margin:0;padding:0;list-style:none;font-size:.9em}.rcl li{margin:0;padding:0;display:flex;align-items:center}.rcl li:before{display:none}
.rcs{display:flex;gap:var(--s5);align-items:center;flex-wrap:wrap;margin:var(--s3) 0;font-size:.78em;border:var(--hair);padding:.4em .8em;background:var(--paper-2)}
.rcs .pi{display:inline-flex;align-items:center;font-weight:600}
table.dz{width:100%;border-collapse:collapse;font-size:.74em;margin-bottom:var(--s2)}
table.dz th,table.dz td{border-top:var(--hair);padding:.25em .6em;text-align:left;vertical-align:top;line-height:1.3}
table.dz thead th{font-size:.8em;color:var(--ink-3)}table.dz tbody th{white-space:nowrap;color:var(--tone-2);width:1%}
.ln1{height:1.4em;border-bottom:2.5px solid var(--ink-4)}
.six{display:grid;grid-template-columns:1fr 1fr;gap:var(--s3) var(--s7)}
.sx{display:flex;gap:.6em;align-items:flex-start;padding:.5em 0;border-top:var(--hair);font-size:.92em;font-weight:600}
.sx .box{flex:none;width:1.05em;height:1.05em;margin-top:.15em}
.foot{font-size:.7em;color:var(--ink-3);margin-top:var(--s4)}
.g2{grid-template-columns:1fr 1fr;gap:var(--s5) var(--s7)}
.anti h4,.faq h4{font-size:1.05em}
.anti p,.faq p{font-size:.92em;color:var(--ink-2)}
.rx{display:inline-block;font-size:14px;font-weight:800;letter-spacing:.1em;color:var(--teal-2);margin-right:.6em;vertical-align:.12em}
.faq .ey{color:var(--ink-3)}
.faq.fb{border-top-color:var(--teal)} .faq.fb .ey{color:var(--teal)}
.faq .sm{font-size:.74em;color:var(--teal-2);font-weight:700;margin-top:.3em}
.refs{display:flex;flex-direction:column}
.refs>li{display:grid;grid-template-columns:5.2em 1fr;gap:.6em;padding:.45em 0;margin:0;border-top:var(--hair);font-size:.92em}
.refs>li:first-child{border-top:var(--rule-ink)}
.refs>li:before{display:none}
.refs .rk{font-size:15px;font-weight:800;letter-spacing:.06em;color:var(--tone-2);padding-top:.35em}
.nextc{border-top:5px solid var(--accent);background:var(--paper-hi);padding:16px 20px;display:flex;flex-direction:column;gap:10px}
.nextc .ey{font-size:15px;font-weight:800;letter-spacing:.1em;color:var(--accent)}
.nextc p{font-size:1.05em;font-weight:700}
.qr .ph{width:100%;justify-content:center;min-height:120px}

/* ---------- 표지·휴식(대담한 한 곳) ---------- */
.slide.cover,.slide.brk{background:var(--night);color:var(--on-night)}
.slide.cover .hd,.slide.brk .hd{color:var(--on-night-2)}
.slide.cover .ft,.slide.brk .ft{border-top-color:var(--night-rule);color:var(--on-night-2)}
.slide.cover .ft-num b,.slide.brk .ft-num b{color:var(--on-night)}
.slide.cover .ft-bar i,.slide.brk .ft-bar i{background:var(--night-rule)}
.slide.cover .title,.slide.cover .hd{display:none}
.slide.cover strong,.slide.brk strong{color:var(--on-night);background:none}
.cv{flex:1;display:grid;grid-template-columns:1fr 330px;gap:var(--s6);padding:24px 0 26px;min-height:0}
.cv-l{display:flex;flex-direction:column;min-width:0}
.cv-k{font-size:16px;font-weight:800;letter-spacing:.2em;color:#f0a58c;display:flex;align-items:center;gap:12px}
.cv-k:before{content:"";width:44px;height:3px;background:var(--accent)}
.cv-t{font-size:var(--t-cover);line-height:1.06;font-weight:800;letter-spacing:-.045em;margin:26px 0 0;color:#fbf3e2}
.cv-t span{color:#f0a58c}
.cv-s{font-size:26px;color:var(--on-night-2);margin-top:22px;font-weight:500}
.cv-by{margin:30px 0 0;font-size:var(--t-small);font-weight:600;color:#fbf3e2;display:flex;align-items:baseline;gap:14px}
.cv-by span{font-size:var(--t-label);letter-spacing:.2em;color:#f0a58c;font-weight:800}
.cv-g{margin-top:auto}
.cv-g .lbl{color:var(--on-night-2)}
.cv-g ol{display:grid;grid-template-columns:repeat(3,1fr);gap:0;border-top:1px solid var(--night-rule)}
.cv-g li{padding:16px 22px 0 0;margin:0;display:flex;gap:14px;align-items:flex-start;font-size:24px;font-weight:700;line-height:1.3;color:#fbf3e2}
.cv-g li+li{padding-left:22px;border-left:1px solid var(--night-rule)}
.cv-g li:before{display:none}
.cv-g svg{flex:none;width:40px;height:40px}
.cv-g .gn{display:block;font-size:14px;letter-spacing:.14em;color:#f0a58c;margin-bottom:4px}
.cv-r{display:flex;align-items:center;justify-content:center}
.brkb{flex:1;display:grid;grid-template-columns:auto 1fr;gap:var(--s8);align-items:center;margin-bottom:var(--s5)}
.tcol{display:flex;flex-direction:column;gap:var(--s6);align-items:flex-start}
.timer{display:flex;font:800 190px/1 var(--font);color:#f0a58c;white-space:nowrap}
.timer .c{display:inline-block;width:.74em;text-align:center}
.timer .c.s{width:.32em}
.timer.paused{opacity:.55}
.timer.done{color:#fff;animation:tmb 1s steps(1,end) infinite}
@keyframes tmb{50%{opacity:.3}}
.tctl{display:flex;gap:var(--s4)}
.tbtn{font:700 30px/1 var(--font);color:var(--on-night);background:var(--night-2);border:2px solid var(--night-rule);border-radius:999px;padding:.55em 1.3em;cursor:pointer}
.tbtn:hover:not(:disabled){border-color:var(--accent);color:#fff}
.tbtn:disabled{opacity:.4;cursor:default}
.brkb ul>li{font-size:30px;margin:.2em 0 .6em;color:var(--on-night)}
.brkb ul>li:before{background:var(--accent)}
.slide.brk .title{color:#fbf3e2}
.brkb code{background:var(--night-2);color:#f0c9b8}
.map .prep{flex:none;display:flex;gap:28px;align-items:center;font-size:.8em;border-top:var(--hair);padding-top:12px}
.map .prep .lbl{margin:0}
.pi{display:flex;align-items:center}
.map .lead p{font-size:1.15em;font-weight:800;letter-spacing:-.02em}
.thanks{font-size:1.2em;font-weight:800;color:var(--accent)}

/* ---------- 오버레이: 발표자 노트 · 목차 ---------- */
#notes{position:fixed;left:0;right:0;bottom:0;max-height:44vh;overflow:auto;background:rgba(28,23,15,.97);color:#efe5cf;padding:16px 32px 22px;
  font-size:17px;line-height:1.65;display:none;z-index:50;border-top:3px solid var(--accent);font-family:var(--font)}
#notes.show{display:block}
#notes code{background:#3b3126;color:#f1c8b8;font-size:.9em}
#notes .nmeta{font-size:13px;font-weight:800;letter-spacing:.12em;color:#f0a58c;margin-bottom:8px}
#notes p{margin:.25em 0}
#notes .nx{margin-top:12px;padding:10px 14px;background:#2f271b;border-left:3px solid var(--ochre);border-radius:var(--r-s)}
#notes .nx b{color:#f0c987}
#notes .chk{background:#c99a3f;color:#2a2314;box-shadow:none}
#notes .chk:before{border-color:#2a2314}
#notes ul,#notes ol{padding-left:1.2em;list-style:disc}#notes li{padding-left:0}#notes li:before{display:none}
#notes ol{list-style:decimal}
#notes strong{color:#fff;background:none}
#notes pre{font-size:.9em;background:#17120c;padding:8px;border-radius:6px}
#notes table{font-size:.9em}#notes th{color:#efe5cf;border-color:#6f5f42}#notes td{border-color:#4a3f2c}
#notes .prompt-box,#notes .file-box,#notes .terminal,#notes .code-block{font-size:.9em;padding-top:12px}
#notes .prompt-box:before,#notes .prompt-box:after,#notes .terminal:before,#notes .terminal:after,#notes .file-box:after,#notes .code-block:before,#notes .code-block:after{display:none}
#notes .copy{display:none}
#grid{position:fixed;inset:0;background:rgba(23,19,13,.97);z-index:60;overflow:auto;padding:28px 36px;display:none;font-family:var(--font)}
#grid.show{display:block}
#grid .gh{color:#efe5cf;font-size:15px;font-weight:800;letter-spacing:.14em;margin-bottom:18px}
#grid .gm{color:#b3a483;font-size:13px;font-weight:800;letter-spacing:.12em;margin:18px 0 8px;display:flex;gap:10px;align-items:center}
#grid .gm b{color:#fff;padding:3px 7px;border-radius:3px;background:var(--tone)}
#grid .tiles{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:8px}
.tile{background:var(--paper);border-radius:var(--r-s);padding:9px 12px 10px;cursor:pointer;border-top:4px solid var(--tone);font-size:14px;line-height:1.35;min-height:72px;color:var(--ink)}
.tile:hover{background:var(--paper-hi)}
.tile.cur{outline:3px solid var(--accent);outline-offset:1px}
.tile small{display:flex;gap:8px;color:var(--ink-3);font-weight:700;font-size:12px;letter-spacing:.04em;margin-bottom:3px;font-variant-numeric:tabular-nums}
.tile[data-kind="실습"] small i{color:var(--accent)}
.tile i{font-style:normal}
.tile code{font-size:.85em}
#help{position:fixed;left:50%;transform:translateX(-50%);bottom:6px;z-index:40;color:#efe5cf;background:rgba(23,19,13,.8);padding:4px 14px;border-radius:4px;font:12px var(--font);letter-spacing:.04em;transition:opacity 1s}
#help.off{opacity:0}
@page{size:1280px 720px;margin:0}
@media print{
  html,body{overflow:visible;height:auto;background:#fff}
  #viewport{position:static;display:block}
  #stage{transform:none!important;width:auto;height:auto;box-shadow:none;overflow:visible}
  .slide{position:relative;visibility:visible;opacity:1;width:1280px;height:720px;page-break-after:always;break-after:page;overflow:hidden;transition:none}
  #notes,#grid,#help,.copy{display:none!important}
  *{-webkit-print-color-adjust:exact;print-color-adjust:exact}
}
"""

JS = r"""
(function(){
var slides=[].slice.call(document.querySelectorAll('.slide')),total=slides.length,cur=0,started=false;
var stage=document.getElementById('stage'),notes=document.getElementById('notes'),grid=document.getElementById('grid');
function scale(){var s=Math.min(innerWidth/1280,innerHeight/720);stage.style.transform='scale('+s+')';stage.dataset.k=s;}
function over(sl){
  var els=sl.querySelectorAll('.ovc,.vis,.prompt-box,.file-box,.terminal,.code-block,table');
  for(var i=0;i<els.length;i++){var e=els[i];
    if(e.scrollHeight>e.clientHeight+1||e.scrollWidth>e.clientWidth+1)return e;}
  var ft=sl.querySelector('.ft'),b=sl.querySelector('.band')||sl.querySelector('.body');
  if(ft&&b&&b.getBoundingClientRect().bottom>ft.getBoundingClientRect().top+1)return b;
  return null;
}
var KEYS=['fs','fp','fr','fk'];
var PH=[{fs:27,fp:22,fr:18,fk:21},{fs:24,fp:22,fr:15,fk:20},{fs:24,fp:20,fr:13,fk:19},{fs:22,fp:18,fr:12,fk:18},{fs:18,fp:15,fr:11,fk:16},{fs:12,fp:11,fr:9,fk:12}];
function setv(sl,v){for(var k in v)sl.style.setProperty('--'+k,v[k]+'px');}
function present(sl,el){
  if(!el||el.classList.contains('body')||el===sl)return {fs:true,fp:true,fr:true,fk:true};
  if(el.closest('.band'))return {fs:false,fp:false,fr:false,fk:true};
  var inR=!!el.closest('.rescode'),box=el.matches('.prompt-box,.file-box,.terminal,.code-block');
  if(box)return {fs:false,fp:!inR,fr:inR,fk:false};
  var has={fs:true};
  has.fp=!!el.querySelector('.prompt-box,.code-block,.file-box:not(.rescode .file-box)')&&!inR;
  has.fr=inR||!!el.querySelector('.rescode');
  has.fk=!!el.querySelector('.stkbox,.resbox');
  return has;
}
function run(sl,mx){
  var v={fs:mx,fp:24,fr:22,fk:22};setv(sl,v);
  for(var ph=0;ph<PH.length;ph++){
    var fl=PH[ph],g=0,el;
    while((el=over(sl))&&g++<400){
      var has=present(sl,el),best=null,bd=0;
      for(var i=0;i<4;i++){var k=KEYS[i];if(!has[k])continue;var d=(v[k]-fl[k])/fl[k];if(d>bd+1e-9){bd=d;best=k;}}
      if(!best){has={fs:true,fp:true,fr:true,fk:true};for(var j=0;j<4;j++){var k2=KEYS[j];var d2=(v[k2]-fl[k2])/fl[k2];if(d2>bd+1e-9){bd=d2;best=k2;}}}
      if(!best)break;v[best]-=0.5;setv(sl,v);
    }
    if(!over(sl))return {v:v,ph:ph};
  }
  return {v:v,ph:PH.length};
}
function fitTitle(sl){
  var t=sl.querySelector('.title');if(!t||!t.offsetHeight)return 46;var f=(sl.classList.contains('tight')||sl.classList.contains('k-실습'))?42:46;sl.style.setProperty('--ft',f+'px');
  while(t.offsetHeight>f*1.16*2+4&&f>34){f-=1;sl.style.setProperty('--ft',f+'px');}
  return f;
}
function minText(sl){
  var k=1,mn=99,mc=99,who='';
  var all=sl.querySelectorAll('.body *,.band *,.title,.title *,.rail *');
  for(var i=0;i<all.length;i++){var e=all[i];
    if(e.closest('.chk,.lbl,.copy,.fb-title,.ph,.tag,.kind,.rlab,.ey,.rk,.req,.fm-p,.cl,.rx,.uk>span,.gt,.cav,.quote small,.pat small,.rail dt,.stamp,.timer,.tctl'))continue;
    if(e.tagName==='CODE'&&!e.closest('pre'))continue;
    var txt=false;for(var c=e.firstChild;c;c=c.nextSibling){if(c.nodeType===3&&c.textContent.trim()){txt=true;break;}}
    if(!txt)continue;
    var r=e.getBoundingClientRect();if(!r.width)continue;
    var fs;
    if(e instanceof SVGElement){var svg=e.ownerSVGElement||e;var vb=svg.viewBox&&svg.viewBox.baseVal;
      var sc=vb&&vb.width?svg.getBoundingClientRect().width/vb.width/(+stage.dataset.k||1):1;
      fs=parseFloat(getComputedStyle(e).fontSize)*sc;}
    else fs=parseFloat(getComputedStyle(e).fontSize);
    var code=!!e.closest('pre');
    if(code){if(fs<mc)mc=fs;}else if(fs<mn){mn=fs;who=e.tagName+'.'+(e.className&&e.className.baseVal!==undefined?e.className.baseVal:e.className);}
  }
  return {min:Math.round(mn*10)/10,minCode:mc===99?null:Math.round(mc*10)/10,who:who};
}
var report=[];
function score(r,sl){
  var s=Math.min(r.v.fs/26,1.2);
  if(sl.querySelector('.body .prompt-box,.body .code-block'))s=Math.min(s,r.v.fp/22);
  if(sl.querySelector('.rescode'))s=Math.min(s,r.v.fr/15+.15);
  if(sl.querySelector('.stkbox,.resbox,.band'))s=Math.min(s,r.v.fk/20+.05);
  if(r.ov)s-=1;
  return s;
}
function attempt(sl,mx,hide){
  sl.classList.toggle('nostuck',hide);
  var a=run(sl,mx);a.ov=!!over(sl);return a;
}
function place(m,col){if(m.classList.contains('top'))col.insertBefore(m,col.firstChild);else col.appendChild(m);}
function fit(sl){
  var ft=fitTitle(sl),mx=+sl.dataset.fsmax||32;
  var movs=[].slice.call(sl.querySelectorAll('.mov')),cols=sl.querySelectorAll('.body.prac>.col');
  var hasStk=!!sl.querySelector('.cell.stk,.stkbox');
  var best=null;
  var combos=(movs.length&&cols.length===2)?(1<<movs.length):1;
  var home=movs.map(function(m){return m.parentNode;});
  for(var c=0;c<combos;c++){
    if(combos>1)movs.forEach(function(m,i){place(m,((c>>i)&1)?(home[i]===cols[0]?cols[1]:cols[0]):home[i]);});
    for(var h=0;h<(hasStk?2:1);h++){
      var a=attempt(sl,mx,!!h),sc=score(a,sl)-(h?.06:0);
      if(!best||sc>best.sc+1e-6)best={c:c,h:!!h,sc:sc};
    }
  }
  if(combos>1)movs.forEach(function(m,i){place(m,((best.c>>i)&1)?(home[i]===cols[0]?cols[1]:cols[0]):home[i]);});
  var a=attempt(sl,mx,best.h);
  var m=minText(sl);
  return {n:+sl.dataset.n,fs:a.v.fs,fp:a.v.fp,fr:a.v.fr,fk:a.v.fk,ft:ft,over:!!over(sl),stuckHidden:best.h,moved:best.c,min:m.min,minCode:m.minCode,who:m.who};
}
var fitted=[],t0=0;
function ensure(i){if(!fitted[i]){fitted[i]=1;report[i]=fit(slides[i]);}}
function fitAll(){
  t0=performance.now();var i=0;
  (function step(){var t=performance.now();while(i<total&&performance.now()-t<40){ensure(i);i++;}
    if(i<total)setTimeout(step,0);
    else{var r=report.slice();r.push({n:0,ms:Math.round(performance.now()-t0)});var el=document.getElementById('report');if(el)el.textContent=JSON.stringify(r);}
  })();
}
/* 휴식 슬라이드: 화면에 들어오면 카운트다운 시작. 다른 장에 다녀와도 시간은 계속 흐른다. 일시 정지·다시 시작·처음부터 버튼 */
var brkEnd=0,brkRem=0,brkTimer=null; /* brkEnd: 실행 중일 때 종료 시각(ms), brkRem: 일시 정지 중 남은 시간(ms) */
function brkFmt(n){var m=Math.floor(n/60),r=n%60;return (m<10?'0':'')+m+':'+(r<10?'0':'')+r;}
function brkLeft(){return brkEnd?Math.max(0,brkEnd-Date.now()):brkRem;}
function brkPaint(box){
  var el=box.querySelector('.timer'),pb=box.querySelector('[data-act=pause]');
  var left=Math.ceil(brkLeft()/1000),str=brkFmt(left);
  if(el.dataset.t!==str){var h='';for(var i=0;i<str.length;i++){var c=str.charAt(i);h+='<span class="c'+(c===':'?' s':'')+'">'+c+'</span>';}el.innerHTML=h;el.dataset.t=str;}
  var done=brkEnd>0&&left===0,paused=brkEnd===0&&brkRem>0;
  el.classList.toggle('done',done);el.classList.toggle('paused',paused);
  pb.textContent=paused?'다시 시작':'일시 정지';pb.disabled=done;
  if(done&&brkTimer){clearInterval(brkTimer);brkTimer=null;}
}
function brkSync(){
  if(brkTimer){clearInterval(brkTimer);brkTimer=null;}
  var box=slides[cur]&&slides[cur].querySelector('.tcol');if(!box)return;
  var sec=+box.querySelector('.timer').dataset.sec||600;
  if(!brkEnd&&!brkRem)brkEnd=Date.now()+sec*1000;
  brkPaint(box);
  if(brkEnd&&Date.now()<brkEnd)brkTimer=setInterval(function(){brkPaint(box);},250);
}
document.addEventListener('click',function(e){
  var b=e.target.closest&&e.target.closest('.tbtn');if(!b)return;
  var box=b.closest('.tcol'),sec=+box.querySelector('.timer').dataset.sec||600;
  if(b.dataset.act==='reset'){brkEnd=Date.now()+sec*1000;brkRem=0;}
  else if(brkEnd){brkRem=Math.max(0,brkEnd-Date.now());brkEnd=0;}
  else if(brkRem){brkEnd=Date.now()+brkRem;brkRem=0;}
  brkSync();
});
function show(i,keep){
  i=Math.max(0,Math.min(total-1,i));cur=i;
  if(started)ensure(i);
  slides.forEach(function(s,k){s.classList.toggle('on',k===i);s.setAttribute('aria-hidden',k===i?'false':'true');});
  if(!keep)history.replaceState(null,'','#'+(i+1));
  notes.innerHTML=slides[i].querySelector('.notes').innerHTML;notes.scrollTop=0;
  document.title='['+(i+1)+'/'+total+'] 하네스 엔지니어링 교원 연수';
  brkSync();
}
function buildGrid(){
  var h='<div class="gh">슬라이드 목차 · 클릭하거나 Enter, G 또는 Esc로 닫기</div>',mod='';
  slides.forEach(function(s,k){
    if(s.dataset.module!==mod){if(mod)h+='</div>';mod=s.dataset.module;
      var nm=s.querySelector('.hd-mod').textContent.replace(mod,'');
      h+='<div class="gm" data-track="'+s.dataset.track+'" style="--tone:'+getComputedStyle(s).getPropertyValue('--tone')+'"><b>'+mod+'</b>'+nm+'</div><div class="tiles">';}
    h+='<div class="tile" tabindex="0" data-i="'+k+'" data-kind="'+s.dataset.kind+'" style="--tone:'+getComputedStyle(s).getPropertyValue('--tone')+'"><small><span>'+(k+1)+'</span><i>'+s.dataset.kind+'</i><span>'+s.dataset.min+'분</span></small>'+s.querySelector('.title').innerHTML+'</div>';
  });
  grid.innerHTML=h+'</div>';
}
function openTile(t){show(+t.dataset.i);grid.classList.remove('show');}
grid.addEventListener('click',function(e){var t=e.target.closest('.tile');if(t)openTile(t);});
document.addEventListener('click',function(e){
  var b=e.target.closest('.copy');if(!b)return;
  var box=b.parentNode,c=box.querySelector('code');if(!c)return;
  var txt=c.textContent;
  function ok(){b.textContent='복사됨';b.classList.add('done');setTimeout(function(){b.textContent='복사';b.classList.remove('done');},1200);}
  if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(txt).then(ok,function(){fb()});}else fb();
  function fb(){var t=document.createElement('textarea');t.value=txt;document.body.appendChild(t);t.select();try{document.execCommand('copy');ok();}catch(x){}document.body.removeChild(t);}
});
document.addEventListener('keydown',function(e){
  if(e.ctrlKey||e.metaKey||e.altKey)return;
  var k=e.key;
  /* 한글 입력 상태(ㄹ·ㅎ·ㅜ·ㅔ)에서도 단축키가 되도록 글자 키는 물리 키 위치로 인식 */
  var kc={KeyF:'f',KeyG:'g',KeyN:'n',KeyP:'p'};
  if(e.code&&kc[e.code])k=kc[e.code];
  if(grid.classList.contains('show')){
    if(k==='Enter'&&document.activeElement&&document.activeElement.classList.contains('tile')){openTile(document.activeElement);return;}
    if(k!=='g'&&k!=='G'&&k!=='Escape')return;
  }
  if(e.target&&e.target.closest&&e.target.closest('.copy,.tbtn')&&(k===' '||k==='Enter'))return;
  if(k==='ArrowRight'||k===' '||k==='PageDown'){e.preventDefault();show(cur+1);}
  else if(k==='ArrowLeft'||k==='PageUp'){e.preventDefault();show(cur-1);}
  else if(k==='Home'){show(0);}else if(k==='End'){show(total-1);}
  else if(k==='g'||k==='G'){grid.classList.toggle('show');var t=grid.querySelectorAll('.tile');t.forEach(function(x,i){x.classList.toggle('cur',i===cur);});
    if(grid.classList.contains('show')&&t[cur]){t[cur].focus({preventScroll:true});t[cur].scrollIntoView({block:'center'});}}
  else if(k==='Escape'){grid.classList.remove('show');}
  else if(k==='n'||k==='N'){notes.classList.toggle('show');}
  else if(k==='f'||k==='F'){var de=document.documentElement;
    if(document.fullscreenElement){document.exitFullscreen();}
    else if(de.requestFullscreen){var r=de.requestFullscreen();if(r&&r.catch)r.catch(function(){});}
    else if(de.webkitRequestFullscreen){de.webkitRequestFullscreen();}}
  else if(k==='p'||k==='P'){window.print();}
});
var tx=null;
document.addEventListener('touchstart',function(e){tx=e.touches[0].clientX;},{passive:true});
document.addEventListener('touchend',function(e){if(tx===null)return;var d=e.changedTouches[0].clientX-tx;if(Math.abs(d)>50)show(cur+(d<0?1:-1));tx=null;});
addEventListener('resize',scale);
addEventListener('hashchange',function(){var n=parseInt(location.hash.slice(1),10);if(n)show(n-1,true);});
scale();setTimeout(function(){document.getElementById('help').classList.add('off');},6000);
var n0=parseInt(location.hash.slice(1),10);show(n0?n0-1:0,true);
function start(){if(started)return;started=true;ensure(cur);show(cur,true);fitAll();}
buildGrid();
if(document.fonts&&document.fonts.ready)document.fonts.ready.then(start);else start();
addEventListener('load',start);
addEventListener('beforeprint',function(){for(var i=0;i<total;i++)ensure(i);});
})();
"""


# ----------------------------------------------------------------- 슬라이드별 도식·맞춤 레이아웃
def body_lines(p):
    return [l.strip() for l in p["body_raw"].split("\n") if l.strip()]


CREDIT = "대구과학고등학교 교사 이준구"


def ov_cover(p):
    lines = body_lines(p)
    first = lines[0]
    items = re.findall(r"[①②③]\s*([^①②③\n]+)", p["body_raw"])
    head = re.match(r"^(.*?)[:：]\s*①", lines[1]).group(1) if len(lines) > 1 and "①" in lines[1] else "오늘 가져갈 것 3개"
    icons = [
        # 폴더 / 설계도 / 지도 (선 아이콘)
        '<svg viewBox="0 0 40 40" aria-hidden="true"><path d="M3 9h12l4 5h18v20H3z" fill="none" stroke="#f0a58c" stroke-width="2.2" stroke-linejoin="round"/></svg>',
        '<svg viewBox="0 0 40 40" aria-hidden="true"><rect x="4" y="5" width="32" height="30" fill="none" stroke="#f0a58c" stroke-width="2.2"/><path d="M4 15h32M15 15v20M20 24h11" fill="none" stroke="#f0a58c" stroke-width="2.2"/></svg>',
        '<svg viewBox="0 0 40 40" aria-hidden="true"><path d="M3 9l11-4 12 4 11-4v26l-11 4-12-4-11 4z M14 5v26 M26 9v26" fill="none" stroke="#f0a58c" stroke-width="2.2" stroke-linejoin="round"/></svg>',
    ]
    lis = "".join('<li>%s<div><span class="gn">%s</span>%s</div></li>' % (icons[i], "①②③"[i], inline(t.strip()))
                  for i, t in enumerate(items))
    # 오른쪽: 하네스 고리(22번 도식의 축약형, 장식). 글자 없음
    d = D(330, 420, "모델을 둘러싼 하네스 고리 장식")
    cx, cy = 165, 210
    for r, op in ((150, .22), (112, .35), (74, .55)):
        d.add('<circle cx="%d" cy="%d" r="%d" fill="none" stroke="#efe5cf" stroke-opacity="%.2f" stroke-width="1.5"/>' % (cx, cy, r, op))
    d.add('<circle cx="%d" cy="%d" r="34" fill="#b0402c"/>' % (cx, cy))
    import math
    for i in range(4):
        a = math.radians(-90 + i * 90 + 20)
        d.add('<circle cx="%.1f" cy="%.1f" r="9" fill="#231d14" stroke="#f0a58c" stroke-width="2.5"/>' % (cx + 112 * math.cos(a), cy + 112 * math.sin(a)))
    for i in range(3):
        a = math.radians(-60 + i * 120)
        d.add('<circle cx="%.1f" cy="%.1f" r="5" fill="#efe5cf" fill-opacity=".6"/>' % (cx + 150 * math.cos(a), cy + 150 * math.sin(a)))
    title = esc(p["title"]).replace("로 배우는 ", "로 배우는<br>").replace("하네스 엔지니어링", "<span>하네스 엔지니어링</span>")
    return ('<div class="cv"><div class="cv-l"><div class="cv-k">%s</div><h1 class="cv-t">%s</h1>'
            '<p class="cv-s">%s</p>'
            '<p class="cv-by"><span>제작</span>%s</p>'
            '<div class="cv-g">%s<ol>%s</ol></div></div><div class="cv-r">%s</div></div>'
            % ("교원 연수", title, inline(first), esc(CREDIT), lbl(esc(head)), lis, d.svg())), "cover"


def ov_map(p):
    lines = body_lines(p)
    lead, prep = lines[0], (lines[1] if len(lines) > 1 else "")
    W = 1152
    mins = {}
    for a, b, c, _ in MODULES:
        mins[c] = sum(SLIDE_MIN.get(k, 0) for k in range(a, b + 1) if k != BREAK_SLIDE)
    brk = SLIDE_MIN.get(BREAK_SLIDE, 10)
    row1 = [("M1", "t1"), ("M2", "t1"), ("M3", "t1"), ("M4", "t2"), ("M5", "t2")]
    row2 = [("휴식", "brk"), ("M6", "fb"), ("M7", "t2")]
    tot2 = brk + sum(mins[c] for c, _ in row2 if c != "휴식")
    tot1 = sum(mins[c] for c, _ in row1)
    k = (W - 5 * 4) / float(max(tot1, tot2))
    d = D(W, 330, "오늘의 지도: 모듈별 시간 막대")
    fill = {"t1": "nblue", "t2": "nteal", "fb": "noch", "wrap": "n", "brk": "nm"}
    tcol = {"t1": "tb", "t2": "tteal", "fb": "to", "wrap": "t2", "brk": "t3"}

    def row(items, y, title, now=None):
        d.text(0, y - 22, title, 20, "t2 b", anchor="start")
        cx = 0
        for c, tr in items:
            m = brk if c == "휴식" else mins[c]
            w = m * k
            cl = fill[tr]
            if c == now:
                cl = "na"
            d.rect(cx, y, w, 96, cl, 4)
            tc = "tw" if c == now else tcol[tr]
            if c == "휴식":
                d.text(cx + w / 2, y + 36, "휴식", 22, "t3 b")
            else:
                d.text(cx + 14, y + 30, c, 24, tc + " b", anchor="start")
                d.text(cx + 14, y + 64, SHORT[c], 20, ("tw" if c == now else "t2") + " m", anchor="start")
            d.text(cx + w - 12, y + 80 if c != "휴식" else y + 66, "%g분" % m, 20, ("tw" if c == now else "t3") + " num", anchor="end")
            if c == now:
                d.add('<path d="M%g %g l-9 12 h18 z" class="fa"/>' % (cx + 26, y + 100))
                d.text(cx + 40, y + 120, "현재 위치", 20, "ta b", anchor="start")
            cx += w + 4
        return cx

    end1 = row(row1, 40, "Claude Code 기본 (M1–M5)", now="M1")
    row(row2, 222, "휴식, 이어서 M6–M7")
    d.text(W, 18, "합계 %g분" % sum(SLIDE_MIN.values()), 20, "t3 num", anchor="end")
    vis = d.svg()
    prep_html = ""
    if prep:
        head, _, rest = prep.partition(":")
        items = [t.strip() for t in rest.split("·") if t.strip()]
        prep_html = ('<div class="prep"><span class="lbl">%s</span>%s</div>'
                     % (esc(head.strip()), "".join('<span class="pi"><i class="box"></i>%s</span>' % inline(t) for t in items)))
    return ('<div class="body stack map ovc"><div class="lead"><p>%s</p></div><div class="vis">%s</div>%s</div>'
            % (inline(lead), vis, prep_html)), "", 30


def ov_break(p):
    mm = SLIDE_MIN.get(BREAK_SLIDE, 10)
    t0 = "%02d:00" % mm
    cells = "".join('<span class="c%s">%s</span>' % (" s" if c == ":" else "", c) for c in t0)
    return ('<div class="body brkb ovc"><div class="tcol"><div class="timer" data-sec="%d" data-t="%s" role="timer" aria-label="휴식 %d분 카운트다운. 이 화면에 들어오면 시작한다">%s</div>'
            '<div class="tctl"><button type="button" class="tbtn" data-act="pause">일시 정지</button><button type="button" class="tbtn" data-act="reset">처음부터</button></div></div>'
            '<div class="col">%s</div></div>' % (mm * 60, t0, mm, cells, p["body"])), "brk"


OVERRIDES = {1: ov_cover, 2: ov_map, 33: ov_break}
SLIDE_MIN = {}




import math as _m


def arc(cx, cy, r, a1, a2):
    """시계 방향 호(도 단위)."""
    p1 = (cx + r * _m.cos(_m.radians(a1)), cy + r * _m.sin(_m.radians(a1)))
    p2 = (cx + r * _m.cos(_m.radians(a2)), cy + r * _m.sin(_m.radians(a2)))
    large = 1 if (a2 - a1) % 360 > 180 else 0
    return "M%.1f %.1f A%g %g 0 %d 1 %.1f %.1f" % (p1[0], p1[1], r, r, large, p2[0], p2[1])


def diag_items(p):
    return li_texts(p["diag_rest"])


def table_from(raw, tokens=None):
    rows = [re.sub(r"^-\s+", "", l.strip()) for l in raw.split("\n") if re.match(r"^\s*(?:-\s+)?\|", l)]
    return render_table(rows, tokens if tokens is not None else []) if rows else ""


# ---- 3: 채팅 AI vs 에이전틱 루프
def ov_3(p):
    d = D(666, 420, "일반 채팅 AI와 Claude Code의 에이전틱 루프 비교")
    d.text(115, 22, "일반 채팅 AI", 22, "t3 b")
    for i, t in enumerate(["묻고", "복사하고", "붙여넣는다"]):
        y = 70 + i * 100
        d.node(20, y, 190, 58, t, "nm", 22, "t3 m")
        if i < 2:
            d.arrow(115, y + 62, 115, y + 96, "ln mute", "mute")
    d.add('<line x1="262" y1="10" x2="262" y2="400" class="rule"/>')
    cx, cy, r = 470, 215, 118
    d.text(cx, 22, "Claude Code", 22, "tteal b")
    for a1, a2 in ((-62, 2), (58, 122), (178, 242)):
        d.path(arc(cx, cy, r, a1, a2), "ln teal thick", "teal")
    for (a, t) in ((-90, "해 보기"), (30, "결과 보기"), (150, "다음 행동")):
        nx, ny = cx + r * _m.cos(_m.radians(a)), cy + r * _m.sin(_m.radians(a))
        d.node(nx - 66, ny - 27, 132, 54, t, "nteal", 22, "b")
    d.text(cx, cy, "에이전틱\n루프", 22, "tteal b")
    d.text(cx, 392, "직접 읽고, 쓰고, 실행한다", 22, "t2 m")
    return L_split(p, d.svg())


# ---- 7: 모호한 요청 vs 구체적인 요청(네 요소 색 표시)
def ov_7(p):
    items = diag_items(p)
    bad = re.search(r'"(.+?)"', items[0]).group(1)
    good = re.search(r'"(.+)"', items[1]).group(1)
    g = esc(good)
    marks = [("고1 정보 수업", "m1"), ("&#x27;변수와 자료형&#x27; 단원 복습용", "m2"), ("'변수와 자료형' 단원 복습용", "m2"),
             ("객관식 5문항", "m3"), ("정답과 한 줄 해설", "m3"), ("쉬움 3개·보통 2개", "m4")]
    for t, c in marks:
        g = g.replace(t, '<mark class="%s">%s</mark>' % (c, t), 1)
    legend = ('<div class="mlegend"><span class="m1">대상</span><span class="m2">범위</span>'
              '<span class="m3">형식</span><span class="m4">기준</span></div>')
    vis = ('<div class="cards c-req"><div class="card bad"><div class="ey">모호한 요청</div><p class="q">“%s”</p></div>'
           '<div class="card good"><div class="ey">구체적인 요청</div><p class="q">“%s”</p>%s</div></div>' % (esc(bad), g, legend))
    return L_split(p, vis, "r30")


# ---- 8: 컨텍스트 표 + 플랜 모드 흐름
def ov_8(p):
    tbl = table_from(p["diag_rest"])
    items = ["요청", "계획만 제시\n(파일 안 고침)", "사람이 승인", "실제 작업"]
    W = 666
    d = D(W, 150, "플랜 모드 흐름: 요청, 계획만 제시, 사람이 승인, 실제 작업")
    tot = hflow_width(items, 22, 36)
    x0 = (W - tot) / 2
    hflow(d, x0, 40, items, 76, 22, 36, cls=["n", "nt", "naw", "n"])
    d.text(0, 14, "플랜 모드", 20, "t3 b", anchor="start")
    vis = '<div class="panel">%s</div><div class="panel">%s</div>' % (tbl, d.svg())
    return L_split(p, vis)


# ---- 11: 세 가지가 실습에 모두 들어 있었다
def ov_11(p):
    W = 1152
    d = D(W, 300, "구체적인 프롬프트, 플랜 모드, 컨텍스트 유지 세 단계와 첫 산출물")
    steps = [("①", "구체적인 프롬프트", "대상·시간·구조·형식 지정"),
             ("②", "플랜 모드", "파일을 만들기 전\n계획 확인"),
             ("③", "컨텍스트 유지", "다시 설명하지 않고\n“더 쉽게 바꿔줘”만으로 이어서 수정")]
    bw, gap = 340, 66
    for i, (nm, t, sub) in enumerate(steps):
        x0 = i * (bw + gap)
        d.rect(x0, 0, bw, 150, "n", 4)
        d.rect(x0, 0, bw, 5, "ntf", 0)
        d.text(x0 + 24, 40, nm, 26, "tt b", anchor="start")
        d.text(x0 + 60, 40, t, 26, "b", anchor="start")
        d.text(x0 + 24, 98, sub, 21, "t2", anchor="start", lh=1.35)
        if i < 2:
            d.arrow(x0 + bw + 8, 75, x0 + bw + gap - 8, 75, "ln thick", "ink")
        d.line([(x0 + bw / 2, 152), (x0 + bw / 2, 190), (W / 2, 190)], "ln mute", None)
    d.line([(W / 2, 190), (W / 2, 214)], "ln", "ink")
    ic_doc(d, W / 2 - 150, 222, 40, 50, "n")
    d.text(W / 2 - 96, 236, "lesson-01.md", 24, "mono b", anchor="start")
    d.text(W / 2 - 96, 266, "나의 첫 산출물", 21, "tt b", anchor="start")
    return L_stack(p, d.svg()), "", 30


# ---- 12: CLAUDE.md 구성
def ov_12(p):
    d = D(520, 430, "CLAUDE.md의 네 구성 항목: 형식, 독자·어조, 반복 제약, 금지")
    d.rect(0, 0, 360, 290, "n2", 4)
    d.rect(0, 0, 360, 48, "nk", 4)
    d.text(20, 25, "CLAUDE.md", 22, "tp b mono", anchor="start")
    for i, t in enumerate(["형식", "독자·어조", "반복 제약", "금지"]):
        cx0 = 20 + (i % 2) * 166
        cy0 = 70 + (i // 2) * 106
        d.rect(cx0, cy0, 154, 86, "n", 3)
        d.circle(cx0 + 77, cy0 + 2, 6, "na")
        d.text(cx0 + 77, cy0 + 47, t, 23, "b" if t != "금지" else "ta b")
    d.path("M366 92 C 420 92, 420 222, 368 222", "ln tone thick", "teal")
    d.text(460, 157, "대화를 새로\n시작해도\n다시 읽힘", 20, "tt b", lh=1.3)
    d.rect(0, 322, 520, 62, "naw", 3)
    d.text(20, 353, "산문으로 적은 부탁 → 가끔 놓칠 수 있음", 22, "ta b", anchor="start")
    return L_split(p, d.svg(), "r46")


# ---- 15: 슬래시 커맨드 표 + 스킬 폴더 도식
def ov_15(p):
    d = D(540, 250, "스킬 폴더 .claude/skills/quiz/SKILL.md가 /quiz 명령이 된다")
    d.node(0, 10, 360, 56, ".claude/skills/quiz/SKILL.md", "n", 20, "mono m")
    d.arrow(366, 38, 416, 38, "ln acc thick", "acc")
    d.node(424, 6, 110, 64, "/quiz", "na", 28, "tw b mono")
    d.rect(0, 86, 420, 160, "n", 4)
    d.text(18, 108, "SKILL.md", 20, "t3 b mono", anchor="start")
    d.rect(18, 126, 384, 50, "nt", 3)
    d.text(34, 151, "description", 21, "mono b", anchor="start")
    d.text(390, 151, "한 줄, 늘 기억", 20, "tt m", anchor="end")
    d.rect(18, 184, 384, 50, "nm", 3)
    d.text(34, 209, "본문", 21, "b", anchor="start")
    d.text(390, 209, "필요할 때만 읽음", 20, "t3 m", anchor="end")
    left = p["body"] + '<div class="vis-in">%s</div>' % d.svg()
    return L_split(p, '<div class="panel">%s</div>' % p["diag"], "r50", left=left)


# ---- 18: 권한 모드 표 + 경고 띠
def ov_18(p):
    tbl = table_from(p["diag_rest"])
    m = re.search(r"경고 띠:\s*\"?(.+?)\"?\s*$", p["diag_rest"], re.M)
    warn = '<div class="warn">%s</div>' % inline(m.group(1)) if m else ""
    return L_table(p, '<div class="modes">%s</div>' % tbl, warn), "", 30


# ---- 19: 체크포인트 6문장
def ov_19(p):
    items = diag_items(p)
    rows = "".join('<li><i class="box"></i><span>%s</span></li>' % inline(t) for t in items)
    vis = ('<ol class="checks">%s</ol><div class="tally"><span>손 든 인원</span><i></i><span>/ 6문장</span></div>' % rows)
    return L_question(p, vis), "", 34
OVERRIDES.update({3: ov_3, 7: ov_7, 8: ov_8, 11: ov_11, 12: ov_12, 15: ov_15, 18: ov_18, 19: ov_19})


# ---- 20: 하네스가 해 주는 일 (말로 요청 -> 팀 파일 생성 -> 실행·검수)
def ov_20(p):
    W = 1152
    d = D(W, 250, "말로 요청하면 하네스가 팀 파일을 만들고, 만드는 쪽과 검수하는 쪽이 실행한다")
    cw, gap = 330, 81
    xs = [i * (cw + gap) for i in range(3)]
    heads = ["① 말로 요청", "② 하네스가 팀 파일 생성", "③ 팀 실행 · 검수"]
    for x0, h in zip(xs, heads):
        d.text(x0 + cw / 2.0, 16, h, 22, "t2 b")
    # 칸 1: 말풍선
    x0 = xs[0]
    d.rect(x0, 44, cw, 150, "naw", 14)
    d.add('<path d="M%g 194 l-18 30 l46 -30 z" class="naw"/>' % (x0 + 44))
    d.text(x0 + cw / 2.0, 119, "“형성평가 문항을 만들고\n검수하는 하네스를\n구성해줘”", 23, "ta b", lh=1.35)
    # 칸 2: .claude/ 폴더
    x0 = xs[1]
    d.rect(x0, 44, cw, 150, "nteal", 10)
    d.add(ic_folder(x0 + cw / 2.0 - 52, 62, 104, "ln tone"))
    d.text(x0 + cw / 2.0, 168, ".claude/", 26, "mono b tteal")
    # 칸 3: 만드는 쪽 / 검수하는 쪽
    x0 = xs[2]
    d.node(x0, 44, cw, 62, "만드는 쪽", "n", 24, "b")
    d.node(x0, 132, cw, 62, "검수하는 쪽", "nt", 24, "tt b")
    d.arrow(x0 + cw / 2.0, 108, x0 + cw / 2.0, 130, "ln", "ink")
    for i in range(2):
        a = xs[i] + cw + 8
        d.arrow(a, 119, a + gap - 16, 119, "ln acc thick", "acc")
    its = li_texts(p["body_raw"])
    return L_stack(p, d.svg()), "", 30


# ---- 24: 만드는 에이전트 -> 검수 에이전트(다른 눈)
def ov_24(p):
    W = 666
    d = D(W, 128, "quiz-writer가 만든 문항을 quiz-checker가 별도 컨텍스트에서 읽기만 하며 검수한다")
    d.node(0, 36, 200, 76, "quiz-writer", "n", 21, "mono b", sub="문항 생성", sfs=20)
    d.arrow(204, 74, 236, 74, "ln", "ink")
    d.node(240, 36, 250, 76, "quiz-checker", "nt", 21, "mono b", sub="별도 컨텍스트, 읽기만", sfs=20, scls="tt m")
    d.rect(386, 2, 104, 30, "ntf", 15)
    d.text(438, 17, "다른 눈", 20, "tw b")
    d.arrow(494, 74, 526, 74, "ln acc", "acc")
    d.node(530, 46, 136, 56, "지적 사항", "naw", 21, "ta b")
    main = '<div class="grp">%s</div><div class="grp">%s</div>' % (d.svg(), p["prompt"])
    return L_practice(p, main=main)


def tree_rows(d, rows, x0, y0, step=34, fs=21):
    """폴더 트리 한 줄씩 그린다. rows: [(들여쓴 글자, 굵게?)]. 반환: 줄별 (끝 x 추정, 가운데 y)."""
    out = []
    for i, (t, b) in enumerate(rows):
        yy = y0 + i * step
        d.text(x0, yy, t.replace(" ", "\u00a0"), fs, "mono " + ("b" if b else "m"), anchor="start")
        out.append((x0 + len(t) * fs * 0.6 + 14, yy))
    return out


# ---- 25: 정리 - 폴더 트리와 구성 요소 한 줄 정의, 심화 선택
def ov_25(p):
    W = 1152
    d = D(W, 400, "mini-harness 폴더 트리와 에이전트·스킬·오케스트레이터의 한 줄 정의, 심화 선택 /harness:evolve")
    rows = [("mini-harness/", 1), ("└── .claude/", 1), ("    ├── agents/", 0), ("    │   ├── quiz-writer.md", 1),
            ("    │   └── quiz-checker.md", 1), ("    └── skills/", 0), ("        └── quiz-format/", 0),
            ("            └── SKILL.md", 1)]
    step = 34
    y0 = 18
    pos = tree_rows(d, rows, 0, y0, step, 22)
    # 오른쪽 정의 상자
    bx, bw = 640, 512
    defs = [("에이전트", "역할이 정해진 하위 작업자 파일", ".claude/agents/*.md", "nt", "tt", (3, 4)),
            ("스킬", "재사용하는 절차를 적은 파일", ".claude/skills/*/SKILL.md", "nteal", "tteal", (7,)),
            ("오케스트레이터", "실행 순서를 정한 스킬 파일", None, "n", "t2", (5, 6, 7))]
    ys = [y0 + 3.5 * step, y0 + 7 * step, None]
    # 에이전트
    for k, (nm, line, path, cl, tc, rws) in enumerate(defs):
        top = (6, 118, 232)[k]
        h = 98 if k < 2 else 86
        d.rect(bx, top, bw, h, cl, 6)
        d.text(bx + 18, top + 26, nm, 24, tc + " b", anchor="start")
        d.text(bx + 18, top + 58, line, 21, "t2 m", anchor="start")
        if path:
            d.text(bx + 18, top + 84, path, 18, "mono t3", anchor="start")
    # 연결선
    wy = y0 + 3.5 * step
    d.line([(pos[4][0] + 12, y0 + 3 * step), (590, y0 + 3 * step), (590, 6 + 49), (bx - 4, 6 + 49)], "ln tone", "teal") if False else None
    d.line([(pos[3][0], y0 + 3 * step), (590, y0 + 3 * step), (590, 55), (bx - 4, 55)], "ln", "ink")
    d.line([(pos[4][0], y0 + 4 * step), (590, y0 + 4 * step), (590, 55)], "ln", None)
    d.line([(pos[7][0], y0 + 7 * step), (610, y0 + 7 * step), (610, 167), (bx - 4, 167)], "ln teal", "teal")
    d.line([(pos[6][0], y0 + 6 * step), (570, y0 + 6 * step), (570, 275), (bx - 4, 275)], "ln mute", "mute")
    # 심화 선택
    d.rect(0, 336, W, 58, "n2", 6)
    d.rect(14, 348, 110, 34, "ntf", 17)
    d.text(69, 365, "심화 선택", 20, "tw b")
    d.text(140, 365, "/harness:evolve = 팀을 고친 뒤 처음 설계와 최종 형태가 어떻게 달라졌는지 기록하는 명령. 지금은 이런 게 있다는 정도만.", 19, "t2 m", anchor="start")
    its = li_texts(p["body_raw"])
    lead = "".join("<p>%s</p>" % inline(t) for t in (its[0], its[-1]) if t)
    return '<div class="body stack ovc"><div class="lead ovc">%s</div><div class="vis ovc">%s</div></div>' % (lead, d.svg()), "", 30


# ---- 26: 하네스가 만든 폴더 지도 (트리 + 파일별 한 줄 정의)
def ov_26(p):
    W = 1152
    d = D(W, 340, "mini-harness 폴더 트리와 각 파일의 한 줄 정의. 파일 이름과 개수는 하네스가 정한다")
    rows = [("mini-harness/", 1), ("└── .claude/", 1), ("    ├── agents/", 0), ("    │   ├── quiz-writer.md", 1),
            ("    │   └── quiz-checker.md", 1), ("    └── skills/", 0), ("        └── quiz-.../", 1),
            ("            └── SKILL.md", 1)]
    step, y0 = 34, 18
    pos = tree_rows(d, rows, 0, y0, step, 22)
    notes = [(3, "에이전트: 문항을 만드는 역할", "nt", "tt"), (4, "에이전트: 문항을 검수하는 역할", "nt", "tt"),
             (6, "오케스트레이터 스킬: writer → checker 순서를 정한 절차 (예)", "nteal", "tteal")]
    for r, t, cl, tc in notes:
        yy = y0 + r * step
        d.arrow(pos[r][0], yy, 468, yy, "ln " + ("teal" if r == 6 else ""), "teal" if r == 6 else "ink")
        w = 676 if r == 6 else 430
        d.rect(474, yy - 15, w, 30, cl, 6)
        d.text(474 + 14, yy, t, 19, tc + " b", anchor="start")
    d.text(0, 316, "파일 이름과 개수는 하네스가 실행마다 정한다. 위는 예시.", 21, "ta b", anchor="start")
    its = li_texts(p["body_raw"])
    keep = [t for t in its if not t.startswith(("에이전트 =", "스킬 =", "오케스트레이터 ="))]
    lead = "".join("<p>%s</p>" % inline(t) for t in keep)
    defs = "".join("<p>%s</p>" % inline(t) for t in its if t.startswith(("에이전트 =", "스킬 =", "오케스트레이터 =")))
    return ('<div class="body stack ovc"><div class="lead ovc">%s</div><div class="vis ovc">%s</div></div>' % (lead + defs, d.svg())), "", 30


# ---- 31: 점검 - 체크박스 3개 카드(가로)
def ov_31(p):
    its = [re.sub(r"^\[[ xX]?\]\s*", "", t) for t in li_texts(p["body_raw"])]
    cards = "".join('<div class="card ckc"><i class="box"></i><p>%s</p></div>' % inline(t) for t in its)
    return ('<div class="body stack ovc"><div class="vis"><div class="cards c3 ckcs">%s</div></div></div>' % cards), "", 30


# ---- 32: 정리 - 4칸 가로 흐름(요청 -> 읽기 -> 고치기 -> 실행) + 다음: Firebase(M6)
def ov_32(p):
    W = 1152
    d = D(W, 130, "말로 요청, 생성 파일 읽기, 말로 고치기, 다시 실행해 비교로 이어지고 다음은 Firebase(M6)")
    labels = ["말로 요청", "생성 파일 읽기", "말로 고치기", "다시 실행"]
    bw, gap = 170, 48
    for i, t in enumerate(labels):
        x0 = i * (bw + gap)
        d.node(x0, 20, bw, 84, t, ("nt", "n", "nteal", "nt")[i], 24, "b", sub=("M4", "M5 27", "M5 28", "M5 29")[i], sfs=18)
        if i < 3:
            d.arrow(x0 + bw + 6, 62, x0 + bw + gap - 6, 62, "ln", "ink")
    ex = 4 * bw + 3 * gap
    d.arrow(ex + 8, 62, ex + 72, 62, "ln acc thick", "acc")
    d.node(ex + 80, 20, W - ex - 80, 84, "다음: Firebase(M6)", "na", 24, "tw b")
    its = li_texts(p["body_raw"])
    lead = "".join("<p>%s</p>" % inline(t) for t in its[1:2])
    return ('<div class="body stack summ ovc"><div class="lead ovc">%s</div><div class="vis ovc">%s</div></div>' % (lead, d.svg())), "", 32


# ---- 콘솔 설정(M6): 왼쪽 요점·예상 결과, 오른쪽 콘솔 단계
def L_console(p, left_extra="", right_extra="", diag=None, result=True):
    res = ""
    if result and p["result"]:
        res = '<div class="resbox mov">%s%s</div>' % (lbl("예상 결과", "l-res"), p["result"])
    right = diag if diag is not None else p["diag"]
    stk = ('<div class="stkbox mov">%s%s</div>' % (lbl("막힐 때", "l-stk"), p["stuck"])) if p["stuck"] else ""
    return ('<div class="body prac console ovc"><div class="col ovc">%s%s%s%s</div><div class="col main ovc">%s%s</div></div>'
            % (p["body"], left_extra, res, stk, ('<div class="grp diag csteps">%s</div>' % right) if right else "", right_extra)), "", 28


def ov_console(p):
    return L_console(p)


def chk_boxes(h):
    return h.replace("☐ ", '<i class="box"></i>').replace("☐", '<i class="box"></i>')


# ---- 34: Firebase 기능 지도
def ov_34(p):
    rows = [l for l in p["diag_rest"].split("\n") if l.strip().startswith("|")]
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows][2:]
    leg = re.search(r"범례:\s*(.+)$", p["diag_rest"], re.M)
    mine = []
    if leg:
        m = re.search(r"내가 직접 해 볼 것 = ([^/]+)", leg.group(1))
        mine = [x.strip() for x in m.group(1).split("·")] if m else []
    cards = ""
    for name, ana, plan, ex in cells:
        nm = name.replace("요금제(Spark/Blaze)", "요금제")
        own = any(nm.startswith(x) or x.startswith(nm) for x in mine)
        pl = plan.replace("**", "")
        pcls = "blaze" if "Blaze" in pl else ("none" if pl in ("—", "-") else "spark")
        cards += ('<div class="fm %s"><div class="fm-a">%s</div><div class="fm-n">%s</div><div class="fm-x">%s</div><div class="fm-p %s">%s</div></div>'
                  % ("own" if own else "demo", esc(ana), esc(name), esc(ex), pcls, esc(pl) if pl not in ("—", "-") else "선택"))
    legend = ""
    if leg:
        parts = [x.strip() for x in leg.group(1).split(" / ")]
        legend = '<div class="fmleg"><span class="own">%s</span><span class="demo">%s</span></div>' % (esc(parts[0]), esc(parts[1].rstrip(".")) if len(parts) > 1 else "")
    nm_ = re.search(r"표 아래 한 줄:\s*(.+)$", p["diag_rest"], re.M)
    note = '<div class="info" style="margin-top:16px">%s</div>' % inline(nm_.group(1).strip()) if nm_ else ""
    return L_stack(p, '<div class="fmap%s">%s</div>%s%s' % (" c3" if len(cells) == 6 else "", cards, legend, note)), "", 26


# ---- 36: 프로젝트 -> 웹 앱 -> firebaseConfig, 공개 vs 비공개
def ov_36(p):
    W = 1152
    d = D(W, 150, "Firebase 프로젝트 안에 웹 앱을 등록하면 firebaseConfig가 나온다. 공개해도 되는 값과 비공개 자격증명의 구분")
    d.rect(0, 30, 560, 116, "n2", 6)
    d.text(16, 14, "Firebase 프로젝트", 20, "t2 b", anchor="start")
    d.node(20, 50, 230, 80, "웹 앱 등록", "n", 22, "b", sub="웹 앱 구성 생성", sfs=19 + 1)
    d.arrow(256, 90, 300, 90, "ln", "ink")
    d.node(306, 50, 236, 80, "firebaseConfig", "nteal", 22, "mono b", sub="apiKey 포함 · 프로젝트 식별", sfs=20, scls="tteal m")
    d.rect(306, 0, 236, 32, "fteal", 4)
    d.text(424, 16, "공개해도 OK", 20, "tw b")
    d.add('<line x1="600" y1="20" x2="600" y2="146" class="rule"/>')
    d.rect(640, 30, 512, 116, "naw", 6)
    d.rect(640, 0, 512, 32, "fa", 4)
    d.text(896, 16, "절대 공개 금지 · 서버 측 자격증명", 20, "tw b")
    d.text(660, 72, "서비스 계정 키(JSON)", 22, "b", anchor="start")
    d.text(660, 110, "AI 서비스 키(Gemini 등) · 외부 서비스 비밀 키", 21, "m", anchor="start")
    steps = re.sub(r"<ul><li><span class=\"ph\">.*?</span></li></ul>", "", p["diag"].split("<p>비교 카드")[0])
    ph = re.findall(r'<span class="ph">.*?</span>', p["diag"])
    return ('<div class="body stack con51 ovc"><div class="vis">%s</div><div class="row2"><div class="col ovc">%s</div><div class="col csteps ovc">%s%s</div></div></div>%s'
            % (d.svg(), p["body"], steps, "".join(ph), band(p["result"], p["stuck"]))), "", 26


# ---- 37: Authentication 흐름 + 쓰는 상황
def ov_37(p):
    its = li_texts(p["body_raw"])
    W = 1152
    d = D(W, 110, "학생이 구글 계정으로 로그인하면 Authentication이 사용자를 인증하고 고유 번호 uid를 발급한다")
    items = ["구글 계정 로그인", "사용자 인증\nAuthentication", "고유 번호(uid)"]
    x0 = (W - hflow_width(items, 22, 70)) / 2 + 40
    ic_person(d, x0 - 80, 60, 1.25, "fi3")
    d.text(x0 - 80, 104, "학생", 20, "t2 m")
    d.add('<path d="M%g 56 H%g" class="ln" marker-end="url(#ah-ink)"/>' % (x0 - 52, x0 - 8))
    hflow(d, x0, 18, items, 76, 22, 70, cls=["n", "noch", "nk"])
    uses = re.findall(r"[①②]\s*([^①②]+)", its[1]) if len(its) > 1 else []
    nouse = its[2].split(":", 1)[1].strip() if len(its) > 2 and ":" in its[2] else ""
    cards = "".join('<div class="card good"><div class="ey">쓰는 상황 %d</div><p>%s</p></div>' % (i + 1, inline(u.strip())) for i, u in enumerate(uses))
    cards += '<div class="card mute"><div class="ey">안 쓰는 상황</div><p>%s</p></div>' % inline(nouse)
    return ('<div class="body stack ovc"><div class="lead"><p>%s</p></div><div class="vis">%s</div><div class="cards c3 use">%s</div></div>'
            % (inline(its[0]), d.svg(), cards)), "", 30


def use_split(p, svg, ratio="r46"):
    """사용 상황 슬라이드: 왼쪽 정의 + 쓴다/안 쓴다, 오른쪽 도식."""
    its = li_texts(p["body_raw"])
    h = '<p class="def">%s</p>' % inline(its[0])
    for t in its[1:]:
        k, _, v = t.partition(":")
        cls = "nouse" if k.strip().startswith("안 쓴다") else "use"
        if k.strip() in ("쓴다", "안 쓴다"):
            items = [x.strip() for x in re.split(r"[①②]", v) if x.strip()]
            h += '<div class="uk %s"><span>%s</span>%s</div>' % (cls, esc(k.strip()), "".join("<p>%s</p>" % inline(x) for x in items))
        else:
            h += "<p>%s</p>" % inline(t)
    return L_split(p, svg, ratio, left=h), "", 28


# ---- 39: Firestore 데이터 구조
def ov_39(p):
    d = D(640, 420, "Firestore 데이터 구조: 컬렉션 안에 문서, 문서 안에 필드")
    d.rect(20, 120, 330, 290, "n2", 4)
    d.add('<rect x="20" y="120" width="330" height="290" rx="4" fill="none" stroke="var(--ink-3)" stroke-width="2"/>')
    # 열린 서랍(users/{uid})
    d.rect(0, 60, 370, 130, "n", 4)
    d.add('<rect x="0" y="60" width="370" height="130" rx="4" fill="none" stroke="var(--ochre)" stroke-width="2"/>')
    for k, xx in enumerate((40, 150, 260)):
        d.add('<path d="M%d 66 v-50 h22 l8 -10 h40 v60 z" class="noch"/>' % xx)
        for j in range(3):
            d.add('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="var(--ochre)" stroke-width="2"/>' % (xx + 10, 26 + j * 12, xx + 58, 26 + j * 12))
    d.rect(110, 116, 150, 46, "nk", 3)
    d.text(185, 139, "users/{uid}", 20, "tp b mono")
    # 닫힌 서랍(classes/{classId})
    d.rect(40, 230, 290, 120, "n", 4)
    d.rect(80, 270, 210, 46, "nk", 3)
    d.text(185, 293, "classes/{classId}", 20, "tp b mono")
    d.rect(160, 330, 50, 10, "fi3", 3)
    # 설명선
    for (yy, ty, a, b) in ((40, 30, "필드", "문서의 키·값"), (110, 110, "문서", "필드의 묶음"), (190, 200, "컬렉션", "문서의 묶음")):
        d.line([(372 if yy != 190 else 352, yy), (432, ty)], "ln mute", None)
        d.text(442, ty - 13, a, 22, "b", anchor="start")
        d.text(442, ty + 15, "= " + b, 21, "to m", anchor="start")
    return use_split(p, d.svg())


# ---- 41: Spark vs Blaze
def ov_41(p):
    tbl = table_from(p["diag_rest"])
    tbl = tbl.replace("<td>사용 불가</td>", '<td class="na">사용 불가</td>')
    head = ('<div class="plans"><div class="pl spark"><b>Spark</b><span>무료 요금제</span><small>무료 한도 안에서만</small></div>'
            '<div class="pl blaze"><b>Blaze</b><span>종량제 요금제</span><small>한도 안은 무료, 넘으면 청구</small></div></div>')
    return L_split(p, head + '<div class="ptbl">%s</div>' % tbl, "r30"), "", 28


# ---- 43: Storage vs Firestore
def ov_43(p):
    d = D(640, 400, "큰 파일은 Storage(객체 저장), 짧은 글은 Firestore(문서 DB)로")
    d.node(0, 40, 220, 84, "이미지·PDF·영상\n같은 파일", "n", 22, "b")
    d.node(0, 250, 220, 84, "짧은 글·\nHTML 텍스트", "n", 22, "b")
    d.arrow(226, 82, 330, 82, "ln acc thick", "acc")
    d.arrow(226, 292, 350, 292, "ln teal thick", "teal", "문서 한도 1MiB", 20, "t3 m", ldy=-20)
    # 창고
    d.add('<path d="M340 60 L470 10 L600 60 V170 H340 Z" class="naw"/>')
    d.rect(440, 110, 60, 60, "n", 2)
    d.text(470, 76, "파일 저장", 22, "ta b")
    d.text(470, 196, "Storage", 22, "b mono")
    d.rect(520, 0, 120, 32, "na", 16)
    d.text(580, 16, "Blaze 필요", 20, "tw b")
    # 서류함
    d.rect(360, 236, 220, 120, "nteal", 4)
    for k in range(2):
        d.rect(380, 250 + k * 52, 180, 40, "n", 3)
        d.rect(450, 266 + k * 52, 40, 8, "fteal", 2)
    d.text(470, 380, "문서 저장 · Firestore", 22, "tteal b")
    return use_split(p, d.svg())


# ---- 44: Firestore / Storage / 올리지 않음
def ov_44(p):
    its = li_texts(p["body_raw"])
    qs = re.findall(r"([^?*]+\?)", its[0].replace("**", ""))
    opts = ["Firestore", "Storage", "올리지 않음"]
    rows = "".join('<div class="qc"><div class="qq">%s</div><div class="qo">%s</div></div>'
                   % (esc(q.strip()), "".join('<span><i class="box"></i>%s</span>' % o for o in opts)) for q in qs)
    q2 = dict(p)
    q2["body"] = "<ul>%s</ul>" % "".join("<li>%s</li>" % inline(t) for t in its[1:])
    return L_question(q2, '<div class="qgrid">%s</div>' % rows), "", 34


# ---- 46: Hosting 공개 주소
def ov_46(p):
    d = D(620, 400, "Hosting: PROJECT_ID.web.app 공개 주소로 정적 파일을 배포하며, 개인정보 파일은 올리지 않는다")
    d.rect(40, 70, 540, 250, "noch", 4)
    d.add('<rect x="40" y="70" width="540" height="250" rx="4" fill="none" stroke="var(--ochre-2)" stroke-width="3"/>')
    d.rect(150, 30, 320, 56, "nk", 4)
    d.text(310, 58, "PROJECT_ID.web.app", 23, "tp b mono")
    for k, xx in enumerate((80, 250, 420)):
        d.rect(xx, 120, 120, 150, "n", 2)
        d.circle(xx + 60, 124, 6, "na")
        for j in range(4):
            d.add('<line x1="%d" y1="%d" x2="%d" y2="%d" class="rule"/>' % (xx + 16, 160 + j * 24, xx + 104 - (j % 2) * 24, 160 + j * 24))
    d.rect(40, 340, 540, 52, "naw", 3)
    d.text(310, 366, "개인정보 파일은 올리지 않는다", 22, "ta b")
    return use_split(p, d.svg())


# ---- 48: 배포 전에 사람이 꼭 볼 것 3가지
def ov_48(p):
    vis = ('<div class="blanks"><div class="bl"><b>①</b><i></i></div><div class="bl"><b>②</b><i></i></div><div class="bl"><b>③</b><i></i></div>'
           '<span class="stamp big" title="사람이 확인하는 단계">확인</span></div>')
    return L_question(p, vis), "", 36


# ---- 49: Cloud Functions 서버 측 호출
def ov_49(p):
    d = D(660, 330, "학생 브라우저에는 키가 없고, Cloud Functions가 서버 측에 보관한 AI 키로 AI 서비스를 호출한다")
    d.rect(0, 70, 180, 150, "n", 6)
    d.rect(0, 70, 180, 26, "n2", 6)
    for k in range(3):
        d.circle(16 + k * 14, 83, 4, "fi3")
    d.text(90, 140, "학생 브라우저", 22, "b")
    d.rect(30, 172, 120, 32, "nm", 16)
    d.text(90, 188, "키 없음", 20, "t3 b")
    d.arrow(186, 145, 236, 145, "ln", "ink")
    d.rect(242, 40, 220, 210, "noch", 6)
    d.text(352, 74, "서버 측", 24, "to b")
    d.text(352, 104, "Cloud Functions", 20, "b mono")
    d.rect(290, 132, 124, 96, "nk", 6)
    d.circle(352, 168, 14, "fw")
    d.rect(347, 168, 10, 22, "fw", 2)
    d.text(352, 212, "AI 키", 20, "tp b")
    d.text(352, 276, "서버에 보관한 AI 키", 20, "to m")
    d.arrow(468, 145, 520, 145, "ln acc thick", "acc")
    d.node(526, 110, 134, 70, "AI 서비스", "n", 22, "b")
    return L_split(p, d.svg(), "r38"), "", 28


# ---- 51: 상황 카드 4장
def ov_51(p):
    cards = diag_items(p)
    ans = re.search(r"내 답 칸:\s*`([^`]+)`", p["diag_rest"])
    h = '<ol class="sits">%s</ol>' % "".join('<li><p>%s</p><div class="sa">기능 <i></i> 요금제 Spark · Blaze</div></li>' % inline(c.strip('"“”')) for c in cards)
    return L_practice(p, main='<div class="grp">%s</div><div class="grp">%s</div>' % (h, p["prompt"])), "", 28


# ---- 52: 설정 체크리스트
def ov_52(p):
    tbl = chk_boxes(table_from(p["diag_rest"]))
    m = re.search(r"하단:\s*(.+)$", p["diag_rest"], re.M)
    after = '<div class="info">%s</div>' % inline(m.group(1)) if m else ""
    return L_table(p, '<div class="chkt">%s</div>' % tbl, after), "", 28


# ---- 53: 프로젝트 흐름 5단계 + 슬라이드 범위 + 폴더 트리(출처 구분) + 안전 원칙
def ov_53(p):
    W = 1152
    d = D(W, 410, "프로젝트 흐름 5단계: 단원 명세, 하네스 구성, 수업 슬라이드, 워크북 배포, 점검·공유. 작업 폴더 unit-project의 파일 출처와 안전 원칙 3가지")
    bw, gap = 204, 33
    rngs = ["54", "55", "56–57", "58–62", "63–64"]
    m = re.search(r"칸 아래에 슬라이드 번호 범위:\s*(.+?)\.\s", p["diag_raw"])
    if m:
        got = [x.strip() for x in re.split(r"[①②③④⑤]", m.group(1)) if x.strip()]
        if len(got) == 5:
            rngs = got
    steps = [("① 단원 명세", "unit-spec.md\n(내가 씀)", "nt"),
             ("② 하네스 구성", "팀 생성\n(계획은 내가 승인)", "nteal"),
             ("③ 수업 슬라이드", "slides.html", "n"),
             ("④ 워크북 배포", "workbook/ + 규칙\n+ 배포 주소", "nteal"),
             ("⑤ 점검 · 공유", "사람이 확인 · 짝 점검\n배포 주소 전달", "naw")]
    for i, (t, sub, cl) in enumerate(steps):
        x0 = i * (bw + gap)
        d.node(x0, 0, bw, 104, t, cl, 22, "b", sub=sub, sfs=17)
        if i < 4:
            d.arrow(x0 + bw + 4, 52, x0 + bw + gap - 4, 52, "ln", "ink")
        d.text(x0 + bw / 2.0, 126, "슬라이드 " + rngs[i], 19, "t3 m num")
    # 왼쪽 아래: 안전 원칙 3개
    d.text(0, 168, "지켜야 할 것", 19, "t2 b", anchor="start")
    for i, t in enumerate(["테스트 계정만", "실제 학생 정보 없음", "교과 내용은 교사 확인"]):
        d.node(0, 190 + i * 54, 440, 46, t, "naw", 21, "ta m", rx=23)
    # 오른쪽 아래: 폴더 트리 + 출처
    tx, ty, tw_, th = 490, 150, 662, 258
    d.rect(tx, ty, tw_, th, "n2", 4)
    d.add(ic_folder(tx + 16, ty + 10, 36, "ln"))
    d.text(tx + 62, ty + 28, "unit-project/", 21, "mono b", anchor="start")
    rows = [("├ unit-spec.md", 0), ("├ .claude/agents/", 1), ("├ .claude/skills/", 1), ("├ slides.html", 2),
            ("├ workbook/", 2), ("├ firestore.rules", 2), ("└ firebase.json", 2)]
    who = [("내가 씀", "nt", "tt", (0, 0)), ("하네스가 생성", "nteal", "tteal", (1, 2)), ("Claude Code가 생성", "n", "t2", (3, 6))]
    for i, (f, g) in enumerate(rows):
        d.text(tx + 28, ty + 62 + i * 28, f, 19, "mono m", anchor="start")
    for lab, cl, tc, (a, b) in who:
        y1 = ty + 62 + a * 28 - 13
        y2 = ty + 62 + b * 28 + 13
        d.add('<path d="M%g %g h8 v%g h-8" class="ln" style="stroke-width:2"/>' % (tx + 300, y1, y2 - y1))
        d.node(tx + 320, (y1 + y2) / 2.0 - 17, 322, 34, lab, cl, 19, tc + " b", rx=17)
    return L_stack(p, d.svg()), "", 28


# ---- 58: 사람 / Claude Code 역할 분담 두 열 카드 + 결과 띠
def ov_58(p):
    W, H = 760, 470
    d = D(W, H, "역할 분담: 내가 하는 일 3가지에서 Claude Code가 하는 일 5가지로 이어지고, 결과는 배포 주소")
    cw, ch = 330, 340
    rx0 = W - cw
    for x0, title, cl, items, hc in [(2, "내가 하는 일", "nt", ["M6 콘솔 설정\n완료 확인", "firebase login\n로그인 승인", "계획·명령 승인"], "tt b"),
                                     (rx0 - 2, "Claude Code가 하는 일", "nteal", ["웹앱 코드 작성", "연결 값 가져오기", "firestore.rules 작성", "배포", "주소 안내"], "tteal b")]:
        d.rect(x0, 2, cw, ch, cl, 8)
        d.text(x0 + cw / 2.0, 38, title, 25, hc)
        n = len(items)
        step = 54 if n == 5 else 84
        y1 = 98 if n == 5 else 130
        for i, t in enumerate(items):
            d.text(x0 + 22, y1 + i * step, ("%d  " % (i + 1)) + t.replace("\n", "\n    "), 22, "m", anchor="start")
    d.arrow(cw + 10, ch / 2.0 + 2, rx0 - 10, ch / 2.0 + 2, "ln acc thick", "acc")
    d.rect(0, 366, W, 100, "na", 8)
    d.text(W / 2.0, 394, "결과 : 배포 주소", 22, "tw b")
    d.text(W / 2.0, 436, "https://프로젝트ID.web.app", 28, "mono b tw")
    return L_split(p, d.svg(), "r46"), "", 28


# ---- 57, 62: 점검 4가지(① ② ③ ④ 점검표) + 선택 프롬프트 + 막힐 때
def ov_check4(p):
    its = li_texts(p["body_raw"])
    lead = its[0] if its else ""
    mk = [t for t in its[1:] if "①" in t]
    extra = [t for t in its[1:] if "①" not in t]
    marks = " ".join(mk)
    parts = [x.strip() for x in re.split(r"[①②③④⑤]", marks) if x.strip()]
    checks = '<ol class="checks">%s</ol>' % "".join('<li><i class="box"></i><span>%s</span></li>' % inline(t) for t in parts)
    right = lbl("점검표", "l-step") + checks
    if p["prompt"]:
        right += '<div class="grp">%s</div>' % p["prompt"]
    left = '<div class="lead ovc">%s</div>' % "".join("<p>%s</p>" % inline(t) for t in [lead] + extra)
    return L_split(p, right, "r46", left=left) + band(None, p["stuck"]), "", 26


# ---- 65: 체크리스트 6칸
def ov_65(p):
    its = li_texts(p["body_raw"])
    boxes = []
    for t in its[1:]:
        boxes += [x.strip(" ·") for x in t.split("☐") if x.strip(" ·")]
    grid = '<div class="six">%s</div>' % "".join('<div class="sx"><i class="box"></i><span>%s</span></div>' % inline(b) for b in boxes)
    note = '<p class="foot">나머지 4개는 배포 자료(노트의 10항목 목록)에</p>'
    return ('<div class="body stack ovc"><div class="lead"><p>%s</p></div><div class="vis">%s%s</div></div>%s'
            % (inline(its[0]), grid, note, band(p["result"], p["stuck"]))), "", 28


# ---- 66: 안티패턴 4가지
def ov_66(p):
    its = li_texts(p["body_raw"])
    cards = ""
    for t in its:
        a, _, b = t.partition("→")
        cards += '<div class="card bad anti"><div class="ey">안티패턴</div><h4>%s</h4><p><span class="rx">처방</span>%s</p></div>' % (inline(a.strip()), inline(b.strip()))
    return '<div class="body stack ovc"><div class="vis"><div class="cards c2 g2">%s</div></div></div>%s' % (cards, band(p["result"], p["stuck"])), "", 32


# ---- 67: 자주 묻는 질문 4가지
def ov_67(p):
    its = li_texts(p["body_raw"])
    m = re.search(r'"(Blaze가 필요한 것:[^"]+)"', p["diag_intro"])
    cards = ""
    for k, t in enumerate(its):
        q, _, a = t.partition(":")
        extra = '<p class="sm">%s</p>' % esc(m.group(1)) if (k == 3 and m) else ""
        cards += '<div class="card faq%s"><div class="ey">Q%d</div><h4>%s</h4><p>%s</p>%s</div>' % (" fb" if k == 3 else "", k + 1, inline(q.strip()), inline(a.strip()), extra)
    return '<div class="body stack ovc"><div class="vis"><div class="cards c2 g2">%s</div></div></div>%s' % (cards, band(p["result"], p["stuck"])), "", 32


# ---- 68: 참고 자료와 다음 걸음
def ov_68(p):
    its = li_texts(p["body_raw"])
    refs = []
    for t in its[:2]:
        for part in re.split(r"\s+·\s+(?=[가-힣 ]+:)", t):
            k, _, v = part.partition(":")
            refs.append((k.strip(), v.strip()))
    rl = "".join('<li><span class="rk">%s</span><span>%s</span></li>' % (esc(k), inline(v)) for k, v in refs)
    nxt = its[2] if len(its) > 2 else ""
    k, _, v = nxt.partition(":")
    v_txt = CAPTURE_RE.sub("", v).replace("``", "").strip(" +`")
    ph = CAPTURE_RE.search(v)
    m = re.search(r'"(\d{4}년[^"]+)"', p["diag_intro"])
    foot = '<p class="foot">%s</p>' % esc(m.group(1)) if m else ""
    vis = ('<div class="nextc"><div class="ey">%s</div><p>%s</p><div class="qr">%s</div></div>'
           % (esc(k.strip()), inline(v_txt), inline(ph.group(0)) if ph else ""))
    left = '<ul class="refs">%s</ul>%s' % (rl, foot)
    return ('<div class="body split r50 ovc"><div class="col ovc">%s</div><div class="col vis ovc">%s<p class="thanks">수고하셨습니다</p></div></div>%s'
            % (left, vis, band(p["result"], p["stuck"]))), "", 28


# ---- 58: 터미널 로그인 한 번 -> 컴퓨터에 저장 -> Claude Code 실행 -> 내 승인
def ov_login(p):
    W = 1152
    d = D(W, 330, "터미널 로그인 원리: 내가 한 번 로그인하면 컴퓨터에 저장되고, Claude Code가 같은 로그인으로 명령을 실행하며, 명령마다 내가 승인한다. 예: Firebase 배포, GitHub 올리기")
    steps = [("①", "내가 로그인", "터미널에서\n한 번만", "nt"),
             ("②", "컴퓨터에 저장", "내 컴퓨터에\n로그인 정보가 남음", "n"),
             ("③", "Claude Code 실행", "같은 로그인으로\n명령을 대신 실행", "n"),
             ("④", "내가 승인", "명령마다\n허용 여부 선택", "nt")]
    bw, gap = 240, 64
    for i, (nm, t, sub, cl) in enumerate(steps):
        x0 = i * (bw + gap)
        d.rect(x0, 0, bw, 150, cl, 4)
        d.rect(x0, 0, bw, 5, "ntf", 0)
        d.text(x0 + 20, 42, nm, 24, "tt b", anchor="start")
        d.text(x0 + 54, 42, t, 24, "b", anchor="start")
        d.text(x0 + 20, 96, sub, 21, "t2", anchor="start", lh=1.35)
        if i < 3:
            d.arrow(x0 + bw + 8, 75, x0 + bw + gap - 8, 75, "ln thick", "ink")
    for j, (tool, cmd, work) in enumerate([("Firebase", "firebase login", "프로젝트 조회, 배포를"),
                                           ("GitHub", "gh auth login", "저장소 만들기, 올리기를")]):
        y0 = 190 + j * 66
        d.rect(0, y0, W, 54, "n2", 4)
        d.text(24, y0 + 28, tool, 22, "b", anchor="start")
        d.text(190, y0 + 28, cmd, 22, "ta b mono", anchor="start")
        d.text(470, y0 + 28, "→  " + work + " Claude Code가 실행", 22, "t2", anchor="start")
    return L_stack(p, d.svg()), "", 30


# ---- 64: 패키지 한 장 회고 카드
def ov_64(p):
    made = ["<code>unit-spec.md</code>", "하네스 팀 <code>.claude/</code>", "<code>slides.html</code>",
            "<code>workbook/</code>", "<code>firestore.rules</code>"]
    c1 = '<ul class="rcl">%s</ul>' % "".join('<li><i class="box"></i><span>%s</span></li>' % t for t in made)
    card = ('<div class="rcg">'
            '<div class="rc"><div class="ey">만든 것</div>%s</div>'
            '<div class="rc"><div class="ey">막힌 곳과 푼 방법</div><div class="ln1"></div><div class="ln1"></div></div>'
            '<div class="rc"><div class="ey">다음 단원에 적용할 점</div><div class="ln1"></div><div class="ln1"></div></div></div>'
            '<div class="rcs"><span class="ey">공유 방법</span>'
            '<span class="pi"><i class="box"></i>배포 주소 전달</span><span class="pi"><i class="box"></i>폴더 압축</span>'
            '<span class="pi"><i class="box"></i>둘 다 하지 않음</span></div>'
            '<div class="info">공유 전 확인: 개인정보 없음 · 비밀 키 없음</div>' % c1)
    return L_stack(p, card), "", 30


OVERRIDES.update({20: ov_20, 24: ov_24, 25: ov_25, 26: ov_26, 31: ov_31, 32: ov_32,
                  34: ov_34, 35: ov_console, 36: ov_36, 37: ov_37, 38: ov_console, 39: ov_39, 40: ov_console,
                  41: ov_41, 42: ov_console, 43: ov_43, 44: ov_44, 45: ov_console, 46: ov_46, 47: ov_console,
                  48: ov_48, 49: ov_49, 50: ov_console, 51: ov_51, 52: ov_52,
                  53: ov_53, 57: ov_check4, 58: ov_login, 63: ov_check4, 64: ov_64,
                  65: ov_65, 66: ov_66, 67: ov_67, 68: ov_68})


def main():
    global GOALS
    slides = []
    for code in FILES:
        slides += parse_file(SRC / ("02_writer_%s_slides.md" % code))
    slides.sort(key=lambda s: s["n"])
    nums = [s["n"] for s in slides]
    if nums != list(range(1, 69)):
        sys.exit("슬라이드 번호가 1-68 연속이 아닙니다: %s" % nums)
    total = len(slides)
    for s in slides:
        SLIDE_MIN[s["n"]] = minutes_of(field_text(s, "노트"))
    for a, b, c, _ in MODULES:
        MOD_MIN[c] = sum(SLIDE_MIN[k] for k in range(a, b + 1) if k != BREAK_SLIDE)
    GOALS.update(load_goals_deck())
    GOALS.update(GOALS_NEW)
    parts = [build_slide(s, total) for s in slides]
    total_min = sum(s["min"] for s in slides)
    doc = (
        '<!DOCTYPE html>\n<html lang="ko"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        "<title>클로드 코드 기반 하네스 엔지니어링 교원 연수 (슬라이드)</title>"
        "<style>%s</style></head><body>%s"
        '<div id="viewport"><div id="stage">%s</div></div>'
        '<div id="notes" aria-live="polite"></div><div id="grid" role="dialog" aria-label="슬라이드 목차"></div>'
        '<div id="help">→ 다음 · ← 이전 · G 목차 · N 노트 · F 전체화면(한글 입력 상태에서도 가능) · P 인쇄</div>'
        '<pre id="report" style="display:none"></pre>'
        "<script>%s</script></body></html>\n" % (CSS, SVG_DEFS, "\n".join(parts), JS)
    )
    OUT.write_text(doc, encoding="utf-8")
    kinds = {}
    for s in slides:
        k = parse_type(field_text(s, "유형"))[0]
        kinds[k] = kinds.get(k, 0) + 1
    print("슬라이드 %d장, 시간 합계 %g분, 유형 %s" % (total, total_min, json.dumps(kinds, ensure_ascii=False)))
    missing = [s["n"] for s in slides if not s["min"]]
    if missing:
        print("노트에서 분을 못 찾은 슬라이드:", missing)
    print("출력:", OUT)


if __name__ == "__main__":
    main()
