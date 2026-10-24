#!/usr/bin/env python3
"""완성된 전체 덱에서 '하네스(M4·M5)'와 'Firebase(M6)' 슬라이드만 뽑아 별도 덱을 만든다.

입력: 하네스엔지니어링_교원연수_슬라이드.html (build_deck.py 산출물, 수정하지 않는다)
출력: 하네스_파이어베이스_슬라이드.html

원 덱의 슬라이드 HTML을 그대로 쓰고, 다음만 바꾼다.
  - 표지 1장 추가, 휴식(33)과 다른 모듈(M1~M3, M7, MW) 제외
  - 모듈 이름표 M4→M1, M5→M2, M6→M3, 슬라이드 번호·참조·진행 막대·레일 범위 다시 계산
  - 제외된 모듈(M7 프로젝트, 지난 실습 폴더)을 가리키는 문장 정리
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "하네스엔지니어링_교원연수_슬라이드.html"
OUT = HERE / "하네스_파이어베이스_슬라이드.html"

KEEP = list(range(20, 33)) + list(range(34, 53))          # M4(20-25) M5(26-32) M6(34-52)
MOD_OF = {"M4": "M1", "M5": "M2", "M6": "M3"}
NEWN = {old: i + 2 for i, old in enumerate(KEEP)}          # 표지가 1번
TOTAL = len(KEEP) + 1
TITLE = "Claude Code 하네스와 Firebase 기능 지도 (슬라이드)"


def num(m):
    return NEWN[int(m)]


def renumber_refs(t):
    """본문·노트 속 '슬라이드 N', 'N번', 'M4 23·24번' 같은 번호 참조를 새 번호로."""
    def mod_ref(m):                      # M4 23·24번 / M5 27 / M4 22번
        nums = [str(num(x)) for x in re.split(r"·", m.group(2))]
        return "%s번" % "·".join(nums)
    t = re.sub(r"(M[45]) (\d+(?:·\d+)*)(번?)", mod_ref, t)
    t = re.sub(r"슬라이드 (\d+)(?![–\d])", lambda m: "슬라이드 %d" % num(m.group(1)) if int(m.group(1)) in NEWN else m.group(0), t)
    t = re.sub(r"(?<![\d·])(\d+)번(?!째)", lambda m: "%d번" % num(m.group(1)) if int(m.group(1)) in NEWN else m.group(0), t)
    return t


def rewrite(sec, old_n, idx_in_mod, mod_total, mod_code, bars):
    """슬라이드 한 장을 새 덱 규칙으로."""
    new_n = NEWN[old_n]
    new_mod = MOD_OF[mod_code]
    # 본문·노트(푸터 제외)만 문장 치환
    foot_i = sec.index("<footer")
    foot_j = sec.index("</footer>") + len("</footer>")
    head, foot, tail = sec[:foot_i], sec[foot_i:foot_j], sec[foot_j:]

    def fix_text(t):
        t = renumber_refs(t)
        # 제외된 모듈을 가리키는 문장
        t = t.replace("(M7 60)", "")
        t = t.replace("(M7)", "")
        t = t.replace("시간상 하지 않고 M7 프로젝트에서 본격적으로 한다.", "시간상 하지 않는다.")
        t = t.replace("오늘 익힌 흐름은 M7 프로젝트에서 같은 방식으로 쓴다(단원 명세를 쓰고 하네스에게 팀 구성을 요청). 휴식 슬라이드는 별도(33)이다.",
                      "오늘 익힌 흐름(요청 → 읽기 → 고치기 → 실행)은 자기 교과 업무에도 같은 방식으로 쓸 수 있다.")
        t = t.replace("여기까지는 Claude Code 혼자와 대화하는 법이었다고 전환한다.", "Claude Code 기본 사용법을 안다는 전제에서 시작한다고 전환한다.")
        t = t.replace(">M4</text>", ">M1</text>")
        t = t.replace("M7에서 만든 워크북을 계속 쓸 사람은 삭제하지 않는다.", "이 프로젝트로 앱을 계속 만들 사람은 삭제하지 않는다.")
        t = t.replace("M7에서 ", "")
        t = re.sub(r"M([456])에서", lambda m: MOD_OF["M" + m.group(1)] + "에서", t)
        t = t.replace("지난 실습 폴더(<code>claude-training</code>) 바로 아래에 만들어도 된다", "원하는 위치에 만들어도 된다")
        t = t.replace("다음 M5", "다음 M2")
        t = re.sub(r"\bM([45]) ", lambda m: MOD_OF["M" + m.group(1)] + " ", t)
        t = t.replace("다음: Firebase(M6)", "다음: Firebase(M3)")
        t = t.replace("Firebase(M6)", "Firebase(M3)")
        return t

    head = fix_text(head)
    tail = fix_text(tail)
    # 속성·id
    head = head.replace('id="s%d"' % old_n, 'id="s%d"' % new_n, 1)
    head = head.replace('data-n="%d"' % old_n, 'data-n="%d"' % new_n, 1)
    head = head.replace('data-module="%s"' % mod_code, 'data-module="%s"' % new_mod, 1)
    head = head.replace("<b>%s</b>" % mod_code, "<b>%s</b>" % new_mod, 1)
    head = head.replace('<span class="rn">%s</span>' % mod_code[1:], '<span class="rn">%s</span>' % new_mod[1:], 1)
    head = re.sub(r"(<dt>슬라이드</dt><dd>)[^<]*(</dd>)",
                  lambda m: "%s%s%s" % (m.group(1), RANGE[mod_code], m.group(2)), head)
    tail = re.sub(r'(<div class="nmeta">)슬라이드 \d+ · M\d',
                  lambda m: "%s슬라이드 %d · %s" % (m.group(1), new_n, new_mod), tail)
    # 푸터: 모듈 진행 막대와 쪽 번호
    segs = []
    for code in ("M4", "M5", "M6"):
        cnt = COUNT[code]
        if code == mod_code:
            cls, w = "cur", 100.0 * (idx_in_mod + 1) / mod_total
        elif ("M4", "M5", "M6").index(code) < ("M4", "M5", "M6").index(mod_code):
            cls, w = "past", 100.0
        else:
            cls, w = "fut", 0.0
        segs.append('<i class="%s" style="flex:%d"><b style="width:%.1f%%"></b></i>' % (cls, cnt, w))
    foot = re.sub(r'<span class="ft-bar">.*?</span>', '<span class="ft-bar">%s</span>' % "".join(segs), foot, flags=re.S)
    foot = re.sub(r'<span class="ft-num">.*?</span>',
                  '<span class="ft-num"><b>%d</b> / %d</span>' % (new_n, TOTAL), foot, flags=re.S)
    return head + foot + tail


def cover(sec1, minutes):
    """원 덱 표지의 마크업·도식을 재사용해 새 표지로."""
    s = sec1
    s = s.replace('class="slide k-정리 cover"', 'class="slide k-정리 cover"', 1)
    s = re.sub(r'data-min="\d+"', 'data-min="1"', s, count=1)
    s = s.replace('data-module="M1"', 'data-module="M1"', 1)
    s = s.replace("<b>M1</b>도입 · Claude Code 첫 대화", "<b>개요</b>하네스 · Firebase", 1)
    s = s.replace('<h2 class="title">Claude Code로 배우는 하네스 엔지니어링</h2>',
                  '<h2 class="title">Claude Code 하네스와 Firebase</h2>', 1)
    s = re.sub(r'<h1 class="cv-t">.*?</h1>',
               '<h1 class="cv-t">Claude Code 하네스와<br><span>Firebase 기능 지도</span></h1>', s, count=1, flags=re.S)
    s = re.sub(r'<p class="cv-s">.*?</p>',
               '<p class="cv-s">하네스로 팀을 만들어 고치고, Firebase 기능을 골라 설정한다 (약 %d분)</p>' % minutes, s, count=1)
    # '가져갈 것' 3개: 원 덱의 아이콘 3개를 재사용
    items = re.findall(r"<li>(<svg.*?</svg>)<div><span class=\"gn\">(.)</span>.*?</div></li>", s, flags=re.S)
    texts = ["하네스로 만든 팀 파일을 읽고, 말로 고쳐 다시 실행해 보는 경험",
             "Firebase 6개 기능을 언제 쓰는지 고르는 기준",
             "콘솔에서 인증과 데이터베이스를 직접 설정한 내 테스트 프로젝트"]
    lis = "".join('<li>%s<div><span class="gn">%s</span>%s</div></li>' % (svg, gn, t)
                  for (svg, gn), t in zip(items, texts))
    s = re.sub(r'(<div class="cv-g"><div class="lbl ">)[^<]*(</div><ol>).*?(</ol>)',
               lambda m: "%s시작 전 준비 + 가져갈 것 3개%s%s%s" % (m.group(1), m.group(2), lis, m.group(3)), s, count=1, flags=re.S)
    foot_i = s.index("<footer")
    foot_j = s.index("</footer>") + len("</footer>")
    segs = "".join('<i class="%s" style="flex:%d"><b style="width:%s"></b></i>'
                   % ("cur" if i == 0 else "fut", COUNT[c], "100.0%" if i == 0 else "0.0%")
                   for i, c in enumerate(("M4", "M5", "M6")))
    foot = s[foot_i:foot_j]
    foot = re.sub(r'<span class="ft-tr">.*?</span>', '<span class="ft-tr">하네스 · Firebase</span>', foot, count=1)
    foot = re.sub(r'<span class="ft-bar">.*?</span>', '<span class="ft-bar">%s</span>' % segs, foot, flags=re.S)
    foot = re.sub(r'<span class="ft-num">.*?</span>', '<span class="ft-num"><b>1</b> / %d</span>' % TOTAL, foot, flags=re.S)
    notes = (
        '<div class="notes"><div class="nmeta">슬라이드 1 · 개요 · 소요 1분</div>'
        "<p>이 덱은 전체 연수에서 하네스(revfactory/harness)와 Firebase 부분만 따로 뗀 것이다. "
        "앞부분(Claude Code 설치·첫 대화, 프롬프트, CLAUDE.md·스킬)은 이미 알고 있다고 전제한다. "
        "시작 전 확인: ① Claude Code가 설치되어 로그인되어 있다(Pro·Max·Team·Enterprise 또는 Console 계정) "
        "② Firebase 실습용 개인 구글 계정(학교 관리 계정은 프로젝트 생성이 막힐 수 있음) "
        "③ 실제 학생 이름·계정은 쓰지 않는다. "
        "M1·M2(하네스)는 39분, M3(Firebase)는 27분이다. 두 부분은 서로 독립이라 하나만 써도 된다. (1분)</p></div>"
    )
    return s[:foot_i] + foot + notes + "</section>"


COUNT, RANGE = {}, {}


def main():
    h = SRC.read_text(encoding="utf-8")
    pre, _, body = h.partition('<div id="stage">')
    stage, _, post = body.partition('</div></div><div id="notes"')
    if not post:
        sys.exit("stage 끝 경계를 찾지 못했다: 원 덱 구조가 바뀌었는지 확인")
    # 슬라이드 분리
    secs = re.split(r"(?=<section class=\"slide)", stage)
    head_html, secs = secs[0], secs[1:]
    by_n = {int(re.search(r'data-n="(\d+)"', s).group(1)): s for s in secs}
    mod_of = {n: re.search(r'data-module="(M\d)"', by_n[n]).group(1) for n in KEEP}
    for code in ("M4", "M5", "M6"):
        ns = [n for n in KEEP if mod_of[n] == code]
        COUNT[code] = len(ns)
        RANGE[code] = "%d–%d" % (NEWN[ns[0]], NEWN[ns[-1]])
    out = []
    minutes = 0
    for code in ("M4", "M5", "M6"):
        ns = [n for n in KEEP if mod_of[n] == code]
        for i, n in enumerate(ns):
            minutes += int(re.search(r'data-min="(\d+)"', by_n[n]).group(1))
            out.append(rewrite(by_n[n], n, i, len(ns), code, None))
    first = cover(by_n[1], minutes)
    doc = pre.replace("<title>클로드 코드 기반 하네스 엔지니어링 교원 연수 (슬라이드)</title>", "<title>%s</title>" % TITLE)
    doc += '<div id="stage">' + head_html + first + "\n".join(out) + '</div></div><div id="notes"' + post
    doc = doc.replace("] 하네스 엔지니어링 교원 연수'", "] 하네스와 Firebase'")
    OUT.write_text(doc, encoding="utf-8")
    print("슬라이드 %d장, 약 %d분 → %s" % (TOTAL, minutes, OUT))


if __name__ == "__main__":
    main()
