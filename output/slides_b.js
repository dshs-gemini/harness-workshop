// 슬라이드 27~54 (모듈 4~7)
const L = require('./lib');
const { C, FONT, MONO } = L;

module.exports = function (pres, N) {
  const mk = (n, mod, type, title) => L.frame(pres, { mod, type, title }, N[n].notes);
  const P = pres.ShapeType;
  const checks = (s, items, x, y, w, size = 18, gap = 0.62) => items.forEach((c, i) => {
    s.addShape(P.rect, { x, y: y + i * gap + 0.08, w: 0.32, h: 0.32, fill: { color: C.card }, line: { color: C.red, width: 2 } });
    s.addText(c, { x: x + 0.45, y: y + i * gap, w: w - 0.45, h: 0.5, fontSize: size, color: C.ink, fontFace: FONT, valign: 'middle', margin: 0, isTextBox: true });
  });
  const cp = (s, name, x, y, w) => { s.addText('그래도 막히면', { x, y, w: 2.0, h: 0.5, fontSize: 18, color: C.ink, fontFace: FONT, valign: 'middle', margin: 0, isTextBox: true }); L.folder(pres, s, name, x + 2.0, y, w || 3.2, 0.55); };
  const CODE = '프롬프트 핵심 (전문은 발표자 노트)';

  // ---------- 모듈 4 ----------
  const M4 = '모듈 4 · HTML 수업자료 등록';
  { // 27
    const s = mk(27, M4, '개념', '내 HTML 자료, 클래스룸에 올리자');
    L.body(s, ['만들어 둔 HTML 수업자료를 클래스룸에 한 번만 올린다', '우리 수업 학생들이 자기 화면에서 바로 연다', '올린 자료는 Firestore(학급 서류함)에 저장된다'], 0.6, 1.7, 12.1, 2.1);
    L.flow(pres, s, ['교사 PC의\nHTML 파일', '자료 등록 폼\n(제목 + HTML 붙여넣기)', 'Firestore\nclasses/{classId}/\nmaterials/{id}', '학생 수업 화면의\n자료 목록'], 0.6, 4.1, 12.1, 1.5, { fontSize: 18, gap: 0.45 });
    s.addText('저장 필드: title · html · createdAt', { x: 5.0, y: 5.75, w: 4.5, h: 0.4, fontSize: 16, color: C.mute, fontFace: MONO, margin: 0, align: 'center', isTextBox: true });
  }
  { // 28
    const s = mk(28, M4, '개념', '자료는 유리 진열장에 넣어서 보여 준다');
    L.body(s, ['원칙 1: 가입한 수업 자료만 읽는다', '원칙 5: 교사 HTML은 유리 진열장(sandbox iframe)에 넣어 보여 준다. 보이지만 손댈 수 없다'], 0.6, 1.7, 12.1, 1.8);
    L.box(pres, s, '', 0.6, 3.75, 5.9, 3.0, { fill: { color: C.card }, line: { color: C.teal, width: 2 } });
    s.addText('원칙 1', { x: 0.8, y: 3.85, w: 3, h: 0.4, fontSize: 18, bold: true, color: C.teal, fontFace: FONT, margin: 0, isTextBox: true });
    L.box(pres, s, '교실 A (가입함)\n문 열림', 0.9, 4.4, 2.5, 1.3, { fontSize: 18, fill: { color: C.tealT }, line: { color: C.teal, width: 2 } });
    L.box(pres, s, '교실 B (미가입)\n문 잠김', 3.7, 4.4, 2.5, 1.3, { fontSize: 18, fill: { color: C.redT }, line: { color: C.red, width: 2 } });
    s.addText('열쇠(수업코드)로 가입한 학생만 들어간다', { x: 0.9, y: 5.85, w: 5.3, h: 0.7, fontSize: 16, color: C.ink, fontFace: FONT, margin: 0, isTextBox: true });
    L.box(pres, s, '', 6.8, 3.75, 5.9, 3.0, { fill: { color: C.card }, line: { color: C.red, width: 2 } });
    s.addText('원칙 5', { x: 7.0, y: 3.85, w: 3, h: 0.4, fontSize: 18, bold: true, color: C.red, fontFace: FONT, margin: 0, isTextBox: true });
    L.box(pres, s, '유리 진열장\n(sandbox iframe)\nHTML 자료', 7.1, 4.35, 2.9, 1.7, { fontSize: 18, fill: { color: C.gold }, line: { color: C.goldL, width: 4 } });
    L.box(pres, s, '진열장 밖\n로그인 정보', 10.2, 4.35, 2.2, 1.7, { fontSize: 18, fill: { color: C.tealT }, line: { color: C.teal, width: 2 } });
    s.addText('✕', { x: 9.75, y: 4.55, w: 0.7, h: 0.7, fontSize: 36, bold: true, color: C.red, align: 'center', valign: 'middle', fontFace: FONT, margin: 0 });
    s.addText('진열장 안에서 밖으로 손댈 수 없다', { x: 7.1, y: 6.15, w: 5.4, h: 0.5, fontSize: 16, color: C.ink, fontFace: FONT, margin: 0, isTextBox: true });
  }
  { // 29
    const s = mk(29, M4, '실습', '실습 1: 교사 자료 등록 폼');
    L.body(s, ['수업 화면에 자료 등록 폼을 추가한다', '제목을 쓰고 HTML을 붙여넣어 저장한다'], 0.6, 1.65, 7.0, 1.3);
    L.box(pres, s, '[ 제목 ]\n[ HTML 붙여넣기 ]\n[ 저장 ]  저장했습니다', 8.0, 1.65, 4.7, 1.6, { fontSize: 16, fill: { color: C.card }, line: { color: C.ink, width: 2 } });
    L.code(pres, s, ['교사용 수업 화면에 "수업자료 등록" 폼을 추가해 줘.', '- 입력칸: 제목(title), HTML 붙여넣기(html)', '- 저장 → classes/{classId}/materials 에 title, html, createdAt(서버 시간)', '- 그 수업 교사(teacherUid가 내 uid)에게만 보이게', '- 제목이 비면 저장 금지, html이 90만 바이트를 넘으면 거부', '- 기존 로그인, 수업 만들기 기능은 건드리지 마'], 0.6, 3.65, 12.1, 2.2, 15, CODE);
    L.hint(s, '폼이 안 보이면 내가 만든 수업에 교사 계정으로 들어갔는지 확인. 권한 오류면 임시 규칙 게시 확인', 6.3, 16);
  }
  { // 30
    const s = mk(30, M4, '실습', '실습 2: 학생 목록과 유리 진열장');
    L.body(s, ['학생 화면에 자료 목록을 만든다', '제목을 누르면 유리 진열장(sandbox iframe) 안에 자료를 보여 준다'], 0.6, 1.65, 7.4, 1.8);
    L.box(pres, s, '자료 1\n자료 2\n자료 3', 8.3, 1.65, 1.8, 1.6, { fontSize: 16, fill: { color: C.card }, line: { color: C.ink, width: 2 } });
    L.box(pres, s, '선택한 자료 표시\n(sandbox)', 10.3, 1.65, 2.4, 1.6, { fontSize: 16, fill: { color: C.gold }, line: { color: C.goldL, width: 4 } });
    L.code(pres, s, ['학생용 수업 화면에 "수업자료" 목록을 추가해 줘.', '- materials를 최신순으로 제목만 보여 주고', '- 제목을 누르면 html을 iframe의 srcdoc으로 보여 줘', '- iframe에 sandbox 속성을 값 없이 붙여 줘 (allow-same-origin, allow-scripts는 절대 넣지 마)', '- 자료가 없으면 "아직 등록된 자료가 없습니다"', '- html을 innerHTML로 다른 곳에 넣지 마'], 0.6, 3.85, 12.1, 2.1, 15, CODE);
    L.hint(s, '자료 속 버튼이 안 눌리는 것은 오류가 아니다. 유리 진열장의 정상 동작이다', 6.35, 18);
  }
  { // 31
    const s = mk(31, M4, '실습', '실습 3: 학생 계정으로 확인');
    L.body(s, ['테스트 학생 계정(시크릿 창)으로 가입한 수업의 자료를 열어 본다', '실제 차단 검증은 모듈 7에서 한다'], 0.6, 1.65, 12.1, 1.4);
    checks(s, ['교사 계정: 자료 등록 완료', '학생 계정(가입함): 목록·열람 OK', '학생 계정(미가입): 모듈 7에서 차단 확인 (예고)'], 0.6, 3.0, 7.0, 18, 0.55);
    L.code(pres, s, ['방금 만든 수업자료 기능을 점검해 줘.', '1. 목록과 iframe 열람이 정상인지 코드로 점검', '2. sandbox에 allow-same-origin/allow-scripts가 없는지 확인', '3. 자료 html을 innerHTML로 넣는 곳이 없는지 찾기', '4. 문제가 있으면 고치고 3줄 이내로 요약'], 0.6, 5.2, 12.1, 1.65, 15, CODE);
  }
  { // 32
    const s = mk(32, M4, '정리', '정리: 막힘 모음과 복구 지점');
    L.body(s, ['오늘 만든 것: 자료 등록 폼 + 자료 목록·열람(유리 진열장)', '다음은 웹 학습지'], 0.6, 1.65, 12.1, 1.3);
    L.flow(pres, s, ['등록\nmaterials', '목록', '유리 진열장 열람'], 0.6, 3.15, 12.1, 1.0, { fontSize: 20, gap: 0.6 });
    L.box(pres, s, '저장이 안 되고 오류: 문서 1개는 1MiB(1,048,576바이트)까지. 큰 이미지가 원인. 우리 폼은 90만 바이트(한글 위주 약 30만 글자)를 넘으면 먼저 알려 준다', 0.6, 4.4, 5.9, 1.75, { fontSize: 16, align: 'left', margin: 10 });
    L.box(pres, s, '이미지가 깨져 보임: 이미지가 내 컴퓨터 안의 경로로만 걸려 있다. 웹 주소로 바꾸거나 자료 안에 포함한다', 6.8, 4.4, 5.9, 1.75, { fontSize: 16, align: 'left', margin: 10 });
    cp(s, 'checkpoint-m4', 0.6, 6.3);
  }

  // ---------- 모듈 5 ----------
  const M5 = '모듈 5 · 웹 학습지';
  { // 33
    const s = mk(33, M5, '개념', '학습지 = 문항지 1장 + 학생별 답안지');
    L.body(s, ['문항지는 교사가 1장 만든다', '답안지는 학생마다 1장씩 쌓인다', 'Firestore(학급 서류함)에 두 종류를 나눠 보관한다'], 0.6, 1.7, 12.1, 2.0);
    L.box(pres, s, '문항지  classes/{classId}/worksheets/{id}\ntitle, questions[]', 0.6, 3.85, 12.1, 1.0, { fontSize: 18, fill: { color: C.tealT }, line: { color: C.teal, width: 3 } });
    ['uid-A 답안지', 'uid-B 답안지', 'uid-C 답안지'].forEach((t, i) => {
      L.arrowD(pres, s, 2.2 + i * 3.1, 4.9, 0.4, C.mute);
      L.box(pres, s, 'submissions/' + t + '\nanswers, submittedAt', 0.7 + i * 3.1, 5.35, 2.9, 1.1, { fontSize: 15, fill: { color: C.redT }, line: { color: C.red, width: 2 } });
    });
    L.box(pres, s, 'feedback\n(모듈 6에서 채움)', 10.0, 5.35, 2.7, 1.1, { fontSize: 15, fill: { color: C.bg }, line: { color: C.mute, width: 2, dashType: 'dash' }, color: C.mute });
  }
  { // 34
    const s = mk(34, M5, '개념', '답안지 이름이 학생 번호인 이유');
    L.body(s, ['답안지 문서 이름 = 그 학생의 uid(출석 번호표)', '내 번호표와 같은 이름의 답안지만 열 수 있다', '보안 규칙 원칙 2: 학생은 자기 제출물만 읽고 쓴다'], 0.6, 1.7, 12.1, 2.1);
    [['uid-A', '열림', C.tealT, C.teal], ['uid-B', '잠김', C.redT, C.red], ['uid-C', '잠김', C.redT, C.red]].forEach((d, i) => {
      L.box(pres, s, d[0] + '\n' + d[1], 0.6 + i * 2.6, 4.2, 2.35, 1.6, { fontSize: 20, bold: true, fill: { color: d[2] }, line: { color: d[3], width: 3 } });
    });
    s.addText('학생 A의 서랍장', { x: 0.6, y: 3.8, w: 4, h: 0.4, fontSize: 16, color: C.mute, fontFace: FONT, margin: 0, isTextBox: true });
    L.box(pres, s, '교사: 해당 수업 서랍 전체 열람 가능', 8.6, 4.2, 4.1, 1.6, { fontSize: 18, bold: true, fill: { color: C.gold }, line: { color: C.goldL, width: 2 } });
  }
  { // 35
    const s = mk(35, M5, '실습', '교사 학습지 작성 화면 만들기');
    L.body(s, ['교사 화면에서 문항을 추가해 학습지를 저장한다', '서술형과 선택형(정답 포함) 두 종류. 정답은 모듈 6에서 쓴다'], 0.6, 1.65, 12.1, 1.5);
    L.code(pres, s, ['교사 수업 화면에 "학습지 만들기"를 추가해 줘 (학생에게는 안 보이게).', '- "서술형 문항 추가" / "선택형 문항 추가" 버튼. 선택형은 보기 2~5개 + 정답 하나', '- classes/{classId}/worksheets 에 title, questions[] 두 필드만 저장', '- 문항 필드: type("essay"/"choice"), text, choices, answer', '  answer: 선택형은 0부터 센 번호, 서술형은 null', '- 제목·문항·보기·정답이 빠지면 저장하지 말고 무엇이 빠졌는지 알려 줘'], 0.6, 3.5, 12.1, 2.2, 15, CODE);
    s.addText('화면에는 보기 1, 2, 3 · 저장은 0, 1, 2  (첫 번째 보기가 정답이면 answer = 0)', { x: 0.6, y: 5.85, w: 12.1, h: 0.5, fontSize: 18, bold: true, color: C.red, fontFace: FONT, margin: 0, isTextBox: true });
    L.hint(s, '권한 오류는 임시 규칙 게시 확인. 폼이 안 보이면 내가 만든 수업인지 확인', 6.45, 16);
  }
  { // 36
    const s = mk(36, M5, '실습', '학생 학습지 풀기와 제출');
    L.body(s, ['학생 화면에서 학습지를 열어 답하고 제출한다', '답안지 문서 이름은 내 uid. 다시 제출하면 병합 저장으로 답만 바꾼다'], 0.6, 1.65, 12.1, 1.5);
    L.code(pres, s, ['학생이 학습지를 풀고 제출하는 기능을 추가해 줘.', '- 서술형은 글상자, 선택형은 라디오 버튼. 정답은 화면에 보여 주지 마', '- 제출 → .../submissions/{내 uid} 에 answers, submittedAt(서버 시각)', '- 문서 이름은 반드시 로그인한 학생의 uid', '- 이미 제출했으면 이전 답을 채워 주고, 다시 제출은 merge로', '  answers와 submittedAt만 바꿔 줘 (feedback 같은 다른 필드는 지우지 마)'], 0.6, 3.5, 12.1, 2.2, 15, CODE);
    L.hint(s, '목록에 학습지가 없으면 그 수업에 가입했는지 확인. 제출 권한 오류는 오류 메시지 붙여넣기', 6.2, 16);
  }
  { // 37
    const s = mk(37, M5, '실습', '교사 제출현황 표');
    L.body(s, ['교사 화면에 학생별 제출 여부 표를 만든다', '학생을 누르면 그 학생의 답안을 본다. 해당 수업 교사만 본다'], 0.6, 1.65, 12.1, 1.5);
    L.table(pres, s, [['학생 이름', '제출 여부', '제출 시각'], ['테스트 학생 1', '제출', '10:42'], ['테스트 학생 2', '미제출', '-']], 0.6, 3.3, [4.0, 3.0, 5.1], { fontSize: 16, rowH: 0.5 });
    L.code(pres, s, ['교사용 "제출현황" 표를 추가해 줘.', '- 가입 학생(members)을 한 줄씩: 이름 / 제출·미제출 / 시각 (이름은 users/{uid}의 name)', '- 제출 여부는 submissions/{uid} 문서가 있는지로 판단', '- 학생 줄을 누르면 문항별 답, 선택형은 맞음/틀림 표시 (보기 번호는 1부터)', '- 학생에게는 보이지 않게'], 0.6, 5.3, 12.1, 1.55, 15, CODE);
  }
  { // 38
    const s = mk(38, M5, '개념', '생각해 보기: 정답이 문항 속에 있으면?');
    L.body(s, ['정답을 questions[]에 같이 저장했다', '학생이 문항 문서를 읽으면 정답도 읽을 수 있지 않을까?', '옆 사람과 1분 토론한 뒤 대안을 찾아 본다'], 0.6, 1.7, 12.1, 2.1);
    L.box(pres, s, '문항 문서\n질문 / 보기 / 정답', 0.6, 4.15, 3.6, 2.0, { fontSize: 20, bold: true, fill: { color: C.card }, line: { color: C.ink, width: 2 } });
    L.arrowR(pres, s, 4.3, 5.15, 0.6, C.red);
    L.box(pres, s, '학생이 열면\n정답 줄까지 보임', 5.1, 4.45, 2.8, 1.4, { fontSize: 18, fill: { color: C.redT }, line: { color: C.red, width: 2 } });
    L.box(pres, s, '대안 ① 정답 없이 서술형 중심으로 운영', 8.3, 4.1, 4.4, 0.95, { fontSize: 16, fill: { color: C.tealT }, line: { color: C.teal, width: 2 } });
    L.box(pres, s, '대안 ② 정답을 교사만 읽는 별도 문서로 분리 (심화)', 8.3, 5.2, 4.4, 0.95, { fontSize: 16, fill: { color: C.tealT }, line: { color: C.teal, width: 2 } });
  }
  { // 39
    const s = mk(39, M5, '정리', '막힘 모음과 복구 지점');
    L.body(s, ['모듈 5 완성: 작성 → 제출 → 제출현황', '막히면 오류 메시지를 그대로 Claude Code에 붙여넣는다'], 0.6, 1.65, 12.1, 1.4);
    [['교사 학습지 작성', '콘솔에서 worksheets 문서 생성 확인'], ['학생 제출', '콘솔에서 submissions/{내 uid} 문서 확인'], ['교사 제출현황', '제출한 학생이 "제출"로 보이는지']].forEach((c, i) => {
      const x = 0.6 + i * 4.1;
      L.box(pres, s, '', x, 3.3, 3.9, 2.0, { fill: { color: C.card }, line: { color: C.teal, width: 2 } });
      s.addShape(P.rect, { x: x + 0.2, y: 3.5, w: 0.32, h: 0.32, fill: { color: C.card }, line: { color: C.red, width: 2 } });
      s.addText(c[0], { x: x + 0.65, y: 3.4, w: 3.1, h: 0.5, fontSize: 20, bold: true, color: C.ink, fontFace: FONT, valign: 'middle', margin: 0, isTextBox: true });
      s.addText(c[1], { x: x + 0.2, y: 4.1, w: 3.5, h: 1.0, fontSize: 16, color: C.ink, fontFace: FONT, valign: 'top', margin: 0, isTextBox: true });
    });
    s.addText('정답 비교가 모두 틀림 → 콘솔에서 answer가 0부터 센 숫자인지 확인', { x: 0.6, y: 5.55, w: 12.1, h: 0.5, fontSize: 18, color: C.red, bold: true, fontFace: FONT, margin: 0, isTextBox: true });
    cp(s, 'checkpoint-m5', 0.6, 6.25);
  }

  // ---------- 모듈 6 ----------
  const M6 = '모듈 6 · 개인별 맞춤 피드백';
  { // 40
    const s = mk(40, M6, '개념', '맞춤 피드백, 세 단계로 만든다');
    L.body(s, ['답안 읽기 → 초안 만들기 → 교사가 검토해 전달', '초안은 보조교사가, 최종 책임은 교사가', '학생에게는 교사가 저장한 피드백만 보인다'], 0.6, 1.7, 12.1, 2.1);
    L.flow(pres, s, [{ t: '1 답안 읽기\n(학생 답안지\nsubmissions/{uid})', fill: C.tealT, color: C.teal }, { t: '2 초안 만들기\n(정답 비교 +\n안내 문구)', fill: C.tealT, color: C.teal }, { t: '3 교사 검토·수정 후 저장\n(feedback)\n교사 확인', fill: C.redT, color: C.red, bold: true }], 0.6, 4.1, 12.1, 1.9, { fontSize: 20, gap: 0.7 });
  }
  { // 41
    const s = mk(41, M6, '개념', '비밀은 서버에, 피드백은 본인만');
    L.body(s, ['AI 열쇠(API 키)를 브라우저에 두면 누구나 꺼내 쓴다', '열쇠는 서버(Cloud Functions = 교무실 금고)에 둔다', '피드백도 본인 답안지에 붙어 있어 본인만 본다'], 0.6, 1.7, 12.1, 2.1);
    L.box(pres, s, 'X  브라우저에 키 보관\n학생이 개발자 도구(F12)로 열면 키가 보임', 0.6, 4.0, 5.9, 1.7, { fontSize: 20, fill: { color: C.redT }, line: { color: C.red, width: 3 } });
    L.box(pres, s, 'O  서버(Cloud Functions)에 키 보관\n브라우저는 결과만 받음', 6.8, 4.0, 5.9, 1.7, { fontSize: 20, fill: { color: C.tealT }, line: { color: C.teal, width: 3 } });
    s.addText('보안 원칙 2: 학생은 자기 제출물만 읽는다 (피드백도 제출물 안에 있다)', { x: 0.6, y: 6.0, w: 12.1, h: 0.6, shape: P.roundRect, rectRadius: 0.1, fill: { color: C.gold }, line: { color: C.goldL, width: 1.5 }, fontSize: 18, bold: true, color: C.ink, fontFace: FONT, align: 'center', valign: 'middle', margin: 6 });
  }
  { // 42
    const s = mk(42, M6, '실습', '정답 비교로 피드백 초안 만들기');
    L.body(s, ['선택형은 정답과 비교해 "맞음 / 다시 보기"', '제출현황 표에 "피드백 초안 만들기" 버튼 추가'], 0.6, 1.65, 12.1, 1.4);
    L.code(pres, s, ['학생 답안 화면에 "피드백 초안 만들기" 버튼을 추가해 줘. 누르면 입력칸에 채워 줘.', '1) 선택형: 정답(answer)과 비교 → "문항 N: 맞았어요" / "다시 한 번 살펴보세요"', '2) 교사가 문항마다 적은 "틀렸을 때 안내 문구"를 틀린 문항에 이어 붙인다', '3) 서술형: "문항 N: 선생님이 직접 읽고 코멘트를 남길게요"', '4) 마지막 줄: "총 N문항 중 M문항 맞았어요" (N은 선택형 문항 수)', 'AI는 부르지 말고, 아직 Firestore에 저장하지 마. 입력칸에 채우기만 해.'], 0.6, 3.4, 12.1, 2.35, 15, CODE);
    L.hint(s, '모두 틀림으로 나오면 학습지의 정답 입력 확인. 버튼이 안 보이면 강력 새로고침', 6.2, 16);
  }
  { // 43
    const s = mk(43, M6, '실습', '고쳐서 저장하면 학생 화면에 도착');
    L.body(s, ['교사가 초안을 마음대로 고친 뒤 "저장"', '저장 위치는 submissions/{uid}의 feedback', '학생 화면에 "선생님 피드백" 카드가 보인다'], 0.6, 1.7, 12.1, 2.0);
    L.code(pres, s, ['입력칸 아래에 "피드백 저장" 버튼을 추가해 줘.', '- submissions/{uid}의 feedback 필드에만 저장 (updateDoc, 다른 필드는 건드리지 마)', '- 이미 저장된 피드백이 있으면 다시 열 때 입력칸에 불러오기', '- 학생 화면: feedback이 있을 때만 "선생님 피드백" 카드, 없으면 "아직 피드백이 없어요"', '- 피드백 글은 HTML로 해석하지 말고 글자 그대로 출력'], 0.6, 4.0, 12.1, 1.95, 15, CODE);
    L.hint(s, '권한 오류는 임시 규칙 확인. 카드가 안 보이면 학생이 가입·제출했는지 확인 후 새로고침', 6.3, 16);
  }
  { // 44
    const s = mk(44, M6, '실습', '확인: 제출부터 피드백 수신까지');
    L.body(s, ['두 계정을 크롬 일반 창(교사)과 시크릿 창(학생)으로 나눠 쓴다', '전체 한 바퀴가 되면 완료'], 0.6, 1.65, 12.1, 1.4);
    ['시크릿 창: 학생 로그인 → 학습지 풀고 제출', '일반 창: 교사 로그인 → 제출현황에서 학생 선택 → "피드백 초안 만들기"', '초안 끝에 교사 한마디를 직접 써 넣고 "피드백 저장"', '시크릿 창: 새로고침 → "선생님 피드백" 카드에 내 글이 보이는지', '(선택) 학생 답을 바꿔 다시 제출 → 초안을 다시 만들어 비교'].forEach((t, i) => {
      const y = 3.1 + i * 0.6;
      L.numCircle(pres, s, i + 1, 0.6, y + 0.02, 0.5, i === 4 ? C.mute : C.red);
      s.addText(t, { x: 1.3, y, w: 11.4, h: 0.55, fontSize: 18, color: C.ink, fontFace: FONT, valign: 'middle', margin: 0, isTextBox: true });
    });
    L.hint(s, '피드백이 사라졌다면 "재제출해도 feedback은 지우지 말고 병합 저장으로 바꿔 줘"', 6.35, 16);
  }
  { // 45 심화 선택
    const s = mk(45, M6, '데모', '심화: AI가 초안을 써 주는 피드백');
    L.optionalFrame(pres, s);
    L.body(s, ['선택 과정: 오늘은 강사 시연, 직접 만들기는 연수 후 과제', 'AI 키는 서버에만. Functions 배포는 Blaze(종량제) 요금제가 필요하고 AI 비용도 든다'], 0.7, 1.8, 12.0, 1.6);
    L.flow(pres, s, ['브라우저\n(교사가 버튼 클릭)', 'Cloud Functions\n(키 보관, 답안 전달)', 'AI\n(초안 생성)', '교사 화면 입력칸\n(초안만 돌려줌,\n저장 안 함)', { t: '교사가 검토 후 저장\n(Firestore feedback)\n교사 확인', fill: C.redT, color: C.red, bold: true }], 0.7, 4.0, 12.0, 1.6, { fontSize: 15, gap: 0.3 });
    s.addText('API 키는 여기만', { x: 3.15, y: 3.55, w: 2.4, h: 0.4, shape: P.roundRect, rectRadius: 0.1, fill: { color: C.ink }, color: 'FFFFFF', bold: true, fontSize: 14, align: 'center', valign: 'middle', fontFace: FONT, margin: 2 });
    s.addText('함수는 Firestore에 직접 쓰지 않는다', { x: 0.7, y: 5.85, w: 8.0, h: 0.5, fontSize: 18, color: C.ink, bold: true, fontFace: FONT, margin: 0, isTextBox: true });
    L.placeholder(pres, s, '[QR/링크 자리: 연수 후 과제 프롬프트]', 9.2, 5.8, 3.4, 0.95, 14);
  }
  { // 46
    const s = mk(46, M6, '정리', 'AI를 쓸 때 지킬 것, 그리고 복구 지점');
    L.body(s, ['교사가 반드시 검토한 뒤 전달한다', '학생 이름·이메일 등 개인정보는 최소한만 AI에 보낸다', '막혔다면 checkpoint-m6에서 이어가기'], 0.6, 1.7, 12.1, 2.1);
    checks(s, ['교사 검토 필수', '개인정보 최소 전달 (이름 대신 번호 등)', '기관 지침 확인'], 0.6, 4.2, 8.0, 22, 0.75);
    L.folder(pres, s, 'checkpoint-m6', 9.3, 4.4, 3.4, 0.75);
  }

  // ---------- 모듈 7 ----------
  const M7 = '모듈 7 · 배포·보안 규칙·마무리';
  { // 47
    const s = mk(47, M7, '개념', '보안 규칙 = 교무실 출입 규칙');
    L.body(s, ['누가 어떤 서류함을 열 수 있는지 규칙이 정한다', '지금까지의 5가지 원칙을 오늘 한 번에 걸어 잠근다', '화면 버튼을 숨기는 것은 안전이 아니다'], 0.6, 1.65, 12.1, 2.0);
    L.table(pres, s, [['원칙', '한 줄 뜻', '처음 만난 곳'], ['1 가입한 수업 자료만 읽는다', '열쇠 없으면 교실 못 들어감', '슬라이드 28'], ['2 내 제출물만 읽고 쓴다', '내 답안지만 열람', '슬라이드 34, 41'], ['3 수업·자료·학습지 작성은 그 수업 교사만', '교사만 교실을 꾸밈', '슬라이드 20'], ['4 수업코드를 아는 사람만 1건, 전체 목록은 못 본다', '열쇠로 문 하나만 열기', '슬라이드 20'], ['5 교사 HTML은 sandbox iframe으로', '유리 진열장', '슬라이드 28']], 0.6, 3.5, [5.6, 3.9, 2.6], { fontSize: 15, rowH: 0.46 });
    s.addText('원칙 1–4는 규칙(서버 쪽)이, 원칙 5는 화면(iframe)이 지킨다', { x: 0.6, y: 6.5, w: 12.1, h: 0.4, fontSize: 16, color: C.red, bold: true, fontFace: FONT, margin: 0, isTextBox: true });
  }
  { // 48
    const s = mk(48, M7, '실습', '5원칙을 문장으로 주고 규칙 파일 만들기');
    L.body(s, ['보안 규칙 파일(firestore.rules)도 Claude Code가 쓴다', '줄마다 몇 번 원칙인지 설명을 요청한다. 경로는 데이터 모델과 같아야 한다'], 0.6, 1.65, 12.1, 1.5);
    L.code(pres, s, ['firestore.rules를 새로 작성해 줘. 기존 임시 규칙은 지우고, 기본은 모두 거부.', '경로는 이 이름 그대로: users, classes, members, materials, worksheets, submissions', '원칙 1  가입한 수업의 자료·학습지만 읽는다', '원칙 2  내 제출물만 읽고 쓴다 (학생은 feedback을 못 고침)', '원칙 3  작성은 그 수업의 teacherUid만 (role은 수업을 만들 때만 확인)', '원칙 4  목록은 내 수업만, 코드를 알면 1건 get과 가입은 허용', '원칙 5  규칙이 아니라 화면 일: iframe의 sandbox 확인만', '각 줄 위에 "이 줄은 원칙 N번" 주석 + 마지막에 대응표'], 0.6, 3.35, 12.1, 2.85, 15, CODE);
    L.hint(s, 'role == teacher 줄이 수업 만들기 말고 다른 곳에 있으면 "권한은 teacherUid로 판단하도록 고쳐 줘"', 6.4, 16);
  }
  { // 49
    const s = mk(49, M7, '실습', '규칙과 웹사이트를 인터넷에 올리기');
    L.body(s, ['규칙 배포 = 출입 규칙을 교무실 문에 붙이는 일', 'Hosting 배포 = 우리 클래스룸을 학교 게시판에 올리는 일', '끝나면 누구나 열 수 있는 공개 주소가 생긴다'], 0.6, 1.7, 12.1, 2.0);
    L.code(pres, s, ['firestore.rules를 배포하고, 이어서 Hosting에도 배포해 줘.', '1. firebase.json에 규칙·색인·hosting(현재 폴더)이 맞게 있는지 확인', '   (규칙·색인·README·samples·functions·숨김 파일은 공개 제외)', '2. 프로젝트 ID는 firebase-config.js의 projectId', '3. 규칙·색인 먼저, 이어서 Hosting 배포', '4. 끝나면 공개 주소(Hosting URL)를 알려 줘'], 0.6, 4.0, 12.1, 2.1, 15, CODE);
    L.hint(s, '로그인 오류면 안내받은 firebase login을 내가 직접 실행. "콘솔에만 있는 색인을 지울까요?"는 N', 6.3, 16);
  }
  { // 50
    const s = mk(50, M7, '실습', '막히는지 직접 눈으로 확인하기');
    s.addText('rules-check.html 점검: 막힘 6개 + 열림 2개가 나오면 성공 · 준비: 수업 A, B 만들기 / 학생은 B에만 가입', { x: 0.6, y: 1.6, w: 12.1, h: 0.7, fontSize: 18, bold: true, color: C.red, fontFace: FONT, margin: 0, valign: 'middle', isTextBox: true });
    L.table(pres, s, [['버튼', '시도', '기대', '원칙'],
      ['1', '가입하지 않은 수업(A) 자료 읽기', '막힘', '1'], ['2', '제출물 목록 읽기 / 다른 학생 제출물 읽기', '막힘', '2'], ['3', '학생 계정으로 수업 만들기', '막힘', '3'],
      ['4', '수업 전체 목록 읽기', '막힘', '4'], ['5', '내 제출물의 feedback 고치기', '막힘', '2'], ['6', '가입한 수업(B)에 자료 1건 쓰기', '막힘', '3'],
      ['확인', '가입한 수업 자료 읽기 + 내 제출물 읽기', '열림 2개', '1, 2']], 0.6, 2.35, [1.3, 6.9, 2.2, 1.7], { fontSize: 15, rowH: 0.38, align: 'left' });
    L.code(pres, s, ['checkpoint-final의 rules-check.html, rules-check.js를 이 폴더에 복사하고 Hosting을 다시 배포해 줘.'], 0.6, 6.3, 12.1, 0.55, 14, '점검 페이지가 없는 분만');
    s.addText('안 막히면 규칙이 틀린 것 → 슬라이드 48로', { x: 0.6, y: 5.55, w: 12.1, h: 0.4, fontSize: 16, bold: true, color: C.red, fontFace: FONT, margin: 0, isTextBox: true });
  }
  { // 51
    const s = mk(51, M7, '정리', '검증 체크리스트 5항목');
    L.body(s, ['원칙 1–5를 하나씩 확인하고 O, X로 기록한다'], 0.6, 1.65, 12.1, 0.6);
    L.table(pres, s, [['원칙', '확인 방법', '결과'], ['1 가입한 수업 자료만 읽는다', '버튼 1 막힘, 확인 버튼 열림', '☐'], ['2 내 제출물만 읽고 쓴다', '버튼 2·5 막힘, 내 제출물 열림', '☐'], ['3 작성은 그 수업 교사만', '버튼 3·6 막힘', '☐'], ['4 코드로 1건만, 전체 목록 불가', '버튼 4 막힘, 코드로 가입은 정상', '☐'], ['5 자료는 sandbox iframe', 'Claude Code에게 확인 요청', '☐']], 0.6, 2.45, [4.8, 6.0, 1.3], { fontSize: 16, rowH: 0.55 });
    L.box(pres, s, '로그인이 안 되면: 콘솔 보안 > Authentication > 설정 탭 > 승인된 도메인에 내 배포 주소(프로젝트ID.web.app) 추가', 0.6, 5.95, 12.1, 0.75, { fontSize: 16, fill: { color: C.gold }, line: { color: C.goldL, width: 1.5 } });
  }
  { // 52
    const s = mk(52, M7, '정리', '오늘 만든 것: 7개 모듈 회고');
    L.body(s, ['마무리 5분. 오늘 만든 것을 한 장으로 돌아본다', '내 주소로 누구나 들어올 수 있는 클래스룸이 생겼다'], 0.6, 1.65, 12.1, 1.5);
    const tl = [['1 도입', '빈 폴더 +\n"환영합니다"'], ['2 로그인', '구글 로그인 +\n역할 저장'], ['3 수업코드', '수업 만들기 +\n코드 가입'], ['4 자료', 'HTML 자료 +\nsandbox 열람'], ['5 학습지', '작성·제출·\n제출현황'], ['6 피드백', '초안·수정·\n학생 열람'], ['7 배포', '보안 규칙 +\n공개 주소']];
    const w = 1.62, g = 0.127;
    tl.forEach((t, i) => {
      const x = 0.6 + i * (w + g);
      L.chip(pres, s, t[0], x, 3.5, w, 0.6, i === 6 ? C.red : C.teal, 16);
      L.box(pres, s, t[1], x, 4.2, w, 1.4, { fontSize: 15, fill: { color: C.card }, line: { color: i === 6 ? C.red : C.teal, width: 2 } });
    });
    s.addText('오늘의 최종 산출물: 내 클래스룸 공개 주소', { x: 0.6, y: 5.95, w: 12.1, h: 0.6, fontSize: 24, bold: true, color: C.red, fontFace: FONT, margin: 0, isTextBox: true });
  }
  { // 53
    const s = mk(53, M7, '정리', '우리 학교에서 쓰기 전에 확인할 3가지');
    L.body(s, ['개인정보: 학생 이름·이메일은 꼭 필요한 것만. 기관 지침을 따른다', '정리: 오늘 쓴 테스트 계정과 테스트 데이터는 지운다', '요금: Firebase 요금제와 무료 한도를 확인한다. AI 피드백(Functions)은 Blaze가 필요하다'], 0.6, 1.7, 12.1, 2.9);
    [['개인정보', C.teal], ['정리', C.mute], ['요금', C.red]].forEach((c, i) => {
      const x = 0.6 + i * 4.1;
      s.addText(['방패', '빗자루', '동전'][i], { x, y: 4.8, w: 1.1, h: 1.1, shape: P.ellipse, fill: { color: c[1] }, color: 'FFFFFF', bold: true, fontSize: 18, align: 'center', valign: 'middle', fontFace: FONT, margin: 0 });
      s.addShape(P.rect, { x: x + 1.3, y: 5.2, w: 0.34, h: 0.34, fill: { color: C.card }, line: { color: C.red, width: 2 } });
      s.addText(c[0] + ' 확인', { x: x + 1.8, y: 5.05, w: 2.1, h: 0.65, fontSize: 20, bold: true, color: C.ink, fontFace: FONT, valign: 'middle', margin: 0, isTextBox: true });
    });
    s.addText('실제 학생 정보는 이 연수에서 쓰지 않았습니다.', { x: 6.2, y: 6.45, w: 6.5, h: 0.4, fontSize: 14, color: C.mute, fontFace: FONT, align: 'right', margin: 0, isTextBox: true });
  }
  { // 54
    const s = mk(54, M7, '정리', '다음 걸음과 설문');
    L.body(s, ['심화 과제: AI 피드백 붙이기, 화면 디자인 다듬기', '막혔던 분은 checkpoint-final에서 이어서', '설문에 답하고 내 공개 주소를 적어 두자'], 0.6, 1.7, 12.1, 2.0);
    [['심화 과제', '[QR 자리]\n슬라이드 45의 후 과제 프롬프트\n예: "학생 화면을 글자를 크게, 색을 부드럽게 바꿔 줘"'], ['자료 링크', '[링크 자리: 강사가 연수 직전에 채움]\n오늘 슬라이드 · 프롬프트 모음 · checkpoint-final'], ['설문', '[설문 링크/QR 자리: 강사가 연수 직전에 채움]']].forEach((c, i) => {
      const x = 0.6 + i * 4.1;
      s.addText(c[0], { x, y: 3.9, w: 3.9, h: 0.5, fontSize: 20, bold: true, color: C.teal, fontFace: FONT, margin: 0, isTextBox: true });
      L.placeholder(pres, s, c[1].replace('슬라이드 45의 후 과제', '슬라이드 45 연수 후 과제'), x, 4.45, 3.9, 2.3, 15);
    });
  }
};
