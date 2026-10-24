# 03. 검수 보고서 (content-reviewer)

- 검수일: 2026-10-03
- 대상: `02_writer_M1~M7_slides.md`(새 번호 1~54), `02_engineer_prompts.md`, `02_engineer_rules.md`, `.claude/skills/firebase-classroom-spec/SKILL.md`(members `uid`, classes 문서 이름 = 수업코드 반영본), `01_designer_curriculum.md`
- 방법: 원고·문서 전체 정독, 최종·임시 규칙 본문 정적 검토, 공식 문서(firebase.google.com, MDN, docs.claude.com, npm registry, firebase-tools 소스) 대조, SDK CDN 주소 `curl` 확인
- 참고: `_workspace/reference-app/` 폴더는 현재 **없다**(삭제됨). 그래서 rules 문서 9-1절의 에뮬레이터·로직 테스트 결과, "참고 구현과 글자 단위로 같다(diff)", `rules-check.html`·`sample-material.html` 참고 구현은 모두 지금 재확인할 수 없다.

## 0. 요약

| # | 검증 항목 | 결과 | 수정필요 건수 |
|---|---|---|---|
| 1 | 슬라이드 프롬프트 ↔ `02_engineer_prompts.md` 일치, 파일명·필드명 일관성 | 수정필요 | 7 |
| 2 | 콘솔 메뉴·CLI·SDK·요금제 `[확인필요]` 공식 문서 대조 | 수정필요 | 6 |
| 3 | 시간 합계 180분, 실습 분량 | 수정필요 (합계는 통과, 커리큘럼 문서 낡음·일부 슬라이드 시간 부족) | 3 |
| 4 | 보안(규칙 논리, 비밀키, sandbox) | 수정필요 (5원칙은 규칙 본문에서 성립. 보완 7건) | 7 |
| 5 | 전문 용어·슬라이드 분량 | 수정필요 | 3 |
| 6 | 개인정보 안내 | 통과 (권장 1건) | 0 (+권장 1) |
| 7 | 모듈 간 전제 연속성 | 통과 (문서 낡은 표기 정리 필요) | 2 |
| 합계 | | | **28** |

가장 중요한 5개
1. **[2-1] localhost 승인된 도메인**: 2025-04-28 이후 만든 프로젝트에는 localhost가 기본으로 **없다**(공식 문서). 슬라이드 12는 "없으면 추가"라 동작은 하지만, "있는지 확인" 위주로 쓰여 있고 엔지니어 문서 0-3절은 "기본으로 들어 있다"고 잘못 적었다. 오늘 만드는 새 프로젝트는 모두 해당되므로 반드시 추가 단계로 고쳐야 한다.
2. **[2-2] 콘솔 메뉴 위치 "빌드 묶음" 불일치**: 현재 공식 문서는 `Security > Authentication`, `Databases & Storage > Firestore`로 안내한다. 슬라이드 11·13의 "빌드 묶음 안"은 맞지 않다.
3. **[1-1] 슬라이드 15 프롬프트 코드 블록 안에 `[확인필요: 연수 당일 SDK 버전]` 표시가 들어 있다**: 참가자가 그대로 Claude Code에 붙여넣게 된다. SDK 12.19.0은 오늘 기준 최신이고 주소 4개 모두 HTTP 200으로 확인했으므로 블록에서 빼야 한다.
4. **[4-3] 막힐 때 "임시 규칙을 고쳐 줘" 요청(슬라이드 21·22·23·29)**: 임시 규칙은 이미 해당 동작을 모두 허용한다. 이 요청은 콘솔에 게시되지 않는 로컬 파일을 고치게 하거나 규칙을 더 느슨하게 만들 수 있고, 슬라이드 13 노트("임의로 고치지 않는다")와도 어긋난다.
5. **[2-6]/[1-3] 규칙 검증 근거와 점검 페이지**: 모듈 7에서 `[확인필요]` 3건을 해제한 근거(에뮬레이터 테스트)와 `rules-check.html` 참고 구현이 삭제되어 재확인할 수 없다. 슬라이드 50이 "오늘의 핵심"인데 점검 페이지의 명세는 표 하나뿐이고, 슬라이드 50 복사 프롬프트는 `rules-check.js`를 빠뜨린다.

---

## 1. 프롬프트 일치, 파일명·필드명 일관성 — 수정필요

### 일치 확인 결과
| 슬라이드 | 결과 |
|---|---|
| 5 첫 요청 | 일치 |
| 13 임시 규칙 | 규칙 본문 일치(머리 주석만 줄임, 규칙 줄은 같음). 파일명 `firestore.temp.rules`, 복구 폴더 `firestore.rules` 일치 |
| 14 firebase-config.js 저장 | **엔지니어 문서에 없음** (1-2) |
| 15 로그인 | **불일치** (1-1, 1-2) |
| 16 users + 역할 | 일치(보충 문장 "역할은 처음 한 번만" 반영됨) |
| 17, 18, 26 복구 문장 | 일치(0-2절 문장과 글자 동일) |
| 21, 22, 23 (M3) | 일치(글자 동일). `classes/{수업코드}`, `getDoc`, `joinedAt`·`uid`, `collectionGroup` 모두 반영 |
| 29, 30, 31 (M4) | 일치 |
| 35, 36, 37 (M5) | 일치(35 5·7번, 36 3·4번 merge, 37 4번 반영) |
| 42, 43, 45 (M6) | 일치(42의 1) 보충안·"N은 선택형 문항 수" 반영, 45 과제 1·2 글자 동일, 도식 5칸으로 수정 반영) |
| 48, 49, 50 (M7) | 프롬프트 본문 일치. 50 복사 프롬프트는 1-3 참고 |
| 51 원칙 5 확인 문장 | 일치 |

필드명(`uid`, `joinedAt`, `type`/`text`/`choices`/`answer`, `answers`, `feedback`, `submittedAt`, `title`/`html`/`createdAt`, `name`/`email`/`role`, `teacherUid`/`joinCode`)과 경로는 원고·프롬프트 문서·최종 규칙·명세에서 모두 일치한다. 파일명 `firebase-config.js`, `rules-check.html`, `firestore.temp.rules`도 일치한다.

### 수정필요
- **1-1 [높음] `02_writer_M2_slides.md` 슬라이드 15 프롬프트**: 코드 블록 안 둘째 조건 끝의 `` `[확인필요: 연수 당일 SDK 버전]` ``를 삭제한다. 블록 안 글은 참가자가 통째로 붙여넣는다. 확인 결과(2-4) 12.19.0이 현재 npm 최신이고 공식 문서 예시 버전도 12.19.0이므로, 필요하면 노트에 "연수 당일 아침 강사가 최신 버전 확인"만 남긴다.
- **1-2 [중] `02_engineer_prompts.md` 모듈 2**: (가) 슬라이드 15 프롬프트가 원고와 다르다. 엔지니어 문서는 "아래 firebaseConfig는 firebase-config.js 파일에만 넣고" + 설정값 블록 붙여넣기 방식이고, 원고는 슬라이드 14에서 만든 파일을 "그대로 쓰고 내용은 바꾸지 마 / 설정값을 app.js나 index.html에 다시 쓰지 마" 방식이다. 원고 쪽(14→15 분리)이 최신이므로 엔지니어 문서를 원고 문장으로 바꾼다. (나) 슬라이드 14 프롬프트가 엔지니어 문서 일치표와 본문에 없다. `[신규]`로 추가한다.
- **1-3 [중] `02_writer_M7_slides.md` 슬라이드 50 프롬프트 / `02_engineer_prompts.md` 슬라이드 50**: 엔지니어 문서는 점검 페이지를 "`rules-check.html`(+ 보조 js)", "`rules-check.html`·`rules-check.js`"로 적었는데 복사 프롬프트는 `rules-check.html` 하나만 복사한다. 수정안: "checkpoint-final에 있는 rules-check.html과 rules-check.js(점검 페이지가 쓰는 파일 전부)를 이 폴더에 복사해 넣고 …". 또한 참고 구현이 삭제되었으므로 엔지니어 문서에 점검 페이지의 버튼별 동작(어떤 경로를 어떤 호출로 시도하는지)을 명세로 적어 강사가 다시 만들 수 있게 한다.
- **1-4 [낮음] `02_engineer_prompts.md` 모듈 4**: "25는 `createdAt(서버 시간)`…", "26의 `sandbox` 값 비움…"은 옛 번호다. 29, 30으로 고친다. 일치표의 "6 | 42 | … '총 N문항' 의미 확인 필요"는 원고에서 확정(선택형 문항 수)되었으므로 "확정"으로 바꾼다.
- **1-5 [낮음] `02_writer_M7_slides.md` 슬라이드 49 프롬프트 1번 ignore 목록**: 엔지니어 문서 0-1 공통 조건 7("README는 Hosting 배포 대상에서 뺀다")과 checkpoint-final `firebase.json`(ignore에 README 포함)과 달리 `README.md`가 빠졌다. "firebase.json, firestore.rules, firestore.indexes.json, README.md, samples 폴더, functions 폴더(있으면), 숨김 파일"로 고친다(functions는 심화 과제 후 같은 폴더를 다시 배포할 때 함수 소스가 공개 주소로 올라가는 것을 막기 위함). 엔지니어 문서 49도 같이 고친다.
- **1-6 [낮음] `02_engineer_prompts.md` checkpoint-m4 상태**: "약 90만 바이트 초과 거부"가 들어 있으나 슬라이드 29 프롬프트에는 이 요청이 없다. 같은 문서의 원칙("직전 폴더에서 다음 모듈 프롬프트를 실행했을 때 나와야 하는 결과와 같은 범위")과 어긋난다. 슬라이드 29 프롬프트에 "html이 너무 크면(약 90만 글자 이상) 저장하지 말고 '자료가 너무 큽니다'라고 알려 줘" 한 줄을 넣거나, checkpoint-m4에서 이 기능을 뺀다.
- **1-7 [낮음] `02_writer_M4_slides.md` 가정 7번째 줄·슬라이드 29 노트**: 샘플 파일명이 아직 "`sample-material.html`… 파일명은 `[확인필요]`", "practice-engineer 제공"으로 남아 있다. 엔지니어 문서 0-1b에서 확정되었으므로 `[확인필요]`를 지우고 노트에 "강사 배포 자료 또는 복구 폴더의 `samples/sample-material.html`"을 적는다. 가정 5번째 줄("실제 구조와 다르면 practice-engineer가 알려 주면 수정")도 확정 문장으로 바꾼다.

---

## 2. `[확인필요]` 공식 문서 대조 — 수정필요

### 대조표
| 항목 (슬라이드) | 공식 근거 | 결과 |
|---|---|---|
| 콘솔 주소 `console.firebase.google.com` (8) | firebase.google.com/docs/web/setup | 일치 |
| 프로젝트 만들기 흐름: 이름 → 약관·계속 → Gemini in Firebase(선택) → Google 애널리틱스(선택) → 프로젝트 만들기 (8) | docs/web/setup | 일치(영문). 한국어 버튼 이름은 확인불가 |
| 웹 앱 등록: 웹 아이콘 → 앱 닉네임 → 앱 등록 (9) | docs/web/setup | 일치. "Firebase Hosting도 설정" 체크 칸, CDN/npm 선택 화면은 확인불가 |
| Authentication 메뉴 위치 "빌드 묶음" (11) | docs/auth/web/google-signin: "Security > Authentication" | **불일치** (2-2) |
| 로그인 방법 탭 → Google 사용 설정 → 저장 (11) | docs/auth/web/google-signin | 일치. "프로젝트 지원 이메일" 칸은 확인불가 |
| 승인된 도메인 위치: Authentication > 설정 탭 > 승인된 도메인 > 도메인 추가 (12, 18, 51) | docs/auth/web/email-link-auth, docs/auth/faq-and-troubleshooting | 일치 |
| localhost 기본 포함 여부 (12, 18, 엔지니어 0-3절) | 같은 문서: "In projects created after April 28, 2025, Firebase Authentication no longer includes localhost as an authorized domain by default." | **불일치** (2-1) |
| Firestore 메뉴 위치 "빌드 묶음" (13) | docs/firestore/quickstart: "Databases & Storage > Firestore" | **불일치** (2-2) |
| 데이터베이스 만들기 → 위치 → 모드(테스트/프로덕션) → 만들기 (13) | docs/firestore/quickstart | 일치. 에디션(Standard/Enterprise) 선택 화면 유무는 확인불가 |
| 위치는 만든 뒤 못 바꿈 (13) | docs/firestore/locations: "once you provision a database instance, you cannot change its location setting" | 일치 |
| 서울 `asia-northeast3` (13) | docs/firestore/locations | 일치(권장 리전 결정은 강사 몫) |
| Firestore 생성에 Blaze 필요 여부 (13) | firebase.google.com/pricing: Firestore Standard edition 무료 한도(1 GiB, 읽기 5만/일, 쓰기 2만/일) | 일치(Blaze 불필요). `[확인필요]` 해제 가능 |
| 테스트 모드 공개 범위·기간 (13) | quickstart: "allows anyone to read and overwrite your data" | 공개 범위 일치. 기간(30일) 표현은 확인불가 |
| 규칙 탭 → 게시(Publish) (13) | docs/firestore/security/get-started: "Firestore > Rules tab … click the Publish button" | 일치 |
| 문서 최대 1 MiB(1,048,576바이트) (32) | docs/firestore/quotas | 일치. `[확인필요]` 해제 |
| 규칙 `get()`/`exists()` 요청당 한도 (rules 9-2 #11) | docs/firestore/quotas: 단일 문서·쿼리 요청 10회 | 일치. 최종 규칙의 최대 호출(제출물 update: exists 1 + get 1~2)은 한도 안 |
| SDK 12.19.0 CDN 주소 (15, 45) | docs/web/setup 예시 버전 12.19.0, npm `firebase` latest = 12.19.0, `firebase-{app,auth,firestore,functions}.js` 4개 HTTP 200 (2026-10-03 curl) | 일치 |
| 단일 필드 자동 색인(자료 `createdAt` 정렬, 교사 `teacherUid` where) (30, 23) | docs/firestore/query-data/index-overview: 컬렉션 범위 단일 필드 색인 자동 유지 | 일치. 슬라이드 30 "색인 필요" 막힐 때는 "보통은 나오지 않음"으로 낮춰도 된다 |
| 컬렉션 그룹 조회는 색인 필요 (23) | 같은 문서: "Automatic indexes with collection group scope are not maintained by default" | 일치. 오류 문구 `COLLECTION_GROUP_ASC`의 정확한 표기와 소요 시간은 확인불가 |
| Firebase CLI 설치 `npm install -g firebase-tools` (3) | docs/cli | 일치(Node.js 필요) |
| `firebase login` (49) | docs/cli: 브라우저 페이지가 localhost로 연결 | 일치 |
| `firebase deploy --only hosting` (49) | docs/hosting/quickstart | 일치 |
| `firebase deploy --only firestore` (49) | docs/firestore/security/get-started | 일치 |
| `firebase use <ID>` (49) | docs/cli: 명령 존재 | 명령 존재는 일치. `.firebaserc` 없을 때 동작은 확인불가 |
| 색인 삭제 질문 문구 (49) | firebase-tools 소스 `src/firestore/api.ts`: "The following indexes are defined in your project but are not present in your firestore indexes file … Would you like to delete these indexes? Selecting no will continue the rest of the deployment." (필드 재정의도 같은 형식) | 일치. "아니요(N)" 안내 맞음 |
| 공개 주소 `프로젝트ID.web.app` (1, 49) | docs/hosting/quickstart: web.app, firebaseapp.com 하위 도메인 | 일치. 승인된 도메인 자동 등록 여부(51)는 확인불가 |
| Cloud Functions 배포에 Blaze 필요 (10, 41, 45, 53, 54, 명세) | docs/functions/get-started: "to deploy functions, your project must be on the Blaze pricing plan" | **"필요할 수 있다"는 부정확** (2-3) |
| `firebase functions:secrets:set AI_API_KEY` (45 노트, 엔지니어 45) | docs/functions/config-env | 일치 |
| Functions 지역 `asia-northeast3` (45) | docs/functions/locations: Seoul, 1st·2nd gen, Tier 2 요금 | 일치 |
| Claude Code 설치·요금제 (3) | docs.claude.com setup: 기본 설치는 네이티브 설치(`curl -fsSL https://claude.ai/install.sh \| bash`, Windows PowerShell `irm … \| iex`), npm 설치도 가능. "Claude Code requires a Pro, Max, Team, Enterprise, or Console account. The free claude.ai plan does not include Claude Code access." | 확인됨 → 2-5 |
| Claude Code 실행 `claude` (5) | 같은 문서 | 일치 |
| Claude Code `!` 셸 명령 (49) | docs.claude.com interactive-mode: "Shell mode with ! prefix" | 일치. `firebase login`의 대화형 질문이 `!` 모드에서 끝까지 되는지는 확인불가 |
| `npx --yes http-server -p 5500 -c-1` (15) | npm http-server README: `-p` 포트, "`-c-1` … disable caching" | 옵션 일치. 실제 실행은 확인불가 |
| sandbox `allow-scripts`+`allow-same-origin` 동시 금지 (28, 30, 51) | MDN iframe: "strongly discouraged to use both allow-scripts and allow-same-origin, as that lets the embedded document remove the sandbox attribute" | 일치 |
| 모듈 7에서 해제한 `[확인필요]` 3건(48 원칙 4 구현 일치, 48 원칙 2 feedback 제한, 50 검증 방법) | 근거로 든 `reference-app/tests/rules.test.mjs`가 삭제됨 | **재확인 필요** (2-6) |
| Claude Code 권한 확인 화면 문구(5), 한국어 콘솔 버튼 이름 전반, 프로젝트 ID 편집, 문서 삭제 메뉴(16, 53) | 공식 문서에 화면 문구 없음 | 확인불가 → 강사 리허설 캡처로 대체 |

### 수정필요
- **2-1 [높음] localhost 승인된 도메인**
  - `02_writer_M2_slides.md` 슬라이드 12 본문 2·3번째 줄: "우리 실습 주소인 `localhost`가 목록에 있는지 확인 / 없으면 추가한다" → "새로 만든 프로젝트에는 `localhost`가 기본으로 없다 → '도메인 추가'로 `localhost`를 넣는다". 프롬프트 3단계, 도식(기본 목록에 localhost 동그라미)도 "추가 후 목록" 그림으로 바꾸고 `[확인필요: localhost 기본 포함 여부]`는 지운다. 노트에 "운영 단계에서는 localhost를 지우는 것이 공식 권장"을 한 줄 넣는다(모듈 7 슬라이드 53 현장 적용 체크에도 한 줄).
  - 슬라이드 18 도식 1행의 `[확인필요: … localhost 기본 포함 여부]` 삭제.
  - `02_engineer_prompts.md` 0-3절 "`localhost`는 … 기본으로 들어 있다" → "2025-04-28 이후 만든 프로젝트에는 기본으로 없으므로 슬라이드 12에서 추가한다". `02_engineer_rules.md` 9-2 #4도 같이 고친다.
- **2-2 [높음] 콘솔 메뉴 위치**: `02_writer_M2_slides.md` 슬라이드 11 프롬프트 1단계·도식, 슬라이드 13 프롬프트 1단계·도식의 "'빌드' 묶음 안" → 공식 문서 표기 기준 "왼쪽 메뉴 **보안(Security) > Authentication**", "**데이터베이스 및 스토리지(Databases & Storage) > Firestore**". 한국어 라벨은 확인불가이므로 `[확인필요: 한국어 메뉴 표기]`는 남기고 강사 리허설 캡처를 넣는다. 슬라이드 51 안내 상자 "Firebase 콘솔 > Authentication > 설정 > 승인된 도메인"도 "보안 > Authentication > 설정 탭 > 승인된 도메인"으로 맞춘다.
- **2-3 [중] Functions 요금제 표현**: "Blaze 요금제가 필요할 수 있다"를 "Cloud Functions를 배포하려면 Blaze(종량제) 요금제가 필요하다(공식 문서). 무료 사용량과 AI API 비용은 연수 시점에 확인"으로 바꾼다. 대상: `02_writer_M2_slides.md` 슬라이드 10 노트, `02_writer_M6_slides.md` 슬라이드 41 노트·45 본문 3번째 줄·45 노트, `02_writer_M7_slides.md` 슬라이드 53·54 노트, `02_engineer_prompts.md` 45 주의, `firebase-classroom-spec/SKILL.md` 비밀 정보 원칙 둘째 줄, `01_designer_curriculum.md` 공지·모듈 6.
- **2-4 [낮음] 확인된 항목의 `[확인필요]` 해제**: 슬라이드 13 막힐 때 "Firestore 생성에 요금제 필요 여부"(Spark에서 가능), 슬라이드 15 SDK 버전(1-1과 함께), 슬라이드 32 1MiB, 슬라이드 49 색인 삭제 질문 문구(위 원문 그대로 노트에 적기), 슬라이드 13 위치 변경 불가.
- **2-5 [중] Claude Code 요금제 사전 안내**: `02_writer_M1_slides.md` 슬라이드 3 노트의 `[확인필요: Claude Code 설치 방법·요금제]`를 "Claude Code는 Pro·Max·Team·Enterprise 또는 Console(API) 계정이 필요하고 무료 플랜으로는 쓸 수 없다. 설치는 공식 설치 명령(macOS: `curl -fsSL https://claude.ai/install.sh | bash`)"으로 채우고, 연수 사전 안내문에도 넣는다. 유료 계정 준비 여부는 연수 당일이 아니라 사전 안내 단계에서 걸러야 한다.
- **2-6 [중] 재확인 필요 분류**: `02_writer_M7_slides.md` 원고 작성자 메모의 "해제한 `[확인필요]` … 모두 에뮬레이터 규칙 테스트 통과가 근거" 3건은 근거 파일이 삭제되어 **재확인 필요**로 되돌린다. 검수자가 규칙 본문을 정적으로 읽은 결과(4절)는 세 가지 모두 논리상 성립하지만 실행 근거는 아니다. 같은 이유로 `02_engineer_rules.md` 머리말(참고 코드와 diff 동일), 9-1절 표 전체, `02_engineer_prompts.md` 부록 B 첫 문단을 "당시 확인, 현재 재현 불가"로 고치고, 연수 전 강사 리허설(실제 프로젝트에서 `rules-check.html` 실행)을 필수 항목으로 둔다.

---

## 3. 시간 합계와 실습 분량 — 수정필요

### 합계 검산 (원고 노트 기준)
| 모듈 | 슬라이드별 분 | 합계 | 원고 노트 검산 |
|---|---|---|---|
| M1 (1–6) | 1+3+2+2+5+2 | 15 | 일치 |
| M2 (7–18) | 4+2+3+4+2+2+3+2+4+4+3+2 | 35 | 일치(설명 8 / 실습 27, 옛 30분 대비 +5 설명도 맞음) |
| M3 (19–25) | 3+4+6+5+4+2+1 | 25 | 일치(설명 7 / 실습 18) |
| 휴식 (26) | 10 | 10 | 일치 |
| M4 (27–32) | 2+3+5+5+3+2 | 20 | 일치 |
| M5 (33–39) | 3+3+5+5+4+3+2 | 25 | 일치 |
| M6 (40–46) | 2+2+6+6+6+2+1 | 25 | 일치(설명 7 / 실습 18) |
| M7 (47–54) | 3+4+4+5+4 + 2+2+1 | 25 | 일치(20 + 마무리 5) |
| 합계 | | **180** | 통과. 슬라이드 수 6+12+7+1+6+7+7+8 = 54 통과 |

### 수정필요
- **3-1 [중] `01_designer_curriculum.md` 낡은 값**: 원고가 기준이므로 아래를 고친다.
  - 1절 개요 "휴식 10분, 마무리 10분 포함" → "마무리 5분".
  - 시간 배분 원칙 "고정 확보 20분, 나머지 160분 = 설명 48 / 실습 112" → 고정 15분(휴식 10 + 마무리 5), 나머지 165분. 원고 노트 기준 설명 47 / 실습 118(M1 10/5, M2 8/27, M3 7/18, M4 5/15, M5 6/19, M6 7/18, M7 전반 4/16: 47 개념 3 + 48 설명 1, 나머지 실습).
  - 2절 모듈표 M2 "30 | 8 / 22" → "35 | 8 / 27", M7 "30 (배포·보안 20 + 마무리 10) | 5 / 15 + 마무리 10" → "25 (20 + 마무리 5) | 4 / 16 + 마무리 5", 합계 행, 검산 줄 "15 + 30 + 25 + 10 + 20 + 25 + 25 + 30" → "15 + 35 + 25 + 10 + 20 + 25 + 25 + 25".
  - 3절 시간표: 0:15–0:50 M2, 0:50–1:15 M3, 1:15–1:25 휴식, 1:25–1:45 M4, 1:45–2:10 M5, 2:10–2:35 M6, 2:35–2:55 M7 전반, 2:55–3:00 마무리.
  - 5절 모듈 2 지시사항 "시간 30분(설명 8 / 실습 22)", 슬라이드 구성 안(14번 없음, 11–13 묶음)을 원고의 7–18 구성(14 = firebase-config.js 저장)으로, 모듈 7 "30분 … 마무리 10분", 슬라이드 52 "(10분 시작)"을 5분으로.
- **3-2 [중] 실습 분량이 빠듯한 슬라이드** (원고 자체에 근거가 있는 것만)
  - 슬라이드 49 (4분): 첫 `firebase login`(브라우저 인증 + CLI 질문), `firebase.json` 생성, 규칙·색인·Hosting 배포를 4분 안에 끝내야 한다. 원고 노트도 "첫 배포에서 CLI 로그인 대기가 길어질 수 있다"고 적었고 엔지니어 문서는 Claude Code가 로그인을 대신 끝내지 못할 수 있다고 했다. 수정안: 슬라이드 3 준비물 체크에 "터미널에서 `firebase login` 완료"를 넣고 사전 안내문에 포함, 못 한 사람은 휴식 시간(26)에 하게 한다.
  - 슬라이드 23 (4분): 노트 기준 거의 전원이 색인 오류를 만나고 "1~5분 기다린 뒤 새로고침"이다. 대기 시간이 슬라이드 시간을 다 쓸 수 있다. 수정안: 노트에 "색인을 만드는 동안 슬라이드 24 짝 활동(교사 쪽 가입 확인)을 먼저 진행"을 넣는다. 강사가 연수 전에 강사 프로젝트에서 색인 생성 시간을 재 둔다(엔지니어 checkpoint-m3 점검 항목과 연결).
  - 슬라이드 13 (3분): DB 만들기 + 위치·모드 선택 + 규칙 전문 붙여넣기·게시까지 3분이다. 2-2의 메뉴 혼선이 겹치면 넘친다. 수정안: 규칙 전문은 슬라이드에서 빼고 배포 파일에서 복사하게 하며(5-2), 리허설 캡처를 단계마다 넣는다.
- **3-3 [낮음] 마무리 5분의 노트 분량**: 슬라이드 53 노트(2분)는 개인정보·D9 한계·정리·요금 네 덩어리라 2분 안에 읽기 어렵다. 4-2·4-7 내용까지 더하면 더 길어진다. 상세는 배포 자료(QR, 슬라이드 54)로 넘기고 노트는 3문장으로 줄인다.

---

## 4. 보안 — 수정필요 (5원칙 자체는 규칙 본문에서 성립)

### 규칙 정적 검토 결과 (`02_engineer_rules.md` 5절)
| 확인 내용 | 판정 | 근거(규칙 줄) |
|---|---|---|
| 원칙 1: 미가입 학생의 자료·학습지 읽기 차단 | 성립 | `materials`/`worksheets` `allow read: if isTeacher(classId) \|\| isMember(classId)`. `isMember`는 `members/{me()}` 존재, `members` create는 `uid == me()`라 남의 이름으로 가입 불가 |
| 원칙 2: 학생 간 제출물 열람 | 차단 성립 | `submissions` get은 교사 또는 `uid == me() && isMember`, list는 교사만 |
| 원칙 2: 학생의 feedback 쓰기 | 차단 성립 | create `onlyKeys(['answers','submittedAt'])`, update `changedOnly(['answers','submittedAt'])`. 덮어쓰기로 feedback을 지우면 affectedKeys에 feedback이 들어가 거부. merge 재제출은 통과(D5와 일치) |
| 교사의 답안 수정 | 차단 성립 | 교사 update는 `changedOnly(['feedback'])` |
| 원칙 3: 수업 만들기 | 성립 | create에 `role == 'teacher'`, `teacherUid == me()`, `joinCode == classId`, 형식 `^[A-HJ-NP-Z2-9]{6}$`(0·O·1·I 제외 32자). 같은 코드가 이미 있으면 update로 판정되어 남의 수업은 거부 |
| 원칙 3: 자료·학습지 쓰기 | 성립 | `isTeacher(classId)` = 수업 문서 `teacherUid == me()` |
| role 변경 차단 | 성립 | users update `role == resource.data.role`, delete 규칙 없음(지우고 다시 만들기 불가) |
| 원칙 4: 코드로 get 허용, list 제한 | 성립 | `classes` get `signedIn()`, list `resource.data.teacherUid == me()`(조회 조건이 teacherUid == 나가 아니면 거부) |
| members 컬렉션 그룹 조회 노출 범위 | 본인 문서만 | `{path=**}/members` list `resource.data.uid == me()`. create가 `uid` 필드 = 문서 이름 = 나를 강제하므로 최종 규칙 이후 만든 문서는 본인 것만 걸린다. 같은 수업의 다른 학생 가입 문서는 get(본인·교사)·list(교사)로만 읽힘 |
| `get()`/`exists()` 호출 수 | 한도 안 | 최대 3회, 공식 한도 10회 |
| 원칙 5 sandbox | 성립(화면 쪽) | 슬라이드 30 프롬프트가 값 없는 `sandbox` + `srcdoc` + innerHTML 금지, 슬라이드 31·51에서 재확인. 설명은 MDN과 일치 |
| 비밀키 | 통과 | firebaseConfig만 브라우저, AI 키는 `defineSecret`/`secrets:set`(과제 1 프롬프트), 복구 폴더에 비밀 값 없음(0-1 공통 조건 3), 학생 이름·이메일·uid를 AI에 보내지 않음 |

### 수정필요
- **4-1 [중] 원칙 3 검증 공백**: `rules-check.html` 버튼 3은 "학생 계정으로 수업 만들기"만 시도한다. 원칙 3의 나머지("자료·학습지 작성은 해당 수업 교사만"), 즉 **가입한 학생이 그 수업에 자료·학습지를 쓰는 시도**는 점검하지 않는다. 임시 규칙에서 되던 동작이라 최종 규칙이 실제로 막는지 눈으로 보여 줄 가치가 크다. 수정안: 버튼 6 "가입한 수업에 자료 1건 쓰기 시도 → 막힘(원칙 3)"을 추가하고 슬라이드 50 도식·예상 결과("막힘 6개"), 슬라이드 51 원칙 3 행, 엔지니어 문서 50 표를 함께 고친다. 슬라이드 51 원칙 3 행 문구 "수업 만들기는 그 수업 교사만"도 "수업·자료·학습지 작성은 그 수업 교사만"으로 바로잡는다.
- **4-2 [중] 교사 이메일 노출 범위 안내 누락**: 수업코드를 아는 사람은 누구나 `classes/{코드}`의 `teacherUid`를 읽고, `users` get이 로그인한 사람에게 열려 있으므로 **그 교사의 이름·이메일을 읽을 수 있다**. `02_engineer_rules.md` 6절은 "학생은 앱 안에서 다른 학생의 uid를 알 방법이 없다"만 적었고 교사 쪽은 빠졌다. 수정안: 슬라이드 53 노트 D9 문장에 "수업코드를 아는 사람은 담당 교사의 이름·이메일도 볼 수 있다. 실제 운영에서는 users에 이메일을 저장하지 않거나 교사용 공개 이름만 두는 방식을 검토한다"를 더하고, rules 문서 D9·6절에도 적는다.
- **4-3 [중] 막힐 때 "임시 규칙을 고쳐 달라"는 요청**: 대상 `02_writer_M3_slides.md` 슬라이드 21 막힐 때 (1) "모듈 2에서 쓴 임시 규칙에 맞게 고쳐 줘", 22 막힐 때 (1) "모듈 2 임시 규칙에서 학생이 … 할 수 있게 고쳐 줘", 23 막힐 때 (2) "임시 규칙을 고쳐 줘", `02_writer_M4_slides.md` 슬라이드 29 막힐 때 "임시 규칙에 materials 쓰기를 추가해 줘 … `[확인필요]`". 임시 규칙(7절)은 이 동작을 모두 허용하므로(엔지니어 7절 확인표) 권한 오류의 원인은 규칙 미게시나 로그아웃이다. 참가자 규칙은 콘솔에 붙여넣어 게시한 것이라 Claude Code가 로컬 파일을 고쳐도 반영되지 않고, 규칙을 더 느슨하게 바꿀 위험도 있으며, 슬라이드 13 노트("강사가 임의로 고치지 않는다")와 충돌한다. 수정안(모듈 5 슬라이드 35 방식과 통일): "콘솔 Firestore 규칙 탭에 `firestore.temp.rules`가 게시되어 있는지, 로그인 상태인지 확인한다. 그래도 같으면 오류 메시지를 그대로 붙여넣고 '규칙 파일은 바꾸지 말고 앱 코드에서 원인을 찾아 줘'라고 요청한다."
- **4-4 [낮음] 원칙 4 문구와 실제 규칙의 차이**: 규칙은 "가입 시점"을 구분할 수 없어 코드를 아는 로그인 사용자에게 언제든 get을 허용한다(설계상 불가피, D1). 그런데 슬라이드 47 표 4행은 "수업코드는 가입할 때만 조회", 51 표 4행은 "수업 전체 목록은 못 본다"로 적혀 있다. 수정안: 47 표 4행을 "수업코드를 아는 사람만 그 수업 1건을 찾는다, 전체 목록은 못 본다"로 바꾼다. 명세 원칙 4의 "가입 시점에만" 표현을 그대로 둘지는 리더가 정하되, 규칙으로 강제되는 범위가 "코드를 알 때만"이라는 점을 명세 또는 rules 문서 D1에 한 줄 적는다.
- **4-5 [낮음] users 이름·이메일 위조**: users create/update는 `name`, `email`을 본인이 아무 값이나 쓸 수 있다. 교사 제출현황(슬라이드 37)은 `users/{uid}.name`을 보여 주므로 학생 계정이 다른 학생 이름으로 바꾸면 교사가 혼동할 수 있다. 권장 보완(심화 또는 최종 규칙): create·update에 `request.resource.data.email == request.auth.token.email`을 넣고, 노트에 "제출현황의 이름은 학생이 정한 값"이라고 적는다. 연수 기본 범위를 늘리지 않으려면 rules 문서 한계 목록에만 추가한다.
- **4-6 [낮음] 임시 규칙 기간에 생긴 데이터**: 최종 규칙은 이미 저장된 데이터를 고치지 않는다. 임시 규칙(모듈 3~6)에서는 학생 계정이 수업을 만들 수 있고(엔지니어 7절), 그 계정은 최종 규칙 이후에도 그 수업의 `teacherUid`로 남는다. `uid` 필드 없이 만든 가입 문서, 아무나 쓴 feedback도 남는다. 수정안: 슬라이드 53 "정리" 항목에 "실제 학급용은 연습 데이터를 모두 지운 뒤(또는 새 프로젝트로) 최종 규칙을 먼저 게시하고 시작한다"를 넣는다.
- **4-7 [낮음] 명세 승인 상태 표기 낡음**: members `uid`와 classId = 수업코드는 승인·반영되었는데 아래 문서가 아직 "제안/미승인 시 대안"으로 적혀 있다. `02_engineer_rules.md` 머리말 3번째 줄, 0절 D2 "필요 (제안만, 명세 파일은 수정하지 않음)", 2절 결정 제목과 "승인되지 않으면(대안 B)", 4절 D7 표 "uid는 D2 제안 필드", 5절 규칙 주석 "(uid 필드는 … 명세 변경 제안 항목)", 8절 "승인 시 도식에 uid 추가", 9-2 #10. `02_engineer_prompts.md` M3 머리말·23 제목·부록 A 마지막 행. `02_writer_M7_slides.md` 가정 4번째 줄("승인 전제. 승인되지 않으면…")과 원고 작성자 메모 마지막에서 두 번째 줄("승인 여부를 리더가 정한다"). 모두 "승인·반영됨(2026-10-03)"으로 바꾸고 대안 B는 삭제하거나 부록으로 내린다. 규칙 주석은 참가자가 복사하는 checkpoint-final 파일에 들어가므로 특히 고친다.

---

## 5. 초보자 접근성 — 수정필요

- **5-1 [중] 설명 없이 나온 용어** (`course-slide-authoring` "전문 용어는 처음 나올 때 교실 비유 한 줄")
  - "터미널": 슬라이드 5 프롬프트·예상 결과에 처음 나온다. 노트에 "터미널 = 컴퓨터에 글자로 명령을 내리는 창(교무실 내선 전화)" 한 줄과 여는 방법(macOS: 터미널 앱, Windows: PowerShell)을 넣는다.
  - "Node.js", "Firebase CLI": 슬라이드 3 준비물에 설명 없이 나오고 49 막힐 때·노트에도 설명 없다. 슬라이드 3 노트에 "Node.js = 도구를 돌리는 엔진, Firebase CLI = 터미널에서 Firebase에 올리는 배달 도구"를 넣는다.
  - "개발자 도구": 슬라이드 38 노트, 41 도식·노트. "브라우저 속 데이터를 들여다보는 점검 창(F12)" 한 줄을 38 노트에 넣는다.
  - "srcdoc": 슬라이드 30 본문 "sandbox iframe(srcdoc)". 본문에서는 괄호를 빼고 노트에 "srcdoc = 자료 글을 진열장 안에 직접 넣는 방식"을 적는다.
  - "컬렉션 그룹 조회": 슬라이드 23 노트는 색인만 비유하고 이 말은 설명하지 않는다. "모든 수업의 출석 명단을 한꺼번에 훑어 내 이름표만 찾는 조회" 한 줄을 넣는다.
- **5-2 [낮음] 슬라이드 본문 분량** (규칙: 본문 3줄 이내, 메시지 하나)
  - 슬라이드 28 본문은 4문장(원칙 1, 원칙 5, 유리 진열장 정의, 손댈 수 없다)이다. "원칙 1: 가입한 수업 자료만 읽는다 / 원칙 5: 교사 HTML은 유리 진열장(sandbox iframe)에 넣어 보여 준다 / 보이지만 손댈 수 없다" 3줄로 줄인다.
  - 슬라이드 13은 프롬프트 칸에 콘솔 5단계와 규칙 전문(약 28줄)이 함께 있다. 규칙 전문은 화면에서 빼고 "강사 배포 파일 `firestore.temp.rules`를 통째로 복사" 한 줄 + 노트로 옮긴다(3-2와 연결).
  - 슬라이드 19 본문 3문장은 각 문장이 길다. "수업을 만들면 6자리 수업코드가 생긴다 / 그 코드가 수업 문서 이름이다 / 학생은 코드(교실 열쇠)로 들어온다"로 줄인다.
- **5-3 [낮음] 원고 형식**: 슬라이드 24 유형 "질문"은 `course-slide-authoring`의 유형 목록(개념·실습·데모·정리)에 없다. 조립 단계 파싱이 이 키를 기준으로 하므로 유형 목록에 "질문"을 추가하거나 24를 "실습"으로 바꾼다. M3 슬라이드 21·22·23의 "- 프롬프트: |"(파이프 문자)는 다른 모듈과 형식이 달라 파서가 `|`를 본문으로 읽을 수 있다. "- 프롬프트:"로 통일한다.

---

## 6. 개인정보 안내 — 통과

- 안내 위치: 슬라이드 2(시연 계정 테스트), 3(테스트 계정 원칙·기관 지침), 8, 16(최소 수집 3필드), 17(임시 규칙에서 users 읽기 가능), 24, 31, 36, 37, 42, 44, 46(AI 전달 최소화), 50, 53(최소 수집, 보호자 동의 절차 확인, D9 한계, 테스트 데이터 삭제). 명세 개인정보 절과 일치한다.
- 권장(수정필요 아님): 슬라이드 46 본문 "개인정보는 최소한만 AI에 보낸다"는 과제 1 프롬프트("학생 이름, 이메일, uid는 AI에게 보내지 마")보다 약하다. "이름·이메일은 AI에 보내지 않는다"로 맞추면 메시지가 하나로 정리된다. 4-2(교사 이메일 노출)는 4절에서 수정필요로 셌다.

---

## 7. 모듈 간 전제 연속성 — 통과 (문서 정리 2건)

| 연결 | 확인 결과 |
|---|---|
| M1 → M2 | M2는 M1 폴더(index.html)에서 이어감, 복구는 checkpoint-0. 일치 |
| M2 임시 규칙 → M3~M6 | 7절 규칙이 classes 아래 전체 읽기·쓰기와 `{path=**}/members` 읽기를 허용하므로 M3(수업 생성·코드 1건 읽기·가입·컬렉션 그룹), M4(자료), M5(학습지·제출·users 이름), M6(feedback 저장·읽기) 모두 동작. 일치 |
| M2 role 한 번만 → M7 role 변경 금지 | 슬라이드 16 프롬프트와 최종 규칙 일치 |
| M3 수업 화면 → M4 | 슬라이드 23이 `#/class/{classId}` 수업 화면을 만들고 M4 29·30이 그 화면에 붙인다. 일치 |
| M3 D1·D2 → M7 규칙 | 21·22·23 프롬프트가 `classes/{코드}` getDoc, members `joinedAt`·`uid` 2필드만, 컬렉션 그룹 조회라 최종 규칙의 create `hasAll/onlyKeys`와 맞는다 |
| M4·M5 필드 → M7 규칙 | 자료 `title`·`html`·`createdAt`(서버 시각), 학습지 `title`·`questions` 두 필드만, 제출 `answers`·`submittedAt`만 쓰도록 프롬프트가 지정. 최종 규칙 `onlyKeys`와 맞는다 |
| M5 재제출 병합 → M6 feedback 보존 | 36 프롬프트 4번 merge, 43 교사 `updateDoc` feedback만, 44 막힐 때가 임시/최종 규칙 차이를 정확히 설명. 규칙 정적 검토(4절)와 일치 |
| M6 → M7 | 41 노트 "모듈 7 슬라이드 48에서 적용", 47 표의 처음 만난 곳(20, 28, 34, 41) 모두 새 번호와 일치 |

### 수정필요
- **7-1 [낮음] `02_engineer_rules.md` 옛 번호**: 0절 D2 "M3 슬라이드 19 도식·18·19 프롬프트 수정 필요"의 "18·19"는 옛 번호다(현재 22·23). D2 원고 영향 칸, 8절 표의 "M3 슬라이드 19 도식"(현재도 19이므로 유지)과 구분해 "22·23 프롬프트"로 고친다. 이미 반영된 항목(8절 "필요한 수정" 칸 대부분)은 "반영됨"으로 표시한다.
- **7-2 [낮음] `02_writer_M4_slides.md` 가정**: "모듈 3 결과물에 … 수업 화면이 있다고 가정", "실제 구조와 다르면 practice-engineer가 알려 주면 수정" → M3 슬라이드 23이 수업 화면(`#/class/{classId}`, 제목·교사용 코드·"← 내 수업으로")을 만든다고 확정 문장으로 바꾼다(1-7과 함께).

---

## 출처
- Firebase 웹 설정: https://firebase.google.com/docs/web/setup
- Google 로그인(Security > Authentication, 로그인 방법 탭): https://firebase.google.com/docs/auth/web/google-signin
- localhost 기본 미포함(2025-04-28 이후 프로젝트), 승인된 도메인 위치: https://firebase.google.com/docs/auth/web/email-link-auth , https://firebase.google.com/docs/auth/faq-and-troubleshooting
- Firestore 만들기(Databases & Storage > Firestore, 모드): https://firebase.google.com/docs/firestore/quickstart
- Firestore 위치·서울 리전: https://firebase.google.com/docs/firestore/locations
- 규칙 게시·CLI 배포: https://firebase.google.com/docs/firestore/security/get-started
- 문서 크기·규칙 호출 한도: https://firebase.google.com/docs/firestore/quotas
- 색인 범위: https://firebase.google.com/docs/firestore/query-data/index-overview
- CLI: https://firebase.google.com/docs/cli , Hosting: https://firebase.google.com/docs/hosting/quickstart
- 색인 삭제 질문 원문: https://github.com/firebase/firebase-tools/blob/master/src/firestore/api.ts
- Functions Blaze: https://firebase.google.com/docs/functions/get-started , 비밀 값: https://firebase.google.com/docs/functions/config-env , 지역: https://firebase.google.com/docs/functions/locations
- 요금(Spark 무료 한도): https://firebase.google.com/pricing
- iframe sandbox: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/iframe
- Claude Code 설치·계정: https://docs.claude.com/en/docs/claude-code/setup , `!` 셸 모드: https://docs.claude.com/en/docs/claude-code/interactive-mode
- http-server 옵션, firebase 최신 버전: https://registry.npmjs.org/http-server , https://registry.npmjs.org/firebase/latest
