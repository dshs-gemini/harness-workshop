// 공통 도형 헬퍼. 시각 토큰: 배경 f8f2e4 / 본문 2a2314 / 강조 b0402c / 보조 356e67
const pptxgen = require('pptxgenjs');
const C = { bg: 'F8F2E4', ink: '2A2314', red: 'B0402C', teal: '356E67', card: 'FFFBF0', line: 'D9CDB0', mute: '6B5E45',
  tealT: 'DCE9E5', redT: 'F3DDD6', gold: 'FFF1CC', goldL: 'C9A24A', dark: '2A2314' };
const FONT = 'Malgun Gothic', MONO = 'Consolas';

function makePres() {
  const pres = new pptxgen();
  pres.layout = 'LAYOUT_WIDE'; // 13.33 x 7.5
  pres.title = '온라인 클래스룸 교원 연수';
  pres.author = '교원 연수 팀';
  pres.theme = { headFontFace: FONT, bodyFontFace: FONT };
  pres.defineSlideMaster({
    title: 'BASE', background: { color: C.bg },
    objects: [
      { text: { text: '온라인 클래스룸 교원 연수', options: { x: 0.6, y: 7.02, w: 5, h: 0.3, fontSize: 12, color: C.mute, fontFace: FONT, margin: 0 } } },
      { placeholder: { options: { name: 'title', type: 'title', x: 0.6, y: 0.72, w: 12.1, h: 0.85, fontSize: 36, bold: true, color: C.ink, fontFace: FONT, align: 'left', valign: 'middle', margin: 0 }, text: '' } },
    ],
    slideNumber: { x: 12.2, y: 7.0, w: 0.6, h: 0.3, fontSize: 12, color: C.mute, fontFace: FONT, align: 'right' },
  });
  return pres;
}

const BADGE = { 개념: C.teal, 실습: C.red, 데모: C.goldL, 정리: C.mute };

function frame(pres, spec, notes) {
  const s = pres.addSlide({ masterName: 'BASE' });
  s.addText(spec.mod, { x: 0.6, y: 0.3, w: 5.4, h: 0.36, fontSize: 16, color: C.teal, bold: true, fontFace: FONT, margin: 0, isTextBox: true });
  s.addText(spec.type, { x: 5.9, y: 0.3, w: 0.9, h: 0.36, shape: pres.ShapeType.roundRect, rectRadius: 0.18, fill: { color: BADGE[spec.type] || C.mute },
    color: 'FFFFFF', fontSize: 14, bold: true, align: 'center', valign: 'middle', fontFace: FONT, margin: 0 });
  s.addText(spec.title, { placeholder: 'title' });
  s.addNotes(notes);
  return s;
}

// 줄 목록 본문 (24pt). 각 줄 앞에 작은 원 글머리
function body(s, lines, x, y, w, h, size = 24) {
  size = Math.max(size, 24); // 본문 24pt 이상
  const runs = [];
  lines.forEach((t, i) => runs.push({ text: t, options: { bullet: { indent: 24 }, breakLine: i < lines.length - 1, paraSpaceAfter: 6 } }));
  s.addText(runs, { x, y, w, h, fontSize: size, color: C.ink, fontFace: FONT, valign: 'top', margin: 0, isTextBox: true });
}

function box(pres, s, text, x, y, w, h, o = {}) {
  s.addText(text, Object.assign({ x, y, w, h, shape: pres.ShapeType.roundRect, rectRadius: 0.12, fill: { color: C.card },
    line: { color: C.line, width: 1.25 }, color: C.ink, fontSize: 18, align: 'center', valign: 'middle', fontFace: FONT, margin: 6 }, o));
}
function arrowR(pres, s, x, y, w = 0.32, color = C.mute) {
  s.addShape(pres.ShapeType.rightArrow, { x, y: y - 0.16, w, h: 0.32, fill: { color }, line: { color, width: 0 } });
}
function arrowD(pres, s, x, y, h = 0.32, color = C.mute) {
  s.addShape(pres.ShapeType.downArrow, { x: x - 0.16, y, w: 0.32, h, fill: { color }, line: { color, width: 0 } });
}
// 가로 흐름: items=[text | {t,color,fill}]
function flow(pres, s, items, x, y, w, h, o = {}) {
  const gap = o.gap || 0.42, n = items.length, bw = (w - gap * (n - 1)) / n;
  items.forEach((it, i) => {
    const d = typeof it === 'string' ? { t: it } : it;
    const bx = x + i * (bw + gap);
    box(pres, s, d.t, bx, y, bw, h, Object.assign({ fontSize: o.fontSize || 18, fill: { color: d.fill || o.fill || C.card },
      line: { color: d.color || o.color || C.line, width: d.color || o.color ? 2 : 1.25 }, color: d.tc || C.ink, bold: d.bold }, d.o || {}));
    if (i < n - 1) arrowR(pres, s, bx + bw + (gap - 0.3) / 2, y + h / 2, 0.3, o.arrow || C.mute);
  });
}
// 자리표시 박스: 점선 + 눈에 띄는 색
function placeholder(pres, s, label, x, y, w, h, size = 16) {
  s.addText(label, { x, y, w, h, shape: pres.ShapeType.rect, fill: { color: C.gold }, line: { color: C.red, width: 2, dashType: 'dash' },
    color: C.red, bold: true, fontSize: size, align: 'center', valign: 'middle', fontFace: FONT, margin: 6 });
}
// 복사 가능한 코드 블록 (모노스페이스)
function code(pres, s, lines, x, y, w, h, size = 15, label) {
  if (label) s.addText(label, { x, y: y - 0.32, w, h: 0.3, fontSize: 14, color: C.mute, fontFace: FONT, margin: 0, isTextBox: true });
  s.addShape(pres.ShapeType.roundRect, { x, y, w, h, rectRadius: 0.1, fill: { color: C.dark }, line: { color: C.dark, width: 0 } });
  const runs = lines.map((t, i) => ({ text: t, options: { breakLine: i < lines.length - 1 } }));
  s.addText(runs, { x: x + 0.2, y: y + 0.1, w: w - 0.4, h: h - 0.2, fontSize: size, color: 'F8F2E4', fontFace: MONO, valign: 'top', margin: 0, isTextBox: true, paraSpaceAfter: 2 });
}
function hint(s, text, y = 6.45, size = 18) {
  s.addText([{ text: '막힐 때  ', options: { bold: true, color: C.red } }, { text, options: { color: C.ink } }],
    { x: 0.6, y, w: 12.1, h: 0.5, fontSize: size, fontFace: FONT, margin: 0, valign: 'middle', isTextBox: true });
}
function table(pres, s, rows, x, y, colW, o = {}) {
  const fs = o.fontSize || 16, rowH = o.rowH || 0.5;
  const data = rows.map((r, ri) => r.map((c) => {
    const head = ri === 0;
    return { text: String(c), options: { bold: head, color: head ? 'FFFFFF' : C.ink, fill: { color: head ? (o.head || C.teal) : (ri % 2 ? C.card : 'F1E8D2') },
      fontSize: fs, fontFace: FONT, valign: 'middle', align: o.align || 'left', margin: [0.04, 0.1, 0.04, 0.1] } };
  }));
  s.addTable(data, { x, y, w: colW.reduce((a, b) => a + b, 0), colW, rowH, border: { type: 'solid', color: C.line, pt: 1 } });
}
function chip(pres, s, text, x, y, w, h, color, size = 16) {
  s.addText(text, { x, y, w, h, shape: pres.ShapeType.roundRect, rectRadius: 0.12, fill: { color: color || C.teal }, color: 'FFFFFF', bold: true,
    fontSize: size, align: 'center', valign: 'middle', fontFace: FONT, margin: 4 });
}
function numCircle(pres, s, n, x, y, d = 0.5, color = C.red) {
  s.addText(String(n), { x, y, w: d, h: d, shape: pres.ShapeType.ellipse, fill: { color }, color: 'FFFFFF', bold: true, fontSize: 18, align: 'center', valign: 'middle', fontFace: FONT, margin: 0 });
}
function folder(pres, s, text, x, y, w = 2.6, h = 0.5, fs = 16) {
  s.addText(text, { x, y, w, h, shape: pres.ShapeType.roundRect, rectRadius: 0.08, fill: { color: C.gold }, line: { color: C.goldL, width: 1.5 },
    color: C.ink, bold: true, fontSize: fs, fontFace: MONO, align: 'center', valign: 'middle', margin: 2 });
}
// 점선 박스 + 리본 (심화 선택)
function optionalFrame(pres, s) {
  s.addShape(pres.ShapeType.roundRect, { x: 0.35, y: 1.62, w: 12.63, h: 5.3, rectRadius: 0.1, fill: { color: 'FFFFFF', transparency: 100 }, line: { color: C.teal, width: 3, dashType: 'dash' } });
  s.addText('심화 선택 · 시간 되는 분만', { x: 9.0, y: 0.26, w: 3.95, h: 0.46, shape: pres.ShapeType.roundRect, rectRadius: 0.1, fill: { color: C.teal }, color: 'FFFFFF', bold: true, fontSize: 18, align: 'center', valign: 'middle', fontFace: FONT, margin: 2 });
}
module.exports = { C, FONT, MONO, makePres, frame, body, box, arrowR, arrowD, flow, placeholder, code, hint, table, chip, numCircle, folder, optionalFrame };
