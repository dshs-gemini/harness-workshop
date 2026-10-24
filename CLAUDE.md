# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A single self-contained static HTML document: `클로드코드_하네스엔지니어링_교원연수.html` (Korean-language teacher-training guide, "Claude Code based Harness Engineering"). There is no build system, package manager, linter, or test suite, and the directory is not a git repository. To "run" it, open the file in a browser (e.g. `open 클로드코드_하네스엔지니어링_교원연수.html` on macOS). All content is in Korean; keep new content in Korean.

## Structure of the HTML file (~1600 lines)

Everything lives in one file, in this order:
- `<style>` (top): all CSS. Theme is defined as CSS variables on `:root` (warm paper palette: `--bg`, `--accent`, `--blue`, `--green`, …). Reuse these variables rather than hard-coding colors. Responsive breakpoint is 900px (sidebar becomes an off-canvas drawer).
- `<aside class="sidebar">`: the hand-written table of contents (`<nav class="toc">`). Each entry is `<a href="#section-id" class="kind-concept|kind-practice|kind-check">`.
- `<main>`: a series of `<section class="section" id="...">` blocks. The `kind-*` class on the TOC link must match the badge on the section (`badge-concept` 개념, `badge-practice` 실습, `badge-check` 점검).
- `<script>` (bottom): vanilla JS, no dependencies — mobile sidebar toggle, scrollspy (IntersectionObserver over TOC `href`s), reading-progress bar, copy buttons, OS tabs, FAQ accordion. All handlers are delegated on `document` or keyed off class names/`data-os`, so new content using the existing classes works without JS changes.

Content organization: intro → **Track 1** (Claude Code basics, ids `t1-*`, sections 1.1–1.10) → **Track 2** (harness engineering: agents, skills, orchestrator, integrated workshop; ids `t2-*`, sections 2.1–2.7) → wrap-up (`wrap-checklist`, `wrap-faq`, `wrap-antipattern`, `wrap-references`).

## Editing conventions

- Adding or renaming a section requires keeping three things in sync: the `<section id>`, the TOC `<a href="#id">`, and the numbered heading text (e.g. "2.7 …"). Renumbering a section means updating the numbers in both the TOC and the `<h2 class="section-title">`, plus any in-text cross-references.
- Reusable components (copy an existing instance instead of inventing markup): `.practice-shell` > `.step` (`.step-num` + `.step-body`) for hands-on steps; `.terminal` (with `.term-you/.term-claude/.term-prompt/.term-comment` spans) for sample sessions; `.code-block` with `.copy-btn` and optional `.os-tabs`/`.os-panel[data-os]`; `.file-box` for example file contents; `.callout` with `-tip/-concept/-warn`; `.pattern-card`; `.card.good/.bad`; `.faq-item`.
- The copy button copies the text of the first `<code>` inside the enclosing `.code-block`, `.terminal`, or `.file-box`, so keep a `<code>` element in any block that has a `.copy-btn`.
- HTML-escape `<`, `>`, `&` inside `<code>` blocks (the file uses `&gt;`, `&ldquo;`, etc.).
- Keep the file self-contained: no external scripts, stylesheets, or build step.

## 하네스: 온라인 클래스룸 교원 연수 PPT

**목표:** Claude Code로 Firebase 기반 온라인 클래스룸을 만드는 3시간 교원 연수 PPT 제작.

**호출 조건:** 클래스룸 앱 제작 실습 PPT는 `classroom-course-builder`, 가이드 HTML 기반 "Claude·하네스 엔지니어링 + Firebase 기능·설정" HTML 슬라이드 제작·수정은 `harness-training-deck` 스킬을 사용한다.  단순 질문에는 직접 답해도 된다.

**변경 이력:**
| 날짜 | 변경 내용 | 대상 | 사유 |
| --- | --- | --- | --- |
| 2026-10-03 | Harness v2로 처음 구성 | 전체 | - |
| 2026-10-03 | 첫 실행: 연수 PPT 54장 제작(설계→병렬 원고→검수 2회→조립). 모듈 2 콘솔 설정 확장, 명세에 members.uid 추가·수업 문서 이름=수업코드 | 명세, 원고, 엔지니어 문서 | 사용자 요청과 검수 결과 반영 |
| 2026-10-04 | 방법론 중심 HTML 슬라이드용 오케스트레이터 `harness-training-deck`, 에이전트 `html-deck-builder`·`firebase-guide-researcher`, 스킬 `html-slide-deck-spec` 추가. curriculum-designer에 브리프 우선 규칙 추가 | 하네스 확장 | 목적이 앱 제작에서 Claude·하네스 방법과 Firebase 기능·설정 교육으로 바뀌고 산출물이 HTML 슬라이드 |
| 2026-10-04 | 첫 실행: 방법론 중심 HTML 슬라이드 79장 제작(설계→원고 10개 병렬+Firebase 조사→검수 2회→조립). 검수로 /lesson 이름, hook exit 2, 실험 플래그 제거, 보안 규칙 role 허점, firebaseConfig 구분 등 반영 | harness-training-deck 산출물 | 검수 결과 반영 |
| 2026-10-04 | 인쇄용 교재판(A4 세로, 78쪽) `build_handout.py` 추가, html-slide-deck-spec에 교재판 규칙·html-deck-builder 출력에 교재판 추가 | 스킬, 에이전트 | 배포용 교재 출력 요청(발표용 글꼴·레이아웃은 종이에 부적합) |
| 2026-10-04 | 복구 지점(cp-m1~cp-m9, practice-kit) 개념과 안내 문구 전부 삭제(원고·설계서·교재 빌더·curriculum-designer·html-slide-deck-spec), 덱·교재 재조립(교재 77쪽) | 원고, 설계서, 빌더, 에이전트·스킬 | 사용자 요청: 강사가 준비해야 하는 완성본 폴더를 쓰지 않기로 함 |
| 2026-10-04 | 발표용 덱 디자인 개편: 토큰 시스템(트랙별 색·타입 스케일), 유형별 레이아웃 템플릿, 슬라이드 약 50장 SVG 도식, 프롬프트 글자 확대. 교재 출력 불변(해시 확인) | build_deck.py, html-slide-deck-spec | 사용자 요청: 디자인 완성도 향상 |
| 2026-10-11 | 슬라이드 모듈 옛 M6(팀 패턴)·옛 M7(검증·훅·휴먼 리뷰 게이트) 삭제: 덱·교재 79→67장, 150분, 교재 66쪽. 옛 M8→M6(37~58), 옛 M9→M7(59~63), MW 64~67(번호 -12), M7 설계도 7→5항목, 가이드 HTML 2.7~2.11절 삭제(2.12→2.7). 같은 날 앞서: 교실 비유 전면 제거(정의·동작 원리 서술)·슬라이드 18 권한 모드/permissions 관계 보강. 삭제 원고는 `_workspace/deck/_removed/` | 원고, 설계서, build_deck.py, build_handout.py, 가이드 HTML, 지침 4개 | 사용자 요청: 연수 범위 축소, 정보교사 대상 비유 제거 |
| 2026-10-11 | M7을 '프로젝트: 우리 교과 단원 수업 패키지 만들기'(슬라이드 59~70, 12장 42분)로 확장: 단원 명세→하네스 설계도→수업 슬라이드(slides.html)→학생 워크북 웹앱(Firebase Authentication·Firestore·보안 규칙, 로컬 확인, Hosting 배포는 선택)→짝 점검. 마무리는 71~74. 덱·교재 67→74장, 150→180분. content-reviewer 검수(오류 5·위험 10·개선 10) 전부 반영: 새 .claude 폴더 재시작, 서브에이전트에 지시 전달, 교사용 정답 비포함, localhost 승인된 도메인 추가(M6 41 연동) 등 | 원고 M7·M6·MW·M1·M5, 설계서, build_deck.py, build_handout.py | 사용자 요청: 교과 단원 슬라이드와 학생 워크북 웹앱을 함께 개발하는 프로젝트(※ 번호·구성은 아래 후속 행에서 다시 바뀜) |
| 2026-10-11 | 슬라이드 전면 개편, revfactory/harness 활용 중심(멀티 에이전트 원리 설명 제외): M3 20·M4 21·22·27·28을 M4 20·25로 압축(M4 6장), M5를 '하네스가 만든 파일 읽고 고치기'(26~32, 에이전트·스킬 직접 설계 폐기)로 교체, M7을 단원 명세→하네스에게 팀 구성 요청→수업 슬라이드→학생 워크북 웹앱을 Firebase Hosting에 배포하고 URL로 확인하는 구성으로 재작성(사람은 Firebase 설정과 승인만, 코드·규칙 파일·배포는 Claude Code). 설계도 5항목, `.claude` 직접 만들기, 규칙 플레이그라운드, localhost, python 로컬 서버 단계 삭제. 덱·교재 74→70장, 180분 유지. 빌더에 설계서 학습 목표를 덮어쓰는 `GOALS_NEW` 추가 | 원고 M1·M3~M7·MW·M6 번호, build_deck.py, build_handout.py | 사용자 지시: 연수는 하네스 활용이 목적이고 복잡한 설정은 교사에게 인지 부하. 수정 범위를 슬라이드로 한정(가이드 HTML·설계서·`.claude` 지침은 새 구성과 어긋나 있음) |
| 2026-10-11 | M7 'Firebase 연결: 미리 로그인해 두기'(현재 58번) 실습 추가: 콘솔 로그인 확인 → `firebase login` → 공식 Firebase 플러그인(Claude Code용 MCP) 설치 → 프로젝트 목록으로 연동 확인. 공식 문서 확인 결과 콘솔 로그인은 CLI 인증을 대신하지 않으므로 그렇게 쓰지 않음. `! firebase login`(브라우저 상호작용)은 문서 근거가 없어 `[확인필요]`, 일반 터미널 사용 안내 | 원고 M7(58, 배포 59), build_deck.py | 사용자 요청: 콘솔에 미리 로그인해 두면 Claude Code가 Firebase와 바로 연동되는 과정 포함 |
| 2026-10-11 | M6에서 보안 규칙 슬라이드 3장(사용 상황·규칙 플레이그라운드 절차·Claude Code 초안 확인) 삭제, 나머지 슬라이드의 규칙 설명은 '접근 규칙은 Claude Code가 작성·배포(M7)' 한 구절로 정리. 덱·교재 70→67장. 최종 번호: M1 1~6, M2 7~11, M3 12~19, M4 20~25, M5 26~32, 휴식 33, M6 34~52(27분), M7 53~63(50분), MW 64~67. 줄어든 8분은 M7에 배정해 총 180분 유지 | 원고 M6·M7·MW·M1, build_deck.py, build_handout.py | 사용자 요청: 보안 규칙은 Claude Code에게 일임 |
| 2026-10-25 | 설치 전 Git 안내와 터미널 로그인 원리 추가. M1 4번에 Windows는 Git for Windows 권장(필수 아님, 공식 setup 문서 확인), 2번 노트에 사전 준비 항목 추가. M7에 새 개념 슬라이드 58 '터미널에서 한 번 로그인하면 Claude Code가 이어받는다'(Firebase `firebase login`·GitHub `gh auth login`, 자동은 실행이고 승인은 사람) 추가, 옛 58~63은 59~64, MW 64~67은 65~68로 번호 이동. 시간은 53(3→2분)·옛 58(5→4분)에서 줄여 M7 50분·총 180분 유지. 덱·교재 67→68장. 최종 번호: M1 1~6, M2 7~11, M3 12~19, M4 20~25, M5 26~32, 휴식 33, M6 34~52, M7 53~64, MW 65~68 | 원고 M1·M6·M7·MW, build_deck.py, build_handout.py | 사용자 요청: Git 설치 선행 여부와 로그인 후 자동화 설명 추가, 한 슬라이드에 구겨 넣지 말고 새 슬라이드로 분리 |
| 2026-10-25 | 설계서를 현재 원고(68장) 기준으로 전면 동기화: 모듈표(M3 12~19, M4 20~25, M5 26~32, 휴식 33, M6 34~52 27분, M7 53~64 50분, MW 65~68), 설명/실습 35/125, 시간표, 원본 id 대조표(`t2-agent-practice`·`t2-skill-*` 제외 명시), M6 기능 6개 배정, 7절 모듈별 슬라이드 표 전체, 사전 준비(Windows Git 권장·Node/CLI)·용어표(터미널 로그인 추가, 규칙 플레이그라운드·로컬 서버 삭제). 빌더가 읽는 모듈표 학습 목표·산출물 열은 유지해 덱·교재 출력은 해시 동일 | 설계서 `01_designer_curriculum.md` | 사용자 요청: 설계서도 새 번호에 맞춰 수정 |
