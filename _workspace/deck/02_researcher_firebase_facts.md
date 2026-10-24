# Firebase 사실 정리표 (교원 연수용)

- 작성일: 2026-10-04 / 작성: firebase-guide-researcher
- 확인 방법: firebase.google.com 공식 문서 조회. 확인하지 못한 항목은 `[확인필요]`.
- 형식: 한 줄 정의 · 교실 비유 · 쓰는 상황 2 · 안 쓰는 상황 1 · 콘솔 단계 · 흔한 오류 · 요금제 참고 · 출처
- 콘솔 메뉴는 문서 기준 이름이다. 실제 화면 캡처 대조는 하지 못했으므로 연수 전 리허설에서 한 번 확인 권장.

## 0. 핵심 요약 (슬라이드 작성자 주의)
1. **Cloud Storage는 이제 Blaze가 필요하다.** 2026-02-03부터 Spark 프로젝트는 Storage 접근을 잃었고 새 기본 버킷도 만들 수 없다. 교실 실습에서 "무료로 파일 업로드"를 전제로 하면 안 된다. 실습은 Storage 없이 Firestore 문서(HTML 문자열)로 설계하는 편이 안전하다. (Firestore 문서 1개 최대 1 MiB 제한은 [확인필요])
2. **Cloud Functions도 Blaze가 필요하다.** Blaze여도 무료 사용량 안에서는 비용이 0일 수 있으나 결제 수단 등록은 필수.
3. **firebaseConfig(웹 API 키 포함)는 비밀이 아니다.** 보안은 보안 규칙이 맡는다. 반면 AI API 키 등은 비밀이며 Functions의 Secret으로 보관한다.
4. **Firestore 테스트 모드는 30일 뒤 만료**, 프로덕션 모드는 처음에 전부 거부.
5. **예산 알림은 비용을 막지 못하고 알려주기만 한다.**

---

## 1. 프로젝트 생성과 웹 앱 등록 (firebaseConfig)
- **한 줄 정의**: Firebase 프로젝트는 앱이 쓰는 모든 기능(로그인, DB 등)을 담는 상자이고, 웹 앱 등록은 그 상자에 우리 웹페이지를 연결해 접속 정보를 받는 일이다.
- **교실 비유**: 학교(프로젝트)를 세우고, 그 안에 "우리 반 웹페이지"의 출입증(설정값)을 발급받는 것.
- **쓰는 상황**: ① 새 클래스룸 앱을 처음 만들 때 ② 같은 프로젝트에 다른 웹 앱(교사용/학생용)을 추가할 때
- **안 쓰는 상황**: 이미 만든 프로젝트에 기능만 추가할 때는 새 프로젝트를 만들지 않는다(기능은 같은 프로젝트에서 켠다).
- **콘솔 설정 단계**
  1. console.firebase.google.com 에 구글 계정으로 로그인
  2. 프로젝트 만들기(추가) 버튼 클릭. 정확한 버튼 문구는 [확인필요] (문서는 "프로젝트 생성 버튼"으로만 기술)
  3. 프로젝트 이름 입력 후 약관 확인 → 계속
  4. (선택) Gemini in Firebase 사용 설정 → 연수에서는 끄거나 기본값 [확인필요: 화면 순서]
  5. (선택) Google Analytics 설정 → 연수 실습에는 불필요하므로 끄는 것을 권장(권장은 작성자 판단)
  6. "프로젝트 만들기(Create project)" 클릭
  7. 프로젝트 개요 페이지에서 **웹 아이콘(`</>`)** 클릭
  8. 앱 닉네임 입력(내부 구분용 이름일 뿐) → **앱 등록(Register app)**
  9. 화면에 나오는 SDK 추가 안내와 `firebaseConfig` 코드를 복사해 앱에 붙여넣기
- **firebaseConfig 구분**
  - 형태: `const firebaseConfig = { apiKey, authDomain, projectId, storageBucket, messagingSenderId, appId, (measurementId) }` — 항목 전체 목록은 문서 본문에서 확인되지 않아 [확인필요]. 위 목록은 일반적으로 알려진 형태.
  - 공개 가능: Firebase 서비스로 제한된 API 키는 "비밀로 취급할 필요가 없고 코드·설정 파일에 포함해도 안전"하다고 공식 문서가 명시. 키는 프로젝트와 앱을 **식별**할 뿐 **권한 부여**는 보안 규칙·IAM·App Check가 한다.
  - 비밀: 서비스 계정 키(JSON), AI API 키, 외부 서비스 비밀번호 등은 코드·HTML·깃에 넣지 않는다.
- **흔한 오류**: 설정값을 비밀이라 오해해 숨기려다 앱이 안 돌아감 / 반대로 보안 규칙 없이 공개해 데이터 노출.
- **요금제 참고**: 프로젝트 생성은 Spark(무료)로 시작.
- **출처**: https://firebase.google.com/docs/web/setup , https://firebase.google.com/docs/projects/api-keys

---

## 2. Authentication (구글 로그인, 승인된 도메인)
- **한 줄 정의**: 접속한 사람이 누구인지 확인해 고유 번호(uid)를 주는 로그인 서비스.
- **교실 비유**: 출석부 확인. 이름표(구글 계정)를 보고 "이 사람은 김OO"라고 확인한다.
- **쓰는 상황**: ① 학생·교사별로 보이는 화면과 권한을 나눌 때 ② 학생 제출물을 본인 것으로 저장할 때
- **안 쓰는 상황**: 누구나 보는 공개 안내 페이지(로그인 불필요).
- **콘솔 설정 단계**
  1. Firebase 콘솔 왼쪽 메뉴 **보안(Security) > Authentication** (영문 UI 기준 문서 표기)
  2. 시작하기(Get started) 후 **로그인 방법(Sign-in method)** 탭 [시작하기 버튼 문구는 확인필요]
  3. **Google** 공급자 선택 → 사용 설정 → 프로젝트 지원 이메일 선택 [지원 이메일 항목은 문서 본문 미확인, 확인필요] → **저장**
  4. 승인된 도메인(Authorized domains) 점검: 문서는 "Authentication 설정의 Authorized domains"로 안내. 정확한 탭 이름(예: 설정 탭 아래)은 [확인필요]
  5. 코드: `signInWithPopup(auth, new GoogleAuthProvider())` (공식 예제)
- **승인된 도메인**: 로그인 팝업을 허용하는 사이트 주소 목록. 개발 중 도메인은 자동 추가되나, 직접 연결한 도메인은 추가해야 한다. Firebase Hosting 기본 주소(`PROJECT_ID.web.app`, `PROJECT_ID.firebaseapp.com`)와 localhost가 기본 포함인지는 이번 조회에서 문서 문장으로 확인하지 못함 [확인필요].
- **흔한 오류**
  - `auth/unauthorized-domain`: 현재 접속 주소가 승인된 도메인에 없음 → 목록에 추가.
  - 로컬 파일을 `file://`로 열어 로그인 시도 → 동작하지 않음 [확인필요: 공식 문장]. Hosting 주소나 localhost 서버 사용 권장.
  - 모바일/일부 브라우저에서 `signInWithRedirect`가 서드파티 저장소 차단으로 실패 → 초보 실습은 `signInWithPopup` 권장(문서가 대안으로 제시, 단 일부 기기 제약 언급).
- **요금제 참고**: 기본 인증은 월간 활성 사용자 5만 명까지 무료(Spark·Blaze 동일). SAML/OIDC는 50명까지.
- **출처**: https://firebase.google.com/docs/auth/web/google-signin , https://firebase.google.com/docs/auth/web/redirect-best-practices , https://firebase.google.com/pricing

---

## 3. Firestore (데이터베이스 만들기, 위치, 모드, 색인)
- **한 줄 정의**: 문서(document)를 컬렉션(collection)에 담아 저장하는 실시간 클라우드 데이터베이스.
- **교실 비유**: 학급 서류함. 서랍(컬렉션) 안에 서류철(문서)이 있고, 서류철 안에 항목(필드)이 적혀 있다.
- **쓰는 상황**: ① 수업·학습지·제출물 저장 ② 교사가 올린 자료를 학생이 실시간으로 보기
- **안 쓰는 상황**: 용량이 큰 파일(영상, 큰 이미지)은 DB보다 파일 저장소(Storage)가 맞다. 다만 Storage는 Blaze 필요(5절).
- **콘솔 설정 단계**
  1. 프로젝트 선택 → 왼쪽 패널 **Databases & Storage > Firestore** (한국어 UI 번역명은 [확인필요])
  2. **Create database(데이터베이스 만들기)** 클릭
  3. 에디션 선택 화면(Standard/Enterprise)이 있는지는 이번 조회에서 Standard Edition 기준 안내만 확인. 연수는 Standard로 진행 [화면 순서 확인필요]
  4. **위치(location)** 선택. 위치 변경 가능 여부는 문서 본문에 명시 없음. 일반적으로 생성 후 변경 불가로 알려져 있으나 [확인필요]. 한국 학생 대상이면 서울(asia-northeast3) 선택지가 목록에 있는지 [확인필요]. 위치를 못 고르는 경우는 프로젝트 기본 Google Cloud 리소스 위치가 이미 정해진 것.
  5. 보안 모드 선택: **테스트 모드** 또는 **프로덕션 모드**
  6. **Create(만들기)** 클릭 (Cloud Firestore API도 자동 사용 설정됨)
- **테스트 모드 vs 프로덕션 모드**
  | 구분 | 테스트 모드 | 프로덕션 모드 |
  |---|---|---|
  | 규칙 | 누구나 읽기·쓰기 허용 | 클라이언트(웹/앱) 접근 전부 거부 |
  | 기간 | 규칙이 30일 후 만료 | 만료 없음 |
  | 용도 | 아주 초기 개발 | 실제 사용(규칙을 직접 작성해야 접근 가능) |
  | 교실 판단 | 연수 첫 체험용으로만. 학생 정보가 들어가면 위험 | 연수에서는 프로덕션 모드로 만들고 4절 규칙을 게시하는 흐름 권장(작성자 의견) |
  - "테스트 모드 규칙이 30일 뒤 만료"는 quickstart 문서에서 확인. 만료 후 동작 상세는 [확인필요].
- **색인(Indexes)**
  - 기본 쿼리에 필요한 색인은 자동 생성된다. 여러 필드를 조합한 쿼리(복합 쿼리)에서 범위 조건 등이 있으면 직접 만드는 **복합 색인**이 필요할 수 있다.
  - 콘솔 위치: **Databases & Storage > Firestore > Indexes 탭**.
  - 가장 쉬운 방법: 색인이 없어 쿼리가 실패하면 **오류 메시지에 색인 생성 링크**가 포함된다. 링크를 열어 필드를 확인하고 생성 → 빌드 완료까지 대기.
  - 컬렉션 그룹 색인: 같은 이름의 하위 컬렉션 전체를 한 번에 조회할 때 쓰는 범위 옵션. 우리 명세의 `members` 컬렉션 그룹 조회('내가 가입한 수업')가 해당하며 색인 1개가 필요(명세 기준). 컬렉션 그룹 쿼리의 단일 필드 색인 설정 정확한 메뉴(예외 추가 등)는 [확인필요].
- **흔한 오류**: `The query requires an index` (링크 클릭으로 해결) / `Missing or insufficient permissions` (보안 규칙 거부) / 테스트 모드 30일 경과 후 접근 거부 [후자 확인필요].
- **요금제 참고**: Standard Edition 무료 한도 1 GiB 저장, 하루 읽기 5만, 쓰기 2만 (Spark). Blaze에서도 같은 무료 한도 후 종량 과금.
- **출처**: https://firebase.google.com/docs/firestore/quickstart , https://firebase.google.com/docs/firestore/query-data/indexing , https://firebase.google.com/pricing

---

## 4. 보안 규칙 (Firestore)
- **한 줄 정의**: "누가 어떤 데이터를 읽고 쓸 수 있는지"를 적은 문 열쇠 규칙표.
- **교실 비유**: 교무실 문의 출입 규정. 학생은 자기 서류철만, 교사는 자기 반 서류철 전체를 열 수 있다.
- **쓰는 상황**: ① 학생이 다른 학생의 제출물을 못 보게 할 때 ② 교사만 수업·자료를 만들게 할 때
- **안 쓰는 상황**: 없다. Firestore를 쓰면 항상 필요(웹 설정값이 공개이기 때문).
- **콘솔 설정 단계**
  1. **Databases & Storage > Firestore > Rules 탭**
  2. 규칙 편집기에 규칙 작성(또는 Claude Code가 만든 규칙 붙여넣기)
  3. **Rules Playground(규칙 플레이그라운드)**: 작업 유형(get/create/update/delete), 문서 경로, 로그인 상태를 지정해 **Run** → 허용/거부 확인. 주의: 시뮬레이션은 **편집기 안 규칙**으로 실행되며 게시된 규칙이 아님.
  4. **게시(Publish)** [버튼 문구 확인필요]. 반영에는 최대 1분 소요.
  - CLI 방법: `firebase init firestore` → `.rules` 파일 편집 → `firebase deploy --only firestore`(또는 `firestore:rules`). CLI 배포는 콘솔 규칙을 **덮어쓴다**.
- **우리 클래스룸 규칙 원칙**(spec 기준): 학생은 가입한 수업 자료만 / 본인 제출물만 / 작성은 해당 수업 교사만 / 수업 목록 전체 열람 금지 / 코드 조회는 가입 시점만.
- **흔한 오류**: `request.auth != null`만 검사(로그인만 하면 전부 허용) — 공식 문서가 위험 사례로 명시 / 규칙 수정 후 바로 반영 안 됨(최대 1분) / 규칙 문법 오류로 게시 실패.
- **요금제 참고**: 규칙 자체는 무료 기능. 규칙 평가를 위한 문서 조회(get/exists)는 읽기로 계산될 수 있음 [확인필요].
- **출처**: https://firebase.google.com/docs/firestore/security/get-started , https://firebase.google.com/docs/firestore/security/insecure-rules

---

## 5. Cloud Storage for Firebase
- **한 줄 정의**: 이미지·PDF·영상 같은 파일을 올리고 내려받는 클라우드 파일 보관함.
- **교실 비유**: 학급 자료실 사물함. 큰 파일을 보관한다.
- **쓰는 상황**: ① 교사가 PDF·이미지·영상 수업자료 업로드 ② 학생이 사진 과제 제출
- **안 쓰는 상황**: 짧은 텍스트(문항, 답안, HTML 문자열)는 Firestore 문서에 두면 충분. 이번 클래스룸 실습은 이 방식을 우선 권장(결제 수단 불필요).
- **현재 요금제 요건(중요)**
  - Storage 사용에는 **Blaze(종량제) 요금제 필요**. 2026-02-03부터 적용: Spark 프로젝트는 기존 버킷 포함 Storage 읽기/쓰기 접근 상실(데이터는 남아 있고 업그레이드 시 복구), 새 기본 버킷도 Blaze에서만 생성 가능.
  - 무료 사용량은 Blaze에서도 계속 제공: 기존 `*.appspot.com` 기본 버킷은 5 GB 저장, 하루 1 GB 다운로드, 일 2만 업로드, 일 5만 다운로드. 새 버킷(`PROJECT_ID.firebasestorage.app`)은 Google Cloud Storage "Always Free"(US-CENTRAL1, US-EAST1, US-WEST1 한정) 적용, 다른 리전은 일반 요금.
  - 신규 사용자는 $300 무료 체험 크레딧 대상일 수 있음(문서 표기). 교원 연수 참가자 계정에 적용되는지는 [확인필요].
  - pricing 페이지에는 Spark Storage 5GB 무료가 표기되어 있어 위 FAQ와 충돌. **FAQ(2026-02-03 요건)를 최신으로 간주**, 표기 불일치는 [확인필요].
- **콘솔 설정 단계**
  1. **Databases & Storage > Storage**
  2. **Get started(시작하기)** 클릭 (Blaze 업그레이드 요구 화면이 먼저 나올 수 있음 [확인필요])
  3. 버킷 **위치** 선택
  4. 보안 규칙 설정(개발용 공개 접근 옵션이 있으나 연수 중 학생 파일에는 사용하지 않는다)
  5. 완료 후 웹 코드에서 `getStorage(app, 'BUCKET_NAME')`
- **흔한 오류**: Spark 프로젝트에서 접근 불가/버킷 생성 불가(Blaze 필요) / 규칙 미설정으로 업로드 거부 / 버킷 이름 혼동(`appspot.com` vs `firebasestorage.app`).
- **요금제 참고**: 출시 전 권장 점검 항목으로 App Check, 예산 알림, 사용량 대시보드 확인을 문서가 안내.
- **출처**: https://firebase.google.com/docs/storage/web/start , https://firebase.google.com/docs/storage/faqs-storage-changes-announced-sept-2024

---

## 6. Hosting (firebase-tools로 배포)
- **한 줄 정의**: 만든 웹페이지를 인터넷 주소로 공개해 주는 서비스(CDN, 기본 HTTPS).
- **교실 비유**: 학급 게시판에 작품을 붙여 모두가 볼 수 있게 하는 것.
- **쓰는 상황**: ① 학생들이 링크로 접속하는 클래스룸 앱 공개 ② 수정 후 다시 배포해 즉시 반영
- **안 쓰는 상황**: 나 혼자 로컬에서 테스트만 할 때(브라우저에서 파일 열기·로컬 서버로 충분).
- **설정 단계 (터미널)**
  1. Node.js 설치 후 `npm install -g firebase-tools` (Firebase CLI 설치. 설치 명령은 Functions 문서에서 확인)
  2. `firebase login` (브라우저에서 구글 계정 인증)
  3. 프로젝트 폴더에서 `firebase init hosting`: 연결할 Firebase 프로젝트 선택 → 공개 폴더(public directory, 기본 `public`) 지정 → 단일 페이지 앱 rewrite 여부 등 질문에 답함. 질문 순서와 문구는 CLI 버전에 따라 달라질 수 있음 [확인필요]
  4. `firebase.json`, `.firebaserc`, 기본 `index.html`/`404.html` 생성됨
  5. 공개 폴더에 웹 파일(`index.html` 등) 두기
  6. `firebase deploy --only hosting`
  7. 배포 후 `PROJECT_ID.web.app`, `PROJECT_ID.firebaseapp.com` 으로 접속
- **흔한 오류**: 로그인 안 된 상태에서 배포 / 공개 폴더 안에 `index.html` 없음(기본 안내 페이지가 뜸) / 배포 주소를 승인된 도메인에 추가하지 않아 `auth/unauthorized-domain`(기본 주소는 이미 포함 여부 [확인필요]) / 같은 터미널의 잘못된 프로젝트 선택(`.firebaserc` 확인).
- **요금제 참고**: 저장 10 GB, 전송 하루 360 MB 무료(Spark, Blaze 동일 무료 한도). 사용자 지정 도메인은 선택 사항.
- **출처**: https://firebase.google.com/docs/hosting/quickstart , https://firebase.google.com/pricing

---

## 7. Cloud Functions (Blaze 요건, 비밀 값 관리)
- **한 줄 정의**: 서버를 직접 두지 않고, 필요할 때만 실행되는 서버 쪽 코드를 올려 두는 서비스.
- **교실 비유**: 교무실에 맡겨 둔 "대리 처리 담당 선생님". 학생 화면(브라우저)이 직접 못 하는 일(AI 호출 등)을 대신해 준다.
- **쓰는 상황**: ① 학생 답안을 AI에 보내 맞춤 피드백 생성(API 키를 서버에만 보관) ② 제출 시 자동으로 후처리(문서 변경 시 실행되는 트리거)
- **안 쓰는 상황**: 단순 저장·조회는 Firestore와 보안 규칙만으로 충분.
- **요금제 요건**: 함수 **배포에는 Blaze 필요**(공식 문서 확인). 2세대 무료 사용량(Blaze): 월 200만 호출, 40만 GB-초. Spark에서는 해당 없음.
- **설정 단계**
  1. 콘솔에서 Blaze로 업그레이드(결제 수단 등록) 후 예산 알림 설정(8절)
  2. Node.js 20 또는 22 + `npm install -g firebase-tools` (문서상 완전 지원 버전)
  3. 프로젝트 폴더에서 `firebase init functions` (언어 선택: JavaScript/TypeScript 등 질문은 [확인필요])
  4. 웹에서 부르는 함수는 callable(`onCall`) 사용: Firebase Auth 토큰이 자동 전달되어 `request.auth`로 로그인 사용자 확인 가능
  5. `firebase deploy --only functions`. 배포 명령 자체는 이번 문서 본문에서 문장으로 확인하지 못함 [확인필요: 일반적으로 알려진 명령]
- **비밀 값 관리**
  - 권장 방식은 **매개변수화된 구성(Parameterized configuration)**. 유형에 Secret 포함. Secret 값은 **Cloud Secret Manager**에 저장되고 **개별 함수에 바인딩**해야 쓸 수 있다.
  - 코드: `defineSecret('이름')` 로 선언 후 함수 옵션에 `secrets: [...]` 바인딩 (secrets 옵션 형식은 [확인필요: 이번 조회에서 코드 예시 미확인]).
  - 값 입력: `firebase functions:secrets:set 이름` [확인필요: 이번 조회에서 명령어 문장 미확인].
  - 일반(비밀 아닌) 설정은 `functions/.env` 파일.
  - 옛 방식 `functions.config()`는 deprecated(v6.0.0), 2027년 3월 중단 예정 → **연수 자료에서 사용하지 않는다**.
  - Secret 값은 브라우저 코드, HTML 자료, `.env` 커밋 등에 넣지 않는다.
- **흔한 오류**: Blaze 아님으로 배포 거부 / 필요한 매개변수·Secret 값이 없으면 CLI가 배포를 막음 / Node 버전 불일치 / Secret을 함수에 바인딩하지 않아 런타임에 값이 비어 있음.
- **요금제 참고**: 무료 한도 초과 시 종량 과금. 사용량 상한을 거는 "지출 한도(Spend cap) 예산"을 Cloud Functions에 적용 가능(8절). AI 호출 비용은 별도(AI 제공업체 요금)이며 [확인필요: 연수에서 사용할 AI 서비스 확정 후].
- **출처**: https://firebase.google.com/docs/functions/get-started , https://firebase.google.com/docs/functions/config-env , https://firebase.google.com/docs/functions/callable , https://firebase.google.com/docs/functions/2nd-gen-upgrade

---

## 8. 요금제 (Spark / Blaze)와 예산 알림
- **한 줄 정의**: Spark는 무료 요금제, Blaze는 쓴 만큼 내는 종량제(무료 한도는 Blaze에도 포함).
- **교실 비유**: Spark = 학교 지급 소모품 한도 안에서만 사용. Blaze = 법인카드 연결, 한도 안은 무료지만 넘으면 청구.
- **공식 이름**: "No-cost (Spark plan)", "Pay as you go (Blaze plan)".
- **Blaze가 필요한 것(이번 조사 기준)**: Cloud Functions(배포), Cloud Storage(2026-02-03부터). 이 밖에 App Hosting, Cloud SQL 등. 기본 Authentication, Firestore, Hosting은 Spark에서 사용 가능.
- **무료 한도 비교(문서 표기)**
  | 기능 | Spark | Blaze |
  |---|---|---|
  | Authentication(기본) | 월 5만 MAU | 동일 |
  | Firestore Standard | 1 GiB, 읽기 5만/일, 쓰기 2만/일 | 동일 무료 한도 후 종량 |
  | Storage | 5GB, 1GB/일 다운로드 (표기이나 5절 요건과 충돌, [확인필요]) | 5GB 저장, 월 100GB 다운로드 표기 |
  | Hosting | 10 GB 저장, 360 MB/일 전송 | 동일 무료 한도 |
  | Functions | 사용 불가 | 월 200만 호출, 40만 GB-초 |
- **예산 알림 설정**
  1. 콘솔 **설정(Settings) > Usage and billing(사용량 및 결제)** 에서 결제·사용량 확인 [한국어 메뉴명 확인필요]
  2. Blaze 업그레이드 시 알림 전용 예산(Alerts-only budget)이 **자동으로 제안**됨
  3. 금액과 알림 임계값(예: 50%, 90%, 100%)을 정하면 이메일 발송 [임계값 기본값 확인필요]
  - 예산 유형: ① **알림 전용**: 이메일만 발송, 서비스는 멈추지 않음 ② **지출 한도(Spend cap)**: Firebase AI Logic, App Hosting, Cloud Functions, Extensions에 한해 100% 도달 시 해당 서비스를 그 달 남은 기간 중지
  - 핵심 문구(공식): "Budget alerts do **not** pause services."
  - Firestore·Storage·Hosting에는 지출 한도를 걸 수 없다(문서 기준, 나열된 제품에 미포함).
  - 각 제품(Authentication, Firestore, Storage, Functions, Hosting) 사용량 대시보드가 있음.
  - 테스트는 Local Emulator Suite로 하면 실험 코드로 인한 뜻밖의 비용을 피할 수 있다(Functions, Firestore, Realtime Database 대상).
- **연수 운영 권고(작성자 의견)**: 참가자 개인 계정에 결제 수단 등록이 부담될 수 있으므로, Blaze가 필요한 단계(Functions, Storage)는 ① 강사 시연 ② 선택 실습으로 분리하고 Spark만으로 완성되는 경로(Auth + Firestore + Hosting)를 필수 실습으로 두는 안을 검토.
- **출처**: https://firebase.google.com/pricing , https://firebase.google.com/docs/projects/billing/avoid-surprise-bills

---

## 9. 선택표: 교실 상황 → 기능
| 교실 상황 | 고르는 기능 | 이유 | 요금제 |
|---|---|---|---|
| "누가 접속했는지 알고 싶다 / 학생별로 화면을 나누고 싶다" | Authentication(구글 로그인) | 고유 번호(uid)로 사람을 구분 | Spark |
| "수업을 만들고 학생이 코드로 가입하게 하고 싶다" | Firestore + 보안 규칙 | 수업·가입 기록 저장, 규칙으로 가입 시점 조회만 허용 | Spark |
| "학생이 자기 제출물만 보고 남의 것은 못 보게 하고 싶다" | 보안 규칙 | uid 비교로 본인 문서만 허용 | Spark |
| "웹 학습지를 만들고 답안을 모으고 싶다" | Firestore | 문항/제출 문서 저장, 실시간 확인 | Spark |
| "짧은 HTML 수업자료를 올리고 싶다" | Firestore(문서에 HTML 저장) | 결제 수단 없이 가능. 크기 한도 [확인필요] | Spark |
| "PDF·이미지·영상 같은 큰 파일을 올리고 싶다" | Storage | 파일 전용 보관함 | Blaze 필요 |
| "만든 앱을 학생에게 링크로 공개하고 싶다" | Hosting | `web.app` 주소로 배포 | Spark |
| "AI로 제출 답안에 맞춤 피드백을 달고 싶다(API 키 숨김)" | Cloud Functions + Secret | 서버 쪽에 키 보관 | Blaze 필요 |
| "내가 가입한 수업 목록을 모아 보고 싶다" | Firestore 컬렉션 그룹 조회 + 색인 | `members` 전체 조회에 색인 필요 | Spark |
| "비용이 갑자기 나올까 걱정된다" | 예산 알림 (+ Functions 지출 한도) | 알림 전용은 중지 못함 | Blaze 업그레이드 시 설정 |
| "수업 전 연습으로 안전하게 테스트하고 싶다" | Local Emulator Suite | 실제 비용·데이터 영향 없음 | 무료 |
| "친구 계정 없이 혼자 먼저 해 보고 싶다" | Authentication(테스트 계정) + 프로덕션 모드 Firestore | 실제 학생 정보 사용 금지 | Spark |

---

## 10. 출처 목록
- https://firebase.google.com/docs/web/setup
- https://firebase.google.com/docs/projects/api-keys
- https://firebase.google.com/docs/auth/web/google-signin
- https://firebase.google.com/docs/auth/web/redirect-best-practices
- https://firebase.google.com/docs/firestore/quickstart
- https://firebase.google.com/docs/firestore/query-data/indexing
- https://firebase.google.com/docs/firestore/security/get-started
- https://firebase.google.com/docs/firestore/security/insecure-rules
- https://firebase.google.com/docs/storage/web/start
- https://firebase.google.com/docs/storage/faqs-storage-changes-announced-sept-2024
- https://firebase.google.com/docs/hosting/quickstart
- https://firebase.google.com/docs/functions/get-started
- https://firebase.google.com/docs/functions/config-env
- https://firebase.google.com/docs/functions/callable
- https://firebase.google.com/docs/functions/2nd-gen-upgrade
- https://firebase.google.com/pricing
- https://firebase.google.com/docs/projects/billing/avoid-surprise-bills

## 11. [확인필요] 모음 (연수 전 콘솔 실화면 확인 권장)
1. 프로젝트 만들기 버튼의 한국어 문구, Gemini/Analytics 단계 순서
2. Authentication 시작하기 버튼, 지원 이메일 항목, Authorized domains의 정확한 탭 위치와 기본 포함 도메인
3. Firestore 에디션 선택 화면 유무, 서울 리전 선택 가능 여부, 위치 변경 가능 여부, 테스트 모드 만료 후 동작
4. 컬렉션 그룹 단일 필드 색인 설정 메뉴
5. 규칙 "게시" 버튼 문구, 규칙 평가 시 읽기 과금 여부
6. Storage: Blaze 업그레이드 화면 흐름, pricing 페이지(Spark 5GB 표기)와 FAQ(2026-02-03 요건)의 불일치, 연수 계정의 $300 체험 크레딧 적용 여부
7. Functions: `firebase deploy --only functions`, `firebase functions:secrets:set`, `secrets` 옵션 코드 예시 문장 확인
8. Usage and billing 한국어 메뉴명, 예산 기본 임계값
9. Firestore 문서 크기 한도(1 MiB 일반 지식, 공식 문장 미확인)
10. `file://`로 연 페이지에서 구글 로그인 불가 여부의 공식 문장
