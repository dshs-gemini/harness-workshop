# -*- coding: utf-8 -*-
# 54장 교원 연수 슬라이드를 단일 자체 포함 HTML로 생성한다.
# 입력: notes.json (발표자 노트), slides_a.js / slides_b.js 의 슬라이드 구성(아래에 Python으로 옮김)
# 출력: 온라인클래스룸_교원연수.html
import json, re, html, os, difflib

HERE = os.path.dirname(os.path.abspath(__file__))
NOTES = json.load(open(os.path.join(HERE, 'notes.json'), encoding='utf-8'))

INK = 'var(--ink)'; RED = 'var(--red)'; TEAL = 'var(--teal)'; CARD = 'var(--card)'; LINE = 'var(--line)'
MUTE = 'var(--mute)'; TEALT = 'var(--teal-t)'; REDT = 'var(--red-t)'; GOLD = 'var(--gold)'; GOLDL = 'var(--gold-l)'
BG = 'var(--bg)'; PAPER2 = 'var(--paper2)'; WHITE = '#fff'
MONO = 'mono'
PX = 100.0          # 1 inch = 100 stage px (스테이지 1333 x 750)
def pt(v): return round(v * 100 / 72, 2)
def n(v): return ('%.1f' % (v * PX)).rstrip('0').rstrip('.')
def esc(t): return html.escape(str(t), quote=True)
def rich(t):
    return esc(t).replace('\n', '<br>')

MARK = re.compile(r'\s*`?\[(?:재확인 필요|확인필요)[^\]]*\]`?')

S = []          # 현재 슬라이드의 조각들
SLIDES = []     # (번호, 모듈, 유형, 제목, html, 보조)
CODES = []      # 진단용

def put(s): S.append(s)

def pos(x, y, w, h):
    return 'left:%spx;top:%spx;width:%spx;height:%spx' % (n(x), n(y), n(w), n(h))

def T(text, x, y, w, h, fs=18, color=INK, b=False, al='left', va='top', font=None, extra='', cls='', runs=None):
    """텍스트 상자. runs=[(text, {'b':..,'color':..,'fs':..})]"""
    st = pos(x, y, w, h) + ';font-size:%spx;color:%s;text-align:%s' % (pt(fs), color, al)
    if b: st += ';font-weight:700'
    if font == MONO: st += ';font-family:var(--mono)'
    jc = {'top': 'flex-start', 'middle': 'center', 'bottom': 'flex-end'}[va]
    st += ';justify-content:%s' % jc
    if extra: st += ';' + extra
    if runs:
        inner = ''
        for rt, ro in runs:
            rs = ''
            if ro.get('b'): rs += 'font-weight:700;'
            if ro.get('color'): rs += 'color:%s;' % ro['color']
            if ro.get('fs'): rs += 'font-size:%spx;' % pt(ro['fs'])
            inner += '<span style="%s">%s</span>' % (rs, rich(rt))
    else:
        inner = rich(text)
    put('<div class="a %s" style="%s"><div class="t">%s</div></div>' % (cls, st, inner))

def R(x, y, w, h, fill='transparent', ln=None, lw=1.25, rad=0, dash=False, shape=None, extra='', cls=''):
    st = pos(x, y, w, h) + ';background:%s' % fill
    if ln: st += ';border:%spx %s %s' % (pt(lw), 'dashed' if dash else 'solid', ln)
    if rad: st += ';border-radius:%spx' % n(rad)
    if shape == 'ellipse': st += ';border-radius:50%'
    if extra: st += ';' + extra
    put('<div class="a %s" style="%s"></div>' % (cls, st))

def box(text, x, y, w, h, fs=18, fill=CARD, ln=LINE, lw=1.25, tc=INK, b=False, al='center', va='middle', font=None, margin=6, dash=False, rad=0.12, extra=''):
    st = pos(x, y, w, h) + ';background:%s;border:%spx %s %s;border-radius:%spx;font-size:%spx;color:%s;text-align:%s;padding:%spx;justify-content:%s' % (
        fill, pt(lw), 'dashed' if dash else 'solid', ln, n(rad), pt(fs), tc, al, pt(margin), {'top': 'flex-start', 'middle': 'center'}[va])
    if b: st += ';font-weight:700'
    if font == MONO: st += ';font-family:var(--mono)'
    if extra: st += ';' + extra
    put('<div class="a bx" style="%s"><div class="t">%s</div></div>' % (st, rich(text)))

def arrowR(x, y, w=0.32, color=MUTE):
    put('<div class="a ar-r" style="%s;background:%s"></div>' % (pos(x, y - .16, w, .32), color))
def arrowD(x, y, h=0.32, color=MUTE):
    put('<div class="a ar-d" style="%s;background:%s"></div>' % (pos(x - .16, y, .32, h), color))
def arrowU(x, y, h=0.9, color=MUTE):
    put('<div class="a ar-u" style="%s;background:%s"></div>' % (pos(x - .16, y, .32, h), color))

def flow(items, x, y, w, h, fs=18, gap=0.42, fill=None, color=None, arrow=MUTE):
    cnt = len(items); bw = (w - gap * (cnt - 1)) / cnt
    for i, it in enumerate(items):
        d = {'t': it} if isinstance(it, str) else it
        bx = x + i * (bw + gap)
        c = d.get('color') or color
        box(d['t'], bx, y, bw, h, fs=fs, fill=d.get('fill') or fill or CARD, ln=c or LINE, lw=2 if c else 1.25, tc=d.get('tc', INK), b=d.get('bold', False))
        if i < cnt - 1: arrowR(bx + bw + (gap - 0.3) / 2, y + h / 2, 0.3, arrow)

def placeholder(label, x, y, w, h, fs=16):
    st = pos(x, y, w, h) + ';font-size:%spx' % pt(fs)
    put('<div class="a ph" style="%s"><div class="t">%s</div></div>' % (st, rich(label)))

def code(lines, x, y, w, h, fs=15, label=None, key=None):
    idx = len(CODES)
    CODES.append({'lines': lines})
    if label:
        T(label, x, y - .32, w - 1.1, .3, fs=14, color=MUTE)
    st = pos(x, y, w, h)
    txt = '\n'.join(lines)
    put('<div class="a code" style="%s;font-size:%spx"><pre><code>%s</code></pre></div>' % (st, pt(fs), esc(txt)))
    put('<button class="copy-btn" type="button" aria-label="이 프롬프트 복사" data-code="@@CODE%d@@" style="left:%spx;top:%spx;width:%spx;height:%spx">복사</button>' % (
        idx, n(x + w - 1.0), n(y - .36), n(1.0), n(.32)))

def hint(text, y=6.45, fs=18):
    T('', .6, y, 12.1, .5, fs=fs, va='middle', runs=[('막힐 때  ', {'b': True, 'color': RED}), (text, {})])

def table(rows, x, y, colW, fs=16, rowH=0.5, head=TEAL, al='left'):
    w = sum(colW)
    s = '<table class="a tb" style="left:%spx;top:%spx;width:%spx;font-size:%spx"><colgroup>' % (n(x), n(y), n(w), pt(fs))
    for c in colW: s += '<col style="width:%spx">' % n(c)
    s += '</colgroup>'
    for ri, r in enumerate(rows):
        s += '<tr style="height:%spx">' % n(rowH)
        for c in r:
            if ri == 0: s += '<th style="background:%s;text-align:%s">%s</th>' % (head, al, rich(c))
            else: s += '<td style="background:%s;text-align:%s">%s</td>' % (CARD if ri % 2 else PAPER2, al, rich(c))
        s += '</tr>'
    put(s + '</table>')

def chip(text, x, y, w, h, color=None, fs=16):
    T(text, x, y, w, h, fs=fs, color=WHITE, b=True, al='center', va='middle', extra='background:%s;border-radius:%spx;padding:%spx' % (color or TEAL, n(.12), pt(4)))

def numCircle(k, x, y, d=0.5, color=RED):
    T(str(k), x, y, d, d, fs=18, color=WHITE, b=True, al='center', va='middle', extra='background:%s;border-radius:50%%' % color)

def folder(text, x, y, w=2.6, h=0.5, fs=16):
    T(text, x, y, w, h, fs=fs, b=True, al='center', va='middle', font=MONO, extra='background:%s;border:%spx solid %s;border-radius:%spx' % (GOLD, pt(1.5), GOLDL, n(.08)))

def checkbox(x, y, d=0.32):
    R(x, y, d, d, fill=CARD, ln=RED, lw=2)

def body(lines, x, y, w, h, size=24):
    size = max(size, 24)
    items = ''.join('<li>%s</li>' % rich(l) for l in lines)
    put('<ul class="a body" style="%s;font-size:%spx">%s</ul>' % (pos(x, y, w, h), pt(size), items))

def checks(items, x, y, w, size=18, gap=0.62):
    for i, c in enumerate(items):
        checkbox(x, y + i * gap + .08)
        T(c, x + .45, y + i * gap, w - .45, .5, fs=size, va='middle')

def cp(name, x, y, w=None):
    T('그래도 막히면', x, y, 2.0, .5, fs=18, va='middle')
    folder(name, x + 2.0, y, w or 3.2, .55)

def optionalFrame():
    R(.35, 1.62, 12.63, 5.3, ln=TEAL, lw=3, rad=.1, dash=True, extra='pointer-events:none')
    T('심화 선택 · 시간 되는 분만', 9.0, .26, 3.95, .46, fs=18, color=WHITE, b=True, al='center', va='middle', cls='ribbon',
      extra='background:%s;border-radius:%spx' % (TEAL, n(.1)))

def slide(num, mod, typ, title):
    global S
    S = []
    return dict(num=num, mod=mod, typ=typ, title=title)

def end(meta):
    SLIDES.append((meta, ''.join(S)))

def mk(num, mod, typ, title):
    return slide(num, mod, typ, title)

M1 = '모듈 1 · 도입 · 완성본 데모'
M2 = '모듈 2 · Firebase 설정 + 구글 로그인'
M3 = '모듈 3 · 수업코드 수강신청'
M4 = '모듈 4 · HTML 수업자료 등록'
M5 = '모듈 5 · 웹 학습지'
M6 = '모듈 6 · 개인별 맞춤 피드백'
M7 = '모듈 7 · 배포·보안 규칙·마무리'
CODE = '프롬프트 핵심 (전문은 발표자 노트)'

# ------------------------------------------------------------------ 모듈 1
m = mk(1, M1, '정리', '')
T('나만의 온라인 클래스룸 만들기', .6, 1.5, 7.3, 2.0, fs=48, b=True)
T('Claude Code로 만드는 교원 연수 · 180분', .6, 3.6, 7.3, .6, fs=24, color=TEAL, b=True)
T('오늘의 최종 산출물: 배포된 내 클래스룸 웹 주소 1개', .6, 4.4, 7.3, .9, fs=24)
R(8.3, 1.6, 4.5, 3.6, fill=CARD, ln=INK, lw=2, rad=.15)
for i, c in enumerate([RED, GOLDL, TEAL]): R(8.55 + i * .3, 1.8, .18, .18, fill=c, shape='ellipse')
T('https://(내 프로젝트).web.app', 8.55, 2.2, 4.0, .42, fs=16, font=MONO, va='middle', extra='background:%s;border-radius:%spx;padding:0 %spx' % (PAPER2, n(.1), pt(8)))
T('우리 반 온라인 클래스룸', 8.55, 3.2, 4.0, .8, fs=24, color=RED, b=True, al='center')
T('로그인 · 수업코드 · 자료 · 학습지 · 피드백', 8.55, 4.1, 4.0, .7, fs=16, color=MUTE, al='center')
T('오늘 집에 가져갈 것: https://(내 프로젝트).web.app 형태의 주소', .6, 6.1, 12.1, .5, fs=24, color=RED, b=True)
m['cover'] = True
end(m)

m = mk(2, M1, '데모', '완성본 먼저 보기')
body(['오늘 만들 클래스룸을 2분만 먼저 봅니다.', '교사: 수업 만들기 → 자료 → 학습지 → 피드백', '학생: 코드 가입 → 열람 → 제출 → 피드백 확인'], .6, 1.7, 12.1, 1.9)
t = ['수업 만들기', '자료 등록', '학습지 작성', '피드백 전달']; st_ = ['수업코드로 가입', '자료 열람', '학습지 제출', '내 피드백 확인']
x0, bw, gap, y1, y2, h = .6, 1.85, .33, 3.85, 5.75, .75
T('교사', x0, y1 - .38, 1.5, .34, fs=16, color=TEAL, b=True)
T('학생', x0, y2 - .38, 1.5, .34, fs=16, color=RED, b=True)
for i, tx in enumerate(t):
    x = x0 + i * (bw + gap); box(tx, x, y1, bw, h, fill=TEALT, ln=TEAL, lw=2)
    if i < 3: arrowR(x + bw + .02, y1 + h / 2, .29, TEAL)
for i, tx in enumerate(st_):
    x = x0 + i * (bw + gap); box(tx, x, y2, bw, h, fill=REDT, ln=RED, lw=2)
    if i < 3: arrowR(x + bw + .02, y2 + h / 2, .29, RED)
cx = lambda i: x0 + i * (bw + gap) + bw / 2
arrowD(cx(0), y1 + h + .1, .9, MUTE); T('수업코드', cx(0) + .25, 4.95, 1.4, .4, fs=16, b=True)
arrowU(cx(2), y1 + h + .1, .9, MUTE); T('제출 답안', cx(2) - 1.75, 4.95, 1.5, .4, fs=16, b=True, al='right')
arrowD(cx(3), y1 + h + .1, .9, MUTE); T('피드백', cx(3) + .25, 4.95, .9, .4, fs=16, b=True)
placeholder('[화면 캡처 자리]\n교사 화면 1장', 9.0, 3.85, 3.75, 1.35)
placeholder('[화면 캡처 자리]\n학생 화면 1장', 9.0, 5.4, 3.75, 1.35)
end(m)

m = mk(3, M1, '개념', '오늘의 지도와 준비물')
body(['7개 모듈을 하나씩 더해 갑니다.', '연습은 테스트 계정으로만. 실제 학생 정보는 넣지 않습니다.'], .6, 1.65, 12.1, 1.4)
road = ['1 도입', '2 로그인', '3 수업코드', '휴식', '4 HTML 자료', '5 학습지', '6 맞춤 피드백', '7 배포·보안']
w, g = 1.37, .14
for i, r in enumerate(road): chip(r, .6 + i * (w + g), 3.2, w, .62, GOLDL if r == '휴식' else TEAL, 15)
chk = ['구글 계정(교사용) + 테스트 학생용 계정 1개', 'Claude Code 로그인 완료 (유료 계정 필요, 무료 플랜 불가)', 'Node.js, Firebase CLI 설치', '터미널에서 firebase login 완료', '크롬 브라우저']
for i, c in enumerate(chk):
    y = 4.1 + i * .52
    R(.6, y + .07, .3, .3, fill=CARD, ln=RED, lw=2)
    T(c, 1.05, y, 11.6, .45, fs=18, va='middle')
end(m)

m = mk(4, M1, '개념', 'Claude Code는 말로 시키는 보조교사')
body(['말로 시키면 파일을 만들어 주는 보조교사입니다.', '우리는 코드를 읽지 않고, 요청하고 확인합니다.', '요청이 구체적일수록 결과가 정확합니다.'], .6, 1.7, 12.1, 1.9)
flow([{'t': '교사가\n요청 문장을 쓴다', 'fill': TEALT, 'color': TEAL}, {'t': '보조교사\n(Claude Code)가\n파일을 만든다', 'fill': REDT, 'color': RED}, {'t': '교사가\n화면에서 확인한다', 'fill': TEALT, 'color': TEAL}], .6, 4.4, 12.1, 1.3, fs=20, gap=.7)
T('다시 요청 (수정 요청)', .6, 5.85, 12.1, .4, fs=16, color=MUTE, al='center')
T('"환영 문구가 있는 첫 화면을 만들어 줘"', 3.6, 3.85, 6.1, .5, fs=18, al='center', va='middle', cls='callout',
  extra='background:%s;border:%spx solid %s;border-radius:%spx;padding:0 %spx' % (GOLD, pt(1.5), GOLDL, n(.12), pt(4)))
end(m)

m = mk(5, M1, '실습', '첫 요청: "환영합니다" 페이지')
cw, cg, y, h = 3.85, .28, 1.7, 2.2
cards = [('폴더 만들기', 'mkdir my-classroom\ncd my-classroom'), ('Claude Code 실행·붙여넣기', 'claude\n아래 요청을 붙여넣기'), ('브라우저에서 확인', None)]
for i, c in enumerate(cards):
    x = .6 + i * (cw + cg)
    box('', x, y, cw, h)
    numCircle(i + 1, x + .15, y + .15)
    T(c[0], x + .75, y + .12, cw - .9, .55, fs=18, b=True, va='middle')
    if c[1]: T(c[1], x + .2, y + .85, cw - .4, 1.2, fs=16, font=MONO)
    else: placeholder('["환영합니다" 화면 캡처 자리]', x + .2, y + .85, cw - .4, 1.2, 14)
code(['이 폴더에 index.html 파일을 하나 만들어 줘.', '화면 가운데에 "환영합니다. 우리 반 온라인 클래스룸"이라는 큰 제목이 보이게 해 줘.', '배경은 크림색(#f8f2e4), 글자는 진한 갈색(#2a2314)으로 하고, 초등학생도 읽기 쉬운 큰 글씨로 해 줘.', '파일은 index.html 하나만 만들고, 다른 설치나 설정은 하지 마.'], .6, 4.4, 12.1, 1.75, 15, '복사해서 Claude Code에 붙여넣기')
hint('허락을 물으면 yes. 화면이 비면 "index.html이 비어 있어. 다시 만들어 줘". 안 되면 checkpoint-0', 6.4, 16)
end(m)

m = mk(6, M1, '정리', '오늘의 작업 리듬')
body(['요청 → 확인 → 막히면 오류 메시지를 그대로 붙여넣기.', '그래도 막히면 checkpoint 폴더에서 이어가기.', '모듈이 끝날 때마다 복구 지점이 있습니다.'], .6, 1.7, 12.1, 1.9)
flow([{'t': '요청', 'fill': TEALT, 'color': TEAL}, {'t': '확인', 'fill': TEALT, 'color': TEAL}, {'t': '막힘 →\n오류 메시지\n그대로 붙여넣기', 'fill': REDT, 'color': RED}, {'t': '그래도 막힘 →\ncheckpoint\n폴더 열기', 'fill': GOLD, 'color': GOLDL}], .6, 4.0, 8.0, 1.6, fs=18, gap=.4)
T('복구 지점', 9.0, 3.85, 3.3, .4, fs=18, b=True)
for i, f in enumerate(['checkpoint-0', 'checkpoint-m2', 'checkpoint-m3', 'checkpoint-m4', 'checkpoint-m5', 'checkpoint-m6', 'checkpoint-final']):
    folder(f, 9.0 + (i % 2) * 1.95, 4.35 + (i // 2) * .6, 1.8, .5, 13)
end(m)

# ------------------------------------------------------------------ 모듈 2
m = mk(7, M2, '개념', 'Firebase 한 장 정리')
body(['Firebase = 구글이 빌려주는 "학교 운영 도구 세트"'], .6, 1.7, 12.1, .6)
for i, c in enumerate([('A', 'Authentication', '출석부 확인', '누구인지 확인', TEAL), ('F', 'Firestore', '학급 서류함', '데이터 보관', TEAL), ('H', 'Hosting', '학교 게시판', '웹 주소로 공개', MUTE)]):
    x, w = .6 + i * 4.1, 3.9
    box('', x, 2.55, w, 3.0)
    T(c[0], x + .3, 2.8, .9, .9, fs=32, color=WHITE, b=True, al='center', va='middle', extra='background:%s;border-radius:50%%' % c[4])
    T(c[1], x + 1.35, 2.85, w - 1.5, .8, fs=24, b=True, va='middle')
    T(c[2], x + .3, 3.95, w - .6, .6, fs=28, color=c[4], b=True)
    T(c[3], x + .3, 4.6, w - .6, .5, fs=20)
T('오늘 모듈 2는 앞의 두 개(Authentication, Firestore)를 씁니다. Hosting은 모듈 7', .6, 5.95, 12.1, .5, fs=20, color=RED, b=True)
end(m)

m = mk(8, M2, '실습', '프로젝트 만들기')
body(['Firebase 콘솔에서 새 프로젝트 만들기 (이름 예: my-classroom)', '테스트용 구글 계정(교사용)으로 진행. 실제 학생 정보 금지', '순서: 화면에서 찾을 것 → 누를 것 → 확인할 것'], .6, 1.7, 12.1, 2.0)
cw, gap = 3.7, .5
for i, c in enumerate([('1 콘솔 접속', 'console.firebase.google.com'), ('2 프로젝트 추가', '이름 칸에 my-classroom'), ('3 프로젝트 홈 도착', '왼쪽 위에 my-classroom')]):
    x = .6 + i * (cw + gap)
    placeholder('[콘솔 화면 캡처 자리]', x, 3.95, cw, 1.5, 15)
    T(c[0], x, 5.55, cw, .4, fs=18, b=True)
    T(c[1], x, 5.95, cw, .4, fs=16, color=MUTE, font=MONO)
    if i < 2: arrowR(x + cw + .1, 4.7, .3, RED)
hint('만들기 버튼이 안 보이면 개인 구글 계정으로 다시 로그인. 이미 쓰인 이름이면 뒤에 숫자 붙이기', 6.5, 16)
end(m)

m = mk(9, M2, '실습', '웹 앱 등록과 firebaseConfig 복사')
body(['프로젝트 안에 "웹 앱" 등록 = 우리 웹 페이지용 출입문 달기', '등록이 끝나면 firebaseConfig(설정값 묶음)가 나온다 → 통째로 복사', '복사한 값은 메모장에 붙여 둔다 (슬라이드 14에서 사용)'], .6, 1.7, 12.1, 2.1)
cw, gap = 2.8, .3
for i, l in enumerate(['웹 앱 추가  </>  아이콘', '앱 닉네임 입력 (Hosting 체크는 하지 않기)', 'firebaseConfig 블록 보임', '메모장에 복사']):
    x = .6 + i * (cw + gap)
    placeholder('[콘솔 캡처 자리]', x, 4.0, cw, 1.4, 14)
    numCircle(i + 1, x, 5.5, .45)
    T(l, x + .55, 5.45, cw - .55, .95, fs=16)
hint('설정값 화면을 닫았다면 프로젝트 설정(톱니바퀴) → 내 앱에서 다시 볼 수 있다', 6.5, 16)
end(m)

m = mk(10, M2, '개념', '웹 설정값은 공개돼도 괜찮다')
body(['firebaseConfig는 "학교 주소" 같은 것. 알려져도 문은 열리지 않는다', '문을 지키는 것은 보안 규칙(교무실 출입 규칙) → 모듈 7에서 완성', '단, AI API 키는 다르다 → 비밀. 모듈 6에서 이유를 본다'], .6, 1.7, 12.1, 2.1)
box('', .6, 4.05, 5.2, 2.5, fill=TEALT, ln=TEAL, lw=3)
T('', .8, 4.3, 4.8, 1.9, runs=[('공개해도 됨\n', {'b': True, 'fs': 24, 'color': TEAL}), ('firebaseConfig = 학교 주소', {'fs': 20})])
box('', 7.5, 4.05, 5.2, 2.5, fill=REDT, ln=RED, lw=3)
T('', 7.7, 4.3, 4.8, 1.9, runs=[('절대 공개 금지\n', {'b': True, 'fs': 24, 'color': RED}), ('AI API 키 = 교무실 금고 열쇠', {'fs': 20})])
T('보안 규칙\n(교무실 출입 규칙)', 5.9, 4.5, 1.5, 1.6, fs=14, color=WHITE, b=True, al='center', va='middle', cls='hex', extra='background:%s;padding:%spx' % (INK, pt(2)))
end(m)

def consoleChain(items, y, h=1.0, fs=16, gap=.38):
    flow(items, .6, y, 12.1, h, fs=fs, gap=gap)

m = mk(11, M2, '실습', '구글 로그인 제공업체 켜기')
body(['Authentication(출석부 확인)에서 Google 로그인 방법을 켠다', '프로젝트 지원 이메일은 내 교사용 계정으로 선택', '순서: 화면에서 찾을 것 → 누를 것 → 확인할 것'], .6, 1.7, 12.1, 2.1)
consoleChain(['보안 > Authentication', '시작하기', '로그인 방법 탭', 'Google 선택', '사용 설정 + 지원 이메일', '저장'], 4.1, 1.1, 16, .3)
T('예상 결과: Google 줄이 "사용 설정됨"으로 보인다', .6, 5.5, 12.1, .5, fs=20, color=TEAL, b=True)
hint('Google이 안 보이면 "새 제공업체 추가"에서 찾기. 지원 이메일 칸이 비면 계정 확인 후 새로고침', 6.4, 16)
end(m)

m = mk(12, M2, '실습', '승인된 도메인에 localhost 추가')
body(['승인된 도메인 = 로그인 창구를 쓸 수 있는 "허가받은 주소 목록"', '새 프로젝트에는 localhost가 기본으로 없다', '"도메인 추가"로 localhost를 직접 넣는다'], .6, 1.7, 12.1, 2.1)
consoleChain(['Authentication', '설정 탭', '승인된 도메인', '도메인 추가', 'localhost 입력 후 추가'], 4.1, 1.0, 16, .35)
box('추가 후 목록: localhost, (프로젝트 주소).firebaseapp.com …', .6, 5.35, 12.1, .55, fs=16, ln=RED, lw=2, font=MONO, rad=.1)
hint('나중에 auth/unauthorized-domain 오류가 나면 이 슬라이드로 돌아와 주소 목록을 본다', 6.3, 16)
end(m)

m = mk(13, M2, '실습', 'Firestore 만들기와 임시 규칙')
body(['Firestore(학급 서류함) 설치. 위치(리전)는 만든 뒤 못 바꾼다', '모드는 테스트 모드가 아닌 잠금(프로덕션) 모드', '임시 규칙 = 강사가 준 firestore.temp.rules 통째로 복사'], .6, 1.7, 12.1, 2.1)
consoleChain(['데이터베이스 및 스토리지 > Firestore', '데이터베이스 만들기', '위치 선택', '잠금(프로덕션) 모드 → 만들기'], 3.95, 1.1, 16, .35)
flow([{'t': '규칙 탭 열기', 'fill': CARD}, {'t': '강사 파일 firestore.temp.rules 내용 붙여넣기', 'fill': GOLD, 'color': GOLDL}, {'t': '게시(Publish)', 'fill': TEALT, 'color': TEAL}], .6, 5.3, 12.1, .95, fs=16, gap=.4)
T('테스트 모드는 선택하지 않는다 · 규칙 전문은 발표자 노트(부록 A)와 배포 파일', .6, 6.4, 12.1, .5, fs=18, color=RED, b=True)
end(m)

m = mk(14, M2, '실습', '설정값을 프로젝트에 저장')
body(['메모장의 firebaseConfig를 Claude Code에게 전달해 저장', '한 파일(firebase-config.js)에 모아 두고 재사용', '코드는 읽지 않고 붙여넣기 → 확인만'], .6, 1.7, 12.1, 2.0)
flow(['메모장의 firebaseConfig', 'Claude Code에 붙여넣기', '폴더에 firebase-config.js 생성'], .6, 3.8, 12.1, .85, fs=18, gap=.6)
code(['firebase-config.js 파일을 만들어 줘.', '- 아래 firebaseConfig를 export const firebaseConfig = { ... } 형태로 저장', '- 값은 글자 하나도 바꾸지 말고 그대로. 다른 파일은 만들거나 바꾸지 마', '- 코드를 설명하지 말고, 파일 이름과 위치만 알려 줘', '(여기에 슬라이드 9에서 복사한 firebaseConfig 블록 붙여넣기)'], .6, 5.0, 12.1, 1.55, 15, '프롬프트 핵심 (전문은 발표자 노트)')
hint('다른 파일까지 바뀌었다면 "방금 바꾼 다른 파일은 원래대로 되돌려 줘"', 6.6, 16)
end(m)

m = mk(15, M2, '실습', '프롬프트 1: 로그인/로그아웃 버튼')
body(['firebase-config.js를 app.js가 불러와 Firebase를 시작한다', '구글 로그인 버튼, 로그아웃 버튼, 이름 표시'], .6, 1.65, 12.1, 1.3)
box('[ 구글로 로그인 ]', .6, 2.85, 2.6, .8, fs=18, b=True, ln=INK, lw=2)
arrowR(3.35, 3.25, .3, RED)
box('OOO 선생님 환영합니다\n[ 로그아웃 ]', 3.8, 2.8, 3.2, .9, fs=16, ln=INK, lw=2)
code(['index.html을 Firebase 구글 로그인 페이지로 바꿔 줘.', '- 파일 4개: index.html, style.css, app.js, firebase-config.js(그대로 사용)', '- SDK는 CDN 모듈 방식: gstatic.com/firebasejs/12.19.0/ 아래 app·auth·firestore', '- "구글로 로그인" → 구글 팝업 로그인, 로그인하면 이름+로그아웃 표시', '- 새로고침해도 로그인 유지, 글씨는 크게, 배경은 크림색(#f8f2e4)', '- 끝나면 localhost로 여는 명령 한 줄과 접속 주소만 알려 줘'], .6, 4.2, 12.1, 2.15, 15, CODE)
T('file:// 로 열지 말고 localhost 주소로 열기', 7.4, 2.85, 5.3, .7, fs=18, color=RED, b=True, va='middle')
hint('팝업이 안 뜨면 주소창 오른쪽 "팝업 차단됨"을 눌러 허용. 빨간 오류는 그대로 붙여넣기', 6.5, 16)
end(m)

m = mk(16, M2, '실습', '프롬프트 2: users 문서와 역할 선택')
body(['처음 로그인하면 users/{uid} 문서를 만든다', '역할(교사/학생)은 처음 한 번만 고른다 → 화면을 나누는 용도'], .6, 1.65, 12.1, 1.3)
box('', .6, 3.0, 3.1, 1.55, ln=TEAL, lw=2)
T('', .8, 3.07, 2.8, 1.4, fs=16, font=MONO, va='middle', runs=[('users/{uid}\n', {'b': True, 'color': TEAL}), ('name\nemail\nrole', {})])
flow(['처음 로그인', '역할 선택\n교사 / 학생', 'users 문서 저장', '환영 화면'], 4.0, 3.15, 8.7, 1.1, fs=16, gap=.35)
T('두 번째 로그인부터는 역할 선택 건너뛰기 (점선)', 4.0, 4.3, 8.7, .35, fs=14, color=MUTE)
code(['로그인에 성공하면 users/{uid} 문서를 확인해 줘.', '- 없으면 "교사"/"학생" 역할 선택 화면을 보여 줘', '- 저장 필드는 name, email, role("teacher"/"student") 3개만', '- 있으면 선택을 건너뛰고 "OOO 선생님 환영합니다"로 보여 줘', '- 역할은 처음 한 번만 고르고 화면에서 바꿀 수 없게 해 줘'], .6, 5.0, 12.1, 1.6, 15, CODE)
hint('permission-denied면 슬라이드 13의 임시 규칙이 게시됐는지 확인', 6.65, 16)
end(m)

m = mk(17, M2, '실습', '확인: Firestore에서 내 문서 보기')
body(['콘솔 Firestore 데이터 탭에서 users → 내 uid 문서 확인', '시크릿 창에서 테스트 학생 계정으로 로그인', '문서가 2개(교사 1, 학생 1) 보이면 성공'], .6, 1.7, 7.6, 2.4, 22)
for i, c in enumerate(['users 컬렉션이 보인다', '교사 문서: name, email, role=teacher', '학생 문서: name, email, role=student']):
    y = 4.4 + i * .7
    checkbox(.6, y + .08)
    T(c, 1.05, y, 7.1, .5, fs=18, va='middle')
placeholder('[Firestore 문서 화면\n캡처 자리]', 8.6, 1.8, 4.1, 3.6, 16)
T('콘솔: 데이터베이스 및 스토리지 > Firestore > 데이터 탭', 8.6, 5.5, 4.1, .8, fs=16, color=MUTE)
hint('시크릿 창 로그인이 안 되면 주소창 오른쪽에서 팝업 허용 확인', 6.5, 16)
end(m)

m = mk(18, M2, '정리', '막힘 모음과 복구 지점')
body(['이 세 가지가 가장 흔하다. 오류는 메시지 그대로 Claude Code에 붙여넣기'], .6, 1.65, 12.1, .8, 22)
table([['증상', '원인', '해결'],
       ['auth/unauthorized-domain', '승인된 도메인에 현재 주소가 없음', 'Authentication 설정의 승인된 도메인에 localhost 추가 (슬라이드 12)'],
       ['팝업이 안 뜸 / popup-blocked', '브라우저가 팝업 차단', '주소창 오른쪽 차단 표시에서 허용 후 다시'],
       ['버튼 반응 없음, file:// 로 열었음', '파일로 직접 열면 로그인이 안 됨', 'Claude Code가 알려 준 localhost 주소로 접속']], .6, 2.55, [3.4, 3.7, 5.0], 16, .62)
code(['아래 오류가 났어. 원인을 쉬운 말로 한 줄로 알려 주고, 고쳐 줘.', '(여기에 오류 메시지를 그대로 붙여넣기)'], .6, 5.6, 8.0, .95, 15, '공통 문장')
T('그래도 안 되면', 9.0, 5.25, 3.7, .35, fs=16, color=MUTE)
folder('checkpoint-m2', 9.0, 5.65, 3.7, .6)
T('복사한 폴더의 firebase-config.js만 내 설정값으로 바꾼다', .6, 6.6, 12.1, .35, fs=16)
end(m)

# ------------------------------------------------------------------ 모듈 3
m = mk(19, M3, '개념', '수업코드 = 교실 열쇠')
body(['수업을 만들면 6자리 수업코드가 생긴다', '그 코드가 수업 문서의 이름이다', '학생은 코드(교실 열쇠)로 들어온다'], .6, 1.7, 5.4, 2.4, 22)
box('', 6.4, 1.75, 6.3, 3.5, ln=TEAL, lw=3)
T('', 6.6, 1.85, 5.9, 1.2, fs=18, font=MONO, runs=[('classes/{수업코드}\n', {'b': True, 'color': TEAL}), ('폴더 이름표 "K7M4QX"\n', {'b': True, 'color': RED}), ('title · teacherUid · joinCode', {})])
box('', 6.8, 3.3, 5.5, 1.7, fill=TEALT, ln=TEAL, lw=2)
T('', 7.0, 3.45, 5.1, 1.3, fs=18, font=MONO, va='middle', runs=[('members/{uid}\n', {'b': True, 'color': TEAL}), ('joinedAt · uid', {})])
T('열쇠: 수업코드 K7M4QX = 폴더 이름', .6, 4.5, 5.4, .5, fs=18, b=True, al='center', va='middle', extra='background:%s;border:%spx solid %s;border-radius:%spx' % (GOLD, pt(1.5), GOLDL, n(.1)))
flow([{'t': '교사 → classes/{코드} 생성', 'fill': TEALT, 'color': TEAL}, {'t': '학생 → 코드 입력 → 한 장 꺼내기 → members 추가', 'fill': REDT, 'color': RED}], .6, 5.55, 12.1, 1.0, fs=18, gap=.6)
end(m)

m = mk(20, M3, '개념', '보안 원칙 3·4 미리보기')
body(['원칙 3: 수업은 교사만 만든다', '원칙 4: 수업코드를 알아야 들어간다. 전체 수업 목록은 볼 수 없다'], .6, 1.7, 12.1, 1.4)
table([['원칙', '허용 O', '막힘 X'], ['수업 만들기', '교사', '학생'], ['수업 찾기', '코드 한 개로 한 교실 찾기', '모든 교실 목록 훑어보기']], .6, 3.5, [2.8, 4.6, 4.7], 20, .75)
T('보안 규칙 = 교무실 출입 규칙 · 전체를 내려받아 비교하지 않는다', .6, 6.2, 12.1, .5, fs=18, color=MUTE)
end(m)

m = mk(21, M3, '실습', '실습 1: 교사가 수업 만들기')
body(['교사 화면에 "수업 만들기"를 추가한다', '제목을 넣으면 6자리 수업코드가 자동 발급된다'], .6, 1.65, 7.0, 1.3, 22)
box('제목 입력칸   [ 수업 만들기 ]\n\n수업코드: K7M4QX', 7.9, 1.7, 4.8, 1.55, fs=18, ln=INK, lw=2)
code(['교사 화면에 "수업 만들기" 기능을 추가해 줘.', '- 교사(role이 teacher)에게만 보이게', '- 수업코드: 영문 대문자+숫자 6자리 무작위 (0, O, 1, I는 쓰지 마)', '- classes/{수업코드}: 문서 이름을 수업코드와 똑같이', '- 필드는 title, teacherUid, joinCode 세 개만', '- 저장 전에 같은 코드가 있는지 한 건만 읽어 확인', '- 만든 뒤 제목과 수업코드를 크게 보여 줘'], .6, 3.75, 12.1, 2.4, 15, CODE)
hint('권한 오류면 규칙 탭에 임시 규칙 게시 확인. 그래도 같으면 "규칙 파일은 바꾸지 말고 앱 코드에서 원인을 찾아 줘"', 6.4, 16)
end(m)

m = mk(22, M3, '실습', '실습 2: 학생이 코드로 가입')
body(['학생 화면에 수업코드 입력칸을 만든다', '맞는 코드면 그 수업의 members에 내 문서가 생긴다'], .6, 1.65, 12.1, 1.3, 22)
flow(['코드 입력\n[ 가입하기 ]', 'classes/{코드}\n1건 읽기', 'classes/{코드}/members/{내 uid}\n생성 (joinedAt, uid)'], .6, 3.0, 12.1, 1.0, fs=16, gap=.5)
code(['학생 화면에 "수업코드로 가입하기"를 추가해 줘.', '- 코드는 앞뒤 공백 제거 후 대문자로', '- classes/{코드} 문서 한 건만 읽기 (전체 다운로드·where 검색 금지)', '- 있으면 members/{내 uid} 생성: joinedAt, uid 두 개만', '- 이미 가입 → "이미 가입한 수업이에요"', '- 없는 코드 → "수업코드를 다시 확인해 주세요"'], .6, 4.4, 12.1, 1.95, 15, CODE)
hint('맞는 코드인데 "없는 코드"면 소문자·공백이 섞였는지 확인', 6.5, 16)
end(m)

m = mk(23, M3, '실습', '실습 3: 내 수업 목록')
body(['교사는 내가 만든 수업, 학생은 내가 가입한 수업이 목록으로', '학생 목록에는 수업 제목만 보인다'], .6, 1.65, 12.1, 1.3, 22)
box('교사: 내가 만든 수업\n제목 + 수업코드', .6, 3.0, 5.9, 1.0, fs=18, fill=TEALT, ln=TEAL, lw=2)
box('학생: 내가 가입한 수업\n제목만 (수업코드는 숨김)', 6.8, 3.0, 5.9, 1.0, fs=18, fill=REDT, ln=RED, lw=2)
code(['첫 화면에 "내 수업" 목록을 보여 줘.', '- 교사: teacherUid가 내 uid인 수업 (제목+수업코드)', '- 학생: members 컬렉션 그룹 조회로 uid가 내 uid인 가입 문서 → 부모 수업 제목만', '- 비었으면 "아직 수업이 없어요"', '- 제목을 누르면 #/class/{classId} 수업 화면으로'], .6, 4.4, 12.1, 1.55, 15, CODE)
T('거의 모두에게 "색인(index) 필요" 오류가 한 번 나온다 → 오류의 링크를 눌러 색인을 만들고 1~5분 기다린 뒤 새로고침', .6, 6.15, 12.1, .75, fs=18, color=RED, b=True, va='middle',
  extra='background:%s;border:%spx solid %s;border-radius:%spx;padding:0 %spx' % (GOLD, pt(2), RED, n(.1), pt(10)))
end(m)

m = mk(24, M3, '실습', '짝 활동: 옆 사람 코드로 가입')
body(['옆 사람의 수업코드로 가입해 보자', '일부러 틀린 코드도 넣어 보자. 어떻게 되는가?'], .6, 1.65, 12.1, 1.3, 24)
box('교사 역할\n코드 알려 주기', .6, 3.2, 2.8, 1.2, fs=18, fill=TEALT, ln=TEAL, lw=2)
T('⇄', 3.5, 3.35, .8, .9, fs=36, color=MUTE, b=True, al='center', va='middle')
box('학생 역할\n코드 입력', 4.4, 3.2, 2.8, 1.2, fs=18, fill=REDT, ln=RED, lw=2)
for i, q in enumerate(['(1) 맞는 코드를 넣으면?', '(2) 틀린 코드를 넣으면?', '(3) 같은 코드를 두 번 넣으면?']):
    box(q, 7.7, 3.0 + i * .85, 5.0, .72, fs=20, al='left', ln=RED, lw=2, margin=10)
hint('틀린 코드에서 흰 화면이면 "틀린 코드를 넣으면 친절한 안내가 나오게 해 줘"', 6.3, 18)
end(m)

m = mk(25, M3, '정리', '막힘 모음과 복구 지점')
body(['색인 필요 오류는 안내 링크로 해결', '권한 오류는 오류 메시지를 통째로 붙여넣기'], .6, 1.65, 12.1, 1.3, 24)
for i, c in enumerate([('"The query requires an index"', '링크 클릭 → 몇 분 기다리기'), ('"Missing or insufficient permissions"', '오류 전체 붙여넣기'), ('아무것도 안 보임', '로그인한 계정의 role 확인')]):
    x = .6 + i * 4.1
    box('', x, 3.3, 3.9, 2.0, ln=TEAL, lw=2)
    T(c[0], x + .2, 3.4, 3.5, .95, fs=18, color=RED, b=True, va='middle')
    T('→ ' + c[1], x + .2, 4.4, 3.5, .8, fs=18, va='middle')
T('그래도 막히면', .6, 5.75, 3.0, .5, fs=20, va='middle')
folder('checkpoint-m3', 3.5, 5.75, 3.2, .6)
end(m)

m = mk(26, M3, '정리', '휴식 10분')
m['timer'] = True
put('<div class="a timer" data-timer-display style="%s;font-size:%spx">10:00</div>' % (pos(.6, 1.45, 6.4, 2.4), pt(120)))
T('10분 타이머 · 휴식 시간', .6, 3.85, 6.4, .6, fs=24, color=TEAL, b=True, al='center')
put('<div class="a tbtns" style="%s"><button type="button" class="tbtn" data-timer="start" aria-label="타이머 시작">시작</button><button type="button" class="tbtn" data-timer="stop" aria-label="타이머 정지">정지</button><button type="button" class="tbtn ghost" data-timer="reset" aria-label="타이머 10분으로 되돌리기">처음으로</button></div>' % pos(.6, 4.5, 6.4, .55))
R(10.2, 2.75, 1.0, 1.0, fill=CARD, ln=INK, lw=3, shape='ellipse')
R(10.55, 3.1, .3, .3, fill=BG, ln=INK, lw=3, shape='ellipse', extra='display:none')
R(8.2, 2.3, 2.3, 2.0, fill=CARD, ln=INK, lw=3, rad=.2)
T('휴식', 8.2, 2.3, 2.3, 2.0, fs=28, color=RED, b=True, al='center', va='middle')
body(['막힌 분은 강사석으로', 'checkpoint-m3에서 이어 시작할 수 있어요'], .6, 5.25, 8.5, 1.3, 24)
folder('checkpoint-m3', 9.8, 5.5, 2.9, .65)
end(m)

# ------------------------------------------------------------------ 모듈 4
m = mk(27, M4, '개념', '내 HTML 자료, 클래스룸에 올리자')
body(['만들어 둔 HTML 수업자료를 클래스룸에 한 번만 올린다', '우리 수업 학생들이 자기 화면에서 바로 연다', '올린 자료는 Firestore(학급 서류함)에 저장된다'], .6, 1.7, 12.1, 2.1)
flow(['교사 PC의\nHTML 파일', '자료 등록 폼\n(제목 + HTML 붙여넣기)', 'Firestore\nclasses/{classId}/\nmaterials/{id}', '학생 수업 화면의\n자료 목록'], .6, 4.1, 12.1, 1.5, fs=18, gap=.45)
T('저장 필드: title · html · createdAt', 5.0, 5.75, 4.5, .4, fs=16, color=MUTE, font=MONO, al='center')
end(m)

m = mk(28, M4, '개념', '자료는 유리 진열장에 넣어서 보여 준다')
body(['원칙 1: 가입한 수업 자료만 읽는다', '원칙 5: 교사 HTML은 유리 진열장(sandbox iframe)에 넣어 보여 준다. 보이지만 손댈 수 없다'], .6, 1.7, 12.1, 1.8)
box('', .6, 3.75, 5.9, 3.0, ln=TEAL, lw=2)
T('원칙 1', .8, 3.85, 3, .4, fs=18, color=TEAL, b=True)
box('교실 A (가입함)\n문 열림', .9, 4.4, 2.5, 1.3, fs=18, fill=TEALT, ln=TEAL, lw=2)
box('교실 B (미가입)\n문 잠김', 3.7, 4.4, 2.5, 1.3, fs=18, fill=REDT, ln=RED, lw=2)
T('열쇠(수업코드)로 가입한 학생만 들어간다', .9, 5.85, 5.3, .7, fs=16)
box('', 6.8, 3.75, 5.9, 3.0, ln=RED, lw=2)
T('원칙 5', 7.0, 3.85, 3, .4, fs=18, color=RED, b=True)
box('유리 진열장\n(sandbox iframe)\nHTML 자료', 7.1, 4.35, 2.9, 1.7, fs=18, fill=GOLD, ln=GOLDL, lw=4)
box('진열장 밖\n로그인 정보', 10.2, 4.35, 2.2, 1.7, fs=18, fill=TEALT, ln=TEAL, lw=2)
T('✕', 9.75, 4.55, .7, .7, fs=36, color=RED, b=True, al='center', va='middle')
T('진열장 안에서 밖으로 손댈 수 없다', 7.1, 6.15, 5.4, .5, fs=16)
end(m)

m = mk(29, M4, '실습', '실습 1: 교사 자료 등록 폼')
body(['수업 화면에 자료 등록 폼을 추가한다', '제목을 쓰고 HTML을 붙여넣어 저장한다'], .6, 1.65, 7.0, 1.3)
box('[ 제목 ]\n[ HTML 붙여넣기 ]\n[ 저장 ]  저장했습니다', 8.0, 1.65, 4.7, 1.6, fs=16, ln=INK, lw=2)
code(['교사용 수업 화면에 "수업자료 등록" 폼을 추가해 줘.', '- 입력칸: 제목(title), HTML 붙여넣기(html)', '- 저장 → classes/{classId}/materials 에 title, html, createdAt(서버 시간)', '- 그 수업 교사(teacherUid가 내 uid)에게만 보이게', '- 제목이 비면 저장 금지, html이 90만 바이트를 넘으면 거부', '- 기존 로그인, 수업 만들기 기능은 건드리지 마'], .6, 3.65, 12.1, 2.2, 15, CODE)
hint('폼이 안 보이면 내가 만든 수업에 교사 계정으로 들어갔는지 확인. 권한 오류면 임시 규칙 게시 확인', 6.3, 16)
end(m)

m = mk(30, M4, '실습', '실습 2: 학생 목록과 유리 진열장')
body(['학생 화면에 자료 목록을 만든다', '제목을 누르면 유리 진열장(sandbox iframe) 안에 자료를 보여 준다'], .6, 1.65, 7.4, 1.8)
box('자료 1\n자료 2\n자료 3', 8.3, 1.65, 1.8, 1.6, fs=16, ln=INK, lw=2)
box('선택한 자료 표시\n(sandbox)', 10.3, 1.65, 2.4, 1.6, fs=16, fill=GOLD, ln=GOLDL, lw=4)
code(['학생용 수업 화면에 "수업자료" 목록을 추가해 줘.', '- materials를 최신순으로 제목만 보여 주고', '- 제목을 누르면 html을 iframe의 srcdoc으로 보여 줘', '- iframe에 sandbox 속성을 값 없이 붙여 줘 (allow-same-origin, allow-scripts는 절대 넣지 마)', '- 자료가 없으면 "아직 등록된 자료가 없습니다"', '- html을 innerHTML로 다른 곳에 넣지 마'], .6, 3.85, 12.1, 2.1, 15, CODE)
hint('자료 속 버튼이 안 눌리는 것은 오류가 아니다. 유리 진열장의 정상 동작이다', 6.35, 18)
end(m)

m = mk(31, M4, '실습', '실습 3: 학생 계정으로 확인')
body(['테스트 학생 계정(시크릿 창)으로 가입한 수업의 자료를 열어 본다', '실제 차단 검증은 모듈 7에서 한다'], .6, 1.65, 12.1, 1.4)
checks(['교사 계정: 자료 등록 완료', '학생 계정(가입함): 목록·열람 OK', '학생 계정(미가입): 모듈 7에서 차단 확인 (예고)'], .6, 3.0, 7.0, 18, .55)
code(['방금 만든 수업자료 기능을 점검해 줘.', '1. 목록과 iframe 열람이 정상인지 코드로 점검', '2. sandbox에 allow-same-origin/allow-scripts가 없는지 확인', '3. 자료 html을 innerHTML로 넣는 곳이 없는지 찾기', '4. 문제가 있으면 고치고 3줄 이내로 요약'], .6, 5.2, 12.1, 1.65, 15, CODE)
end(m)

m = mk(32, M4, '정리', '정리: 막힘 모음과 복구 지점')
body(['오늘 만든 것: 자료 등록 폼 + 자료 목록·열람(유리 진열장)', '다음은 웹 학습지'], .6, 1.65, 12.1, 1.3)
flow(['등록\nmaterials', '목록', '유리 진열장 열람'], .6, 3.15, 12.1, 1.0, fs=20, gap=.6)
box('저장이 안 되고 오류: 문서 1개는 1MiB(1,048,576바이트)까지. 큰 이미지가 원인. 우리 폼은 90만 바이트(한글 위주 약 30만 글자)를 넘으면 먼저 알려 준다', .6, 4.4, 5.9, 1.75, fs=16, al='left', margin=10)
box('이미지가 깨져 보임: 이미지가 내 컴퓨터 안의 경로로만 걸려 있다. 웹 주소로 바꾸거나 자료 안에 포함한다', 6.8, 4.4, 5.9, 1.75, fs=16, al='left', margin=10)
cp('checkpoint-m4', .6, 6.3)
end(m)

# ------------------------------------------------------------------ 모듈 5
m = mk(33, M5, '개념', '학습지 = 문항지 1장 + 학생별 답안지')
body(['문항지는 교사가 1장 만든다', '답안지는 학생마다 1장씩 쌓인다', 'Firestore(학급 서류함)에 두 종류를 나눠 보관한다'], .6, 1.7, 12.1, 2.0)
box('문항지  classes/{classId}/worksheets/{id}\ntitle, questions[]', .6, 3.85, 12.1, 1.0, fs=18, fill=TEALT, ln=TEAL, lw=3)
for i, tt in enumerate(['uid-A 답안지', 'uid-B 답안지', 'uid-C 답안지']):
    arrowD(2.2 + i * 3.1, 4.9, .4, MUTE)
    box('submissions/' + tt + '\nanswers, submittedAt', .7 + i * 3.1, 5.35, 2.9, 1.1, fs=15, fill=REDT, ln=RED, lw=2)
box('feedback\n(모듈 6에서 채움)', 10.0, 5.35, 2.7, 1.1, fs=15, fill=BG, ln=MUTE, lw=2, tc=MUTE, dash=True)
end(m)

m = mk(34, M5, '개념', '답안지 이름이 학생 번호인 이유')
body(['답안지 문서 이름 = 그 학생의 uid(출석 번호표)', '내 번호표와 같은 이름의 답안지만 열 수 있다', '보안 규칙 원칙 2: 학생은 자기 제출물만 읽고 쓴다'], .6, 1.7, 12.1, 2.1)
for i, d in enumerate([('uid-A', '열림', TEALT, TEAL), ('uid-B', '잠김', REDT, RED), ('uid-C', '잠김', REDT, RED)]):
    box(d[0] + '\n' + d[1], .6 + i * 2.6, 4.2, 2.35, 1.6, fs=20, b=True, fill=d[2], ln=d[3], lw=3)
T('학생 A의 서랍장', .6, 3.8, 4, .4, fs=16, color=MUTE)
box('교사: 해당 수업 서랍 전체 열람 가능', 8.6, 4.2, 4.1, 1.6, fs=18, b=True, fill=GOLD, ln=GOLDL, lw=2)
end(m)

m = mk(35, M5, '실습', '교사 학습지 작성 화면 만들기')
body(['교사 화면에서 문항을 추가해 학습지를 저장한다', '서술형과 선택형(정답 포함) 두 종류. 정답은 모듈 6에서 쓴다'], .6, 1.65, 12.1, 1.5)
code(['교사 수업 화면에 "학습지 만들기"를 추가해 줘 (학생에게는 안 보이게).', '- "서술형 문항 추가" / "선택형 문항 추가" 버튼. 선택형은 보기 2~5개 + 정답 하나', '- classes/{classId}/worksheets 에 title, questions[] 두 필드만 저장', '- 문항 필드: type("essay"/"choice"), text, choices, answer', '  answer: 선택형은 0부터 센 번호, 서술형은 null', '- 제목·문항·보기·정답이 빠지면 저장하지 말고 무엇이 빠졌는지 알려 줘'], .6, 3.5, 12.1, 2.2, 15, CODE)
T('화면에는 보기 1, 2, 3 · 저장은 0, 1, 2  (첫 번째 보기가 정답이면 answer = 0)', .6, 5.85, 12.1, .5, fs=18, color=RED, b=True)
hint('권한 오류는 임시 규칙 게시 확인. 폼이 안 보이면 내가 만든 수업인지 확인', 6.45, 16)
end(m)

m = mk(36, M5, '실습', '학생 학습지 풀기와 제출')
body(['학생 화면에서 학습지를 열어 답하고 제출한다', '답안지 문서 이름은 내 uid. 다시 제출하면 병합 저장으로 답만 바꾼다'], .6, 1.65, 12.1, 1.5)
code(['학생이 학습지를 풀고 제출하는 기능을 추가해 줘.', '- 서술형은 글상자, 선택형은 라디오 버튼. 정답은 화면에 보여 주지 마', '- 제출 → .../submissions/{내 uid} 에 answers, submittedAt(서버 시각)', '- 문서 이름은 반드시 로그인한 학생의 uid', '- 이미 제출했으면 이전 답을 채워 주고, 다시 제출은 merge로', '  answers와 submittedAt만 바꿔 줘 (feedback 같은 다른 필드는 지우지 마)'], .6, 3.5, 12.1, 2.2, 15, CODE)
hint('목록에 학습지가 없으면 그 수업에 가입했는지 확인. 제출 권한 오류는 오류 메시지 붙여넣기', 6.2, 16)
end(m)

m = mk(37, M5, '실습', '교사 제출현황 표')
body(['교사 화면에 학생별 제출 여부 표를 만든다', '학생을 누르면 그 학생의 답안을 본다. 해당 수업 교사만 본다'], .6, 1.65, 12.1, 1.5)
table([['학생 이름', '제출 여부', '제출 시각'], ['테스트 학생 1', '제출', '10:42'], ['테스트 학생 2', '미제출', '-']], .6, 3.3, [4.0, 3.0, 5.1], 16, .5)
code(['교사용 "제출현황" 표를 추가해 줘.', '- 가입 학생(members)을 한 줄씩: 이름 / 제출·미제출 / 시각 (이름은 users/{uid}의 name)', '- 제출 여부는 submissions/{uid} 문서가 있는지로 판단', '- 학생 줄을 누르면 문항별 답, 선택형은 맞음/틀림 표시 (보기 번호는 1부터)', '- 학생에게는 보이지 않게'], .6, 5.3, 12.1, 1.55, 15, CODE)
end(m)

m = mk(38, M5, '개념', '생각해 보기: 정답이 문항 속에 있으면?')
body(['정답을 questions[]에 같이 저장했다', '학생이 문항 문서를 읽으면 정답도 읽을 수 있지 않을까?', '옆 사람과 1분 토론한 뒤 대안을 찾아 본다'], .6, 1.7, 12.1, 2.1)
box('문항 문서\n질문 / 보기 / 정답', .6, 4.15, 3.6, 2.0, fs=20, b=True, ln=INK, lw=2)
arrowR(4.3, 5.15, .6, RED)
box('학생이 열면\n정답 줄까지 보임', 5.1, 4.45, 2.8, 1.4, fs=18, fill=REDT, ln=RED, lw=2)
box('대안 ① 정답 없이 서술형 중심으로 운영', 8.3, 4.1, 4.4, .95, fs=16, fill=TEALT, ln=TEAL, lw=2)
box('대안 ② 정답을 교사만 읽는 별도 문서로 분리 (심화)', 8.3, 5.2, 4.4, .95, fs=16, fill=TEALT, ln=TEAL, lw=2)
end(m)

m = mk(39, M5, '정리', '막힘 모음과 복구 지점')
body(['모듈 5 완성: 작성 → 제출 → 제출현황', '막히면 오류 메시지를 그대로 Claude Code에 붙여넣는다'], .6, 1.65, 12.1, 1.4)
for i, c in enumerate([('교사 학습지 작성', '콘솔에서 worksheets 문서 생성 확인'), ('학생 제출', '콘솔에서 submissions/{내 uid} 문서 확인'), ('교사 제출현황', '제출한 학생이 "제출"로 보이는지')]):
    x = .6 + i * 4.1
    box('', x, 3.3, 3.9, 2.0, ln=TEAL, lw=2)
    checkbox(x + .2, 3.5)
    T(c[0], x + .65, 3.4, 3.1, .5, fs=20, b=True, va='middle')
    T(c[1], x + .2, 4.1, 3.5, 1.0, fs=16)
T('정답 비교가 모두 틀림 → 콘솔에서 answer가 0부터 센 숫자인지 확인', .6, 5.55, 12.1, .5, fs=18, color=RED, b=True)
cp('checkpoint-m5', .6, 6.25)
end(m)

# ------------------------------------------------------------------ 모듈 6
m = mk(40, M6, '개념', '맞춤 피드백, 세 단계로 만든다')
body(['답안 읽기 → 초안 만들기 → 교사가 검토해 전달', '초안은 보조교사가, 최종 책임은 교사가', '학생에게는 교사가 저장한 피드백만 보인다'], .6, 1.7, 12.1, 2.1)
flow([{'t': '1 답안 읽기\n(학생 답안지\nsubmissions/{uid})', 'fill': TEALT, 'color': TEAL}, {'t': '2 초안 만들기\n(정답 비교 +\n안내 문구)', 'fill': TEALT, 'color': TEAL}, {'t': '3 교사 검토·수정 후 저장\n(feedback)\n교사 확인', 'fill': REDT, 'color': RED, 'bold': True}], .6, 4.1, 12.1, 1.9, fs=20, gap=.7)
end(m)

m = mk(41, M6, '개념', '비밀은 서버에, 피드백은 본인만')
body(['AI 열쇠(API 키)를 브라우저에 두면 누구나 꺼내 쓴다', '열쇠는 서버(Cloud Functions = 교무실 금고)에 둔다', '피드백도 본인 답안지에 붙어 있어 본인만 본다'], .6, 1.7, 12.1, 2.1)
box('X  브라우저에 키 보관\n학생이 개발자 도구(F12)로 열면 키가 보임', .6, 4.0, 5.9, 1.7, fs=20, fill=REDT, ln=RED, lw=3)
box('O  서버(Cloud Functions)에 키 보관\n브라우저는 결과만 받음', 6.8, 4.0, 5.9, 1.7, fs=20, fill=TEALT, ln=TEAL, lw=3)
box('보안 원칙 2: 학생은 자기 제출물만 읽는다 (피드백도 제출물 안에 있다)', .6, 6.0, 12.1, .6, fs=18, b=True, fill=GOLD, ln=GOLDL, lw=1.5, rad=.1)
end(m)

m = mk(42, M6, '실습', '정답 비교로 피드백 초안 만들기')
body(['선택형은 정답과 비교해 "맞음 / 다시 보기"', '제출현황 표에 "피드백 초안 만들기" 버튼 추가'], .6, 1.65, 12.1, 1.4)
code(['학생 답안 화면에 "피드백 초안 만들기" 버튼을 추가해 줘. 누르면 입력칸에 채워 줘.', '1) 선택형: 정답(answer)과 비교 → "문항 N: 맞았어요" / "다시 한 번 살펴보세요"', '2) 교사가 문항마다 적은 "틀렸을 때 안내 문구"를 틀린 문항에 이어 붙인다', '3) 서술형: "문항 N: 선생님이 직접 읽고 코멘트를 남길게요"', '4) 마지막 줄: "총 N문항 중 M문항 맞았어요" (N은 선택형 문항 수)', 'AI는 부르지 말고, 아직 Firestore에 저장하지 마. 입력칸에 채우기만 해.'], .6, 3.4, 12.1, 2.35, 15, CODE)
hint('모두 틀림으로 나오면 학습지의 정답 입력 확인. 버튼이 안 보이면 강력 새로고침', 6.2, 16)
end(m)

m = mk(43, M6, '실습', '고쳐서 저장하면 학생 화면에 도착')
body(['교사가 초안을 마음대로 고친 뒤 "저장"', '저장 위치는 submissions/{uid}의 feedback', '학생 화면에 "선생님 피드백" 카드가 보인다'], .6, 1.7, 12.1, 2.0)
code(['입력칸 아래에 "피드백 저장" 버튼을 추가해 줘.', '- submissions/{uid}의 feedback 필드에만 저장 (updateDoc, 다른 필드는 건드리지 마)', '- 이미 저장된 피드백이 있으면 다시 열 때 입력칸에 불러오기', '- 학생 화면: feedback이 있을 때만 "선생님 피드백" 카드, 없으면 "아직 피드백이 없어요"', '- 피드백 글은 HTML로 해석하지 말고 글자 그대로 출력'], .6, 4.0, 12.1, 1.95, 15, CODE)
hint('권한 오류는 임시 규칙 확인. 카드가 안 보이면 학생이 가입·제출했는지 확인 후 새로고침', 6.3, 16)
end(m)

m = mk(44, M6, '실습', '확인: 제출부터 피드백 수신까지')
body(['두 계정을 크롬 일반 창(교사)과 시크릿 창(학생)으로 나눠 쓴다', '전체 한 바퀴가 되면 완료'], .6, 1.65, 12.1, 1.4)
for i, tt in enumerate(['시크릿 창: 학생 로그인 → 학습지 풀고 제출', '일반 창: 교사 로그인 → 제출현황에서 학생 선택 → "피드백 초안 만들기"', '초안 끝에 교사 한마디를 직접 써 넣고 "피드백 저장"', '시크릿 창: 새로고침 → "선생님 피드백" 카드에 내 글이 보이는지', '(선택) 학생 답을 바꿔 다시 제출 → 초안을 다시 만들어 비교']):
    y = 3.1 + i * .6
    numCircle(i + 1, .6, y + .02, .5, MUTE if i == 4 else RED)
    T(tt, 1.3, y, 11.4, .55, fs=18, va='middle')
hint('피드백이 사라졌다면 "재제출해도 feedback은 지우지 말고 병합 저장으로 바꿔 줘"', 6.35, 16)
end(m)

m = mk(45, M6, '데모', '심화: AI가 초안을 써 주는 피드백')
m['optional'] = True
optionalFrame()
body(['선택 과정: 오늘은 강사 시연, 직접 만들기는 연수 후 과제', 'AI 키는 서버에만. Functions 배포는 Blaze(종량제) 요금제가 필요하고 AI 비용도 든다'], .7, 1.8, 12.0, 1.6)
flow(['브라우저\n(교사가 버튼 클릭)', 'Cloud Functions\n(키 보관, 답안 전달)', 'AI\n(초안 생성)', '교사 화면 입력칸\n(초안만 돌려줌,\n저장 안 함)', {'t': '교사가 검토 후 저장\n(Firestore feedback)\n교사 확인', 'fill': REDT, 'color': RED, 'bold': True}], .7, 4.0, 12.0, 1.6, fs=15, gap=.3)
T('API 키는 여기만', 3.15, 3.55, 2.4, .4, fs=14, color=WHITE, b=True, al='center', va='middle', extra='background:%s;border-radius:%spx;padding:%spx' % (INK, n(.1), pt(2)))
T('함수는 Firestore에 직접 쓰지 않는다', .7, 5.85, 8.0, .5, fs=18, b=True)
placeholder('[QR/링크 자리: 연수 후 과제 프롬프트]', 9.2, 5.8, 3.4, .95, 14)
end(m)

m = mk(46, M6, '정리', 'AI를 쓸 때 지킬 것, 그리고 복구 지점')
body(['교사가 반드시 검토한 뒤 전달한다', '학생 이름·이메일 등 개인정보는 최소한만 AI에 보낸다', '막혔다면 checkpoint-m6에서 이어가기'], .6, 1.7, 12.1, 2.1)
checks(['교사 검토 필수', '개인정보 최소 전달 (이름 대신 번호 등)', '기관 지침 확인'], .6, 4.2, 8.0, 22, .75)
folder('checkpoint-m6', 9.3, 4.4, 3.4, .75)
end(m)

# ------------------------------------------------------------------ 모듈 7
m = mk(47, M7, '개념', '보안 규칙 = 교무실 출입 규칙')
body(['누가 어떤 서류함을 열 수 있는지 규칙이 정한다', '지금까지의 5가지 원칙을 오늘 한 번에 걸어 잠근다', '화면 버튼을 숨기는 것은 안전이 아니다'], .6, 1.65, 12.1, 2.0)
table([['원칙', '한 줄 뜻', '처음 만난 곳'], ['1 가입한 수업 자료만 읽는다', '열쇠 없으면 교실 못 들어감', '슬라이드 28'], ['2 내 제출물만 읽고 쓴다', '내 답안지만 열람', '슬라이드 34, 41'], ['3 수업·자료·학습지 작성은 그 수업 교사만', '교사만 교실을 꾸밈', '슬라이드 20'], ['4 수업코드를 아는 사람만 1건, 전체 목록은 못 본다', '열쇠로 문 하나만 열기', '슬라이드 20'], ['5 교사 HTML은 sandbox iframe으로', '유리 진열장', '슬라이드 28']], .6, 3.5, [5.6, 3.9, 2.6], 15, .46)
T('원칙 1–4는 규칙(서버 쪽)이, 원칙 5는 화면(iframe)이 지킨다', .6, 6.5, 12.1, .4, fs=16, color=RED, b=True)
end(m)

m = mk(48, M7, '실습', '5원칙을 문장으로 주고 규칙 파일 만들기')
body(['보안 규칙 파일(firestore.rules)도 Claude Code가 쓴다', '줄마다 몇 번 원칙인지 설명을 요청한다. 경로는 데이터 모델과 같아야 한다'], .6, 1.65, 12.1, 1.5)
code(['firestore.rules를 새로 작성해 줘. 기존 임시 규칙은 지우고, 기본은 모두 거부.', '경로는 이 이름 그대로: users, classes, members, materials, worksheets, submissions', '원칙 1  가입한 수업의 자료·학습지만 읽는다', '원칙 2  내 제출물만 읽고 쓴다 (학생은 feedback을 못 고침)', '원칙 3  작성은 그 수업의 teacherUid만 (role은 수업을 만들 때만 확인)', '원칙 4  목록은 내 수업만, 코드를 알면 1건 get과 가입은 허용', '원칙 5  규칙이 아니라 화면 일: iframe의 sandbox 확인만', '각 줄 위에 "이 줄은 원칙 N번" 주석 + 마지막에 대응표'], .6, 3.35, 12.1, 2.85, 15, CODE)
hint('role == teacher 줄이 수업 만들기 말고 다른 곳에 있으면 "권한은 teacherUid로 판단하도록 고쳐 줘"', 6.4, 16)
end(m)

m = mk(49, M7, '실습', '규칙과 웹사이트를 인터넷에 올리기')
body(['규칙 배포 = 출입 규칙을 교무실 문에 붙이는 일', 'Hosting 배포 = 우리 클래스룸을 학교 게시판에 올리는 일', '끝나면 누구나 열 수 있는 공개 주소가 생긴다'], .6, 1.7, 12.1, 2.0)
code(['firestore.rules를 배포하고, 이어서 Hosting에도 배포해 줘.', '1. firebase.json에 규칙·색인·hosting(현재 폴더)이 맞게 있는지 확인', '   (규칙·색인·README·samples·functions·숨김 파일은 공개 제외)', '2. 프로젝트 ID는 firebase-config.js의 projectId', '3. 규칙·색인 먼저, 이어서 Hosting 배포', '4. 끝나면 공개 주소(Hosting URL)를 알려 줘'], .6, 4.0, 12.1, 2.1, 15, CODE)
hint('로그인 오류면 안내받은 firebase login을 내가 직접 실행. "콘솔에만 있는 색인을 지울까요?"는 N', 6.3, 16)
end(m)

m = mk(50, M7, '실습', '막히는지 직접 눈으로 확인하기')
T('rules-check.html 점검: 막힘 6개 + 열림 2개가 나오면 성공 · 준비: 수업 A, B 만들기 / 학생은 B에만 가입', .6, 1.6, 12.1, .7, fs=18, color=RED, b=True, va='middle')
table([['버튼', '시도', '기대', '원칙'],
       ['1', '가입하지 않은 수업(A) 자료 읽기', '막힘', '1'], ['2', '제출물 목록 읽기 / 다른 학생 제출물 읽기', '막힘', '2'], ['3', '학생 계정으로 수업 만들기', '막힘', '3'],
       ['4', '수업 전체 목록 읽기', '막힘', '4'], ['5', '내 제출물의 feedback 고치기', '막힘', '2'], ['6', '가입한 수업(B)에 자료 1건 쓰기', '막힘', '3'],
       ['확인', '가입한 수업 자료 읽기 + 내 제출물 읽기', '열림 2개', '1, 2']], .6, 2.35, [1.3, 6.9, 2.2, 1.7], 15, .38)
T('안 막히면 규칙이 틀린 것 → 슬라이드 48로', .6, 5.55, 12.1, .4, fs=16, color=RED, b=True)
code(['checkpoint-final의 rules-check.html, rules-check.js를 이 폴더에 복사하고 Hosting을 다시 배포해 줘.'], .6, 6.3, 12.1, .55, 14, '점검 페이지가 없는 분만')
end(m)

m = mk(51, M7, '정리', '검증 체크리스트 5항목')
body(['원칙 1–5를 하나씩 확인하고 O, X로 기록한다'], .6, 1.65, 12.1, .6)
table([['원칙', '확인 방법', '결과'], ['1 가입한 수업 자료만 읽는다', '버튼 1 막힘, 확인 버튼 열림', '☐'], ['2 내 제출물만 읽고 쓴다', '버튼 2·5 막힘, 내 제출물 열림', '☐'], ['3 작성은 그 수업 교사만', '버튼 3·6 막힘', '☐'], ['4 코드로 1건만, 전체 목록 불가', '버튼 4 막힘, 코드로 가입은 정상', '☐'], ['5 자료는 sandbox iframe', 'Claude Code에게 확인 요청', '☐']], .6, 2.45, [4.8, 6.0, 1.3], 16, .55)
box('로그인이 안 되면: 콘솔 보안 > Authentication > 설정 탭 > 승인된 도메인에 내 배포 주소(프로젝트ID.web.app) 추가', .6, 5.95, 12.1, .75, fs=16, fill=GOLD, ln=GOLDL, lw=1.5)
end(m)

m = mk(52, M7, '정리', '오늘 만든 것: 7개 모듈 회고')
body(['마무리 5분. 오늘 만든 것을 한 장으로 돌아본다', '내 주소로 누구나 들어올 수 있는 클래스룸이 생겼다'], .6, 1.65, 12.1, 1.5)
tl = [('1 도입', '빈 폴더 +\n"환영합니다"'), ('2 로그인', '구글 로그인 +\n역할 저장'), ('3 수업코드', '수업 만들기 +\n코드 가입'), ('4 자료', 'HTML 자료 +\nsandbox 열람'), ('5 학습지', '작성·제출·\n제출현황'), ('6 피드백', '초안·수정·\n학생 열람'), ('7 배포', '보안 규칙 +\n공개 주소')]
w, g = 1.62, .127
for i, tt in enumerate(tl):
    x = .6 + i * (w + g)
    chip(tt[0], x, 3.5, w, .6, RED if i == 6 else TEAL, 16)
    box(tt[1], x, 4.2, w, 1.4, fs=15, ln=RED if i == 6 else TEAL, lw=2)
T('오늘의 최종 산출물: 내 클래스룸 공개 주소', .6, 5.95, 12.1, .6, fs=24, color=RED, b=True)
end(m)

m = mk(53, M7, '정리', '우리 학교에서 쓰기 전에 확인할 3가지')
body(['개인정보: 학생 이름·이메일은 꼭 필요한 것만. 기관 지침을 따른다', '정리: 오늘 쓴 테스트 계정과 테스트 데이터는 지운다', '요금: Firebase 요금제와 무료 한도를 확인한다. AI 피드백(Functions)은 Blaze가 필요하다'], .6, 1.7, 12.1, 2.9)
for i, c in enumerate([('개인정보', TEAL), ('정리', MUTE), ('요금', RED)]):
    x = .6 + i * 4.1
    T(['방패', '빗자루', '동전'][i], x, 4.8, 1.1, 1.1, fs=18, color=WHITE, b=True, al='center', va='middle', extra='background:%s;border-radius:50%%' % c[1])
    checkbox(x + 1.3, 5.2, .34)
    T(c[0] + ' 확인', x + 1.8, 5.05, 2.1, .65, fs=20, b=True, va='middle')
T('실제 학생 정보는 이 연수에서 쓰지 않았습니다.', 6.2, 6.45, 6.5, .4, fs=14, color=MUTE, al='right')
end(m)

m = mk(54, M7, '정리', '다음 걸음과 설문')
body(['심화 과제: AI 피드백 붙이기, 화면 디자인 다듬기', '막혔던 분은 checkpoint-final에서 이어서', '설문에 답하고 내 공개 주소를 적어 두자'], .6, 1.7, 12.1, 2.0)
for i, c in enumerate([('심화 과제', '[QR 자리]\n슬라이드 45 연수 후 과제 프롬프트\n예: "학생 화면을 글자를 크게, 색을 부드럽게 바꿔 줘"'), ('자료 링크', '[링크 자리: 강사가 연수 직전에 채움]\n오늘 슬라이드 · 프롬프트 모음 · checkpoint-final'), ('설문', '[설문 링크/QR 자리: 강사가 연수 직전에 채움]')]):
    x = .6 + i * 4.1
    T(c[0], x, 3.9, 3.9, .5, fs=20, color=TEAL, b=True)
    placeholder(c[1], x, 4.45, 3.9, 2.3, 15)
end(m)

assert [m_['num'] for m_, _ in SLIDES] == list(range(1, 55)), 'slide count'

# ------------------------------------------------------------------ 복사 텍스트 (notes의 프롬프트 전문 우선)
def dedent_lines(s):
    lines = s.split('\n')
    return [l[1:] if l.startswith(' ') else l for l in lines]

def clean_copy(s):
    s = MARK.sub('', s)
    s = '\n'.join(l.rstrip() for l in s.split('\n'))
    return s.strip('\n')

def fences_of(notes):
    m_ = re.search(r'\[복사용 프롬프트 전문[^\]]*\]\n(.*?)(?=\n\n\[|\Z)', notes, re.S)
    if not m_: return []
    sect = '\n'.join(dedent_lines(m_.group(1)))
    return [f.strip('\n') for f in re.findall(r'```[^\n]*\n(.*?)```', sect, re.S)]

copy_map = {}
diag = []
for meta, _ in SLIDES:
    pass

def resolve_copies():
    out = {}
    ci = 0
    for meta, _html in SLIDES:
        # 이 슬라이드의 코드 블록 인덱스 찾기
        idxs = [int(x) for x in re.findall(r'@@CODE(\d+)@@', _html)]
        fs_ = fences_of(NOTES[str(meta['num'])]['notes'])
        for i in idxs:
            slide_txt = '\n'.join(CODES[i]['lines'])
            best, bs = None, 0
            for f in fs_:
                sc = difflib.SequenceMatcher(None, slide_txt, f).ratio()
                if sc > bs: best, bs = f, sc
            if len(fs_) == 1:
                out[i] = (clean_copy(fs_[0]), 'notes 전문 (유일한 fence, 유사도 %.2f)' % bs)
            elif best is not None and bs >= 0.45:
                out[i] = (clean_copy(best), 'notes 전문 (%.2f)' % bs)
            else:
                out[i] = (clean_copy(slide_txt), '슬라이드 블록 (fence %d개, best %.2f)' % (len(fs_), bs))
            diag.append((meta['num'], i, out[i][1]))
    return out

COPY = resolve_copies()

# ------------------------------------------------------------------ HTML 조립
BADGE = {'개념': 'var(--teal)', '실습': 'var(--red)', '데모': 'var(--gold-l)', '정리': 'var(--mute)'}
frames = []
for meta, inner in SLIDES:
    num = meta['num']
    for i in range(len(CODES)):
        tok = '@@CODE%d@@' % i
        if tok in inner:
            inner = inner.replace(tok, esc(COPY[i][0]))
    title = meta['title'] or '나만의 온라인 클래스룸 만들기'
    tcls = 'title' + (' long' if len(meta['title']) > 21 else '')
    head = ('<div class="a mod" style="%s">%s</div>' % (pos(.6, .3, 5.2, .36), esc(meta['mod'])) +
            '<div class="a badge" style="%s;background:%s">%s</div>' % (pos(5.9, .3, .9, .36), BADGE[meta['typ']], esc(meta['typ'])))
    if meta['title']:
        head += '<div class="a %s" role="heading" aria-level="2" style="%s">%s</div>' % (tcls, pos(.6, .72, 12.1, .85), esc(meta['title']))
    else:
        head += '<div class="sr" role="heading" aria-level="2">%s</div>' % esc(title)
    foot = '<div class="a foot" style="%s">온라인 클래스룸 교원 연수</div><div class="a pg" style="%s">%d / 54</div>' % (pos(.6, 7.02, 5, .3), pos(11.3, 7.0, 1.5, .3), num)
    frames.append('<section class="frame" id="s%d" data-n="%d" data-title="%s" hidden><div class="slide">%s%s%s</div></section>' % (num, num, esc(title), head, inner, foot))

NOTES_OUT = {k: v['notes'] for k, v in NOTES.items()}
notes_json = json.dumps(NOTES_OUT, ensure_ascii=False).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026').replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
titles_json = json.dumps({m_['num']: (m_['title'] or '나만의 온라인 클래스룸 만들기') for m_, _ in SLIDES}, ensure_ascii=False).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')



CSS = r'''
:root{--bg:#f8f2e4;--ink:#2a2314;--red:#b0402c;--teal:#356e67;--card:#fffbf0;--line:#d9cdb0;--mute:#6b5e45;
--teal-t:#dce9e5;--red-t:#f3ddd6;--gold:#fff1cc;--gold-l:#c9a24a;--paper2:#f1e8d2;--code:#241d15;--shell:#17120c;
--font:"Pretendard","Apple SD Gothic Neo","Malgun Gothic",sans-serif;
--mono:"D2Coding","SF Mono","Consolas","Menlo","Malgun Gothic","Apple SD Gothic Neo",monospace}
*{box-sizing:border-box}
html,body{margin:0;height:100%;background:var(--shell);overflow:hidden;font-family:var(--font)}
button{font-family:inherit}
#viewport{position:fixed;inset:0;overflow:hidden}
#stage{position:absolute;left:0;top:0;width:1333px;height:750px;transform-origin:0 0;background:var(--bg);box-shadow:0 0 40px rgba(0,0,0,.5)}
.frame{position:absolute;left:0;top:0;width:1333px;height:750px}
.frame[hidden]{display:none}
.slide{position:relative;width:1333px;height:750px;background:var(--bg);overflow:hidden;color:var(--ink);line-height:1.28;word-break:keep-all;overflow-wrap:anywhere}
.a{position:absolute;margin:0;display:flex;flex-direction:column}
.a>.t{width:100%}
table.a{display:table}
ul.a{display:block}
.mod{font-size:22.2px;color:var(--teal);font-weight:700;justify-content:center;white-space:nowrap}
.badge{color:#fff;font-size:19.4px;font-weight:700;text-align:center;justify-content:center;border-radius:18px}
.title{font-size:50px;font-weight:700;justify-content:center;white-space:nowrap;line-height:1.15}
.title.long{font-size:44px}
.foot,.pg{font-size:16.7px;color:var(--mute);justify-content:center}
.pg{text-align:right}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
.ph{background:var(--gold);border:2.8px dashed var(--red);color:var(--red);font-weight:700;text-align:center;justify-content:center;padding:8px;border-radius:0}
.ar-r{clip-path:polygon(0 28%,58% 28%,58% 0,100% 50%,58% 100%,58% 72%,0 72%)}
.ar-d{clip-path:polygon(28% 0,72% 0,72% 58%,100% 58%,50% 100%,0 58%,28% 58%)}
.ar-u{clip-path:polygon(50% 0,100% 42%,72% 42%,72% 100%,28% 100%,28% 42%,0 42%)}
.hex{clip-path:polygon(18% 0,82% 0,100% 50%,82% 100%,18% 100%,0 50%);line-height:1.15}
.callout::after{content:"";position:absolute;left:46px;bottom:-17px;border-left:12px solid transparent;border-right:12px solid transparent;border-top:18px solid var(--gold-l)}
.code{background:var(--code);border-radius:10px;padding:10px 20px;color:#f8f2e4;font-family:var(--mono);overflow:hidden;display:block}
.code pre{margin:0;font:inherit;white-space:pre-wrap;line-height:1.32;word-break:normal;overflow-wrap:anywhere}
.code code{font:inherit}
.copy-btn{position:absolute;background:var(--teal);color:#fff;border:0;border-radius:8px;font-size:17px;font-weight:700;cursor:pointer;padding:0}
.copy-btn:hover{background:#2b5a54}
.copy-btn.ok{background:var(--red)}
.body{margin:0;padding:0;list-style:none}
.body li{position:relative;padding-left:33px;margin-bottom:8px}
.body li::before{content:"";position:absolute;left:6px;top:.62em;width:.3em;height:.3em;border-radius:50%;background:var(--ink)}
.tb{border-collapse:collapse;table-layout:fixed}
.tb th,.tb td{border:1.4px solid var(--line);padding:4px 10px;vertical-align:middle;line-height:1.25}
.tb th{color:#fff;font-weight:700}
.timer{font-size:166px;font-weight:700;color:var(--red);text-align:center;justify-content:center;font-variant-numeric:tabular-nums;line-height:1}
.timer.done{animation:blink 1s steps(2) infinite}
@keyframes blink{50%{opacity:.25}}
.tbtns{flex-direction:row;gap:16px;justify-content:center;align-items:center}
.tbtn{font-size:25px;font-weight:700;padding:6px 30px;border:0;border-radius:12px;background:var(--teal);color:#fff;cursor:pointer}
.tbtn[data-timer=stop]{background:var(--red)}
.tbtn.ghost{background:var(--paper2);color:var(--ink);border:1.5px solid var(--line)}
/* 도구 모음 */
#bar{position:fixed;display:flex;align-items:center;gap:4px;background:rgba(36,29,21,.92);color:#f8f2e4;padding:5px 8px;border-radius:14px;transition:opacity .4s;z-index:20;transform:translateX(-50%)}
#bar.idle{opacity:0}
#bar:hover,#bar:focus-within{opacity:1}
#bar button{background:transparent;color:inherit;border:0;border-radius:9px;min-width:42px;height:38px;font-size:16px;cursor:pointer;padding:0 10px}
#bar button:hover,#bar button:focus-visible{background:rgba(255,255,255,.18);outline:none}
#bar button[aria-pressed=true]{background:var(--red)}
#cnt{font-size:16px;min-width:74px;text-align:center;font-variant-numeric:tabular-nums}
#prog{position:fixed;left:0;bottom:0;height:4px;background:var(--red);z-index:19;transition:width .2s}
#notes{position:fixed;background:var(--card);color:var(--ink);z-index:15;display:none;flex-direction:column;border:0 solid var(--line)}
body.notes-open #notes{display:flex}
body.notes-side #notes{right:0;top:0;bottom:0;width:34vw;min-width:300px;border-left-width:2px}
body.notes-bottom #notes{left:0;right:0;bottom:0;height:38vh;border-top-width:2px}
#notes header{display:flex;align-items:center;justify-content:space-between;padding:8px 14px;background:var(--paper2);font-weight:700;font-size:15px;color:var(--teal);flex:none}
#notes header button{border:1px solid var(--line);background:#fff;border-radius:8px;padding:3px 10px;cursor:pointer;font-size:14px}
#nbody{overflow:auto;padding:10px 16px 24px;font-size:15px;line-height:1.55;flex:1}
#nbody h3{margin:14px 0 4px;font-size:15px;color:var(--teal)}
#nbody h3.chk{color:var(--red)}
#nbody p{margin:3px 0;white-space:pre-wrap;word-break:keep-all;overflow-wrap:anywhere}
#nbody pre{margin:6px 0;background:var(--code);color:#f8f2e4;padding:9px 12px;border-radius:8px;font:13px/1.45 var(--mono);white-space:pre-wrap;overflow-wrap:anywhere}
#nbody code{background:var(--paper2);padding:0 4px;border-radius:4px;font-family:var(--mono);font-size:.92em}
#nbody pre code{background:none;padding:0}
#ov{position:fixed;inset:0;background:#17120c;z-index:30;overflow:auto;display:none;padding:20px 16px 50px}
body.ov-open #ov{display:block}
#ov h2{color:#f8f2e4;font-size:17px;text-align:center;margin:0 0 14px;font-weight:600}
#grid{display:grid;gap:16px 14px;justify-content:center}
.cell{background:none;border:0;padding:0;color:#f8f2e4;text-align:left;cursor:pointer;font-size:13px;width:var(--cw)}
.cell .thumb{position:relative;width:var(--cw);height:calc(var(--cw)*.5627);overflow:hidden;background:var(--bg);border:3px solid transparent;border-radius:6px}
.cell .thumb .frame{position:absolute;left:0;top:0;transform-origin:0 0;pointer-events:none}
.cell:hover .thumb,.cell:focus-visible .thumb{border-color:var(--gold-l)}
.cell:focus-visible{outline:none}
.cell.cur .thumb{border-color:var(--red)}
.cell span{display:block;margin-top:4px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#copydlg{position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:40;display:none;align-items:center;justify-content:center;padding:16px}
body.dlg-open #copydlg{display:flex}
#copydlg div{background:var(--card);border-radius:12px;padding:16px;width:min(720px,100%);color:var(--ink)}
#copydlg p{margin:0 0 8px;font-size:15px}
#copydlg textarea{width:100%;height:240px;font:14px/1.45 var(--mono);padding:8px;border:1px solid var(--line);border-radius:8px;background:#fff}
#copydlg button{margin-top:8px;padding:6px 18px;border:0;border-radius:8px;background:var(--teal);color:#fff;font-size:15px;cursor:pointer}
@media print{
@page{size:13.333in 7.5in;margin:0}
html,body{height:auto;overflow:visible;background:#fff}
#viewport{position:static;overflow:visible}
#stage{position:static;transform:none!important;width:auto;height:auto;box-shadow:none;background:#fff}
.frame,.frame[hidden]{display:block!important;position:relative;width:1280px;height:720px;overflow:hidden;break-after:page;page-break-after:always}
.frame:last-child,.frame[hidden]:last-child{break-after:avoid!important;page-break-after:avoid!important}
body>:not(#viewport){display:none!important}
#viewport,#stage{margin:0;padding:0}
.slide{transform:scale(.96);transform-origin:0 0}
#bar,#notes,#ov,#prog,#copydlg,.copy-btn,.tbtns{display:none!important}
*{-webkit-print-color-adjust:exact;print-color-adjust:exact}
}
'''

JS = r'''
(function(){
'use strict';
var TOTAL=54;
var NOTES=JSON.parse(document.getElementById('notes-data').textContent);
var TITLES=JSON.parse(document.getElementById('titles-data').textContent);
var frames=[].slice.call(document.querySelectorAll('#stage > .frame'));
var stage=document.getElementById('stage'),vp=document.getElementById('viewport');
var bar=document.getElementById('bar'),cnt=document.getElementById('cnt'),prog=document.getElementById('prog');
var notesEl=document.getElementById('notes'),nbody=document.getElementById('nbody'),ntitle=document.getElementById('ntitle');
var status=document.getElementById('status');
var cur=0,body=document.body,idleT=null;

function clamp(n){return Math.max(1,Math.min(TOTAL,n))}
function fromHash(){var m=/^#\/?(\d+)/.exec(location.hash);return m?clamp(parseInt(m[1],10)):1}

function layout(){
  var W=window.innerWidth,H=window.innerHeight,aw=W,ah=H;
  body.classList.remove('notes-side','notes-bottom');
  if(body.classList.contains('notes-open')){
    if(W/H>1.25){body.classList.add('notes-side');aw=W-Math.max(300,W*.34)}
    else{body.classList.add('notes-bottom');ah=H-H*.38}
  }
  var s=Math.min(aw/1333,ah/750);
  var x=(aw-1333*s)/2,y=(ah-750*s)/2;
  stage.style.transform='translate('+x+'px,'+y+'px) scale('+s+')';
  bar.style.left=(aw/2)+'px';bar.style.bottom=(H-ah+10)+'px';
}

function inline(parent,text){
  var re=/(`[^`]+`|\*\*[^*]+\*\*)/g,parts=text.split(re);
  parts.forEach(function(p){
    if(!p)return;
    var el;
    if(p.charAt(0)==='`'&&p.length>2){el=document.createElement('code');el.textContent=p.slice(1,-1);parent.appendChild(el)}
    else if(p.slice(0,2)==='**'&&p.length>4){el=document.createElement('strong');el.textContent=p.slice(2,-2);parent.appendChild(el)}
    else parent.appendChild(document.createTextNode(p));
  });
}
function renderNotes(n){
  ntitle.textContent='발표자 노트 · 슬라이드 '+n+' / '+TOTAL+' · '+TITLES[n];
  nbody.textContent='';
  var txt=NOTES[String(n)]||'(노트 없음)',lines=txt.split('\n'),inFence=false,pre=null,first=true;
  lines.forEach(function(l){
    var t=l.replace(/^ /,'');
    if(/^\s*```/.test(t)){
      if(!inFence){pre=document.createElement('pre');pre.appendChild(document.createElement('code'));nbody.appendChild(pre);inFence=true}
      else{inFence=false;pre=null}
      return;
    }
    if(inFence){var c=pre.firstChild;c.textContent+=(c.textContent?'\n':'')+t;return}
    if(!t.trim())return;
    var hm=/^\[([^\]]+)\](.*)$/.exec(t);
    if(hm&&/^(강사 확인|발표자 노트|복사용|예상 결과|막힐 때|연수 후|부록)/.test(hm[1])&&/^\s*(\(.*\))?\s*$/.test(hm[2])){
      var h=document.createElement('h3');h.textContent='['+hm[1]+']'+hm[2];
      if(/^강사 확인/.test(hm[1]))h.className='chk';
      nbody.appendChild(h);return;
    }
    var p=document.createElement('p');inline(p,t);nbody.appendChild(p);
  });
  nbody.scrollTop=0;
}

function go(n,noHash){
  n=clamp(n);
  if(cur){var o=frames[cur-1];o.hidden=true;o.setAttribute('aria-hidden','true')}
  cur=n;var f=frames[n-1];f.hidden=false;f.removeAttribute('aria-hidden');
  cnt.textContent=n+' / '+TOTAL;
  prog.style.width=(n/TOTAL*100)+'%';
  status.textContent='슬라이드 '+n+' / '+TOTAL+': '+TITLES[n];
  document.title='온라인 클래스룸 교원 연수 ('+n+'/'+TOTAL+')';
  if(!noHash){try{history.replaceState(null,'','#'+n)}catch(e){location.hash=n}}
  if(body.classList.contains('notes-open'))renderNotes(n);
  markCells();
}
function next(){go(cur+1)}function prev(){go(cur-1)}

function toggleNotes(force){
  var on=force===undefined?!body.classList.contains('notes-open'):force;
  body.classList.toggle('notes-open',on);
  document.getElementById('bnotes').setAttribute('aria-pressed',on?'true':'false');
  notesEl.setAttribute('aria-hidden',on?'false':'true');
  if(on)renderNotes(cur);
  layout();
}

/* 개요 그리드 */
var ov=document.getElementById('ov'),grid=document.getElementById('grid'),cells=[];
function buildGrid(){
  var cw=window.innerWidth<640?150:(window.innerWidth<1100?200:240);
  grid.style.setProperty('--cw',cw+'px');
  grid.style.gridTemplateColumns='repeat(auto-fill,'+cw+'px)';
  if(cells.length)return;
  frames.forEach(function(fr,i){
    var b=document.createElement('button');b.type='button';b.className='cell';b.dataset.n=i+1;
    b.setAttribute('aria-label','슬라이드 '+(i+1)+': '+TITLES[i+1]);
    var th=document.createElement('div');th.className='thumb';th.setAttribute('aria-hidden','true');
    var cl=fr.cloneNode(true);cl.removeAttribute('id');cl.hidden=false;cl.removeAttribute('aria-hidden');
    cl.setAttribute('inert','');th.appendChild(cl);b.appendChild(th);
    var sp=document.createElement('span');sp.textContent=(i+1)+'. '+TITLES[i+1];b.appendChild(sp);
    grid.appendChild(b);cells.push(b);
  });
}
function scaleThumbs(){
  var cw=parseFloat(grid.style.getPropertyValue('--cw'))-6;
  cells.forEach(function(b){var f=b.firstChild.firstChild;f.style.transform='scale('+(cw/1333)+')'});
}
function markCells(){cells.forEach(function(b,i){b.classList.toggle('cur',i+1===cur)})}
function openOv(){
  buildGrid();scaleThumbs();body.classList.add('ov-open');markCells();
  document.getElementById('bgrid').setAttribute('aria-pressed','true');
  var c=cells[cur-1];if(c){c.focus({preventScroll:true});c.scrollIntoView({block:'center'})}
}
function closeOv(){
  body.classList.remove('ov-open');document.getElementById('bgrid').setAttribute('aria-pressed','false');
}
function toggleOv(){body.classList.contains('ov-open')?closeOv():openOv()}
grid.addEventListener('click',function(e){
  var b=e.target.closest('.cell');if(!b)return;
  go(parseInt(b.dataset.n,10));closeOv();
});
function gridKey(e){
  var i=cells.indexOf(document.activeElement);if(i<0)i=cur-1;
  var cols=1;if(cells.length>1){var t0=cells[0].offsetTop;while(cols<cells.length&&cells[cols].offsetTop===t0)cols++}
  var d={ArrowRight:1,ArrowLeft:-1,ArrowDown:cols,ArrowUp:-cols,PageDown:cols*2,PageUp:-cols*2}[e.key];
  if(d!==undefined){e.preventDefault();var j=Math.max(0,Math.min(cells.length-1,i+d));cells[j].focus();return true}
  if(e.key==='Home'){e.preventDefault();cells[0].focus();return true}
  if(e.key==='End'){e.preventDefault();cells[cells.length-1].focus();return true}
  return false;
}

/* 전체화면 */
function toggleFs(){
  var d=document,el=d.documentElement;
  if(d.fullscreenElement||d.webkitFullscreenElement){(d.exitFullscreen||d.webkitExitFullscreen).call(d)}
  else{var r=el.requestFullscreen||el.webkitRequestFullscreen;if(r){var p=r.call(el);if(p&&p.catch)p.catch(function(){})}}
}

/* 키보드 */
document.addEventListener('keydown',function(e){
  if(e.ctrlKey||e.metaKey||e.altKey)return;
  var tg=e.target,tag=tg&&tg.tagName;
  if(tag==='TEXTAREA'||tag==='INPUT'||tag==='SELECT')return;
  if(body.classList.contains('dlg-open')){if(e.key==='Escape')closeDlg();return}
  var k=e.key;
  if(body.classList.contains('ov-open')){
    if(k==='Escape'||k==='g'||k==='G'||k==='o'||k==='O'){e.preventDefault();closeOv();return}
    if(gridKey(e))return;
    return;
  }
  if((k===' '||k==='Enter')&&tg&&tg.closest&&tg.closest('button,a'))return;
  switch(k){
    case 'ArrowRight':case 'PageDown':e.preventDefault();next();break;
    case ' ':e.preventDefault();e.shiftKey?prev():next();break;
    case 'ArrowLeft':case 'PageUp':e.preventDefault();prev();break;
    case 'Home':e.preventDefault();go(1);break;
    case 'End':e.preventDefault();go(TOTAL);break;
    case 'g':case 'G':case 'o':case 'O':e.preventDefault();openOv();break;
    case 'n':case 'N':e.preventDefault();toggleNotes();break;
    case 'f':case 'F':e.preventDefault();toggleFs();break;
    case 'Escape':if(body.classList.contains('notes-open'))toggleNotes(false);break;
  }
  wake();
});

/* 클릭, 스와이프 */
stage.addEventListener('click',function(e){
  if(e.target.closest('button,a,.code,textarea,input'))return;
  var sel=window.getSelection&&window.getSelection().toString();if(sel)return;
  var r=stage.getBoundingClientRect();
  (e.clientX-r.left)<r.width*.25?prev():next();
});
var tx=0,ty=0,tt=0,tOk=false;
vp.addEventListener('touchstart',function(e){
  tOk=e.touches.length===1&&!e.target.closest('#notes,#ov,#bar,#copydlg,.code');
  if(tOk){tx=e.touches[0].clientX;ty=e.touches[0].clientY;tt=Date.now()}
  wake();
},{passive:true});
vp.addEventListener('touchend',function(e){
  if(!tOk||!e.changedTouches.length)return;tOk=false;
  var dx=e.changedTouches[0].clientX-tx,dy=e.changedTouches[0].clientY-ty;
  if(Math.abs(dx)>50&&Math.abs(dx)>Math.abs(dy)*1.5&&Date.now()-tt<900){dx<0?next():prev()}
},{passive:true});

/* 도구 모음 */
document.getElementById('bprev').addEventListener('click',prev);
document.getElementById('bnext').addEventListener('click',next);
document.getElementById('bgrid').addEventListener('click',toggleOv);
document.getElementById('bnotes').addEventListener('click',function(){toggleNotes()});
document.getElementById('bfs').addEventListener('click',toggleFs);
document.getElementById('nclose').addEventListener('click',function(){toggleNotes(false)});
document.addEventListener('click',function(e){var b=e.target.closest('button');if(b&&e.detail>0)b.blur()});
function wake(){bar.classList.remove('idle');clearTimeout(idleT);idleT=setTimeout(function(){bar.classList.add('idle')},2800)}
['mousemove','pointerdown','touchstart'].forEach(function(ev){document.addEventListener(ev,wake,{passive:true})});

/* 복사 */
var MARKRE=/\s*`?\[(?:재확인 필요|확인필요)[^\]]*\]`?/g;
var dlg=document.getElementById('copydlg'),dta=document.getElementById('dta');
function closeDlg(){body.classList.remove('dlg-open')}
document.getElementById('dclose').addEventListener('click',closeDlg);
function legacyCopy(t){
  var ta=document.createElement('textarea');ta.value=t;ta.setAttribute('readonly','');
  ta.style.cssText='position:fixed;left:-9999px;top:0;opacity:0';document.body.appendChild(ta);
  ta.select();ta.setSelectionRange(0,t.length);var ok=false;
  try{ok=document.execCommand('copy')}catch(e){}
  document.body.removeChild(ta);return ok;
}
function showFallback(t){dta.value=t;body.classList.add('dlg-open');dta.focus();dta.select()}
function copyText(t,btn){
  t=t.replace(MARKRE,'');
  function done(ok){
    if(!ok){showFallback(t);return}
    var o=btn.textContent;btn.textContent='복사됨';btn.classList.add('ok');
    setTimeout(function(){btn.textContent='복사';btn.classList.remove('ok')},1600);
  }
  if(navigator.clipboard&&navigator.clipboard.writeText){
    navigator.clipboard.writeText(t).then(function(){done(true)},function(){done(legacyCopy(t))});
  }else done(legacyCopy(t));
}
document.addEventListener('click',function(e){
  var b=e.target.closest('.copy-btn');if(!b||b.closest('.thumb'))return;
  e.stopPropagation();copyText(b.getAttribute('data-code')||'',b);
});

/* 휴식 타이머 */
var T0=600,left=T0,endAt=0,tid=null;
function fmt(s){var m=Math.floor(s/60),r=s%60;return (m<10?'0':'')+m+':'+(r<10?'0':'')+r}
function paint(){[].forEach.call(document.querySelectorAll('[data-timer-display]'),function(el){el.textContent=fmt(left);el.classList.toggle('done',left===0&&tid===null&&running)})}
var running=false;
function beep(){try{var C=window.AudioContext||window.webkitAudioContext,c=new C(),o=c.createOscillator(),g=c.createGain();o.connect(g);g.connect(c.destination);o.frequency.value=880;g.gain.value=.15;o.start();setTimeout(function(){o.stop();c.close()},700)}catch(e){}}
function tick(){
  left=Math.max(0,Math.ceil((endAt-Date.now())/1000));
  if(left===0){clearInterval(tid);tid=null;beep();paint();return}
  paint();
}
function tStart(){if(tid!==null)return;if(left<=0)left=T0;running=true;endAt=Date.now()+left*1000;tid=setInterval(tick,250);paint()}
function tStop(){if(tid!==null){clearInterval(tid);tid=null;left=Math.max(0,Math.ceil((endAt-Date.now())/1000))}running=false;paint()}
function tReset(){tStop();left=T0;running=false;paint()}
document.addEventListener('click',function(e){
  var b=e.target.closest('[data-timer]');if(!b||b.closest('.thumb'))return;
  var a=b.getAttribute('data-timer');a==='start'?tStart():a==='stop'?tStop():tReset();
});

window.addEventListener('resize',function(){layout();if(body.classList.contains('ov-open')){buildGrid();scaleThumbs()}});
window.addEventListener('hashchange',function(){var n=fromHash();if(n!==cur)go(n,true)});
notesEl.setAttribute('aria-hidden','true');
layout();go(fromHash(),true);wake();
})();
'''

HTML = '''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>온라인 클래스룸 교원 연수</title>
<style>@@CSS@@</style>
<noscript><style>html,body{overflow:auto}#viewport{position:static}#stage{position:static;width:auto;height:auto}.frame,.frame[hidden]{display:block;position:relative;margin:0 auto 12px}</style></noscript>
</head>
<body>
<div id="viewport">
<main id="stage" role="region" aria-label="슬라이드" aria-roledescription="슬라이드 발표" aria-live="polite">
@@FRAMES@@
</main>
</div>
<div id="status" class="sr" role="status" aria-live="polite"></div>
<div id="prog" aria-hidden="true"></div>
<div id="bar" role="toolbar" aria-label="슬라이드 도구">
<button type="button" id="bprev" aria-label="이전 슬라이드">&#9664;</button>
<span id="cnt" aria-label="현재 슬라이드 번호">1 / 54</span>
<button type="button" id="bnext" aria-label="다음 슬라이드">&#9654;</button>
<button type="button" id="bgrid" aria-label="전체 슬라이드 개요 (G)" aria-pressed="false">개요</button>
<button type="button" id="bnotes" aria-label="발표자 노트 보기/숨기기 (N)" aria-pressed="false">노트</button>
<button type="button" id="bfs" aria-label="전체화면 (F)">전체화면</button>
</div>
<aside id="notes" aria-label="발표자 노트" aria-hidden="true">
<header><span id="ntitle">발표자 노트</span><button type="button" id="nclose" aria-label="발표자 노트 닫기">닫기</button></header>
<div id="nbody" tabindex="0"></div>
</aside>
<div id="ov" role="dialog" aria-label="전체 슬라이드 개요"><h2>전체 슬라이드 개요 · 화살표로 이동, Enter로 열기, G 또는 Esc로 닫기</h2><div id="grid"></div></div>
<div id="copydlg" role="dialog" aria-label="복사 대체 창"><div>
<p>자동 복사가 막혀 있습니다. 아래 글이 선택되어 있으니 Ctrl+C(맥은 Cmd+C)로 복사하세요.</p>
<textarea id="dta" readonly aria-label="복사할 프롬프트"></textarea>
<button type="button" id="dclose" aria-label="복사 창 닫기">닫기</button></div></div>
<script type="application/json" id="notes-data">@@NOTES@@</script>
<script type="application/json" id="titles-data">@@TITLES@@</script>
<script>@@JS@@</script>
</body>
</html>
'''

out = (HTML.replace('@@CSS@@', CSS).replace('@@FRAMES@@', '\n'.join(frames))
       .replace('@@NOTES@@', notes_json).replace('@@TITLES@@', titles_json).replace('@@JS@@', JS))
assert '@@' not in out
OUT = os.path.join(HERE, '온라인클래스룸_교원연수.html')
open(OUT, 'w', encoding='utf-8').write(out)
print('wrote', OUT, len(out), 'bytes,', len(SLIDES), 'slides,', len(CODES), 'code blocks')
for d in diag: print('  slide %d code#%d -> %s' % d)
