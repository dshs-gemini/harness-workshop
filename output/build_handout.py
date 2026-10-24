#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""하네스 엔지니어링 교원연수 인쇄용 교재판 조립기.

입력 : _workspace/deck/02_writer_M1..M5,M6,M7,MW_slides.md (슬라이드 1-68), 01_designer_curriculum.md(모듈 학습 목표)
출력 : output/하네스엔지니어링_교원연수_교재.html (A4 세로, 외부 의존 없음)
       output/하네스엔지니어링_교원연수_교재.pdf  (Chrome이 있을 때만; 목차 쪽 번호 계산에도 쓴다)
사용 : python3 output/build_handout.py [--no-pdf]

발표용 덱(build_deck.py)의 파서·인라인·블록 렌더 함수를 import해서 재사용한다.
build_deck.py는 수정하지 않으므로 발표용 산출물은 그대로다.
쪽 번호는 2회 조립으로 채운다: 1회차 HTML -> Chrome PDF -> 슬라이드별 첫 쪽 추출 -> 2회차 HTML(목차 쪽 번호).
"""
import html
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_deck as bd  # noqa: E402

OUT = bd.ROOT / "output" / "하네스엔지니어링_교원연수_교재.html"
PDF = OUT.with_suffix(".pdf")
CURRICULUM = bd.SRC / "01_designer_curriculum.md"
CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "google-chrome", "chromium", "chrome",
]
TITLE = "클로드 코드 기반 하네스 엔지니어링 교원 연수"
KIND_NOTE = {"개념": "개념", "실습": "실습", "점검": "점검", "정리": "정리"}


SANS_LIT = '"Apple SD Gothic Neo","Malgun Gothic","Noto Sans KR",sans-serif'
SERIF_LIT = '"AppleMyungjo","Noto Serif KR","Nanum Myeongjo","Batang",serif'


def esc(t):
    return html.escape(t, quote=False)


# ----------------------------------------------------------------- 모듈 정보
def load_goals():
    """설계서 모듈표에서 학습 목표·실습 산출물을 읽는다."""
    info = {}
    if not CURRICULUM.exists():
        return info
    for ln in CURRICULUM.read_text(encoding="utf-8").split("\n"):
        if not re.match(r"^\|\s*M\d", ln):
            continue
        c = [x.strip() for x in ln.strip().strip("|").split("|")]
        if len(c) >= 8:
            info[c[0]] = {"goal": c[6], "output": c[7]}
    # 설계서(수정하지 않음)의 M4·M5·M7 목표·산출물은 옛 구성 기준이라 새 구성으로 덮어쓴다(덱 빌더와 같은 목표 문구).
    for code, goal in bd.GOALS_NEW.items():
        info.setdefault(code, {"goal": "", "output": ""})["goal"] = goal
    info.setdefault("M4", {})["output"] = "`mini-harness/.claude/` (퀴즈 만드는 에이전트 + 검수 에이전트 + 오케스트레이터 스킬)"
    info.setdefault("M5", {})["output"] = "고친 `.claude/agents/*.md` + 내 업무용 새 팀"
    info.setdefault("M6", {})["output"] = "인증(Google 로그인)과 Firestore 설정을 마친 Firebase 테스트 프로젝트"
    info.setdefault("M7", {})["output"] = "`unit-project/` (`unit-spec.md`, `.claude/`, `slides.html`, `workbook/`, `firestore.rules`) + 배포 주소"
    return info


ROADMAP = (
    '<div class="roadmap"><div class="rh">Claude Code 기본과 하네스 활용 (M1–M5)</div><div class="rr">'
    + '<span class="arr">→</span>'.join('<span class="chip">%s</span>' % t for t in
        ["M1 첫 대화", "M2 프롬프트", "M3 CLAUDE.md·스킬", "M4 하네스 입문", "M5 하네스 파일 고치기"])
    + '</div><div class="rh">쉬는 시간 10분 후, Firebase와 프로젝트 (M6–M7)</div><div class="rr">'
    + '<span class="arr">→</span>'.join('<span class="chip">%s</span>' % t for t in
        ["M6 Firebase 지도", "M7 수업 패키지 프로젝트"])
    + "</div></div>"
)


# ----------------------------------------------------------------- 슬라이드 블록
def clean(h):
    return h.replace('<button class="copy" type="button">복사</button>', "")


def build_block(s, total):
    n = s["n"]
    code, mname = bd.module_of(n)
    kind, tags = bd.parse_type(bd.field_text(s, "유형"))
    raw_note = bd.field_text(s, "노트")
    mins = bd.minutes_of(raw_note)
    s["min"] = mins
    body_tokens, note_tokens = [], []

    body_raw = bd.field_text(s, "본문")
    diag_raw = bd.field_text(s, "도식")
    prompt_raw = bd.field_text(s, "프롬프트")
    result_raw = bd.field_text(s, "예상 결과")
    stuck_raw = bd.field_text(s, "막힐 때")
    if "콘솔 직접 조작" in "\n".join(s["f"].get("프롬프트", [])):
        tags.append("콘솔 직접 조작")
    diag_intro, diag_rest = bd.split_diagram(diag_raw) if diag_raw else ("", "")

    if "☐" in body_raw:  # 한 줄에 여러 ☐가 있으면 항목으로 쪼갠다(덱과 동일)
        out_l = []
        for l in body_raw.split("\n"):
            if l.count("☐") > 1:
                ind = l[: len(l) - len(l.lstrip())]
                out_l += [ind + "- ☐ " + x.strip() for x in re.split(r"\s*·?\s*☐\s*", l.lstrip("- ").strip()) if x.strip()]
            else:
                out_l.append(l)
        body_raw = "\n".join(out_l)

    body_html = bd.render_blocks(body_raw, body_tokens)
    diag_rest = re.sub(r"^(\s*[-*]\s+)(?:표\(원본 그대로\):?|`\.(?:flow|steps|grid2)`[^:\n]{0,20}:)\s*", r"\1", diag_rest, flags=re.M)
    diag_html = bd.render_blocks(diag_rest, body_tokens) if diag_rest else ""
    prompt_html = bd.render_blocks(prompt_raw, body_tokens, "prompt") if prompt_raw else ""
    result_html = bd.render_blocks(result_raw, body_tokens, "result") if result_raw else ""
    stuck_html = bd.render_blocks(stuck_raw, body_tokens) if stuck_raw else ""
    if stuck_raw and not re.search(r"^\s*[-*]\s", stuck_raw, re.M) and re.search(r"\(2\)", stuck_raw):
        parts = [p.strip() for p in re.split(r"(?:^|\s)\(\d\)\s*", stuck_raw) if p.strip()]
        stuck_html = "<ul>" + "".join("<li>%s</li>" % bd.inline(p, body_tokens) for p in parts) + "</ul>"
    note_html = bd.render_blocks(raw_note, note_tokens)

    # 원고에 없던 마지막 슬라이드의 마무리 문구는 교재에서는 넣지 않는다(발표 장식).
    chk_items = []
    for t in body_tokens + note_tokens:
        if t not in chk_items:
            chk_items.append(t)
    has_check = bool(chk_items)

    if n == 2:  # 발표용 덱의 맞춤 도식(ov_map)에 해당하는 교재용 로드맵
        diag_html = ROADMAP + diag_html
    sec = []
    sec.append('<div class="sec main">%s</div>' % body_html)
    if diag_html:
        sec.append('<div class="sec diag"><div class="lbl">도식 · 단계</div>%s</div>' % diag_html)
    if prompt_html:
        sec.append('<div class="sec"><div class="lbl">프롬프트 · 파일</div>%s</div>' % prompt_html)
    if result_html:
        sec.append('<div class="sec"><div class="lbl">예상 결과</div>%s</div>' % result_html)
    if stuck_html:
        sec.append('<div class="sec stuck"><div class="lbl">막힐 때</div>%s</div>' % stuck_html)

    nt = '<div class="nmeta">소요 시간 %s분</div>' % (("%g" % mins) if mins else "-")
    nt += note_html
    if diag_intro:
        nt += '<div class="nx"><b>도식 설명</b> %s</div>' % bd.inline(diag_intro.replace("\n", " "), note_tokens)
    if chk_items:
        li = "".join("<li>%s</li>" % esc(t or "상세 없음") for t in chk_items)
        nt += '<div class="nx"><b>이 쪽의 확인 필요 항목 (연수 전 강사가 확인)</b><ul>%s</ul></div>' % li
    sec.append('<div class="sec notes"><div class="lbl">해설 · 발표자 노트</div>%s</div>' % nt)

    if kind in ("실습", "점검"):
        boxes = ""
        if kind == "실습":
            boxes = ('<div class="ck"><span>☐ 직접 해 보았다</span><span>☐ 예상 결과와 같았다</span>'
                     '<span>☐ 막혀서 도움을 받았다</span></div>')
        sec.append('<div class="sec memo">%s<div class="lbl">%s 메모</div><div class="ruled"></div></div>'
                   % (boxes, "실습" if kind == "실습" else "점검"))

    badges = '<span class="kind k-%s">%s</span>' % (kind, kind)
    badges += "".join('<span class="tag">%s</span>' % esc(t) for t in tags)
    if mins:
        badges += '<span class="tag">%g분</span>' % mins
    if has_check:
        badges += '<span class="chk">확인 필요</span>'
    return (
        '<article class="slide k-%s" id="s%d" data-n="%d">'
        '<header class="sh"><div class="sn">%d</div><div class="sm"><div class="sid">슬라이드 %d / %d</div>'
        '<h3 class="st">%s</h3></div><div class="badges">%s</div></header>%s</article>'
        % (kind, n, n, n, n, total, bd.inline(s["title"]), badges, clean("".join(sec)))
    )


# ----------------------------------------------------------------- 표지·목차·모듈 도입
def pg(pages, key):
    v = pages.get(key)
    return str(v) if v else "·"


def module_intro(code, name, slides, info, pages):
    a, b = slides[0]["n"], slides[-1]["n"]
    mins = sum(s["min"] for s in slides)
    g = info.get(code, {})
    rows = "".join(
        '<tr><td class="c">%d</td><td>%s</td><td class="c">%s</td><td class="c">%s</td><td class="c">%s</td></tr>'
        % (s["n"], bd.inline(s["title"]), bd.parse_type(bd.field_text(s, "유형"))[0],
           ("%g분" % s["min"]) if s["min"] else "-", pg(pages, s["n"]))
        for s in slides
    )
    dl = ""
    if g.get("goal") and g["goal"] != "—":
        dl += '<div class="gl"><div class="lbl">학습 목표</div><p class="goal">%s</p></div>' % bd.inline(g["goal"])
    meta = [("시간", "%g분" % mins), ("슬라이드", "%d–%d (%d장)" % (a, b, len(slides)))]
    if g.get("output") and g["output"] != "—":
        meta.append(("실습 산출물", bd.inline(g["output"])))
    mt = "".join("<dt>%s</dt><dd>%s</dd>" % (k, v) for k, v in meta)
    label = "모듈 %s" % code if code != "MW" else "마무리"
    return (
        '<section class="module" id="mod-%s"><div class="mi"><div class="mk">MODULE %s</div>'
        '<div class="mlabel">%s</div><h2 class="mt">%s</h2>%s<dl class="meta">%s</dl>'
        '<div class="lbl">이 모듈의 슬라이드</div><table class="mtab"><thead><tr><th>번호</th><th>제목</th><th>유형</th><th>시간</th><th>쪽</th></tr></thead>'
        "<tbody>%s</tbody></table></div>" % (code, code, label, esc(name), dl, mt, rows)
    )


def cover_html(total, total_min):
    return (
        '<section class="front cover"><div class="cv-top">교원 연수 교재</div>'
        '<h1>클로드 코드 기반<br>하네스 엔지니어링</h1>'
        '<p class="cv-sub">Claude Code로 반복 업무를 맡기는 팀을 설계하고, Firebase 기능 지도를 익힌다</p>'
        '<dl class="cv-meta"><dt>연수 시간</dt><dd>%g분 (3시간)</dd><dt>구성</dt><dd>7개 모듈 + 마무리, 슬라이드 %d장</dd>'
        '<dt>판형</dt><dd>A4 세로 인쇄용 교재판</dd><dt>제작</dt><dd>%s</dd></dl>'
        '<div class="cv-name"><span>소속</span><i></i><span>이름</span><i></i></div></section>'
        % (total_min, total, esc(bd.CREDIT))
    )


def usage_html():
    return (
        '<section class="front usage"><h2 class="ft">이 교재를 쓰는 법</h2>'
        "<p>슬라이드 한 장이 교재 한 항목입니다. 항목은 아래 순서로 읽습니다.</p>"
        '<ol class="seq"><li><b>본문</b> 슬라이드에 나오는 내용</li><li><b>도식 · 단계</b> 콘솔·화면에서 따라 할 순서</li>'
        "<li><b>프롬프트 · 파일</b> Claude Code에 입력하거나 저장할 문구</li><li><b>예상 결과</b> 성공했을 때 보이는 모습</li>"
        "<li><b>막힐 때</b> 자주 막히는 곳과 해결</li><li><b>해설</b> 발표자 노트. 왜 그렇게 하는지 설명</li></ol>"
        '<div class="lbl">표시 읽는 법</div>'
        '<table class="legend"><tbody>'
        '<tr><td><span class="kind k-개념">개념</span></td><td>설명을 듣고 이해하는 쪽</td></tr>'
        '<tr><td><span class="kind k-실습">실습</span></td><td>직접 손을 움직이는 쪽. 체크 칸과 메모 줄이 있습니다.</td></tr>'
        '<tr><td><span class="kind k-점검">점검</span></td><td>스스로 답해 보는 질문 쪽</td></tr>'
        '<tr><td><span class="kind k-정리">정리</span></td><td>한 모듈을 마무리하는 쪽</td></tr>'
        '<tr><td><span class="chk">확인 필요</span></td><td>콘솔 화면·메뉴 이름처럼 연수 전에 실제 화면으로 다시 확인해야 하는 내용</td></tr>'
        '<tr><td><span class="ph">설문 링크/QR</span></td><td>점선 상자는 강사가 연수 전에 링크를 채우는 자리</td></tr>'
        "</tbody></table>"
        '<div class="lbl">상자 읽는 법</div>'
        '<div class="prompt-box"><pre><code>붙여 넣어 쓰는 프롬프트는 이렇게 왼쪽 붉은 선이 있는 상자에 담깁니다.</code></pre></div>'
        '<div class="file-box"><div class="fb-title">파일 이름.md</div><pre><code>저장할 파일의 내용은 왼쪽 청록색 선이 있는 상자에 담깁니다.</code></pre></div>'
        "</section>"
    )


def toc_html(mods, pages):
    out = ['<section class="front toc"><h2 class="ft">목차</h2>']
    for code, name, slides in mods:
        label = "모듈 %s" % code if code != "MW" else "마무리"
        out.append('<div class="tm"><span class="tn">%s</span><span class="tt">%s</span><span class="tp">%s</span></div>'
                   % (label, "" if code == "MW" else esc(name), pg(pages, "mod-" + code)))
        out.append('<ol class="ts">%s</ol>' % "".join(
            '<li><span class="no">%d</span><span class="tl">%s</span><span class="tp">%s</span></li>'
            % (s["n"], bd.inline(s["title"]), pg(pages, s["n"])) for s in slides))
    out.append("</section>")
    return "".join(out)


# ----------------------------------------------------------------- CSS
def page_rules(mods):
    r = []
    for code, name, _ in mods:
        label = ("%s · %s" % (code, name)) if code != "MW" else name
        label = label.replace('"', "'")
        r.append('@page %s{@top-left{content:"%s";font:8.5pt @SANS@;color:#555;border-bottom:.4pt solid #999;'
                 'padding-bottom:2mm;vertical-align:bottom}'
                 '@top-right{content:"%s";font:8.5pt @SANS@;color:#555;border-bottom:.4pt solid #999;'
                 'padding-bottom:2mm;white-space:nowrap;vertical-align:bottom}'
                 '@bottom-center{content:counter(page);font:9pt @SERIF@;color:#333}}'
                 '.m-%s{page:%s}' % (code, label, TITLE, code, code))
    return "\n".join(r)


CSS = r"""
:root{
  --ink:#1c1c1c; --dim:#3c3c3c; --faint:#666; --rule:#c9c9c9; --soft:#f3f3f2; --soft2:#e9e8e6;
  --accent:#b0402c; --teal:#356e67; --gold:#7f5e1c;
  --serif:"Noto Serif KR","Nanum Myeongjo","AppleMyungjo","Source Han Serif K","Batang","Songti SC",serif;
  --sans:"Pretendard","Apple SD Gothic Neo","Malgun Gothic","Noto Sans KR","Nanum Gothic","Segoe UI",sans-serif;
  --mono:"JetBrains Mono","SF Mono","D2Coding",Consolas,"Liberation Mono","Apple SD Gothic Neo",monospace;
}
*{box-sizing:border-box}
html{background:#dcdcdb}
body{margin:0;font-family:var(--sans);font-size:10.5pt;line-height:1.65;color:var(--ink);word-break:keep-all;overflow-wrap:break-word;
  -webkit-print-color-adjust:exact;print-color-adjust:exact;orphans:3;widows:3}
main{width:210mm;margin:8mm auto;background:#fff;padding:18mm 16mm 20mm;box-shadow:0 2px 14px rgba(0,0,0,.25)}
h1,h2,h3{font-family:var(--serif);margin:0;font-weight:700;color:#111;break-after:avoid;page-break-after:avoid}
p{margin:.35em 0}
strong,b{font-weight:700}
.lbl{font-family:var(--sans);font-size:8.5pt;font-weight:700;letter-spacing:.06em;color:var(--teal);margin:.9em 0 .25em;break-after:avoid;page-break-after:avoid}

/* 표지·사용법·목차 */
.front,.module{break-after:page;page-break-after:always}
.cover{page:front;min-height:255mm;display:flex;flex-direction:column;padding-top:46mm}
.cv-top{font-family:var(--sans);font-size:11pt;letter-spacing:.3em;color:var(--accent);font-weight:700;border-top:2.2pt solid var(--accent);padding-top:5mm;width:62mm}
.cover h1{font-size:34pt;line-height:1.25;margin:10mm 0 8mm;letter-spacing:-.01em}
.cv-sub{font-size:12pt;color:var(--dim);max-width:130mm;line-height:1.7}
.cv-meta{margin:22mm 0 0;display:grid;grid-template-columns:28mm 1fr;gap:2mm 0;font-size:10.5pt}
.cv-meta dt{color:var(--faint)}.cv-meta dd{margin:0;font-weight:600}
.cv-name{margin-top:auto;display:flex;align-items:flex-end;gap:3mm;font-size:10.5pt;color:var(--dim)}
.cv-name i{flex:1;border-bottom:.6pt solid #888;height:6mm}
.front{page:front}
.ft{font-size:20pt;margin-bottom:6mm;padding-bottom:2mm;border-bottom:1.2pt solid #111}
.seq{margin:2mm 0 4mm;padding-left:5mm}.seq li{margin:.15em 0}
.legend{width:100%}.legend td{padding:2mm 3mm}.legend td:first-child{width:34mm;white-space:nowrap}
.toc{break-after:auto;page-break-after:auto}
.toc{page:front}
.tm{display:flex;gap:3mm;align-items:baseline;margin:3.2mm 0 .8mm;padding-bottom:.8mm;border-bottom:.6pt solid #777;font-family:var(--serif);font-weight:700;font-size:11pt;break-after:avoid;break-inside:avoid}
.tm .tn{color:var(--accent);min-width:19mm}.tm .tt{flex:1}
.ts{margin:0;padding:0;list-style:none;columns:1;font-size:8.6pt;line-height:1.38}
.ts li{display:flex;gap:2mm;padding:0 0 0 2mm;margin:0;break-inside:avoid;align-items:baseline}
.ts li:before{display:none}
.ts .no{width:7mm;text-align:right;color:var(--faint);font-variant-numeric:tabular-nums}
.ts .tl{flex:0 1 auto;max-width:150mm}
.ts li:after{content:"";flex:1;border-bottom:.6pt dotted #aaa;order:2;transform:translateY(-1mm)}
.tp{font-variant-numeric:tabular-nums;order:3;min-width:7mm;text-align:right}
.ts .tl{order:1}.ts .no{order:0}

/* 모듈 도입 쪽 */
.module{break-before:page;page-break-before:always;min-height:0}
.mi{padding-top:2mm}
.mk{font-family:var(--sans);font-size:9pt;letter-spacing:.3em;color:var(--accent);font-weight:700;border-top:2.2pt solid var(--accent);padding-top:3mm;width:48mm}
.mlabel{font-family:var(--serif);font-size:13pt;color:var(--faint);margin-top:4mm}
.mt{font-size:23pt;line-height:1.3;margin:1mm 0 4mm}
.goal{font-family:var(--serif);font-size:12.5pt;line-height:1.7;border-left:2pt solid var(--accent);padding:1mm 0 1mm 4mm;margin:1mm 0}
.meta{display:grid;grid-template-columns:28mm 1fr;margin:3mm 0 2mm;border-top:.5pt solid var(--rule)}
.meta dt,.meta dd{margin:0;padding:1.1mm 0;border-bottom:.5pt solid var(--rule);font-size:10pt}
.meta dt{color:var(--faint)}.meta dd{font-weight:600}
.mtab{font-size:8.6pt;line-height:1.3;margin-top:1mm}.mtab th,.mtab td{padding:.55mm 2mm}
.mtab td.c,.mtab th{text-align:center;white-space:nowrap}
.mtab td.c{font-variant-numeric:tabular-nums}
.mi{break-inside:auto}
.mod-slides{display:block}
.module+.slide{break-before:page}

/* 슬라이드 블록 */
.slide{margin:0 0 9mm;padding-top:3.5mm;border-top:.8pt solid #333;position:relative}
.slide + .slide{margin-top:0}
.sh{display:flex;gap:4mm;align-items:flex-start;break-after:avoid;page-break-after:avoid;break-inside:avoid;margin-bottom:2.5mm}
.sn{font-family:var(--serif);font-size:25pt;font-weight:700;color:var(--accent);line-height:1;min-width:13mm;padding-top:.5mm;font-variant-numeric:tabular-nums}
.sm{flex:1;min-width:0}
.sid{font-size:7.5pt;letter-spacing:.08em;color:var(--faint);line-height:1.3}
.st{font-size:14pt;line-height:1.38;letter-spacing:-.01em}
.badges{display:flex;flex-direction:row;flex-wrap:wrap;justify-content:flex-end;align-items:center;gap:1mm 1.2mm;flex:none;max-width:58mm}
.kind{display:inline-block;padding:0 3mm;font-family:var(--sans);font-size:8.5pt;font-weight:700;line-height:1.55;border:1pt solid #222;border-radius:1.2mm;white-space:nowrap;background:#fff;color:#111}
.k-실습 .kind,.kind.k-실습{background:var(--accent);border-color:var(--accent);color:#fff}
.k-개념 .kind,.kind.k-개념{background:#fff;color:#111}
.k-점검 .kind,.kind.k-점검{border-style:double;border-width:2.2pt;color:#111;background:#fff}
.k-정리 .kind,.kind.k-정리{background:#222;border-color:#222;color:#fff}
.tag{font-size:7.5pt;line-height:1.5;color:var(--dim);border:.5pt solid #999;border-radius:1mm;padding:0 1.6mm;white-space:nowrap}
.badges .chk{margin:0}
.chk{display:inline-block;font-family:var(--sans);font-size:6.8pt;font-weight:600;color:var(--gold);border-bottom:.5pt dotted var(--gold);line-height:1.3;vertical-align:super;white-space:nowrap;margin:0 .15em;letter-spacing:0}
.sec{margin:2.4mm 0}
.sec.main p,.sec.main li{margin-top:.2em}
.sec>.lbl:first-child{margin-top:.2em}
.slide.k-실습 .st{color:#111}

/* 목록 */
ul,ol{margin:.25em 0;padding:0;list-style:none}
li{position:relative;margin:.22em 0;padding-left:1.3em}
ul>li:before{content:"";position:absolute;left:.25em;top:.72em;width:.3em;height:.3em;border-radius:50%;background:var(--accent)}
ol{counter-reset:c}
ol>li{counter-increment:c;padding-left:1.9em}
ol>li:before{content:counter(c) ".";position:absolute;left:0;top:0;width:1.6em;text-align:right;font-weight:700;color:var(--accent);font-variant-numeric:tabular-nums}
li ul,li ol{font-size:.95em;margin:.1em 0}
li ul>li:before{background:var(--teal);width:.26em;height:.26em}
.diag ol>li{background:none;border:0}
.k-실습 .diag>ol>li,.k-실습 .main>ol>li{padding-left:3.1em}
.k-실습 .diag>ol>li:before,.k-실습 .main>ol>li:before{content:"\2610  " counter(c) ".";width:3em;text-align:left;color:var(--ink);font-weight:700}
.k-실습 .diag>ol>li{break-inside:avoid;page-break-inside:avoid}
li:has(>.ph)::before{display:none}

/* 코드·프롬프트·파일 */
code{font-family:var(--mono);font-size:.88em;background:var(--soft2);padding:0 .28em;border-radius:.8mm;color:#4a1f14;overflow-wrap:anywhere;word-break:break-all}
pre,code{font-variant-ligatures:none;font-feature-settings:"liga" 0,"calt" 0}
pre{margin:0;white-space:pre-wrap;overflow-wrap:anywhere;word-break:break-all;font-family:var(--mono);font-size:8.5pt;line-height:1.55}
pre code{background:none;padding:0;color:inherit;font-size:inherit;border-radius:0}
.prompt-box,.file-box,.terminal,.code-block{position:relative;background:var(--soft);color:#1c1c1c;border-left:1.6mm solid #777;padding:2.2mm 3.5mm;margin:1.6mm 0;break-inside:avoid;page-break-inside:avoid}
.prompt-box{border-left-color:var(--accent)}
.file-box{border-left-color:var(--teal)}
.terminal{border-left-color:#999;background:#f8f8f7;border-top:.4pt solid var(--rule);border-right:.4pt solid var(--rule);border-bottom:.4pt solid var(--rule)}
.fb-title{font-family:var(--mono);font-size:8pt;font-weight:700;color:var(--teal);margin-bottom:1.2mm;padding-bottom:1mm;border-bottom:.4pt solid var(--rule)}
.copy{display:none!important}
.flowline{display:inline-flex;flex-wrap:wrap;align-items:center;gap:.25em;vertical-align:baseline}
.chip{display:inline-block;padding:0 .5em;border:.7pt solid var(--teal);border-radius:1mm;font-size:.92em;background:#fff}
.arr{color:var(--accent);font-weight:700;margin:0 .1em}

/* 표 */
table{border-collapse:collapse;width:100%;font-size:9pt;line-height:1.45;margin:1.6mm 0;break-inside:avoid;page-break-inside:avoid}
th,td{border:.5pt solid #9a9a9a;padding:1.1mm 2mm;text-align:left;vertical-align:top}
th{background:var(--soft2);font-weight:700}
tr{break-inside:avoid;page-break-inside:avoid}
thead{display:table-header-group}
.mtab,.legend{break-inside:auto}
.legend td{border-left:0;border-right:0}

.roadmap{margin:1mm 0}.rh{font-size:8.5pt;font-weight:700;color:var(--teal);margin:1.5mm 0 1mm}.rr{display:flex;flex-wrap:wrap;gap:1.5mm;align-items:center;font-size:9pt}
/* 자리표시 */
.ph{display:flex;align-items:center;justify-content:center;min-height:22mm;margin:1.6mm 0;padding:2mm 4mm;border:1pt dashed #555;color:#444;font-size:9pt;font-weight:600;text-align:center;background:#fafafa;break-inside:avoid}
.legend .ph{display:inline-flex;min-height:0;margin:0;padding:0 2mm;font-size:8pt}

/* 막힐 때·해설·메모 */
.stuck{border:.5pt solid #aaa;border-left:1.6mm solid #aaa;padding:1mm 3.5mm 1.4mm;break-inside:avoid;page-break-inside:avoid}
.stuck .lbl{color:var(--accent);margin-top:.4em}
.stuck ul{margin:0}
.notes{margin-top:3.5mm;padding-top:1.6mm;border-top:.5pt dotted #888;font-size:9.5pt;line-height:1.6;color:var(--dim)}
.notes .lbl{color:var(--faint);margin-top:0}
.notes p{margin:.3em 0}
.nmeta{font-weight:700;color:var(--ink);font-size:9pt;break-after:avoid;page-break-after:avoid}
.sec>ul:has(+ .prompt-box),.sec>ul:has(+ .file-box),.sec>ul:has(+ .code-block),.sec>ul:has(+ .terminal),.sec>ol:has(+ .prompt-box),.sec>ol:has(+ .file-box),.sec>ol:has(+ .code-block),.sec>p:has(+ .prompt-box),.sec>p:has(+ .file-box),.sec>p:has(+ .code-block),.sec>p:has(+ .terminal){break-after:avoid;page-break-after:avoid}
.nx{margin-top:1.8mm;padding:1.4mm 3mm;background:var(--soft);font-size:9pt;break-inside:avoid}
.nx b{color:var(--ink)}
.notes .prompt-box,.notes .file-box,.notes .terminal,.notes .code-block{font-size:.95em}
.memo{break-inside:avoid;page-break-inside:avoid;margin-top:3.5mm}
.memo .lbl{margin-top:2mm}
.ck{display:flex;gap:6mm;font-size:9.5pt;color:var(--ink)}
.ruled{height:23mm;background-image:repeating-linear-gradient(to bottom,transparent 0,transparent 7.4mm,#aaa 7.4mm,#aaa calc(7.4mm + .4pt));border-bottom:.4pt solid #aaa}

@page{size:A4;margin:18mm 16mm 20mm;
  @bottom-center{content:counter(page);font:9pt @SERIF@;color:#333}}
@page front{margin:18mm 16mm 20mm;@top-left{content:none}@top-right{content:none}@bottom-center{content:counter(page);font:9pt @SERIF@;color:#333}}
@page cover{@bottom-center{content:none}}
@media print{
  html{background:#fff}
  main{width:auto;margin:0;padding:0;box-shadow:none}
  .cover{page:cover;min-height:258mm}
}
@media screen{
  .front,.module{border-bottom:1px dashed #bbb;margin-bottom:10mm}
}
"""


def build_html(slides, mods, info, pages):
    total = len(slides)
    total_min = sum(s["min"] for s in slides)
    body = [cover_html(total, total_min), usage_html(), toc_html(mods, pages)]
    for code, name, sl in mods:
        part = [module_intro(code, name, sl, info, pages)]
        part.append("</section>")  # module_intro는 섹션을 열어 둔다: 도입 쪽만 담고 닫는다
        wrap = '<div class="mwrap m-%s">%s' % (code, "".join(part))
        wrap += "".join(build_block(s, total) for s in sl)
        wrap += "</div>"
        body.append(wrap)
    css = CSS + "\n" + page_rules(mods)
    css = css.replace("@SANS@", SANS_LIT).replace("@SERIF@", SERIF_LIT)
    return (
        '<!DOCTYPE html>\n<html lang="ko"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        "<title>%s (교재)</title><style>%s</style></head><body><main>%s</main></body></html>\n"
        % (TITLE, css, "\n".join(body))
    )


# ----------------------------------------------------------------- PDF·쪽 번호
def find_chrome():
    for c in CHROME_CANDIDATES:
        p = shutil.which(c) or (c if Path(c).exists() else None)
        if p:
            return p
    return None


def make_pdf(chrome, html_path, pdf_path):
    """Chrome이 PDF를 쓴 뒤 종료하지 않는 경우가 있어, 파일 크기가 안정되면 프로세스를 끝낸다."""
    import time
    pdf_path = Path(pdf_path)
    if pdf_path.exists():
        pdf_path.unlink()
    with tempfile.TemporaryDirectory() as td:
        cmd = [chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--no-sandbox",
               "--user-data-dir=" + td, "--print-to-pdf=" + str(pdf_path), html_path.as_uri()]
        proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        last, stable, t0 = -1, 0, time.time()
        while time.time() - t0 < 240:
            if proc.poll() is not None:
                break
            size = pdf_path.stat().st_size if pdf_path.exists() else -1
            stable = stable + 1 if (size > 0 and size == last) else 0
            last = size
            if stable >= 3:
                break
            time.sleep(1)
        if proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(10)
            except subprocess.TimeoutExpired:
                proc.kill()
    if not pdf_path.exists() or pdf_path.stat().st_size == 0:
        raise RuntimeError("PDF가 만들어지지 않았습니다")


def page_map(pdf_path):
    from pypdf import PdfReader
    pages = {}
    reader = PdfReader(str(pdf_path))
    for i, p in enumerate(reader.pages, 1):
        txt = p.extract_text() or ""
        for m in re.finditer(r"슬라이드\s*(\d+)\s*/\s*68", txt):
            pages.setdefault(int(m.group(1)), i)
        for m in re.finditer(r"MODULE\s+(M\d|MW)", txt):
            pages.setdefault("mod-" + m.group(1), i)
    return pages, len(reader.pages)


def main():
    slides = []
    for code in bd.FILES:
        slides += bd.parse_file(bd.SRC / ("02_writer_%s_slides.md" % code))
    slides.sort(key=lambda s: s["n"])
    nums = [s["n"] for s in slides]
    if nums != list(range(1, 69)):
        sys.exit("슬라이드 번호가 1-68 연속이 아닙니다: %s" % nums)
    for s in slides:  # 분 계산(모듈 도입 쪽에서 합계를 쓴다)
        s["min"] = bd.minutes_of(bd.field_text(s, "노트"))
    mods = []
    for a, b, code, name in bd.MODULES:
        mods.append((code, name, [s for s in slides if a <= s["n"] <= b]))
    info = load_goals()

    pages = {}
    doc = build_html(slides, mods, info, pages)
    OUT.write_text(doc, encoding="utf-8")
    chrome = None if "--no-pdf" in sys.argv else find_chrome()
    if chrome:
        try:
            make_pdf(chrome, OUT, PDF)
            pages, npages = page_map(PDF)
            doc = build_html(slides, mods, info, pages)
            OUT.write_text(doc, encoding="utf-8")
            make_pdf(chrome, OUT, PDF)
            pages2, npages2 = page_map(PDF)
            print("쪽 수 %d (2회차 %d), 쪽 번호 변동 %s" % (npages, npages2, "없음" if pages2 == pages else "있음(재실행 필요)"))
        except Exception as e:  # noqa: BLE001
            print("PDF/쪽 번호 계산 실패(목차 쪽 번호는 '·'로 남음):", e)
    else:
        print("Chrome 없음: PDF 미생성, 목차 쪽 번호는 '·'")
    print("슬라이드 %d장, 시간 합계 %g분" % (len(slides), sum(s["min"] for s in slides)))
    print("출력:", OUT)


if __name__ == "__main__":
    main()
