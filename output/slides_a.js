// 슬라이드 1~26 (모듈 1~3, 휴식)
const L = require('./lib');
const { C, FONT, MONO } = L;

module.exports = function (pres, N) {
  const mk = (n, mod, type, title) => L.frame(pres, { mod, type, title }, N[n].notes);
  const P = pres.ShapeType;

  // ---------- 모듈 1 ----------
  const M1 = '모듈 1 · 도입 · 완성본 데모';
  { // 1 표지
    const s = L.frame(pres, { mod: M1, type: '정리', title: '' }, N[1].notes);
    s.addText('나만의 온라인 클래스룸 만들기', { x: 0.6, y: 1.5, w: 7.3, h: 2.0, fontSize: 48, bold: true, color: C.ink, fontFace: FONT, margin: 0, valign: 'top', isTextBox: true });
    s.addText('Claude Code로 만드는 교원 연수 · 180분', { x: 0.6, y: 3.6, w: 7.3, h: 0.6, fontSize: 24, color: C.teal, bold: true, fontFace: FONT, margin: 0, isTextBox: true });
    s.addText('오늘의 최종 산출물: 배포된 내 클래스룸 웹 주소 1개', { x: 0.6, y: 4.4, w: 7.3, h: 0.9, fontSize: 24, color: C.ink, fontFace: FONT, margin: 0, isTextBox: true });
    // 브라우저 창 모형
    s.addShape(P.roundRect, { x: 8.3, y: 1.6, w: 4.5, h: 3.6, rectRadius: 0.15, fill: { color: C.card }, line: { color: C.ink, width: 2 } });
    [0, 1, 2].forEach(i => s.addShape(P.ellipse, { x: 8.55 + i * 0.3, y: 1.8, w: 0.18, h: 0.18, fill: { color: [C.red, C.goldL, C.teal][i] }, line: { color: C.card, width: 0 } }));
    s.addText('https://(내 프로젝트).web.app', { x: 8.55, y: 2.2, w: 4.0, h: 0.42, shape: P.roundRect, rectRadius: 0.1, fill: { color: 'F1E8D2' }, color: C.ink, fontSize: 16, fontFace: MONO, align: 'left', valign: 'middle', margin: 8 });
    s.addText('우리 반 온라인 클래스룸', { x: 8.55, y: 3.2, w: 4.0, h: 0.8, fontSize: 24, bold: true, color: C.red, fontFace: FONT, align: 'center', margin: 0, isTextBox: true });
    s.addText('로그인 · 수업코드 · 자료 · 학습지 · 피드백', { x: 8.55, y: 4.1, w: 4.0, h: 0.7, fontSize: 16, color: C.mute, fontFace: FONT, align: 'center', margin: 0, isTextBox: true });
    s.addText('오늘 집에 가져갈 것: https://(내 프로젝트).web.app 형태의 주소', { x: 0.6, y: 6.1, w: 12.1, h: 0.5, fontSize: 24, bold: true, color: C.red, fontFace: FONT, margin: 0, isTextBox: true });
  }
  { // 2 데모
    const s = mk(2, M1, '데모', '완성본 먼저 보기');
    L.body(s, ['오늘 만들 클래스룸을 2분만 먼저 봅니다.', '교사: 수업 만들기 → 자료 → 학습지 → 피드백', '학생: 코드 가입 → 열람 → 제출 → 피드백 확인'], 0.6, 1.7, 12.1, 1.9);
    const t = ['수업 만들기', '자료 등록', '학습지 작성', '피드백 전달'], st = ['수업코드로 가입', '자료 열람', '학습지 제출', '내 피드백 확인'];
    const x0 = 0.6, bw = 1.85, gap = 0.33, y1 = 3.85, y2 = 5.75, h = 0.75;
    s.addText('교사', { x: x0, y: y1 - 0.38, w: 1.5, h: 0.34, fontSize: 16, bold: true, color: C.teal, fontFace: FONT, margin: 0, isTextBox: true });
    s.addText('학생', { x: x0, y: y2 - 0.38, w: 1.5, h: 0.34, fontSize: 16, bold: true, color: C.red, fontFace: FONT, margin: 0, isTextBox: true });
    t.forEach((tx, i) => { const x = x0 + i * (bw + gap); L.box(pres, s, tx, x, y1, bw, h, { fill: { color: C.tealT }, line: { color: C.teal, width: 2 } }); if (i < 3) L.arrowR(pres, s, x + bw + 0.02, y1 + h / 2, 0.29, C.teal); });
    st.forEach((tx, i) => { const x = x0 + i * (bw + gap); L.box(pres, s, tx, x, y2, bw, h, { fill: { color: C.redT }, line: { color: C.red, width: 2 } }); if (i < 3) L.arrowR(pres, s, x + bw + 0.02, y2 + h / 2, 0.29, C.red); });
    // 세로 연결
    const cx = i => x0 + i * (bw + gap) + bw / 2;
    L.arrowD(pres, s, cx(0), y1 + h + 0.1, 0.9, C.mute); s.addText('수업코드', { x: cx(0) + 0.25, y: 4.95, w: 1.4, h: 0.4, fontSize: 16, color: C.ink, bold: true, fontFace: FONT, margin: 0, isTextBox: true });
    s.addShape(P.upArrow, { x: cx(2) - 0.16, y: y1 + h + 0.1, w: 0.32, h: 0.9, fill: { color: C.mute }, line: { color: C.mute, width: 0 } });
    s.addText('제출 답안', { x: cx(2) - 1.75, y: 4.95, w: 1.5, h: 0.4, align: 'right', fontSize: 16, color: C.ink, bold: true, fontFace: FONT, margin: 0, isTextBox: true });
    L.arrowD(pres, s, cx(3), y1 + h + 0.1, 0.9, C.mute); s.addText('피드백', { x: cx(3) + 0.25, y: 4.95, w: 0.7, h: 0.4, fontSize: 16, color: C.ink, bold: true, fontFace: FONT, margin: 0, isTextBox: true });
    L.placeholder(pres, s, '[화면 캡처 자리]\n교사 화면 1장', 9.0, 3.85, 3.75, 1.35);
    L.placeholder(pres, s, '[화면 캡처 자리]\n학생 화면 1장', 9.0, 5.4, 3.75, 1.35);
  }
  { // 3 오늘의 지도와 준비물
    const s = mk(3, M1, '개념', '오늘의 지도와 준비물');
    L.body(s, ['7개 모듈을 하나씩 더해 갑니다.', '연습은 테스트 계정으로만. 실제 학생 정보는 넣지 않습니다.'], 0.6, 1.65, 12.1, 1.4);
    const road = ['1 도입', '2 로그인', '3 수업코드', '휴식', '4 HTML 자료', '5 학습지', '6 맞춤 피드백', '7 배포·보안'];
    const w = 1.37, g = 0.14;
    road.forEach((r, i) => L.chip(pres, s, r, 0.6 + i * (w + g), 3.2, w, 0.62, r === '휴식' ? C.goldL : C.teal, 15));
    const chk = ['구글 계정(교사용) + 테스트 학생용 계정 1개', 'Claude Code 로그인 완료 (유료 계정 필요, 무료 플랜 불가)', 'Node.js, Firebase CLI 설치', '터미널에서 firebase login 완료', '크롬 브라우저'];
    chk.forEach((c, i) => {
      const y = 4.1 + i * 0.52;
      s.addShape(P.rect, { x: 0.6, y: y + 0.07, w: 0.3, h: 0.3, fill: { color: C.card }, line: { color: C.red, width: 2 } });
      s.addText(c, { x: 1.05, y, w: 11.6, h: 0.45, fontSize: 18, color: C.ink, fontFace: FONT, valign: 'middle', margin: 0, isTextBox: true });
    });
  }
  { // 4 보조교사
    const s = mk(4, M1, '개념', 'Claude Code는 말로 시키는 보조교사');
    L.body(s, ['말로 시키면 파일을 만들어 주는 보조교사입니다.', '우리는 코드를 읽지 않고, 요청하고 확인합니다.', '요청이 구체적일수록 결과가 정확합니다.'], 0.6, 1.7, 12.1, 1.9);
    const y = 4.4;
    L.flow(pres, s, [{ t: '교사가\n요청 문장을 쓴다', fill: C.tealT, color: C.teal }, { t: '보조교사\n(Claude Code)가\n파일을 만든다', fill: C.redT, color: C.red }, { t: '교사가\n화면에서 확인한다', fill: C.tealT, color: C.teal }], 0.6, y, 12.1, 1.3, { fontSize: 20, gap: 0.7 });
    s.addText('다시 요청 (수정 요청)', { x: 0.6, y: 5.85, w: 12.1, h: 0.4, fontSize: 16, color: C.mute, fontFace: FONT, align: 'center', margin: 0, isTextBox: true });
    s.addText('"환영 문구가 있는 첫 화면을 만들어 줘"', { x: 3.6, y: 3.85, w: 6.1, h: 0.5, shape: P.wedgeRoundRectCallout, fill: { color: C.gold }, line: { color: C.goldL, width: 1.5 }, color: C.ink, fontSize: 18, fontFace: FONT, align: 'center', valign: 'middle', margin: 4 });
  }
  { // 5 첫 요청
    const s = mk(5, M1, '실습', '첫 요청: "환영합니다" 페이지');
    const cw = 3.85, cg = 0.28, y = 1.7, h = 2.2;
    const cards = [['폴더 만들기', 'mkdir my-classroom\ncd my-classroom'], ['Claude Code 실행·붙여넣기', 'claude\n아래 요청을 붙여넣기'], ['브라우저에서 확인', null]];
    cards.forEach((c, i) => {
      const x = 0.6 + i * (cw + cg);
      L.box(pres, s, '', x, y, cw, h, {});
      L.numCircle(pres, s, i + 1, x + 0.15, y + 0.15);
      s.addText(c[0], { x: x + 0.75, y: y + 0.12, w: cw - 0.9, h: 0.55, fontSize: 18, bold: true, color: C.ink, fontFace: FONT, valign: 'middle', margin: 0, isTextBox: true });
      if (c[1]) s.addText(c[1], { x: x + 0.2, y: y + 0.85, w: cw - 0.4, h: 1.2, fontSize: 16, color: C.ink, fontFace: MONO, valign: 'top', margin: 0, isTextBox: true });
      else L.placeholder(pres, s, '["환영합니다" 화면 캡처 자리]', x + 0.2, y + 0.85, cw - 0.4, 1.2, 14);
    });
    L.code(pres, s, ['이 폴더에 index.html 파일을 하나 만들어 줘.', '화면 가운데에 "환영합니다. 우리 반 온라인 클래스룸"이라는 큰 제목이 보이게 해 줘.', '배경은 크림색(#f8f2e4), 글자는 진한 갈색(#2a2314)으로 하고, 초등학생도 읽기 쉬운 큰 글씨로 해 줘.', '파일은 index.html 하나만 만들고, 다른 설치나 설정은 하지 마.'], 0.6, 4.4, 12.1, 1.75, 15, '복사해서 Claude Code에 붙여넣기');
    L.hint(s, '허락을 물으면 yes. 화면이 비면 "index.html이 비어 있어. 다시 만들어 줘". 안 되면 checkpoint-0', 6.4, 16);
  }
  { // 6 작업 리듬
    const s = mk(6, M1, '정리', '오늘의 작업 리듬');
    L.body(s, ['요청 → 확인 → 막히면 오류 메시지를 그대로 붙여넣기.', '그래도 막히면 checkpoint 폴더에서 이어가기.', '모듈이 끝날 때마다 복구 지점이 있습니다.'], 0.6, 1.7, 12.1, 1.9);
    L.flow(pres, s, [{ t: '요청', fill: C.tealT, color: C.teal }, { t: '확인', fill: C.tealT, color: C.teal }, { t: '막힘 →\n오류 메시지\n그대로 붙여넣기', fill: C.redT, color: C.red }, { t: '그래도 막힘 →\ncheckpoint\n폴더 열기', fill: C.gold, color: C.goldL }], 0.6, 4.0, 8.0, 1.5, { fontSize: 18, gap: 0.4 });
    s.addText('복구 지점', { x: 9.0, y: 3.85, w: 3.3, h: 0.4, fontSize: 18, bold: true, color: C.ink, fontFace: FONT, margin: 0, isTextBox: true });
    ['checkpoint-0', 'checkpoint-m2', 'checkpoint-m3', 'checkpoint-m4', 'checkpoint-m5', 'checkpoint-m6', 'checkpoint-final'].forEach((f, i) => L.folder(pres, s, f, 9.0 + (i % 2) * 1.95, 4.35 + Math.floor(i / 2) * 0.6, 1.8, 0.5, 13));
    s.children;
  }

  // ---------- 모듈 2 ----------
  const M2 = '모듈 2 · Firebase 설정 + 구글 로그인';
  { // 7
    const s = mk(7, M2, '개념', 'Firebase 한 장 정리');
    L.body(s, ['Firebase = 구글이 빌려주는 "학교 운영 도구 세트"'], 0.6, 1.7, 12.1, 0.6);
    const cards = [['A', 'Authentication', '출석부 확인', '누구인지 확인', C.teal], ['F', 'Firestore', '학급 서류함', '데이터 보관', C.teal], ['H', 'Hosting', '학교 게시판', '웹 주소로 공개', C.mute]];
    cards.forEach((c, i) => {
      const x = 0.6 + i * 4.1, w = 3.9;
      L.box(pres, s, '', x, 2.55, w, 3.0, {});
      s.addText(c[0], { x: x + 0.3, y: 2.8, w: 0.9, h: 0.9, shape: P.ellipse, fill: { color: c[4] }, color: 'FFFFFF', bold: true, fontSize: 32, align: 'center', valign: 'middle', fontFace: FONT, margin: 0 });
      s.addText(c[1], { x: x + 1.35, y: 2.85, w: w - 1.5, h: 0.8, fontSize: 24, bold: true, color: C.ink, fontFace: FONT, valign: 'middle', margin: 0, isTextBox: true });
      s.addText(c[2], { x: x + 0.3, y: 3.95, w: w - 0.6, h: 0.6, fontSize: 28, bold: true, color: c[4], fontFace: FONT, margin: 0, isTextBox: true });
      s.addText(c[3], { x: x + 0.3, y: 4.6, w: w - 0.6, h: 0.5, fontSize: 20, color: C.ink, fontFace: FONT, margin: 0, isTextBox: true });
    });
    s.addText('오늘 모듈 2는 앞의 두 개(Authentication, Firestore)를 씁니다. Hosting은 모듈 7', { x: 0.6, y: 5.95, w: 12.1, h: 0.5, fontSize: 20, color: C.red, bold: true, fontFace: FONT, margin: 0, isTextBox: true });
  }
  { // 8
    const s = mk(8, M2, '실습', '프로젝트 만들기');
    L.body(s, ['Firebase 콘솔에서 새 프로젝트 만들기 (이름 예: my-classroom)', '테스트용 구글 계정(교사용)으로 진행. 실제 학생 정보 금지', '순서: 화면에서 찾을 것 → 누를 것 → 확인할 것'], 0.6, 1.7, 12.1, 2.0);
    const cw = 3.7, gap = 0.5;
    [['1 콘솔 접속', 'console.firebase.google.com'], ['2 프로젝트 추가', '이름 칸에 my-classroom'], ['3 프로젝트 홈 도착', '왼쪽 위에 my-classroom']].forEach((c, i) => {
      const x = 0.6 + i * (cw + gap);
      L.placeholder(pres, s, '[콘솔 화면 캡처 자리]', x, 3.95, cw, 1.5, 15);
      s.addText(c[0], { x, y: 5.55, w: cw, h: 0.4, fontSize: 18, bold: true, color: C.ink, fontFace: FONT, margin: 0, isTextBox: true });
      s.addText(c[1], { x, y: 5.95, w: cw, h: 0.4, fontSize: 16, color: C.mute, fontFace: C.MONO || MONO, margin: 0, isTextBox: true });
      if (i < 2) L.arrowR(pres, s, x + cw + 0.1, 4.7, 0.3, C.red);
    });
    L.hint(s, '만들기 버튼이 안 보이면 개인 구글 계정으로 다시 로그인. 이미 쓰인 이름이면 뒤에 숫자 붙이기', 6.5, 16);
  }
  { // 9
    const s = mk(9, M2, '실습', '웹 앱 등록과 firebaseConfig 복사');
    L.body(s, ['프로젝트 안에 "웹 앱" 등록 = 우리 웹 페이지용 출입문 달기', '등록이 끝나면 firebaseConfig(설정값 묶음)가 나온다 → 통째로 복사', '복사한 값은 메모장에 붙여 둔다 (슬라이드 14에서 사용)'], 0.6, 1.7, 12.1, 2.1);
    const labels = ['웹 앱 추가  </>  아이콘', '앱 닉네임 입력 (Hosting 체크는 하지 않기)', 'firebaseConfig 블록 보임', '메모장에 복사'];
    const cw = 2.8, gap = 0.3;
    labels.forEach((l, i) => {
      const x = 0.6 + i * (cw + gap);
      L.placeholder(pres, s, '[콘솔 캡처 자리]', x, 4.0, cw, 1.4, 14);
      L.numCircle(pres, s, i + 1, x, 5.5, 0.45);
      s.addText(l, { x: x + 0.55, y: 5.45, w: cw - 0.55, h: 0.95, fontSize: 16, color: C.ink, fontFace: FONT, valign: 'top', margin: 0, isTextBox: true });
    });
    L.hint(s, '설정값 화면을 닫았다면 프로젝트 설정(톱니바퀴) → 내 앱에서 다시 볼 수 있다', 6.5, 16);
  }
  { // 10
    const s = mk(10, M2, '개념', '웹 설정값은 공개돼도 괜찮다');
    L.body(s, ['firebaseConfig는 "학교 주소" 같은 것. 알려져도 문은 열리지 않는다', '문을 지키는 것은 보안 규칙(교무실 출입 규칙) → 모듈 7에서 완성', '단, AI API 키는 다르다 → 비밀. 모듈 6에서 이유를 본다'], 0.6, 1.7, 12.1, 2.1);
    L.box(pres, s, '', 0.6, 4.05, 5.2, 2.5, { fill: { color: C.tealT }, line: { color: C.teal, width: 3 } });
    s.addText([{ text: '공개해도 됨', options: { bold: true, fontSize: 24, color: C.teal, breakLine: true } }, { text: 'firebaseConfig = 학교 주소', options: { fontSize: 20, color: C.ink } }], { x: 0.8, y: 4.3, w: 4.8, h: 1.9, fontFace: FONT, valign: 'top', margin: 0, isTextBox: true });
    L.box(pres, s, '', 7.5, 4.05, 5.2, 2.5, { fill: { color: C.redT }, line: { color: C.red, width: 3 } });
    s.addText([{ text: '절대 공개 금지', options: { bold: true, fontSize: 24, color: C.red, breakLine: true } }, { text: 'AI API 키 = 교무실 금고 열쇠', options: { fontSize: 20, color: C.ink } }], { x: 7.7, y: 4.3, w: 4.8, h: 1.9, fontFace: FONT, valign: 'top', margin: 0, isTextBox: true });
    s.addText('보안 규칙\n(교무실 출입 규칙)', { x: 5.9, y: 4.5, w: 1.5, h: 1.6, shape: P.hexagon, fill: { color: C.ink }, color: 'FFFFFF', bold: true, fontSize: 14, align: 'center', valign: 'middle', fontFace: FONT, margin: 2 });
  }
  const consoleChain = (s, items, y, o = {}) => L.flow(pres, s, items, 0.6, y, 12.1, o.h || 1.0, { fontSize: o.fs || 16, gap: o.gap || 0.38 });
  { // 11
    const s = mk(11, M2, '실습', '구글 로그인 제공업체 켜기');
    L.body(s, ['Authentication(출석부 확인)에서 Google 로그인 방법을 켠다', '프로젝트 지원 이메일은 내 교사용 계정으로 선택', '순서: 화면에서 찾을 것 → 누를 것 → 확인할 것'], 0.6, 1.7, 12.1, 2.1);
    consoleChain(s, ['보안 > Authentication', '시작하기', '로그인 방법 탭', 'Google 선택', '사용 설정 + 지원 이메일', '저장'], 4.1, { h: 1.1, fs: 16, gap: 0.3 });
    s.addText('예상 결과: Google 줄이 "사용 설정됨"으로 보인다', { x: 0.6, y: 5.5, w: 12.1, h: 0.5, fontSize: 20, bold: true, color: C.teal, fontFace: FONT, margin: 0, isTextBox: true });
    L.hint(s, 'Google이 안 보이면 "새 제공업체 추가"에서 찾기. 지원 이메일 칸이 비면 계정 확인 후 새로고침', 6.4, 16);
  }
  { // 12
    const s = mk(12, M2, '실습', '승인된 도메인에 localhost 추가');
    L.body(s, ['승인된 도메인 = 로그인 창구를 쓸 수 있는 "허가받은 주소 목록"', '새 프로젝트에는 localhost가 기본으로 없다', '"도메인 추가"로 localhost를 직접 넣는다'], 0.6, 1.7, 12.1, 2.1);
    consoleChain(s, ['Authentication', '설정 탭', '승인된 도메인', '도메인 추가', 'localhost 입력 후 추가'], 4.1, { h: 1.0, gap: 0.35 });
    s.addText('추가 후 목록: localhost, (프로젝트 주소).firebaseapp.com …', { x: 0.6, y: 5.35, w: 12.1, h: 0.5, shape: P.roundRect, rectRadius: 0.1, fill: { color: C.card }, line: { color: C.red, width: 2 }, fontSize: 18, color: C.ink, fontFace: MONO, align: 'center', valign: 'middle', margin: 6 });
    L.hint(s, '나중에 auth/unauthorized-domain 오류가 나면 이 슬라이드로 돌아와 주소 목록을 본다', 6.3, 16);
  }
  { // 13
    const s = mk(13, M2, '실습', 'Firestore 만들기와 임시 규칙');
    L.body(s, ['Firestore(학급 서류함) 설치. 위치(리전)는 만든 뒤 못 바꾼다', '모드는 테스트 모드가 아닌 잠금(프로덕션) 모드', '임시 규칙 = 강사가 준 firestore.temp.rules 통째로 복사'], 0.6, 1.7, 12.1, 2.1);
    consoleChain(s, ['데이터베이스 및 스토리지 > Firestore', '데이터베이스 만들기', '위치 선택', '잠금(프로덕션) 모드 → 만들기'], 3.95, { h: 1.1, gap: 0.35 });
    L.flow(pres, s, [{ t: '규칙 탭 열기', fill: C.card }, { t: '강사 파일 firestore.temp.rules 내용 붙여넣기', fill: C.gold, color: C.goldL }, { t: '게시(Publish)', fill: C.tealT, color: C.teal }], 0.6, 5.3, 12.1, 0.95, { fontSize: 16, gap: 0.4 });
    s.addText('테스트 모드는 선택하지 않는다 · 규칙 전문은 발표자 노트(부록 A)와 배포 파일', { x: 0.6, y: 6.4, w: 12.1, h: 0.5, fontSize: 18, bold: true, color: C.red, fontFace: FONT, margin: 0, isTextBox: true });
  }
  { // 14
    const s = mk(14, M2, '실습', '설정값을 프로젝트에 저장');
    L.body(s, ['메모장의 firebaseConfig를 Claude Code에게 전달해 저장', '한 파일(firebase-config.js)에 모아 두고 재사용', '코드는 읽지 않고 붙여넣기 → 확인만'], 0.6, 1.7, 12.1, 2.0);
    L.flow(pres, s, ['메모장의 firebaseConfig', 'Claude Code에 붙여넣기', '폴더에 firebase-config.js 생성'], 0.6, 3.8, 12.1, 0.85, { fontSize: 18, gap: 0.6 });
    L.code(pres, s, ['firebase-config.js 파일을 만들어 줘.', '- 아래 firebaseConfig를 export const firebaseConfig = { ... } 형태로 저장', '- 값은 글자 하나도 바꾸지 말고 그대로. 다른 파일은 만들거나 바꾸지 마', '- 코드를 설명하지 말고, 파일 이름과 위치만 알려 줘', '(여기에 슬라이드 9에서 복사한 firebaseConfig 블록 붙여넣기)'], 0.6, 5.0, 12.1, 1.55, 15, '프롬프트 핵심 (전문은 발표자 노트)');
    L.hint(s, '다른 파일까지 바뀌었다면 "방금 바꾼 다른 파일은 원래대로 되돌려 줘"', 6.6, 16);
  }
  { // 15
    const s = mk(15, M2, '실습', '프롬프트 1: 로그인/로그아웃 버튼');
    L.body(s, ['firebase-config.js를 app.js가 불러와 Firebase를 시작한다', '구글 로그인 버튼, 로그아웃 버튼, 이름 표시'], 0.6, 1.65, 12.1, 1.3);
    L.box(pres, s, '[ 구글로 로그인 ]', 0.6, 2.85, 2.6, 0.8, { fontSize: 18, bold: true, fill: { color: C.card }, line: { color: C.ink, width: 2 } });
    L.arrowR(pres, s, 3.35, 3.25, 0.3, C.red);
    L.box(pres, s, 'OOO 선생님 환영합니다\n[ 로그아웃 ]', 3.8, 2.8, 3.2, 0.9, { fontSize: 16, fill: { color: C.card }, line: { color: C.ink, width: 2 } });
    L.code(pres, s, ['index.html을 Firebase 구글 로그인 페이지로 바꿔 줘.', '- 파일 4개: index.html, style.css, app.js, firebase-config.js(그대로 사용)', '- SDK는 CDN 모듈 방식: gstatic.com/firebasejs/12.19.0/ 아래 app·auth·firestore', '- "구글로 로그인" → 구글 팝업 로그인, 로그인하면 이름+로그아웃 표시', '- 새로고침해도 로그인 유지, 글씨는 크게, 배경은 크림색(#f8f2e4)', '- 끝나면 localhost로 여는 명령 한 줄과 접속 주소만 알려 줘'], 0.6, 4.2, 12.1, 2.15, 15, '프롬프트 핵심 (전문은 발표자 노트)');
    s.addText('file:// 로 열지 말고 localhost 주소로 열기', { x: 7.4, y: 2.85, w: 5.3, h: 0.7, fontSize: 18, bold: true, color: C.red, fontFace: FONT, margin: 0, valign: 'middle', isTextBox: true });
    L.hint(s, '팝업이 안 뜨면 주소창 오른쪽 "팝업 차단됨"을 눌러 허용. 빨간 오류는 그대로 붙여넣기', 6.5, 16);
  }
  { // 16
    const s = mk(16, M2, '실습', '프롬프트 2: users 문서와 역할 선택');
    L.body(s, ['처음 로그인하면 users/{uid} 문서를 만든다', '역할(교사/학생)은 처음 한 번만 고른다 → 화면을 나누는 용도'], 0.6, 1.65, 12.1, 1.3);
    L.box(pres, s, '', 0.6, 3.0, 3.1, 1.55, { align: 'left', fill: { color: C.card }, line: { color: C.teal, width: 2 } });
    s.addText([{ text: 'users/{uid}', options: { bold: true, breakLine: true, color: C.teal } }, { text: 'name', options: { breakLine: true } }, { text: 'email', options: { breakLine: true } }, { text: 'role', options: {} }], { x: 0.8, y: 3.07, w: 2.8, h: 1.4, fontSize: 16, fontFace: MONO, color: C.ink, margin: 0, valign: 'middle', isTextBox: true });
    L.flow(pres, s, ['처음 로그인', '역할 선택\n교사 / 학생', 'users 문서 저장', '환영 화면'], 4.0, 3.15, 8.7, 1.1, { fontSize: 16, gap: 0.35 });
    s.addText('두 번째 로그인부터는 역할 선택 건너뛰기 (점선)', { x: 4.0, y: 4.3, w: 8.7, h: 0.35, fontSize: 14, color: C.mute, fontFace: FONT, margin: 0, isTextBox: true });
    L.code(pres, s, ['로그인에 성공하면 users/{uid} 문서를 확인해 줘.', '- 없으면 "교사"/"학생" 역할 선택 화면을 보여 줘', '- 저장 필드는 name, email, role("teacher"/"student") 3개만', '- 있으면 선택을 건너뛰고 "OOO 선생님 환영합니다"로 보여 줘', '- 역할은 처음 한 번만 고르고 화면에서 바꿀 수 없게 해 줘'], 0.6, 5.0, 12.1, 1.6, 15, '프롬프트 핵심 (전문은 발표자 노트)');
    L.hint(s, 'permission-denied면 슬라이드 13의 임시 규칙이 게시됐는지 확인', 6.65, 16);
  }
  { // 17
    const s = mk(17, M2, '실습', '확인: Firestore에서 내 문서 보기');
    L.body(s, ['콘솔 Firestore 데이터 탭에서 users → 내 uid 문서 확인', '시크릿 창에서 테스트 학생 계정으로 로그인', '문서가 2개(교사 1, 학생 1) 보이면 성공'], 0.6, 1.7, 7.6, 2.4, 22);
    ['users 컬렉션이 보인다', '교사 문서: name, email, role=teacher', '학생 문서: name, email, role=student'].forEach((c, i) => {
      const y = 4.4 + i * 0.7;
      s.addShape(P.rect, { x: 0.6, y: y + 0.08, w: 0.32, h: 0.32, fill: { color: C.card }, line: { color: C.red, width: 2 } });
      s.addText(c, { x: 1.05, y, w: 7.1, h: 0.5, fontSize: 18, color: C.ink, fontFace: FONT, valign: 'middle', margin: 0, isTextBox: true });
    });
    L.placeholder(pres, s, '[Firestore 문서 화면\n캡처 자리]', 8.6, 1.8, 4.1, 3.6, 16);
    s.addText('콘솔: 데이터베이스 및 스토리지 > Firestore > 데이터 탭', { x: 8.6, y: 5.5, w: 4.1, h: 0.8, fontSize: 16, color: C.mute, fontFace: FONT, margin: 0, isTextBox: true });
    L.hint(s, '시크릿 창 로그인이 안 되면 주소창 오른쪽에서 팝업 허용 확인', 6.5, 16);
  }
  { // 18
    const s = mk(18, M2, '정리', '막힘 모음과 복구 지점');
    L.body(s, ['이 세 가지가 가장 흔하다. 오류는 메시지 그대로 Claude Code에 붙여넣기'], 0.6, 1.65, 12.1, 0.8, 22);
    L.table(pres, s, [['증상', '원인', '해결'],
      ['auth/unauthorized-domain', '승인된 도메인에 현재 주소가 없음', 'Authentication 설정의 승인된 도메인에 localhost 추가 (슬라이드 12)'],
      ['팝업이 안 뜸 / popup-blocked', '브라우저가 팝업 차단', '주소창 오른쪽 차단 표시에서 허용 후 다시'],
      ['버튼 반응 없음, file:// 로 열었음', '파일로 직접 열면 로그인이 안 됨', 'Claude Code가 알려 준 localhost 주소로 접속']], 0.6, 2.55, [3.4, 3.7, 5.0], { fontSize: 16, rowH: 0.62 });
    L.code(pres, s, ['아래 오류가 났어. 원인을 쉬운 말로 한 줄로 알려 주고, 고쳐 줘.', '(여기에 오류 메시지를 그대로 붙여넣기)'], 0.6, 5.6, 8.0, 0.95, 15, '공통 문장');
    s.addText('그래도 안 되면', { x: 9.0, y: 5.25, w: 3.7, h: 0.35, fontSize: 16, color: C.mute, fontFace: FONT, margin: 0, isTextBox: true });
    L.folder(pres, s, 'checkpoint-m2', 9.0, 5.65, 3.7, 0.6);
    s.addText('복사한 폴더의 firebase-config.js만 내 설정값으로 바꾼다', { x: 0.6, y: 6.6, w: 12.1, h: 0.35, fontSize: 16, color: C.ink, fontFace: FONT, margin: 0, isTextBox: true });
  }

  // ---------- 모듈 3 ----------
  const M3 = '모듈 3 · 수업코드 수강신청';
  { // 19
    const s = mk(19, M3, '개념', '수업코드 = 교실 열쇠');
    L.body(s, ['수업을 만들면 6자리 수업코드가 생긴다', '그 코드가 수업 문서의 이름이다', '학생은 코드(교실 열쇠)로 들어온다'], 0.6, 1.7, 5.4, 2.4, 22);
    L.box(pres, s, '', 6.4, 1.75, 6.3, 3.5, { fill: { color: C.card }, line: { color: C.teal, width: 3 } });
    s.addText([{ text: 'classes/{수업코드}', options: { bold: true, color: C.teal, breakLine: true } }, { text: '폴더 이름표 "K7M4QX"', options: { color: C.red, bold: true, breakLine: true } }, { text: 'title · teacherUid · joinCode', options: {} }], { x: 6.6, y: 1.85, w: 5.9, h: 1.2, fontSize: 18, fontFace: MONO, color: C.ink, margin: 0, valign: 'top', isTextBox: true });
    L.box(pres, s, '', 6.8, 3.3, 5.5, 1.7, { fill: { color: C.tealT }, line: { color: C.teal, width: 2 }, align: 'left' });
    s.addText([{ text: 'members/{uid}', options: { bold: true, color: C.teal, breakLine: true } }, { text: 'joinedAt · uid', options: {} }], { x: 7.0, y: 3.45, w: 5.1, h: 1.3, fontSize: 18, fontFace: MONO, color: C.ink, margin: 0, valign: 'middle', isTextBox: true });
    s.addText('열쇠: 수업코드 K7M4QX = 폴더 이름', { x: 0.6, y: 4.5, w: 5.4, h: 0.5, shape: P.roundRect, rectRadius: 0.1, fill: { color: C.gold }, line: { color: C.goldL, width: 1.5 }, fontSize: 18, bold: true, fontFace: FONT, color: C.ink, align: 'center', valign: 'middle', margin: 4 });
    L.flow(pres, s, [{ t: '교사 → classes/{코드} 생성', fill: C.tealT, color: C.teal }, { t: '학생 → 코드 입력 → 한 장 꺼내기 → members 추가', fill: C.redT, color: C.red }], 0.6, 5.55, 12.1, 1.0, { fontSize: 18, gap: 0.6 });
  }
  { // 20
    const s = mk(20, M3, '개념', '보안 원칙 3·4 미리보기');
    L.body(s, ['원칙 3: 수업은 교사만 만든다', '원칙 4: 수업코드를 알아야 들어간다. 전체 수업 목록은 볼 수 없다'], 0.6, 1.7, 12.1, 1.4);
    L.table(pres, s, [['원칙', '허용 O', '막힘 X'], ['수업 만들기', '교사', '학생'], ['수업 찾기', '코드 한 개로 한 교실 찾기', '모든 교실 목록 훑어보기']], 0.6, 3.5, [2.8, 4.6, 4.7], { fontSize: 20, rowH: 0.75 });
    s.addText('보안 규칙 = 교무실 출입 규칙 · 전체를 내려받아 비교하지 않는다', { x: 0.6, y: 6.2, w: 12.1, h: 0.5, fontSize: 18, color: C.mute, fontFace: FONT, margin: 0, isTextBox: true });
  }
  { // 21
    const s = mk(21, M3, '실습', '실습 1: 교사가 수업 만들기');
    L.body(s, ['교사 화면에 "수업 만들기"를 추가한다', '제목을 넣으면 6자리 수업코드가 자동 발급된다'], 0.6, 1.65, 7.0, 1.3, 22);
    L.box(pres, s, '제목 입력칸   [ 수업 만들기 ]\n\n수업코드: K7M4QX', 7.9, 1.7, 4.8, 1.55, { fontSize: 18, fill: { color: C.card }, line: { color: C.ink, width: 2 }, fontFace: FONT });
    L.code(pres, s, ['교사 화면에 "수업 만들기" 기능을 추가해 줘.', '- 교사(role이 teacher)에게만 보이게', '- 수업코드: 영문 대문자+숫자 6자리 무작위 (0, O, 1, I는 쓰지 마)', '- classes/{수업코드}: 문서 이름을 수업코드와 똑같이', '- 필드는 title, teacherUid, joinCode 세 개만', '- 저장 전에 같은 코드가 있는지 한 건만 읽어 확인', '- 만든 뒤 제목과 수업코드를 크게 보여 줘'], 0.6, 3.6, 12.1, 2.4, 15, '프롬프트 핵심 (전문은 발표자 노트)');
    L.hint(s, '권한 오류면 규칙 탭에 임시 규칙 게시 확인. 그래도 같으면 "규칙 파일은 바꾸지 말고 앱 코드에서 원인을 찾아 줘"', 6.35, 16);
  }
  { // 22
    const s = mk(22, M3, '실습', '실습 2: 학생이 코드로 가입');
    L.body(s, ['학생 화면에 수업코드 입력칸을 만든다', '맞는 코드면 그 수업의 members에 내 문서가 생긴다'], 0.6, 1.65, 12.1, 1.3, 22);
    L.flow(pres, s, ['코드 입력\n[ 가입하기 ]', 'classes/{코드}\n1건 읽기', 'classes/{코드}/members/{내 uid}\n생성 (joinedAt, uid)'], 0.6, 3.0, 12.1, 1.0, { fontSize: 16, gap: 0.5 });
    L.code(pres, s, ['학생 화면에 "수업코드로 가입하기"를 추가해 줘.', '- 코드는 앞뒤 공백 제거 후 대문자로', '- classes/{코드} 문서 한 건만 읽기 (전체 다운로드·where 검색 금지)', '- 있으면 members/{내 uid} 생성: joinedAt, uid 두 개만', '- 이미 가입 → "이미 가입한 수업이에요"', '- 없는 코드 → "수업코드를 다시 확인해 주세요"'], 0.6, 4.4, 12.1, 1.95, 15, '프롬프트 핵심 (전문은 발표자 노트)');
    L.hint(s, '맞는 코드인데 "없는 코드"면 소문자·공백이 섞였는지 확인', 6.5, 16);
  }
  { // 23
    const s = mk(23, M3, '실습', '실습 3: 내 수업 목록');
    L.body(s, ['교사는 내가 만든 수업, 학생은 내가 가입한 수업이 목록으로', '학생 목록에는 수업 제목만 보인다'], 0.6, 1.65, 12.1, 1.3, 22);
    L.box(pres, s, '교사: 내가 만든 수업\n제목 + 수업코드', 0.6, 3.0, 5.9, 1.0, { fontSize: 18, fill: { color: C.tealT }, line: { color: C.teal, width: 2 } });
    L.box(pres, s, '학생: 내가 가입한 수업\n제목만 (수업코드는 숨김)', 6.8, 3.0, 5.9, 1.0, { fontSize: 18, fill: { color: C.redT }, line: { color: C.red, width: 2 } });
    L.code(pres, s, ['첫 화면에 "내 수업" 목록을 보여 줘.', '- 교사: teacherUid가 내 uid인 수업 (제목+수업코드)', '- 학생: members 컬렉션 그룹 조회로 uid가 내 uid인 가입 문서 → 부모 수업 제목만', '- 비었으면 "아직 수업이 없어요"', '- 제목을 누르면 #/class/{classId} 수업 화면으로'], 0.6, 4.4, 12.1, 1.55, 15, '프롬프트 핵심 (전문은 발표자 노트)');
    s.addText('거의 모두에게 "색인(index) 필요" 오류가 한 번 나온다 → 오류의 링크를 눌러 색인을 만들고 1~5분 기다린 뒤 새로고침', { x: 0.6, y: 6.15, w: 12.1, h: 0.75, shape: P.roundRect, rectRadius: 0.1, fill: { color: C.gold }, line: { color: C.red, width: 2 }, fontSize: 18, bold: true, color: C.red, fontFace: FONT, align: 'left', valign: 'middle', margin: 10 });
  }
  { // 24
    const s = mk(24, M3, '실습', '짝 활동: 옆 사람 코드로 가입');
    L.body(s, ['옆 사람의 수업코드로 가입해 보자', '일부러 틀린 코드도 넣어 보자. 어떻게 되는가?'], 0.6, 1.65, 12.1, 1.3, 24);
    L.box(pres, s, '교사 역할\n코드 알려 주기', 0.6, 3.2, 2.8, 1.2, { fontSize: 18, fill: { color: C.tealT }, line: { color: C.teal, width: 2 } });
    s.addText('⇄', { x: 3.5, y: 3.35, w: 0.8, h: 0.9, fontSize: 36, bold: true, color: C.mute, align: 'center', valign: 'middle', fontFace: FONT, margin: 0 });
    L.box(pres, s, '학생 역할\n코드 입력', 4.4, 3.2, 2.8, 1.2, { fontSize: 18, fill: { color: C.redT }, line: { color: C.red, width: 2 } });
    ['(1) 맞는 코드를 넣으면?', '(2) 틀린 코드를 넣으면?', '(3) 같은 코드를 두 번 넣으면?'].forEach((q, i) => {
      L.box(pres, s, q, 7.7, 3.0 + i * 0.85, 5.0, 0.72, { fontSize: 20, align: 'left', fill: { color: C.card }, line: { color: C.red, width: 2 }, margin: 10 });
    });
    L.hint(s, '틀린 코드에서 흰 화면이면 "틀린 코드를 넣으면 친절한 안내가 나오게 해 줘"', 6.3, 18);
  }
  { // 25
    const s = mk(25, M3, '정리', '막힘 모음과 복구 지점');
    L.body(s, ['색인 필요 오류는 안내 링크로 해결', '권한 오류는 오류 메시지를 통째로 붙여넣기'], 0.6, 1.65, 12.1, 1.3, 24);
    [['"The query requires an index"', '링크 클릭 → 몇 분 기다리기'], ['"Missing or insufficient permissions"', '오류 전체 붙여넣기'], ['아무것도 안 보임', '로그인한 계정의 role 확인']].forEach((c, i) => {
      const x = 0.6 + i * 4.1;
      L.box(pres, s, '', x, 3.3, 3.9, 2.0, { fill: { color: C.card }, line: { color: C.teal, width: 2 } });
      s.addText(c[0], { x: x + 0.2, y: 3.4, w: 3.5, h: 0.95, fontSize: 18, bold: true, color: C.red, fontFace: FONT, valign: 'middle', margin: 0, isTextBox: true });
      s.addText('→ ' + c[1], { x: x + 0.2, y: 4.4, w: 3.5, h: 0.8, fontSize: 18, color: C.ink, fontFace: FONT, valign: 'middle', margin: 0, isTextBox: true });
    });
    s.addText('그래도 막히면', { x: 0.6, y: 5.75, w: 3.0, h: 0.5, fontSize: 20, color: C.ink, fontFace: FONT, valign: 'middle', margin: 0, isTextBox: true });
    L.folder(pres, s, 'checkpoint-m3', 3.5, 5.75, 3.2, 0.6);
  }
  { // 26 휴식
    const s = mk(26, M3, '정리', '휴식 10분');
    s.addText('10:00', { x: 0.6, y: 1.7, w: 6.4, h: 2.4, fontSize: 120, bold: true, color: C.red, fontFace: FONT, align: 'center', valign: 'middle', margin: 0, isTextBox: true });
    s.addText('10분 타이머 · 휴식 시간', { x: 0.6, y: 4.1, w: 6.4, h: 0.6, fontSize: 24, bold: true, color: C.teal, fontFace: FONT, align: 'center', margin: 0, isTextBox: true });
    // 커피잔
    s.addShape(P.roundRect, { x: 8.2, y: 2.3, w: 2.3, h: 2.0, rectRadius: 0.2, fill: { color: C.card }, line: { color: C.ink, width: 3 } });
    s.addShape(P.donut, { x: 10.2, y: 2.75, w: 1.0, h: 1.0, fill: { color: C.card }, line: { color: C.ink, width: 3 } });
    s.addText('휴식', { x: 8.2, y: 2.3, w: 2.3, h: 2.0, fontSize: 28, bold: true, color: C.red, align: 'center', valign: 'middle', fontFace: FONT, margin: 0 });
    L.body(s, ['막힌 분은 강사석으로', 'checkpoint-m3에서 이어 시작할 수 있어요'], 0.6, 5.0, 8.5, 1.3, 24);
    L.folder(pres, s, 'checkpoint-m3', 9.8, 5.5, 2.9, 0.65);
  }
};
