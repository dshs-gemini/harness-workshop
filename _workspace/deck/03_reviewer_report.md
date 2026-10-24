# 03. 검수 보고서: 교원 연수 슬라이드 원고 (79장, 180분)

- 검수일: 2026-10-04 / 검수: content-reviewer
- 대상: `01_designer_curriculum.md`, `02_writer_M1~M9·MW_slides.md`, `02_researcher_firebase_facts.md`, 원본 `클로드코드_하네스엔지니어링_교원연수.html`
- 방법: 원본 27개 섹션과 원고를 직접 대조했다. 공식 문서(code.claude.com, firebase.google.com, support.google.com)와 `revfactory/harness` 저장소를 조회했다. hook 명령은 macOS에서 직접 실행해 확인했다.
- 원고는 수정하지 않았다.

## 요약

| # | 검증 항목 | 판정 |
|---|---|---|
| 1 | 브리프 준수(앱 제작 중심으로 흐르지 않았나) | 통과 |
| 2 | 원본 내용과의 일치·누락(27개 섹션) | 수정필요(경미) |
| 3 | 슬라이드 번호 1–79, 시간 합계 180분 | 통과(분량 위험 2곳 권장 사항) |
| 4 | 하네스 설명 정확성(에이전트·스킬 파일 형식, 프론트매터) | **수정필요(필수 6건)** |
| 5 | [확인필요] 판정 | 아래 5절 표(확인됨/틀림/미확인) |
| 6 | 57번 보안 규칙 문법 | 통과 |
| 7 | 용어·개인정보·보안(API 키/firebaseConfig 구분 포함) | **수정필요(필수 2건)** |

필수 수정 8건: 4-A(`/lesson` 호출 불가), 4-B(서브에이전트와 CLAUDE.md), 4-C(`/agents` 동작 변경), 4-D(실험 플래그 불필요), 4-E(권한 모드·플랜 승인 화면), 4-F(hook 오류가 클로드에게 전달되지 않음), 7-A(58번 규칙 원칙 1의 권한 상승 경로), 7-B(51번 "API 키 = 금고 비밀번호" 혼동).
4-A, 4-F는 원본 HTML에도 있는 오류다. 원본도 같이 고칠지 사용자에게 알리는 것을 권한다.

---

## 1. 브리프 준수: 통과
- 앱 코드를 만드는 프롬프트가 없다. 58(규칙 초안), 65(배포 계획), 69(기능 표), 73(하네스 파일)은 프롬프트 안에 "앱 코드는 만들지 마" 또는 "계획만"을 넣었다.
- 클래스룸은 49, 54, 71, 72에서 "예시 소재"로만 나온다. M9 산출물은 설계도와 `.claude/` 파일이다.
- 시간 비중도 맞다. Claude Code와 하네스(M1–M7, M9)가 145분, Firebase(M8)가 35분이다.

## 2. 원본 일치·누락: 수정필요(경미)
27개 id가 모두 원고에 들어 있다(설계서 4절 대조표대로 확인). 프롬프트와 file-box는 원본과 글자까지 같다. 바꾼 곳에는 노트에 "원본 대비 변경"이 적혀 있다. 고칠 곳:

| 파일 | 슬라이드 | 문제 | 수정안 |
|---|---|---|---|
| M1 | 2 노트 | 원본 intro의 OS 요구사항이 빠졌다 | "macOS 13.0 이상, Windows 10(1809) 이상"을 준비물 점검에 추가(공식 setup 문서와 일치) |
| M4 | 22 노트 | 원본은 7층(환경…관측)을 책과 다른 "관점도 있다"로 소개한다. 원고는 책 인용 바로 뒤에 붙여 저자 주장처럼 읽힌다 | "7층으로 나누어 보는 관점도 있다(원본 표현)"로 출처를 구분 |
| M5 | 36 노트 | "다음 모듈(M8, Firebase 기능 지도)에 대비해"라고 했지만 휴식 다음 모듈은 M6이다 | "휴식 뒤 세 번째 모듈(M8)에 대비해" |
| MW | 76 도식·노트 | "나머지 7개는 연수 자료 HTML 마지막에"는 틀렸다. HTML 체크리스트는 11개이고 Firebase 2개 항목(12·13)은 HTML에 없다. 노트의 "참가자 자료 HTML과 같은 순서"도 맞지 않다 | "나머지 7개는 배포 자료(노트 목록)에"로 바꾸기. 12·13은 덱에서 추가한 항목이라고 노트에 적기 |
| MW | 78 노트 | 원본 FAQ "동료와 공유"의 "버전 기록 습관(증거 원칙)" 문장이 빠졌다(선택) | 노트 셋째 답 끝에 한 문장 추가 |

## 3. 번호·시간: 통과
- 번호 1–79가 빠짐없이 이어지고 중복이 없다(79개 확인).
- 모듈 합계: M1 13, M2 12, M3 21, M4 19, M5 18, 휴식 10, M6 12, M7 18, M8 35, M9 12, MW 10 = **180분**. 각 원고의 슬라이드별 `(n분)`을 합산해 확인했다.
- 설명 48 / 실습 112가 설계서와 일치한다.
- 분량 위험(권장):
  - M8 57(4분)과 58(3분): 초보자가 플레이그라운드 입력 4칸을 채우고, 다음 슬라이드에서 Claude Code 초안을 붙여 다시 실행하기에는 빠듯하다. 58 노트에 "시간이 부족하면 강사 화면 시연으로 전환" 대안을 적는다.
  - 4-D를 반영해 23번 플래그 단계를 빼면 M4에 2분이 남는다. 이 시간은 24(설치 범위 선택)와 26에 나눈다.

## 4. 하네스 설명 정확성: 수정필요

**4-A [필수] `/lesson`은 동작하지 않는다.** 해당: M5 34(프롬프트·file-box·`/lesson 함수와 매개변수`), 35, M9 72 예시 4번, M3 15 본문("폴더 이름이 곧 명령 이름").
- 근거: 공식 Skills 문서에 따르면 명령 이름은 "Frontmatter `name` field if present, otherwise directory name"이다. `name: lesson-plan-writer`이면 명령은 `/lesson-plan-writer`가 된다. 원본 HTML의 오류를 그대로 옮겼다.
- 수정안(택1):
  - (가) 34 프롬프트를 "이름은 lesson,"으로 바꾸고 file-box를 `name: lesson`으로 바꾼다. 폴더는 `lesson-plan-writer` 그대로 둔다. 노트에 원본 대비 변경을 적는다.
  - (나) 호출을 `/lesson-plan-writer 함수와 매개변수`로 바꾸고, description의 "/lesson으로"도 맞춘다.
- 15 본문 수정: "명령 이름 = `name` 값(없으면 폴더 이름). 예: `quiz/SKILL.md` → `/quiz`".

**4-B [필수] 서브에이전트도 CLAUDE.md를 읽는다.** 해당: M5 29 노트 "본문은 메인 세션의 대화와 CLAUDE.md 맥락을 이어받지 않는다".
- 근거: Subagents 문서에 따르면 사용자 정의 서브에이전트는 CLAUDE.md 계층을 모두 읽는다(`omitClaudeMd: true`일 때만 제외). 물려받지 않는 것은 메인 대화와 Claude Code 기본 시스템 프롬프트다.
- 수정안: "본문이 이 에이전트의 지침서가 된다. 메인 대화 내용은 넘어가지 않으므로 필요한 맥락을 본문에 담는다. 프로젝트 CLAUDE.md는 함께 읽는다."

**4-C [필수] `/agents`는 이제 목록을 보여 주지 않는다.** 해당: M5 31(본문 3번째 줄, 프롬프트 `/agents`, 예상 결과 "목록에 difficulty-tagger가 보인다", 노트 "대화형으로 새 에이전트를 만들 수도"), M4 26 막힐 때, M3 15 표.
- 근거: Commands 문서에 따르면 `/agents`는 "Print a reminder to ask Claude to create or manage subagents… On v2.1.197 and earlier, opens an interactive wizard"이다.
- 수정안:
  - 31: `/agents` 대신 "지금 이 폴더에서 쓸 수 있는 서브에이전트 목록을 보여줘"라고 묻거나, 편집기로 `.claude/agents/` 폴더를 열어 확인하게 한다.
  - 15 표: "`/agents`: 서브에이전트 관리 안내(예전 버전은 목록·생성 화면)".
  - 26 막힐 때: "`.claude/agents/` 폴더에 두 파일이 있는지 확인".

**4-D [필수] 플러그인 v2는 실험 플래그가 필요 없다. 플래그를 켜면 오히려 동작이 달라질 수 있다.** 해당: M4 23 전체, 23·24 노트 "이 연수에서 쓸 플러그인이 에이전트 팀이라는 실험 기능을 쓰기 때문에", MW 78 FAQ(노트), 설계서 8절 `cp-m4` 내용(settings.json).
- 근거:
  - `revfactory/harness` README(v2.1.0): "No experimental flags. The `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` dependency is gone entirely." 설치 절에도 "No environment variables or experimental flags required."라고 적혀 있다.
  - Agent teams 문서: "While agent teams are enabled, a subagent that Claude names in the lead's session launches as a teammate." 플래그를 켜 두면 26의 quiz-writer/quiz-checker가 서브에이전트가 아니라 팀원(teammate)으로 실행되어 예시 화면과 달라질 수 있다.
- 수정안:
  - 23을 "`mkdir mini-harness && cd mini-harness` → `claude`"(1분)로 줄이고 settings.json file-box를 지운다.
  - 실험 기능 "에이전트 팀"은 노트 한 줄로만 남긴다(플래그 이름은 확인됨, 이 연수에서는 켜지 않음).
  - 78 FAQ 답변을 "Anthropic이 제공하는 것은 플러그인 마켓플레이스라는 설치 통로이고, harness 플러그인(v2)은 실험 플래그 없이 동작한다"로 바꾼다.
  - `cp-m4` 목록에서 settings.json을 뺀다.

**4-E [필수] 권한 모드 표와 플랜 승인 화면이 현재 Claude Code와 다르다.** 해당: M3 18(표·본문·노트), M2 8·9(예상 결과의 y/n, 막힐 때), M4 25, M9 73(승인 화면 `[확인필요]`).
- 근거(Permission modes 문서):
  - 모드는 Manual(설정값 `default`), Accept edits, Plan, Auto 네 가지가 기본 순환에 들어 있다. 그 밖에 dontAsk, bypassPermissions가 있다.
  - "With Claude Code v2.1.283 or later, auto mode is the built-in starting permission mode for interactive terminal… sessions."
  - Shift+Tab 순서는 "From `auto`, the first press switches to `default`, and the cycle then runs `default` → `acceptEdits` → `plan`"이다.
  - 상태 표시줄 문구는 `⏸ manual mode on`, `⏵⏵ accept edits on`, `⏸ plan mode on`, `⏵⏵ auto mode on`이다.
  - 플랜 승인 선택지는 "Yes, and use auto mode / Yes, manually approve edits / No, keep planning"이다. 첫 번째를 고르면 세션이 Auto 모드로 바뀐다.
- 수정안:
  - 18 표: 4행으로 바꾼다. "일반(Manual) / 편집 자동 승인(Accept edits) / 계획(Plan) / Auto(분류 모델이 대신 검토)". 본문에 "최신 버전은 Auto 모드로 시작한다. 처음 배울 때는 Shift+Tab 한 번으로 Manual로 바꾼다"를 넣는다. "Auto 모드"의 `[확인필요]`는 지운다.
  - 9: 본문 2를 "Shift+Tab을 `⏸ plan mode on`이 보일 때까지 누른다(Auto로 시작했다면 세 번). 또는 프롬프트 앞에 `/plan`을 붙인다"로 바꾼다. 예상 결과의 `[승인하시겠습니까? y/n]`은 세 선택지로 바꾸고, 연수에서는 **"Yes, manually approve edits"** 를 고르게 한다.
  - 25·73: 같은 선택지 안내를 넣는다.
  - 8 노트의 "모드 표시 문구 `[확인필요]`"는 위 문구로 확정한다.

**4-F [필수] hook 오류가 클로드에게 전달되지 않는다. 45번 예상 결과가 부정확하다.** 해당: M7 44(프롬프트·file-box), 45(예상 결과), 42 본문(증거 원칙과 연결).
- 근거(Hooks 문서):
  - 종료 코드가 2가 아닐 때(py_compile 실패 시 1)는 "non-blocking error… the transcript shows a `<hook name> hook error` notice followed by the first line of stderr, prefixed with `Failed with non-blocking status code:`"이다.
  - "Stderr… Claude never sees it… To surface a warning to Claude from a PostToolUse hook, exit 2 instead."
  - macOS에서 직접 실행한 결과, 원본 명령은 종료 코드 1을 냈다. stderr 첫 줄은 `File "...", line 1`이고 "SyntaxError"는 셋째 줄에 있었다.
  - 따라서 사람은 오류 알림 한 줄을 보지만, 클로드는 오류를 모른 채 "완료"라고 말할 수 있다.
- 수정안:
  - 44 프롬프트 끝에 "문법 오류가 있으면 종료 코드 2로 끝나게 해서 클로드도 오류를 보고 고치게 해줘"를 추가한다.
  - file-box 명령 예시를 `jq -r '.tool_input.file_path' | grep '\\.py$' | xargs -r python3 -m py_compile || exit 2`로 바꾼다. macOS에서 실행해 보니 오류 파일은 종료 코드 2와 SyntaxError 전체 출력, 정상 파일과 .md 파일은 종료 코드 0이었다.
  - 45 예상 결과: "hook 오류 알림이 뜨고, 클로드가 오류 내용을 받아 스스로 고친다 = 증거가 클로드에게 돌아간다".
  - 노트에 원본 대비 변경을 적는다.

**4-G [권장]**
- M7 43 제목 "hook이 울리는 네 시점" → "**주요** 네 시점". 공식 이벤트는 SessionStart, UserPromptSubmit, SubagentStop 등 30개 가까이 된다. 원본 표 제목도 "주요 hook 이벤트"다.
- M3 16 막힐 때: 세션 시작 때 `.claude/skills/` 폴더가 없었다면 새 스킬이 자동으로 잡히지 않는다. `/exit` 재시작 대신 `/reload-skills`로 안내한다(Skills 문서: "If you create a top-level skills directory that didn't exist at startup, run `/reload-skills`").
- M4 24: 세션 안에서 `/plugin install`을 입력하면 바로 설치되지 않고 설치 범위를 고르는 패널이 열린다. 막힐 때나 노트에 "패널에서 범위를 고르고 설치"를 적는다.

**프론트매터 키: 통과.**
- 에이전트: `name`·`description` 필수, `tools`(생략 시 전부 상속), `model`(`sonnet`/`opus`/`haiku`. `fable`, `inherit`, 전체 모델 ID도 가능).
- 스킬: `name`, `description`, `disable-model-invocation`, `argument-hint`, `$ARGUMENTS`, SKILL.md 500줄 권장.
- 모두 공식 문서와 일치하고, 원본과 글자까지 같다.

## 5. [확인필요] 판정

### Claude Code
| 원고 위치 | 항목 | 판정 | 근거·조치 |
|---|---|---|---|
| M1 4 | 설치 명령 3종(mac/Linux, PowerShell, CMD) | **확인됨** | setup 문서와 글자까지 일치. `2.1.211 (Claude Code)` 예시도 공식 문서에 있다. 태그 삭제 |
| M1 2, 노트 | 유료 계정 필요(Pro·Max·Team·Enterprise·Console) | 확인됨 | setup 문서 Authenticate 절 |
| M2 8·9, M4 25, M9 73 | 플랜 승인 화면 y/n | **틀림** | 4-E 참조 |
| M2 8, M3 18 | 모드 표시 문구, Shift+Tab 순환 | 확인됨(내용 수정 필요) | 4-E 참조 |
| M3 18 | "Auto 모드" 이름과 동작 | 확인됨 | 이름·설명 맞음. 단 표에 Accept edits가 없고, 기본 시작 모드가 Auto라는 사실이 빠졌다 |
| M3 14 | 같은 세션에서 고친 CLAUDE.md가 즉시 반영되는지 | 미확인 | 공식 문장을 찾지 못했다. 재시작 안내는 안전하므로 유지 |
| M3 16, M5 34 | 새 스킬이 재시작 없이 인식되는지 | 확인됨(조건부) | 스킬은 실시간 반영된다. 단 세션 시작 때 없던 skills 폴더는 `/reload-skills` 필요(4-G) |
| M4 23, MW 78 | `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` | 이름은 확인됨, **플러그인 의존은 틀림** | 4-D 참조 |
| M4 23 노트, MW 78 | 에이전트 팀은 헤드리스(`-p`)에서 안 됨 | 확인됨 | Agent teams 문서: "In non-interactive mode with the `-p` flag… Claude doesn't spawn teammates" |
| M4 24, M9, MW 79 | 마켓플레이스 이름 `harness-marketplace`, 설치 명령 2줄 | **확인됨** | 저장소 `.claude-plugin/marketplace.json`의 `"name": "harness-marketplace"`, README 설치 절 |
| M4 28 | `/harness:evolve` | 확인됨 | README "`/harness:evolve` actually ships" |
| M5 29 | 모델 이름 sonnet/opus/haiku | 확인됨 | `fable`, `inherit`도 있다 |
| M5 31 | `/agents` 대화형 생성·목록 | **틀림**(v2.1.198+) | 4-C 참조 |
| M5 31 | 새 에이전트 파일의 재시작 필요 여부 | 확인됨 | 실시간 반영된다. 단 세션 시작 때 `agents` 폴더가 없었으면 재시작 필요. 기존 막힐 때 문구가 맞으므로 태그만 삭제 |
| M7 43 | hook 이벤트 이름·설정 키 | 확인됨 | 4종 이름·설명과 `hooks > 이벤트 > [{matcher, hooks:[{type:"command", command}]}]` 구조 일치. `Edit\|Write`는 정확 일치 목록으로 유효 |
| M7 44·48 | `xargs -r`의 macOS 동작 | 확인됨(동작함) | macOS xargs 매뉴얼: "-r option for command-line compatibility… does nothing". 직접 실행 확인 |
| M7 48 | `jq` 기본 설치 여부 | 확인됨(macOS 15 이상 기본 포함) / Windows 미확인 | macOS Sequoia부터 `/usr/bin/jq` 포함. Windows는 확인하지 못함. `cp-m7` Windows 판 유지 권장 |
| M7 48 | `python` vs `python3` | 미확인(공식 문장 없음) | 기본 macOS에는 `python3`만 있는 경우가 많다. 44의 "먼저 확인하고 맞춰서" 문장으로 대응되어 있다 |
| M7 48 | Windows 셸 차이 | 확인됨 | Hooks 문서: 기본은 bash(Windows는 Git Bash). Git Bash가 없으면 PowerShell |
| M7 45 | 새 hook이 바로 반영되는지 | 확인됨 | "Direct edits to hooks in settings files are normally picked up automatically". 재시작은 대비책으로만 남김 |

### Firebase
| 원고 위치 | 항목 | 판정 | 근거·조치 |
|---|---|---|---|
| M8 49·59·61·63, MW 78 | Storage Blaze 요건, pricing과 FAQ의 충돌 | **확인됨: Blaze 필요, 충돌 없음** | pricing 페이지 Spark의 Cloud Storage가 "Not applicable"로 바뀌었다. FAQ: Blaze 요건은 2026-02-03 시행, 미업그레이드 시 데이터는 남지만 접근 불가. 충돌 문구와 태그를 모두 지운다. 59 표의 Storage Spark 칸은 "사용 불가" |
| 설계서 공지 2, 5절 6 | "2024-10-30 이후 정책" | **틀림** | FAQ에서 2024-10-30은 "기본 리소스 위치를 더 이상 정하지 않는다"는 변경이다. Blaze 요건은 2026-02-03. 원고(M8)는 이미 사실표를 따랐으므로 수정 불필요 |
| M8 59, 63 | Storage 무료 사용량(appspot 5GB 등, 새 버킷은 US 3개 리전 Always Free) | 확인됨 | FAQ |
| M8 59, 63 | $300 체험 크레딧 | 미확인 | FAQ에 언급이 없다. 슬라이드에서 빼는 것을 권장 |
| M8 59 | Auth 5만 MAU, Firestore 1GiB·읽기 5만·쓰기 2만, Hosting 10GB·360MB/일, Functions Spark 불가 | 확인됨 | pricing 페이지 |
| M8 60 | 예산 알림은 서비스를 멈추지 않음, 지출 한도 4개 제품 | 확인됨 | "Budget alerts do not pause services". 지출 한도: AI Logic, App Hosting, Cloud Functions, Extensions |
| M8 60 | 사용량 및 결제 한국어 메뉴명, 예산 기본 임계값 | 미확인 | 문서에 메뉴 경로와 기본값이 없다. 리허설에서 확인 |
| M8 50 | 프로젝트 만들기 버튼 문구 | 미확인(영문 "Add project" 표기 확인) | Firestore quickstart: "click Add project". 한국어 UI는 리허설에서 확인 |
| M8 50 | Gemini·Analytics 화면 순서 | 미확인 | |
| M8 50, M5 36, 설계서 | 학교 Workspace 계정의 프로젝트 생성 제한 | 미확인 | 학교 관리자 정책에 따라 다르다. "막혀 있을 수 있음" 표현 유지 |
| M8 51 | firebaseConfig 항목 전체 목록 | 미확인 | 일반적인 형태라는 표시 유지 |
| M8 51 | Firebase API 키는 비밀이 아님 | 확인됨(조건부) | api-keys 문서: Firebase 서비스로만 제한된 키라야 하고, 허용 목록에 Generative Language API가 없어야 한다. Gemini API 키는 절대 코드에 넣지 않는다(7-B) |
| M8 53 | 보안(Security) > Authentication, 로그인 방법 탭, Google 사용 설정, 저장 | 확인됨 | google-signin 문서 |
| M8 53 | 프로젝트 지원 이메일 항목 | 미확인 | 문서에 언급이 없다 |
| M8 53 | 승인된 도메인 위치, 2025-04-28 이후 localhost 기본 없음 | **확인됨** | Auth FAQ와 이메일 링크 문서: "In projects created after April 28, 2025… no longer includes localhost… add it in the Settings tab, in Authorized Domains". Google은 운영 프로젝트에 localhost를 쓰지 말라고 권한다. 이 연수는 앱을 만들지 않으므로 "추가하지 않는다"로 정리 |
| M8 53, 65 | Hosting 기본 주소의 승인된 도메인 기본 포함 여부 | 미확인 | |
| M8 55 | Databases & Storage > Firestore, Create database, 위치, 테스트/프로덕션 모드 | 확인됨 | quickstart 단계와 일치. 프로덕션 모드는 "Denies all reads and writes from mobile and web clients" |
| M8 55 | 위치는 생성 후 변경 불가 | **확인됨** | locations 문서: "once you provision a database instance, you cannot change its location" |
| M8 55 | 서울(asia-northeast3) 선택지 | 확인됨 | locations 문서 목록에 있음 |
| M8 55 | 에디션 선택(Standard) 화면 | 미확인(Standard 에디션 존재는 확인) | |
| M8 55 | 테스트 모드 30일 만료 | 미확인 | 현재 quickstart와 보안 규칙 문서에서 문장을 찾지 못했다. "기한이 정해진 임시 규칙"으로 완화 권장 |
| M8 54·61 | 문서 최대 1MiB | **확인됨** | quotas 문서: "Maximum size for a document 1 MiB (1,048,576 bytes)" |
| M8 56 | 규칙 평가의 get/exists가 읽기로 과금 | 확인됨 | rules-conditions 문서: 규칙이 거부해도 읽기 요금이 부과된다 |
| M8 57 | 플레이그라운드 이름·입력 칸, 편집 중 규칙으로 시뮬레이션 | 확인됨 | simulator 문서: 편집기에서 수정 후 Rules Playground → Simulation type `get`, Location, Authentication 켜기 → Provider, 사용자 ID → Run → 편집기 위 배너 |
| M8 57 | 게시(Publish) 버튼 문구 | 미확인 | |
| M8 63 | Databases & Storage > Storage, 업그레이드 화면 흐름 | 미확인(메뉴 그룹은 Firestore와 같은 그룹으로 추정) | 리허설에서 확인 |
| M8 64 | Hosting과 App Hosting의 차이 | 확인됨 | App Hosting은 서버 렌더링 풀스택 웹앱용이고 Blaze 필요("upgrade to the pay-as-you-go Blaze pricing plan to use App Hosting"). Hosting은 정적·단일 페이지 웹을 CDN으로 배포. 한 줄로 추가 가능 |
| M8 65 | `firebase init hosting`, `firebase deploy --only hosting`, web.app·firebaseapp.com | 확인됨 | Hosting quickstart. 질문 순서는 미확인 유지 |
| M8 68 | `firebase init functions`, `firebase functions:secrets:set`, `firebase deploy --only functions`, `defineSecret`·`secrets: [...]` | **확인됨** | functions get-started, config-env 문서. 태그 삭제 |
| M8 68 | Node 20/22 | 미확인 | |
| M8 70 | 프로젝트 삭제 방법 | **확인됨** | Firebase 도움말: 프로젝트 설정 > 일반 > 맨 아래 "프로젝트 삭제", 체크박스 확인. 30일 안에는 Google Cloud 콘솔에서 복구할 수 있다. 70 본문을 이 절차로 채운다 |

## 6. 57번 보안 규칙 문법: 통과
- `rules_version = '2';`, `service cloud.firestore`, `match /databases/{database}/documents`, `match /users/{uid}`, `allow read: if request.auth != null && request.auth.uid == uid;` 모두 문법이 맞다. 중괄호 짝도 맞다.
- 공식 문서 예시 패턴(`request.auth.uid == userId`)과 같다. 잠금 → 거부, test-uid-1 → 허용, test-uid-2 → 거부라는 예상 결과도 맞다.
- 권장: 2단계 입력 문구를 공식 용어로 맞춘다. "Simulation type `get` / Location `/users/test-uid-1` / Authentication 켜기 → Provider 선택 → UID `test-uid-1` → Run". 결과는 편집기 위 배너에서 확인한다.

## 7. 용어·개인정보·보안: 수정필요

**7-A [필수] 58번 원칙 1에 학생이 자기 권한을 올릴 수 있는 경로가 있다.** 해당: M8 58 프롬프트.
- 문제: 원칙 1이 "로그인한 사용자는 자기 문서(users/{uid})만 읽고 **쓸** 수 있다"이다. 그런데 클래스룸 명세(`firebase-classroom-spec`)의 `users/{uid}`에는 `role` 필드가 있다. 이 원칙대로 규칙을 만들면 학생이 자기 문서의 `role`을 "teacher"로 바꿔 교사 권한을 얻을 수 있다. AI 초안이 그대로 이 구멍을 만들 가능성이 높다.
- 수정안: 원칙 1을 "로그인한 사용자는 자기 문서(users/{uid})만 읽을 수 있다. 자기 문서를 고칠 때도 role(교사/학생) 필드는 바꿀 수 없다"로 바꾼다. 노트에 "역할 지정은 사람이 하는 일 = 게이트"를 한 줄 추가한다. 이 사례를 사람이 확인해야 하는 이유로 들면 게이트 실연 효과가 커진다.

**7-B [필수] 51번 본문 "API 키 = 금고 비밀번호"가 firebaseConfig 안의 `apiKey`와 충돌한다.** 해당: M8 51 본문 둘째 줄. 설계서 6절 비유표의 마지막 행도 같다.
- 문제: 참가자는 화면의 firebaseConfig에서 `apiKey`라는 글자를 직접 본다. "API 키는 알려지면 안 된다"는 본문과 정반대로 읽힐 수 있다.
- 수정안:
  - 본문: "firebaseConfig(안에 든 apiKey 포함) = 학교 주소, 알려져도 됨. AI 서비스 키(Gemini 등)·서비스 계정 키 = 금고 비밀번호, 알려지면 안 됨."
  - 노트: "Firebase 키가 안전한 조건은 Firebase 서비스로만 제한되어 있어야 한다는 것. Gemini API 키는 절대 코드에 넣지 않는다(api-keys 문서). 지키는 것은 보안 규칙과 App Check".
  - 50번에서 Gemini in Firebase를 켜는 선택지와 연결해 이 주의를 한 줄 넣는다.

**7-C [권장] 보안**
- M1 5 또는 M3 18: 최신 Claude Code는 Auto 모드로 시작한다(4-E). 개인정보가 있는 폴더에서는 시작하자마자 Shift+Tab으로 Manual 모드로 바꾸라는 안내를 넣는다. 원본 1.9의 "완전 자동 승인 금지" 원칙과 맞추기 위해서다.
- M2 9, M9 73: 플랜 승인 때 "Yes, and use auto mode"를 고르면 세션이 Auto로 바뀐다. 연수에서는 "manually approve"를 고르게 한다.
- 비밀키 노출 경로는 없다. 51, 67, 68에서 AI 키·서비스 계정 키·Secret을 코드·HTML·`.env` 커밋에 넣지 말라고 일관되게 안내한다.

**7-D [권장] 개인정보**
- M8 50: 예시 이름 `classroom-test-본인이름`은 바꾸는 것이 좋다. 프로젝트 ID는 영문 소문자·숫자·하이픈만 되고, `PROJECT_ID.web.app` 같은 공개 주소에 드러난다. "`classroom-test-이니셜`(실명 넣지 않기)"로 바꾼다.
- 나머지는 통과. 2(실제 학생 정보 금지), 13 규칙 4번(개인정보 예시 금지), 36, 40, 62(학생 사진은 올리지 않음), 64·66(공개 폴더 개인정보 확인), 70(실제 학생 계정 미입력 확인)에 안내가 있다.

**7-E [권장] 설명 없이 나온 용어** (처음 나오는 슬라이드 노트나 본문에 한 줄씩 붙인다)
| 슬라이드 | 용어 | 한 줄 설명 예 |
|---|---|---|
| 9 | markdown | 제목·목록을 기호(#, -)로 적는 간단한 글 형식 |
| 16, 34 | 프론트매터(frontmatter) | 파일 맨 위 `---` 사이의 설정 칸 |
| 23(4-D 반영 시 삭제) | 환경변수 | 프로그램에 주는 설정 스위치 |
| 30 | Read, Grep(tools 값) | Read = 파일 읽기, Grep = 파일 속 글자 찾기 |
| 34 | slug | 주제를 파일 이름용 영문으로 바꾼 것 |
| 44 | jq, grep, xargs, py_compile | 풀어 읽기 문장은 있지만 각 단어 뜻은 없다. "jq = 설정 정보에서 파일 이름 꺼내기" 등 괄호 한 줄 |
| 51 | 서비스 계정 키 | 서버가 관리자 권한으로 접속할 때 쓰는 열쇠 파일(JSON) |
| 55 | 에디션(Standard) | 데이터베이스 종류. 기본형 선택 |
| 59 | MAU, GiB, GB-초 | 월간 활성 사용자 수 / 저장 용량 단위 / 함수 실행 시간 × 메모리 |
| 63 | 버킷 | Storage 안의 파일 보관 단위(창고 한 동) |
| 65, 68 | CLI, Node.js | 터미널용 명령 프로그램 / 그 프로그램을 돌리는 실행 환경 |

---

## 출처
- Claude Code: [Advanced setup](https://code.claude.com/docs/en/setup), [Permission modes](https://code.claude.com/docs/en/permission-modes), [Skills](https://code.claude.com/docs/en/skills), [Subagents](https://code.claude.com/docs/en/sub-agents), [Hooks](https://code.claude.com/docs/en/hooks), [Agent teams](https://code.claude.com/docs/en/agent-teams), [Commands](https://code.claude.com/docs/en/commands), [Discover plugins](https://code.claude.com/docs/en/discover-plugins)
- 플러그인: [revfactory/harness README](https://github.com/revfactory/harness), [marketplace.json](https://raw.githubusercontent.com/revfactory/harness/main/.claude-plugin/marketplace.json)
- Firebase: [Storage FAQ](https://firebase.google.com/docs/storage/faqs-storage-changes-announced-sept-2024), [Pricing](https://firebase.google.com/pricing), [Avoid surprise bills](https://firebase.google.com/docs/projects/billing/avoid-surprise-bills), [Firestore quickstart](https://firebase.google.com/docs/firestore/quickstart), [Firestore locations](https://firebase.google.com/docs/firestore/locations), [Firestore quotas](https://firebase.google.com/docs/firestore/quotas), [Rules Playground](https://firebase.google.com/docs/rules/simulator), [Rules conditions](https://firebase.google.com/docs/firestore/security/rules-conditions), [Google sign-in](https://firebase.google.com/docs/auth/web/google-signin), [Auth FAQ](https://firebase.google.com/docs/auth/faq-and-troubleshooting), [API keys](https://firebase.google.com/docs/projects/api-keys), [Functions config-env](https://firebase.google.com/docs/functions/config-env), [Functions get-started](https://firebase.google.com/docs/functions/get-started), [Hosting quickstart](https://firebase.google.com/docs/hosting/quickstart), [App Hosting get-started](https://firebase.google.com/docs/app-hosting/get-started), [Delete your project](https://support.google.com/firebase/answer/9137886)
- jq in macOS: [Hacker News: jq in /usr/bin in Sequoia](https://news.ycombinator.com/item?id=41560170)
