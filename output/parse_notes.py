# 원고(_workspace/02_writer_M*_slides.md)에서 슬라이드별 발표자 노트, 프롬프트 전문, [확인필요] 표시를 추출해 JSON으로 저장
import re, json, glob, os
BASE = '/Users/heback/harness-workshop/_workspace'
KEYS = ['유형','본문','도식','프롬프트','예상 결과','막힐 때','노트','연수 후 과제 프롬프트']
MARK = re.compile(r'`?\[(?:재확인 필요|확인필요)[^\]]*\]`?')
DECK = re.compile(r'\s*`?\[deck-builder 표기[^\]]*\]`?')

def parse_file(path):
    txt = open(path, encoding='utf-8').read()
    # 슬라이드 아님: '---' 이후 부록/메모는 제외. 단 M2 부록 A는 별도 추출
    appendix = None
    m = re.search(r'^## 부록 A.*?\n(```.*?```)', txt, re.S | re.M)
    if m: appendix = m.group(1).strip('`').strip()
    parts = re.split(r'^## \[슬라이드 (\d+)\] (.+)$', txt, flags=re.M)
    out = {}
    for i in range(1, len(parts), 3):
        n = int(parts[i]); title = parts[i+1].strip(); body = parts[i+2]
        body = re.split(r'^---\s*$', body, flags=re.M)[0]  # 슬라이드 뒤 구분선 이후 제외
        body = re.split(r'^## (?!\[슬라이드)', body, flags=re.M)[0]
        fields = {}; cur = None
        for line in body.split('\n'):
            mm = re.match(r'^- (유형|본문|도식|프롬프트|예상 결과|막힐 때|노트|연수 후 과제 프롬프트)\s*(?:\([^)]*\))?\s*:\s?(.*)$', line)
            if mm:
                cur = mm.group(1); fields[cur] = mm.group(2); continue
            if cur is not None: fields[cur] += '\n' + line
        out[n] = {'n': n, 'title': title, 'fields': {k: v.strip('\n') for k, v in fields.items()}, 'appendix': appendix if n == 13 else None}
    return out

def markers(fields):
    items = []
    for k, v in fields.items():
        flat = v.replace('\n', ' ')
        for m in MARK.finditer(flat):
            s = m.group(0).strip('`')
            before = re.sub(r'`', '', MARK.sub('', flat[:m.start()])).strip()
            ctx = before[-45:].strip()
            if len(ctx) < 8:
                ctx = '(표시 뒤) ' + re.sub(r'`', '', MARK.sub('', flat[m.end():])).strip()[:40]
            items.append((k, s, ctx))
    return items

def clean(t):
    t = DECK.sub('', t)
    t = re.sub(r'[ \t]+\n', '\n', t); t = re.sub(r' {2,}', ' ', t)
    return t.strip()

def build():
    slides = {}
    for f in sorted(glob.glob(BASE + '/02_writer_M*_slides.md')):
        slides.update(parse_file(f))
    res = {}
    for n in sorted(slides):
        s = slides[n]; F = s['fields']
        mk = markers(F)
        seen = []; lines = []
        for k, m, ctx in mk:
            key = (k, m, ctx)
            if key in seen: continue
            seen.append(key)
            lines.append('- (%s) %s  <- "%s"' % (k, m.strip('[]'), ctx))
        parts = []
        if lines:
            parts.append('[강사 확인] (청중 화면에서 제외하고 여기로 옮긴 표시. 내용은 삭제하지 않음)\n' + '\n'.join(lines))
        parts.append('[발표자 노트 원문]\n' + clean(F.get('노트', '(노트 없음)')))
        if F.get('프롬프트'): parts.append('[복사용 프롬프트 전문 / 실습 순서]\n' + clean(F['프롬프트']))
        if F.get('예상 결과'): parts.append('[예상 결과]\n' + clean(F['예상 결과']))
        if F.get('막힐 때'): parts.append('[막힐 때]\n' + clean(F['막힐 때']))
        if F.get('연수 후 과제 프롬프트'): parts.append('[연수 후 과제 프롬프트]\n' + clean(F['연수 후 과제 프롬프트']))
        if s['appendix']: parts.append('[부록 A. 임시 규칙 전문 firestore.temp.rules (규칙 줄은 02_engineer_rules.md 7절 기준, 머리 주석만 줄임)]\n' + s['appendix'])
        res[n] = {'title': s['title'], 'type': F.get('유형', '').strip(), 'notes': '\n\n'.join(parts), 'nmark': len(lines)}
    return res

if __name__ == '__main__':
    r = build()
    json.dump(r, open(os.path.join(os.path.dirname(__file__), 'notes.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(len(r), 'slides', sorted(r)[0], sorted(r)[-1], 'missing:', [i for i in range(1, 55) if i not in r])
    print('markers total', sum(v['nmark'] for v in r.values()))
