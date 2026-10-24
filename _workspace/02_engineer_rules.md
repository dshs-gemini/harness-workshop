# 02. 보안 규칙과 설계 결정 (practice-engineer)

> 기준: `firebase-classroom-spec` 데이터 모델·보안 원칙 5개, `01_designer_curriculum.md`, `02_writer_M1~M7_slides.md`
> 범위: 이 문서는 **연수 교재용 설계 문서**다. 규칙 전문은 이 문서 5절(최종)과 7절(임시)에 그대로 실었으므로 이 문서만으로 강사가 규칙 파일을 준비할 수 있다. 강사가 만들 파일 목록은 `02_engineer_prompts.md` 0-0절에 모았다.
> 참고 구현: 예전 `_workspace/reference-app/`의 규칙 파일과 이 문서 규칙이 글자 단위로 같다고 적었으나(당시 diff 확인), 그 폴더가 삭제되어 **현재 재현 불가**다. 이 문서의 5절·7절 본문이 유일한 기준이다.
> 명세 상태: D1(수업 문서 이름 = 수업코드)과 D2(members `uid` 필드)는 **승인·반영됨(2026-10-03)**. `.claude/skills/firebase-classroom-spec/SKILL.md`에 들어가 있다.
> 검증 상태는 문서 맨 끝 9절에 따로 적는다. 당시 확인했으나 지금 재확인할 수 없는 항목("재확인 필요"), 검수자가 규칙 본문을 논리 검토한 결과, 실제 Firebase 프로젝트에서만 확인할 수 있는 항목("미검증")을 구분한다.

---

## 0. 결정 요약 (원고·검수자가 먼저 볼 표)

| # | 항목 | 결정 | 명세 변경 | 원고 영향 |
|---|---|---|---|---|
| D1 | 수업코드 조회(원칙 4) | **수업 문서 이름(classId) = 수업코드(joinCode)**. 학생은 `classes/{입력한 코드}` 문서 1건만 `get`. 규칙에서 `get`은 로그인한 사람에게 허용, `list`는 `teacherUid == 내 uid`인 수업만 허용 | 없음 (joinCode 필드는 그대로 저장, 값이 문서 이름과 같을 뿐) | M3 슬라이드 21·22 프롬프트 수정 필요, M7 슬라이드 48 원칙 4 문장 보완 |
| D2 | 학생 "내가 가입한 수업" 목록 | `members/{uid}`에 **`uid` 필드 1개 추가**(값 = 문서 이름과 같은 uid) 후 컬렉션 그룹 조회 `collectionGroup('members').where('uid','==',내 uid)` + 컬렉션 그룹 단일 필드 색인 1개 | **승인·반영됨(2026-10-03)** | M3 슬라이드 19 도식, 22·23 프롬프트 (반영됨) |
| D3 | 수업 만들기 권한(원칙 3) | 수업 **만들기(create)만** `users/{uid}.role == 'teacher'`를 확인하고 role은 처음 저장 뒤 바꿀 수 없게 막는다. 수업이 생긴 뒤 수정·삭제·자료·학습지·제출물 권한은 모두 `teacherUid`로 판정 | 없음 | M7 슬라이드 48 프롬프트의 "role 값으로 권한을 판단하지 마" 문장 수정(prompts 문서 M7, 반영됨) |
| D4 | 학생의 feedback 쓰기 금지 | 학생의 update는 바뀐 필드가 `answers`, `submittedAt`뿐일 때만 허용(`diff().affectedKeys().hasOnly`). 교사는 `feedback`만 바꿀 수 있다 | 없음 | M7 슬라이드 48 원칙 2 문장 그대로 사용 가능 |
| D5 | 재제출 시 feedback 유지 | 학생 제출은 `setDoc(ref, {answers, submittedAt}, { merge: true })`(병합 저장). 병합하지 않고 덮어쓰면 feedback이 지워지는 변경이 되어 **규칙이 거부**한다(안전장치) | 없음 | M5 슬라이드 36 프롬프트 4번에 "병합 저장" 문장 추가 권장, M6 슬라이드 44 막힐 때 문구 보완 |
| D6 | 정답 저장 | **M5 원고 가정 A 채택**: 정답은 `questions[i].answer`에 함께 저장. 학생이 문항 문서를 읽을 수 있으므로 개발자 도구로 정답을 볼 수 있다는 한계를 그대로 둔다 | 없음 | M5·M6 원고와 일치. 단 `answer` 값 형식(0부터 세는 번호) 명시 필요 |
| D7 | 문항·답안 필드 | 아래 4절 표로 확정 | 없음 (명세에 세부 정의 없음 → 이 문서가 기준) | M5 슬라이드 35 프롬프트 5번 문장 보완 |
| D8 | 임시 규칙(M2 슬라이드 13) | 로그인한 사람만, users는 본인만 쓰기, classes 아래는 로그인하면 모두 읽기·쓰기 + 컬렉션 그룹 members 읽기 | 없음 | 슬라이드 13 5단계에 7절 규칙 파일명(`firestore.temp.rules`) 기재(원고 반영됨) |
| D9 | users 읽기 | 로그인한 사람은 uid를 아는 사용자 문서 1건을 `get` 가능, 목록(`list`)은 금지. 교사 제출현황에서 학생 이름을 보여 주기 위해서다. 수업코드를 아는 사람은 `teacherUid`로 담당 교사의 이름·이메일도 읽을 수 있다(6절) | 없음 | 개인정보 한계로 M7 슬라이드 53 노트에 한 줄 추가 권장(교사 이메일 포함) |

---

## 1. D1 수업코드 조회: "코드 = 문서 이름" 방식

### 문제
원칙 4는 "수업코드 조회는 가입 시점에만, 수업 목록 전체 열람은 막는다"이다. M3 원고는 `classes`에서 `joinCode == 입력값`으로 1건을 찾는 **where 조회**를 가정했다. 그런데 Firestore 규칙에서 where 조회는 `list`(목록 조회) 권한으로 판정된다. 규칙은 "조회에 joinCode 조건이 붙었는지"를 확인할 방법이 없다. `limit 1`만 강제하면 정렬 + 다음 페이지 방식으로 한 건씩 넘기며 전체 수업을 훑을 수 있다. 결국 where 조회를 학생에게 허용하는 순간 원칙 4의 "전체 목록 차단"을 규칙으로 보장할 수 없다.

### 결정
- 교사가 수업을 만들 때 **문서 이름(classId)을 수업코드로 만든다.** `joinCode` 필드에도 같은 값을 저장한다(명세 필드 그대로).
- 학생은 코드를 입력하면 `classes/{코드}` 문서 1건만 읽는다(`getDoc`). 
- 규칙:
  - `allow get: if signedIn();` → 문서 이름(코드)을 알아야만 읽을 수 있다.
  - `allow list: if signedIn() && resource.data.teacherUid == me();` → 목록 조회는 "내가 교사인 수업"만. 학생이 `classes` 전체를 조회하면 거부된다.
  - `create`에서 `request.resource.data.joinCode == classId`와 코드 형식(`^[A-HJ-NP-Z2-9]{6}$`, 0·O·1·I 제외 32글자 6자리)을 강제한다.
- 코드 중복 확인: 교사 화면이 `getDoc(classes/{새 코드})`로 이미 있는지 확인하고 있으면 새로 뽑는다. 동시에 같은 코드를 만들어도, 이미 있는 문서에 대한 쓰기는 `create`가 아니라 `update`로 판정되어 남의 수업이면 거부된다. 그래서 남의 수업을 덮어쓸 수 없다.

### 이유와 한계
- `get`/`list` 구분은 규칙이 가장 확실하게 보장하는 경계라서 초보자 규칙으로도 원칙 4를 지킬 수 있다.
- 코드 경우의 수는 32^6 ≈ 10억 개라 무작위로 맞히기 어렵다. 다만 조회 횟수 제한은 규칙으로 걸 수 없다(심화: App Check).
- 한계: 코드를 바꾸려면 수업 문서를 새로 만들어야 한다(코드 재발급 기능 없음). 연수 범위에서는 문제없다.
- 코드를 아는 사람은 그 수업의 `title`, `teacherUid`, `joinCode`를 볼 수 있다. 가입하려는 학생에게 필요한 정보뿐이다. 다만 `teacherUid`로 `users` 문서를 읽으면 교사 이름·이메일도 보인다(D9, 6절).
- **규칙이 강제하는 원칙 4의 범위:** 규칙은 "가입 시점"을 구분할 수 없다. 그래서 실제로 강제되는 것은 "수업코드를 아는 로그인 사용자만 그 수업 1건을 get할 수 있고, 전체 목록(list)은 못 본다"이다. 가입한 뒤에도, 가입하지 않고도 코드만 알면 get은 언제든 된다(설계상 불가피). 슬라이드 47 표 4행도 "수업코드를 아는 사람만 그 수업 1건을 찾는다, 전체 목록은 못 본다"로 쓰는 것이 맞다(검수 4-4).

### 원고에 주는 영향
- 슬라이드 20 노트의 "코드와 일치하는 수업 한 건만 조회"는 그대로 맞다. 도식의 "전체를 내려받아 비교하지 않는다"도 그대로 쓴다.
- **슬라이드 21·22 프롬프트는 바꿔야 한다**(문장은 `02_engineer_prompts.md` M3 참고). 원고의 where 조회 문장대로 만들면 모듈 3~6에서는 임시 규칙 덕분에 동작하지만, **모듈 7 최종 규칙 배포 후 학생 가입이 권한 오류로 실패**한다.

---

## 2. D2 학생의 "내가 가입한 수업" 목록

### 문제
명세의 `classes/{classId}/members/{uid}`에는 `joinedAt`만 있다. 학생 입장에서 "내가 가입한 수업"을 찾으려면 모든 수업의 members를 가로질러 "문서 이름이 내 uid인 것"을 찾아야 한다. Firestore 컬렉션 그룹 조회는 문서 이름(documentId)으로 거를 때 **전체 경로**를 요구하므로, 내 uid만으로는 거를 수 없다. 필드가 `joinedAt`뿐인 상태에서는 다음 두 방법밖에 없고 둘 다 쓸 수 없다.
- 수업 전체 목록을 받아 하나씩 members를 확인 → 원칙 4 위반, 최종 규칙에서 거부됨
- 브라우저 저장소(localStorage)에 가입 목록 기억 → 다른 기기·시크릿 창에서 사라짐, 데이터 근거 없음

### 결정 (명세 승인·반영됨, 2026-10-03)
**최소 변경:** `classes/{classId}/members/{uid}`: `joinedAt`, **`uid`** (값은 문서 이름과 같은 학생 uid)

- 조회: `collectionGroup(db, 'members')` + `where('uid', '==', 내 uid)` → 결과 문서의 부모의 부모(`doc.ref.parent.parent.id`)가 classId → 각 수업을 `getDoc(classes/{classId})`로 읽어 제목 표시.
- 규칙: `match /{path=**}/members/{memberId} { allow list: if signedIn() && resource.data.uid == me(); }` → 조회 조건이 "uid가 나"일 때만 통과. 다른 사람의 가입 문서는 이 조회로 볼 수 없다.
- 가입(create) 규칙에서 `request.resource.data.uid == me()`와 문서 이름 `uid == me()`를 함께 강제해 값이 어긋나지 않게 한다.
- **색인 필요:** 컬렉션 그룹 조회는 단일 필드라도 "컬렉션 그룹 범위" 색인이 자동으로 만들어지지 않는다. 처음 실행하면 `The query requires a COLLECTION_GROUP_ASC index for collection members and field uid` 같은 오류와 색인 생성 링크가 나온다 `[확인필요: 정확한 오류 문구]`. M3 슬라이드 23 "막힐 때"의 색인 링크 안내가 바로 이 경우다. checkpoint-final에는 같은 색인을 `firestore.indexes.json`의 `fieldOverrides`로 넣었다.

### 변경 범위 확인
- 바뀌는 것은 members 문서에 필드 1개뿐이다. 다른 경로·필드 이름은 명세와 같다.
- 슬라이드 19 도식의 `members/{uid}` 카드는 `joinedAt`, `uid`로 반영되었다.
- 명세 파일(`firebase-classroom-spec`)에 이 필드가 승인·반영되었으므로, 예전에 적어 두었던 "미승인 시 대안 B"(localStorage로 축소)는 삭제했다.
- 채택하지 않은 다른 대안(예: `users/{uid}`에 가입 수업 배열 저장)은 규칙에서 "가입 문서와 배열이 일치하는지"를 강제하기 어려워 쓰지 않았다.

---

## 3. D3·D4·D5 권한 판정과 제출물 보호

### D3 수업 만들기는 교사 계정만 (role 확인은 create 한 곳)
- M7 슬라이드 50의 검증 (3) "학생 계정으로 수업 만들기 → 차단"을 통과하려면 규칙이 학생 계정을 구분해야 한다. teacherUid만으로는 구분할 수 없다. 학생이 수업을 만들면 그 학생이 그 수업의 teacherUid가 되기 때문이다.
- 그래서 `classes` **create에만** `get(users/{내 uid}).data.role == 'teacher'`를 확인한다. 그리고 `users` update에서 `role`을 바꾸지 못하게 해, 학생으로 가입한 계정이 나중에 교사로 바꿔 수업을 만드는 것을 막는다.
- 수업이 만들어진 다음의 모든 권한(수업 수정·삭제, 자료, 학습지, 제출물 열람, 피드백 쓰기)은 **teacherUid로만** 판정한다. "role은 화면 분기용, 권한은 teacherUid"라는 원고 메시지는 수업 이후 권한에 그대로 맞는다.
- **한계(슬라이드 노트에 한 줄 필요):** role은 처음 로그인할 때 본인이 고른다. 따라서 새 계정을 만들어 "교사"를 고르면 수업을 만들 수 있다. 이 확인은 "학생 계정이 실수로 또는 장난으로 수업을 만드는 것"을 막는 수준이다. 실제 운영에서는 교사 명단(관리자가 콘솔에서 넣는 문서)이나 학교 이메일 도메인 확인(`request.auth.token.email.matches('.*@학교도메인$')`)을 추가한다(심화).
- 역할을 잘못 고른 교사는 화면에서 바꿀 수 없다. 콘솔 Firestore에서 `users/{uid}` 문서를 지우고 다시 로그인하면 역할 선택이 다시 나온다 `[확인필요: 콘솔 문서 삭제 메뉴 이름]`.

### D4 학생은 자기 제출물의 feedback을 쓰지 못한다
- `submissions/{uid}` 한 문서에 `answers`, `submittedAt`(학생이 씀)과 `feedback`(교사가 씀)이 함께 있다.
- 학생 create: 필드가 `answers`, `submittedAt`뿐이어야 한다(`hasOnly`). 처음부터 feedback을 넣어 저장할 수 없다.
- 학생 update: 이번 수정으로 바뀐 필드가 `answers`, `submittedAt`뿐이어야 한다(`diff(resource.data).affectedKeys().hasOnly([...])`). feedback을 고치거나 지우면 바뀐 필드에 feedback이 들어가므로 거부된다.
- 교사 update: 바뀐 필드가 `feedback`뿐이어야 한다. 교사도 학생 답안은 고칠 수 없다.

### D5 재제출 시 feedback이 지워지지 않는 방식
- 학생 화면은 제출할 때 **병합 저장**(`setDoc(ref, { answers, submittedAt: serverTimestamp() }, { merge: true })`)을 쓴다. 병합 저장은 적은 필드만 바꾸고 나머지(feedback)는 남긴다.
- 병합 없이 통째로 덮어쓰는 코드가 만들어지면, 피드백이 이미 있는 제출물에서 "feedback 삭제"가 일어난다. 이 경우 D4 규칙이 거부하므로 학생에게 권한 오류가 보인다(모듈 7 이후). 데이터가 몰래 지워지는 대신 오류로 드러나게 한 설계다. 임시 규칙(모듈 3~6)에서는 이 안전장치가 없어서 실제로 지워질 수 있다. M6 슬라이드 44 "막힐 때"가 이 상황이다.
- 재제출 후에도 예전 답안에 대한 피드백이 그대로 보인다. 교사 제출현황에서 "피드백 저장 뒤 다시 제출함"을 알 수 있게 하려면 피드백 시각 필드가 더 필요하다(명세 밖이라 구현하지 않음, 심화).

---

## 4. D6·D7 정답 저장과 문항 필드 확정

### D6 정답 저장: questions[].answer 동봉 (M5 원고 가정 A 채택)
- 정답은 학습지 문서 안 `questions[i].answer`에 저장한다. 명세 경로를 그대로 쓰고, 모듈 6 정답 비교 초안이 같은 문서만 읽으면 되기 때문이다.
- **한계(그대로 둠):** 가입한 학생은 학습지 문서를 읽을 수 있어야 문항을 풀 수 있다. Firestore 규칙은 문서 단위로 읽기를 허용하므로 문서 안 `answer` 필드만 숨길 수 없다. 화면에 정답을 표시하지 않아도 개발자 도구(네트워크 탭)로 정답을 볼 수 있다. → 선택형은 연습·형성평가용, 성적용 평가는 서술형 중심으로 운영(M5 슬라이드 38 노트와 일치).
- **심화 대안(구현하지 않음, 명세 변경 필요):** 정답을 `classes/{classId}/worksheets/{id}/answerKeys/key`처럼 교사만 읽는 별도 문서로 분리하고, 그 문서에는 `allow read, write: if isTeacher(classId)`만 준다. 정답 비교는 교사 화면에서만 하므로 동작에 문제없다.

### D7 문항·답안 필드 (이 표가 기준)

| 위치 | 필드 | 형식 | 값 규칙 |
|---|---|---|---|
| `worksheets/{id}` | `title` | 문자열 | 비어 있으면 저장하지 않음 |
| `worksheets/{id}` | `questions` | 배열(최대 50개) | 문항 순서 = 배열 순서 |
| `questions[i]` | `type` | 문자열 | `"essay"`(서술형) 또는 `"choice"`(선택형) |
| `questions[i]` | `text` | 문자열 | 질문 문장 |
| `questions[i]` | `choices` | 문자열 배열 | 선택형: 보기 2~5개 / 서술형: 빈 배열 `[]` |
| `questions[i]` | `answer` | 숫자 또는 null | 선택형: **정답 보기의 순서 번호, 0부터 센다**(첫 보기 = 0) / 서술형: `null` |
| `submissions/{uid}` | `answers` | 배열 | `answers[i]`는 `questions[i]`의 답. 서술형: 문자열(안 쓰면 `""`) / 선택형: 고른 보기 번호(0부터, 안 고르면 `null`) |
| `submissions/{uid}` | `submittedAt` | 타임스탬프 | 서버 시각(`serverTimestamp()`) |
| `submissions/{uid}` | `feedback` | 문자열 | 교사가 저장한 피드백 글. 줄바꿈 포함, 화면에는 글자 그대로(textContent) 표시 |
| `materials/{id}` | `title`, `html`, `createdAt` | 문자열, 문자열, 타임스탬프 | `createdAt`은 서버 시각 |
| `members/{uid}` | `joinedAt`, `uid` | 타임스탬프, 문자열 | `uid`는 D2로 추가된 필드(명세 반영됨), 값 = 문서 이름 |
| `users/{uid}` | `name`, `email`, `role` | 문자열 3개 | `role`은 `"teacher"` 또는 `"student"`, 처음 저장 뒤 변경 불가 |

- 화면에서는 보기 번호를 1부터 보여 준다("보기 1"). 저장 값만 0부터다. 정답 비교는 `answers[i] === questions[i].answer`.
- 시각 필드는 규칙에서 "타임스탬프인지"만 확인한다. Claude Code가 `serverTimestamp()` 대신 `new Date()`를 써도 통과하도록 일부러 느슨하게 했다(초보자 프롬프트 결과의 차이를 흡수하기 위해).

---

## 5. 최종 규칙 `firestore.rules` 전체 (모듈 7, checkpoint-final)

강사가 연수 전에 준비하는 `checkpoint-final/firestore.rules`에 아래 내용을 그대로 넣는다. 참가자가 복사하는 파일이므로 주석까지 이 본문과 같게 둔다. (예전 참고 파일 `reference-app/rules/firestore.rules`는 삭제됨. 이 본문이 기준)

```
rules_version = '2';

// =====================================================================
// 온라인 클래스룸 최종 보안 규칙 (모듈 7, checkpoint-final)
// 보안 규칙 = 교무실 출입 규칙. 아래에서 허용한 것만 열리고, 나머지는 모두 거부된다.
// 원칙 5(sandbox iframe)는 규칙이 아니라 화면 코드(app.js의 iframe)가 지킨다.
// =====================================================================
service cloud.firestore {
  match /databases/{database}/documents {

    // ---------- 도우미 함수 ----------
    function signedIn() {
      return request.auth != null;
    }
    function me() {
      return request.auth.uid;
    }
    function classDoc(classId) {
      return /databases/$(database)/documents/classes/$(classId);
    }
    // 원칙 3: 권한은 users의 role이 아니라 수업 문서의 teacherUid로 판정한다.
    function isTeacher(classId) {
      return signedIn() && get(classDoc(classId)).data.teacherUid == me();
    }
    // 원칙 1·2: "가입했다" = classes/{classId}/members/{내 uid} 문서가 있다.
    function isMember(classId) {
      return signedIn()
        && exists(/databases/$(database)/documents/classes/$(classId)/members/$(me()));
    }
    // 새로 저장하려는 문서에 정해진 필드만 있는지
    function onlyKeys(keys) {
      return request.resource.data.keys().hasOnly(keys);
    }
    // 이번 수정에서 바뀐 필드가 정해진 필드뿐인지
    function changedOnly(keys) {
      return request.resource.data.diff(resource.data).affectedKeys().hasOnly(keys);
    }

    // ---------- users/{uid}: name, email, role ----------
    match /users/{uid} {
      // 로그인한 사람은 uid를 아는 사용자 문서 1건만 읽을 수 있다(교사 제출현황의 학생 이름 표시용).
      // 사용자 전체 목록 조회(list)는 막는다.
      allow get: if signedIn();
      // 내 문서는 나만 만든다. role은 teacher 또는 student만.
      allow create: if signedIn() && uid == me()
        && request.resource.data.keys().hasAll(['name', 'email', 'role'])
        && onlyKeys(['name', 'email', 'role'])
        && request.resource.data.role in ['teacher', 'student'];
      // 내 문서는 나만 고친다. role은 처음 정한 뒤 바꿀 수 없다(원칙 3 보조: 학생 계정이 교사로 바꾸지 못하게).
      allow update: if signedIn() && uid == me()
        && onlyKeys(['name', 'email', 'role'])
        && request.resource.data.role == resource.data.role;
    }

    // ---------- classes/{classId}: title, teacherUid, joinCode ----------
    // 문서 이름(classId) = 수업코드(joinCode). 코드를 아는 사람만 그 수업 1건을 찾을 수 있다.
    match /classes/{classId} {
      // 원칙 4: 수업코드(=문서 이름)를 알고 1건을 조회(get)하는 것만 허용
      allow get: if signedIn();
      // 원칙 4: 목록 조회(list)는 "내가 교사인 수업"만. 학생은 수업 전체 목록을 볼 수 없다.
      allow list: if signedIn() && resource.data.teacherUid == me();
      // 원칙 3: 수업 만들기는 교사 계정만, teacherUid는 반드시 나 자신
      allow create: if signedIn()
        && get(/databases/$(database)/documents/users/$(me())).data.role == 'teacher'
        && request.resource.data.keys().hasAll(['title', 'teacherUid', 'joinCode'])
        && onlyKeys(['title', 'teacherUid', 'joinCode'])
        && request.resource.data.teacherUid == me()
        && request.resource.data.joinCode == classId
        && classId.matches('^[A-HJ-NP-Z2-9]{6}$')
        && request.resource.data.title is string
        && request.resource.data.title.size() > 0
        && request.resource.data.title.size() <= 100;
      // 원칙 3: 수업 고치기·지우기는 그 수업의 교사만. 제목만 고칠 수 있다.
      allow update: if signedIn() && resource.data.teacherUid == me()
        && changedOnly(['title'])
        && request.resource.data.title is string
        && request.resource.data.title.size() > 0;
      allow delete: if signedIn() && resource.data.teacherUid == me();

      // ---------- classes/{classId}/members/{uid}: joinedAt, uid ----------
      // uid 필드: "내가 가입한 수업" 목록(컬렉션 그룹 조회)에 쓴다. 값은 문서 이름(내 uid)과 같다.
      match /members/{uid} {
        // 내 가입 문서는 나와 그 수업 교사만 읽는다.
        allow get: if signedIn() && (uid == me() || isTeacher(classId));
        // 원칙 3 관련: 가입 학생 명단(list)은 그 수업 교사만 본다.
        allow list: if isTeacher(classId);
        // 원칙 4: 코드를 알고 찾은 수업에, 내 uid 이름으로만 가입한다.
        allow create: if signedIn() && uid == me()
          && exists(classDoc(classId))
          && request.resource.data.keys().hasAll(['joinedAt', 'uid'])
          && onlyKeys(['joinedAt', 'uid'])
          && request.resource.data.uid == me()
          && request.resource.data.joinedAt is timestamp;
        // 탈퇴는 본인, 내보내기는 교사
        allow delete: if signedIn() && (uid == me() || isTeacher(classId));
      }

      // ---------- classes/{classId}/materials/{id}: title, html, createdAt ----------
      match /materials/{materialId} {
        // 원칙 1: 학생은 가입한 수업의 자료만 읽는다(교사는 자기 수업 자료를 읽는다).
        allow read: if isTeacher(classId) || isMember(classId);
        // 원칙 3: 자료 작성·수정·삭제는 그 수업 교사만
        allow create, update: if isTeacher(classId)
          && onlyKeys(['title', 'html', 'createdAt'])
          && request.resource.data.title is string
          && request.resource.data.html is string
          && request.resource.data.createdAt is timestamp;
        allow delete: if isTeacher(classId);
      }

      // ---------- classes/{classId}/worksheets/{id}: title, questions[] ----------
      match /worksheets/{worksheetId} {
        // 원칙 1과 같은 기준: 가입한 학생과 그 수업 교사만 학습지를 읽는다.
        allow read: if isTeacher(classId) || isMember(classId);
        // 원칙 3: 학습지 작성·수정·삭제는 그 수업 교사만
        allow create, update: if isTeacher(classId)
          && onlyKeys(['title', 'questions'])
          && request.resource.data.title is string
          && request.resource.data.questions is list
          && request.resource.data.questions.size() <= 50;
        allow delete: if isTeacher(classId);

        // ---------- .../submissions/{uid}: answers, feedback, submittedAt ----------
        match /submissions/{uid} {
          // 원칙 2: 학생은 문서 이름이 내 uid인 제출물만 읽는다. 교사는 자기 수업 제출물을 읽는다.
          allow get: if isTeacher(classId)
            || (signedIn() && uid == me() && isMember(classId));
          // 원칙 2: 제출물 목록(list)은 그 수업 교사만. 학생은 다른 학생 제출물을 볼 수 없다.
          allow list: if isTeacher(classId);
          // 원칙 2: 첫 제출. 내 uid 이름으로만, answers와 submittedAt만 쓴다(feedback 못 씀).
          allow create: if signedIn() && uid == me() && isMember(classId)
            && exists(/databases/$(database)/documents/classes/$(classId)/worksheets/$(worksheetId))
            && request.resource.data.keys().hasAll(['answers', 'submittedAt'])
            && onlyKeys(['answers', 'submittedAt'])
            && request.resource.data.answers is list
            && request.resource.data.submittedAt is timestamp;
          // 원칙 2: 재제출은 answers, submittedAt만 바꿀 수 있다. feedback은 바꾸거나 지울 수 없다.
          // 원칙 3: 그 수업 교사는 feedback 필드만 쓸 수 있다(답안은 못 고침).
          allow update: if (signedIn() && uid == me() && isMember(classId)
                && changedOnly(['answers', 'submittedAt'])
                && request.resource.data.answers is list
                && request.resource.data.submittedAt is timestamp)
            || (isTeacher(classId)
                && changedOnly(['feedback'])
                && request.resource.data.feedback is string);
          allow delete: if isTeacher(classId);
        }
      }
    }

    // ---------- "내가 가입한 수업" 목록(컬렉션 그룹 조회) ----------
    // 모든 수업의 members를 가로질러 "uid가 나인 문서"만 찾는 조회를 허용한다.
    // 조건 때문에 다른 사람의 가입 문서는 이 조회로 볼 수 없다.
    match /{path=**}/members/{memberId} {
      allow list: if signedIn() && resource.data.uid == me();
    }
  }
}
```

### 함께 배포하는 색인 파일 `firestore.indexes.json`

```json
{
  "indexes": [],
  "fieldOverrides": [
    {
      "collectionGroup": "members",
      "fieldPath": "uid",
      "indexes": [
        { "order": "ASCENDING", "queryScope": "COLLECTION" },
        { "order": "ASCENDING", "queryScope": "COLLECTION_GROUP" }
      ]
    }
  ]
}
```
- 모듈 3에서 오류 링크로 색인을 이미 만든 참가자는 이 파일 없이도 동작한다. `firebase deploy --only firestore:rules`는 색인을 배포하지 않으므로 기존 색인이 지워지지 않는다 `[확인필요: CLI 동작]`.
- 자료 목록(`orderBy('createdAt','desc')`)과 교사 수업 목록(`where('teacherUid','==',…)`)은 단일 필드 자동 색인으로 동작하므로 추가 색인이 필요 없다(교사 수업 목록은 정렬을 브라우저에서 한다. `orderBy`를 붙이면 복합 색인이 필요해진다).

---

## 6. 5원칙별 규칙 대응과 이유

| 원칙 | 규칙 위치 | 핵심 조건 | 왜 이렇게 했나 |
|---|---|---|---|
| 1. 가입한 수업 자료만 읽기 | `materials` read, `worksheets` read | `isTeacher(classId) \|\| isMember(classId)` | "가입"을 `members/{내 uid}` 문서 존재로 정의했다. 문서 이름이 uid이므로 `exists()` 한 번으로 확인되어 규칙이 짧고, 학생이 남의 이름으로 가입 문서를 만들 수 없다(create에서 `uid == me()`). |
| 2. 자기 제출물만 읽고 쓰기 | `submissions` get/list/create/update | 학생: `uid == me()` + get만, list 금지. 쓰기는 `answers`, `submittedAt`만 | 제출물 문서 이름을 uid로 정했기 때문에 "내 번호표 서랍만 연다"가 `uid == me()` 한 줄로 끝난다. list를 학생에게 주지 않아 다른 학생 제출물 목록 자체를 받을 수 없다. feedback은 같은 문서에 있으므로 "바뀐 필드" 검사로 학생이 못 쓰게 했다. |
| 3. 작성은 해당 수업 교사만 | `classes` create/update/delete, `materials`·`worksheets` 쓰기, `submissions` 교사 update, `members` list | `teacherUid == me()` (`isTeacher`), 수업 create만 role 확인 | role은 본인이 고르는 값이라 권한 근거로 약하다. 수업을 만든 사람의 uid(teacherUid)는 규칙이 create 때 "반드시 나 자신"으로 강제하므로 위조할 수 없다. 단 "학생 계정은 수업을 못 만든다"는 teacherUid로 표현할 수 없어서 create 한 곳만 role을 보고, role 변경을 금지했다(D3). |
| 4. 코드 조회는 가입 시점만, 전체 목록 차단 | `classes` get/list, `members` create | get은 로그인만, list는 내 수업만 | Firestore 규칙은 get(이름 알고 1건)과 list(목록 조회)를 따로 판정한다. 코드를 문서 이름으로 써서 "코드를 아는 사람 = 그 문서를 get할 수 있는 사람"이 되게 했다(D1). 규칙이 실제로 강제하는 범위는 "코드를 알 때만 1건"이며 "가입 시점"은 구분하지 못한다(1절 이유와 한계). |
| 5. 교사 HTML은 sandbox iframe | 규칙 파일 아님. `app.js`의 자료 보기 | `<iframe sandbox srcdoc>`, `sandbox` 값 비움 | 규칙은 데이터 접근만 다룬다. 자료 속 스크립트가 우리 페이지(로그인 정보가 있는 출처)에 접근하는 것은 화면 쪽에서 막아야 한다. `sandbox` 값을 비우면 스크립트 실행, 양식 제출, 팝업, 상위 창 이동이 모두 막히고 자료는 고유하지 않은 출처(opaque origin)로 열려 우리 페이지의 저장소(로그인 정보 포함)를 읽을 수 없다. `allow-scripts`와 `allow-same-origin`을 함께 주면 자료 속 스크립트가 같은 출처 권한으로 iframe의 sandbox 속성을 지우고 다시 불러올 수 있어 보호가 사라진다. |

추가 원칙(명세 비밀 정보·개인정보와 연결):
- `users` get 허용(D9): 교사 제출현황에 학생 이름을 보여 주려면 교사가 학생 `users` 문서를 읽어야 한다. 규칙은 "이 학생이 내 수업 학생인지"를 users 경로에서 확인할 수 없어서(classId를 모름) 로그인한 사람에게 1건 get을 허용하고 list는 막았다. 학생은 앱 안에서 다른 학생의 uid를 알 방법이 없다(members 목록·제출물 목록은 교사만 list 가능). 다만 uid를 어떤 경로로든 알면 그 사람의 이름·이메일을 읽을 수 있다는 한계가 있다. **특히 교사 쪽은 앱 안에서 uid가 드러난다.** 수업코드를 아는 사람은 누구나 `classes/{코드}`의 `teacherUid`를 읽을 수 있으므로, 그 값으로 `users/{teacherUid}`를 get해 담당 교사의 이름·이메일을 볼 수 있다. 실제 운영 시에는 users에 이메일을 저장하지 않거나 교사용 공개 이름만 두는 방식을 검토한다(M7 슬라이드 53 노트 보강 권장, 교사 이메일 문장 포함).
- users 이름·이메일 위조 가능(한계, 연수 기본 범위에서는 규칙을 바꾸지 않음): users create·update는 `name`, `email` 값을 본인이 아무렇게나 쓸 수 있다. 교사 제출현황(슬라이드 37)은 `users/{uid}.name`을 보여 주므로, 학생 계정이 다른 학생 이름으로 바꾸면 교사가 혼동할 수 있다. 제출현황의 이름은 "학생이 정한 값"이다. 보완하려면(심화) create·update에 `request.resource.data.email == request.auth.token.email`을 더하고 이름은 교사가 명단과 대조한다. 5절 본문에는 넣지 않았다(checkpoint-final과 원고 규칙 범위를 늘리지 않기 위해).

---

## 7. 모듈 2 임시 규칙 (슬라이드 13 5단계 게시용)

강사 배포 자료에 `firestore.temp.rules` 이름으로 넣는다(강사가 새로 만들어야 하는 파일, prompts 문서 0-0절 #2). 강사가 준비하는 checkpoint-m2 ~ checkpoint-m6 폴더에는 같은 내용을 `firestore.rules` 이름으로 넣는다(참고용. 실제 적용은 콘솔 규칙 탭에 게시한 것). (예전 참고 파일 `reference-app/rules/firestore.temp.rules`는 삭제됨. 이 본문이 기준)

**슬라이드 13 5단계 문장(원고 반영됨):** "규칙 탭을 열고, 강사가 나눠 준 `firestore.temp.rules`(복구 지점 폴더에서는 `firestore.rules`) 파일 내용을 통째로 복사해 붙여넣고 '게시(Publish)' 버튼" `[확인필요: 리허설 캡처 - 한국어 탭·버튼 이름]`.
**슬라이드 13 노트의 한 줄(원고 반영됨):** "이 임시 규칙은 로그인한 사람이면 실습 데이터를 읽고 쓸 수 있는 연습용입니다. 학생끼리 서로의 답안도 보이는 상태이므로 실제 학생 정보는 넣지 않고, 모듈 7에서 진짜 규칙으로 바꿉니다."

```
rules_version = '2';

// =====================================================================
// [임시 규칙] 연수 모듈 2~6 실습용 (슬라이드 13에서 Firestore 규칙 탭에 붙여넣기)
// - 로그인한 사람만 읽고 쓸 수 있다. 로그인하지 않은 사람은 모두 거부.
// - users 문서는 본인만 만들고 고친다.
// - classes 아래(수업, 가입, 자료, 학습지, 제출물)는 로그인한 사람 누구나 읽고 쓴다.
//   → 실습이 막히지 않게 하려는 연습용 설정이다. 학생끼리 서로의 제출물을 볼 수 있는 상태이므로
//     실제 학생 정보는 절대 넣지 않는다. 모듈 7에서 최종 규칙(firestore.rules)으로 반드시 바꾼다.
// =====================================================================
service cloud.firestore {
  match /databases/{database}/documents {
    function signedIn() {
      return request.auth != null;
    }

    match /users/{uid} {
      allow read: if signedIn();
      allow create, update: if signedIn() && request.auth.uid == uid;
    }

    match /classes/{document=**} {
      allow read, write: if signedIn();
    }

    // 모듈 3 "내가 가입한 수업" 목록(컬렉션 그룹 조회)용
    match /{path=**}/members/{memberId} {
      allow read: if signedIn();
    }
  }
}
```

### 임시 규칙이 허용하는 범위 (모듈 3~6 동작 확인표)

| 모듈 | 동작 | 경로 | 임시 규칙에서 |
|---|---|---|---|
| 2 | 내 users 문서 만들기·읽기 | `users/{uid}` | 허용(본인만 쓰기) |
| 3 | 수업 만들기, 코드 중복 확인, 코드로 1건 읽기 | `classes/{classId}` | 허용 |
| 3 | 교사 내 수업 목록(where teacherUid) | `classes` list | 허용 |
| 3 | 가입 문서 만들기 | `classes/{classId}/members/{uid}` | 허용 |
| 3 | 학생 내 가입 수업(컬렉션 그룹) | `{path=**}/members` | 허용 (색인은 별도로 필요) |
| 4 | 자료 등록·목록·열람 | `materials` | 허용 |
| 5 | 학습지 작성·읽기, 제출, 제출현황(members·submissions 목록, users 이름) | `worksheets`, `submissions`, `users` get | 허용 |
| 6 | 교사 feedback 저장, 학생 feedback 읽기 | `submissions/{uid}` | 허용 |

- 임시 규칙에는 원칙 1~4가 **없다**. 학생 계정도 수업을 만들 수 있고, 다른 학생 제출물을 읽을 수 있다. 슬라이드 13 노트에 "연습용이며 모듈 7에서 교체"를 그대로 말한다.
- 임시 규칙은 로그인만 하면 누구나 classes 아래를 쓸 수 있으므로, 연수가 끝나고 모듈 7을 하지 못한 참가자도 **연수 당일 안에** checkpoint-final의 규칙을 게시하도록 안내한다.
- **임시 규칙 기간에 생긴 데이터는 최종 규칙이 고치지 않는다.** 임시 규칙(모듈 3~6)에서 학생 계정이 만든 수업은 최종 규칙 이후에도 그 학생이 `teacherUid`로 남고, `uid` 필드 없이 만든 가입 문서, 아무나 쓴 feedback도 그대로 남는다. 실제 학급용은 연습 데이터를 모두 지운 뒤(또는 새 프로젝트로) 최종 규칙을 먼저 게시하고 시작한다(M7 슬라이드 53 "정리" 항목에 추가 권장).
- 막힐 때 "임시 규칙을 고쳐 달라"고 요청하지 않는다. 위 표처럼 임시 규칙은 모듈 3~6 동작을 모두 허용하므로, 권한 오류의 원인은 보통 규칙 미게시나 로그아웃이다. 콘솔 규칙 탭에 `firestore.temp.rules`가 게시되어 있는지, 로그인 상태인지 먼저 확인하고, 그래도 같으면 "규칙 파일은 바꾸지 말고 앱 코드에서 원인을 찾아 줘"라고 요청한다(검수 4-3, 원고 반영됨).
- (선택) 만료일을 넣고 싶으면 `allow read, write: if signedIn() && request.time < timestamp.date(2026, 12, 31);`처럼 쓴다. 날짜가 지나면 모든 기능이 권한 오류로 멈추므로 기본안에는 넣지 않았다.
- **임시 규칙에서 되던 것이 최종 규칙에서 막히는 경우(모듈 7 막힐 때용):**
  1. 학생 가입을 where 조회로 만든 경우 → 가입 실패. D1 방식(문서 이름 = 코드)으로 고쳐야 한다.
  2. members 문서에 `uid` 필드가 없는 경우 → 가입 실패(create에서 uid 필드 필수) 또는 학생 수업 목록이 비어 보임.
  3. 제출을 병합 없이 덮어쓰는 경우 → 피드백이 있는 제출물의 재제출 실패.
  4. 시각 필드를 문자열(예: `"2026-10-03"`)로 저장한 경우 → 저장 실패. 타임스탬프로 저장해야 한다.
  5. 교사가 role을 student로 고른 계정 → 수업 만들기 실패.

---

## 8. 원고와의 불일치·보완 목록 (규칙 관련)

"상태" 칸의 "반영됨"은 검수 보고서(2026-10-03) 1절 일치 확인과 2회차 보고서(`03_reviewer_report_r2.md`) N6 지적 뒤 원고 대조를 근거로 했다.

| 원고 위치 | 원고 내용(예전) | 이 문서의 결정 | 필요한 수정 | 상태 |
|---|---|---|---|---|
| M3 가정, 슬라이드 22 프롬프트 | `classes`에서 `joinCode == 입력값` where 조회 1건 | 문서 이름 = 코드, `getDoc` 1건 | 슬라이드 21·22 프롬프트 교체(prompts 문서 M3) | 반영됨 |
| M3 슬라이드 19 도식 | `members/{uid}`(joinedAt) | `joinedAt`, `uid` (명세 반영됨) | 도식에 `uid` 추가 | 반영됨 |
| M3 슬라이드 23 프롬프트 | "필드 이름은 바꾸지 말고 처음 정한 그대로" | members에 uid 필드 필요 | 프롬프트 교체(prompts 문서 M3) | 반영됨 |
| M3 슬라이드 23 막힐 때 | 색인 오류 링크 | 실제로 컬렉션 그룹 색인 1개 필요 | 그대로 유효. `[확인필요: 오류 문구·소요 시간]` 유지 | 유지 |
| M3 슬라이드 21·22·23, M4 29 막힐 때 | "임시 규칙을 고쳐 줘" 요청 | 임시 규칙은 이미 모두 허용(7절) | 규칙 게시·로그인 확인 → "규칙 파일은 바꾸지 말고 앱 코드에서 원인을 찾아 줘"로 교체 | 반영됨 |
| M5 슬라이드 35 프롬프트 5번 | answer = "정답 보기 번호, 서술형은 빈 값" | 0부터 세는 숫자, 서술형 `null`, 서술형 choices `[]` | 문장 보완 | 반영됨 |
| M5 슬라이드 36 프롬프트 4번 | "같은 문서에 덮어쓰게" | 병합 저장(merge) | "feedback 같은 다른 필드는 지우지 않도록 병합 저장" 추가 | 반영됨 |
| M5 슬라이드 38 노트 | 정답 동봉 한계, 분리 저장은 심화 | 같음 | `[확인필요]` 해제 가능 | - |
| M6 가정, 슬라이드 41 노트 | 학생 feedback 쓰기 금지는 모듈 7에서 | 같음(D4) | `[확인필요]` 해제 가능 | - |
| M6 슬라이드 44 막힐 때 | 재제출로 feedback 삭제 가능 | 임시 규칙에서는 실제로 삭제 가능, 최종 규칙에서는 거부 | 문구 그대로 유효. `[확인필요]` 해제 가능 | - |
| M7 슬라이드 47 표 4행 | "수업코드는 가입할 때만 조회" | 규칙이 강제하는 범위는 "코드를 알 때만 1건"(1절) | "수업코드를 아는 사람만 그 수업 1건을 찾는다, 전체 목록은 못 본다" | 반영됨 |
| M7 슬라이드 48 프롬프트 원칙 3 | "users 문서의 role 값으로 권한을 판단하지 마" | 수업 create만 role 확인 + role 변경 금지 | 문장 교체(prompts 문서 M7) | 반영됨 |
| M7 슬라이드 48 프롬프트 원칙 4 | "코드를 알고 수업 1건을 찾아 가입하는 경우만 허용" | 문서 이름 = 코드, get 허용·list 차단 | "수업 문서 이름이 수업코드이므로 1건 읽기(get)는 허용, 목록(list)은 자기 수업만" 문장 추가 | 반영됨 |
| M7 슬라이드 48 막힐 때 | `role == 'teacher'` 줄이 있으면 고치라고 요청 | create에는 있어야 정상 | "수업 만들기(create) 외의 곳에 role이 있으면" 으로 수정 | - |
| M7 슬라이드 50 (2) | 다른 학생 제출물 열기, 재현 방법 미정 | 강사가 준비하는 checkpoint-final에 `rules-check.html` + `rules-check.js`(규칙 점검 페이지)를 넣는다. 명세는 prompts 문서 슬라이드 50 절(예전 참고 구현은 삭제됨) | 검증 방법을 이 페이지로 안내, 복사 프롬프트에 rules-check.js 추가 | 반영됨 |
| M7 슬라이드 50·51 원칙 3 | 버튼 3(수업 만들기)만 점검 | 버튼 6 "가입한 수업에 자료 1건 쓰기 → 막힘" 추가 | "막힘 6개", 51 원칙 3 행 "수업·자료·학습지 작성은 그 수업 교사만" | 반영됨(50 본문·도식·예상 결과 "막힘 6개", 51 원칙 3 "버튼 3과 6") |
| M5 슬라이드 35 노트 | "문항 하나는 종류, 질문, 선택지, 정답" | `type`·`text`·`choices`·`answer` 4필드 확정(D7) | `[확인필요: 필드명 일치]` 해제 가능 | - |
| M6 슬라이드 45 도식 | 4번째 칸 "Firestore(`feedback` 초안 저장)" | 함수는 초안을 교사 화면으로 돌려주고 저장은 교사가 한다 | 도식 수정 (규칙 영향: 함수가 Firestore에 직접 쓰지 않으므로 규칙 변경 없음) | 반영됨 |
| M7 슬라이드 53 노트 | users 읽기 범위 언급 없음 | 로그인한 사람은 uid를 아는 사용자 1명 get 가능, 교사 이름·이메일은 코드만 알면 보임(D9) | 개인정보 한 줄 추가 권장, 연습 데이터 정리 문장 추가 | 반영됨 |
| M7 슬라이드 51 항목 4 | 수업 전체 목록 조회 시도 | `rules-check.html` 4번 버튼 | 같음 | - |

---

## 9. 검증 상태 (2026-10-03)

### 9-1. 당시 확인한 것 → 지금은 **재확인 필요** (근거 파일 삭제로 재현 불가)

작성 당시(2026-10-03) 아래 결과를 적었으나, 근거가 된 `_workspace/reference-app/`(규칙 파일, `tests/rules.test.mjs`, `tests/logic.test.mjs`)이 삭제되어 지금은 다시 실행하거나 확인할 수 없다. 그래서 모두 **재확인 필요**로 분류한다. 이 결과를 "통과했다"는 근거로 슬라이드나 강사 안내에 인용하지 않는다.

| 당시 확인 | 당시 방법 | 당시 결과 | 현재 분류 |
|---|---|---|---|
| 이 문서 5절·7절 규칙 = 참고 코드의 규칙 파일 | `diff` | 같음 | 재확인 필요(참고 파일 삭제. 지금은 이 문서 본문이 유일한 기준) |
| 최종 규칙 동작(users·classes·members·materials·worksheets·submissions, 컬렉션 그룹 조회) | 에뮬레이터 + `rules.test.mjs` | 9개 통과 | 재확인 필요 |
| 임시 규칙: 로그인 안 하면 거부, 모듈 3~6 흐름 허용 | 같은 테스트 파일 | 2개 통과 | 재확인 필요 |
| 수업코드 생성·형식 검사, 학습지 검사, 답안 정리, 정답 비교, 피드백 초안 형식 | `logic.test.mjs` | 10개 통과 | 재확인 필요 |

재확인 방법: 연수 전 강사 리허설에서 실제 프로젝트에 5절 규칙을 게시하고 `rules-check.html`로 막힘 6개·열림 2개를 확인한다(prompts 문서 0-0절). 원하면 강사가 에뮬레이터 테스트를 새로 만들어 돌릴 수 있으나, 이번 작업 범위에서는 만들지 않았다.

### 9-1b. 현재 근거: 검수자의 규칙 본문 논리(정적) 검토 (`03_reviewer_report.md` 4절)

규칙 본문(5절)을 줄 단위로 읽은 결과다. **실행 근거는 아니지만** 지금 확인할 수 있는 유일한 근거다.

| 확인 내용 | 판정 | 근거(규칙 줄) |
|---|---|---|
| 원칙 1: 미가입 학생의 자료·학습지 읽기 차단 | 성립 | `materials`/`worksheets` `allow read: if isTeacher(classId) \|\| isMember(classId)`. `isMember`는 `members/{me()}` 존재, `members` create는 `uid == me()`라 남의 이름으로 가입 불가 |
| 원칙 2: 학생 간 제출물 열람 | 차단 성립 | `submissions` get은 교사 또는 `uid == me() && isMember`, list는 교사만 |
| 원칙 2: 학생의 feedback 쓰기 | 차단 성립 | create `onlyKeys(['answers','submittedAt'])`, update `changedOnly(['answers','submittedAt'])`. 덮어쓰기로 feedback을 지우면 affectedKeys에 feedback이 들어가 거부. merge 재제출은 통과(D5) |
| 교사의 답안 수정 | 차단 성립 | 교사 update는 `changedOnly(['feedback'])` |
| 원칙 3: 수업 만들기 | 성립 | create에 `role == 'teacher'`, `teacherUid == me()`, `joinCode == classId`, 형식 `^[A-HJ-NP-Z2-9]{6}$`. 같은 코드가 이미 있으면 update로 판정되어 남의 수업은 거부 |
| 원칙 3: 자료·학습지 쓰기 | 성립 | `isTeacher(classId)` = 수업 문서 `teacherUid == me()` |
| role 변경 차단 | 성립 | users update `role == resource.data.role`, delete 규칙 없음 |
| 원칙 4: 코드로 get 허용, list 제한 | 성립 | `classes` get `signedIn()`, list `resource.data.teacherUid == me()` |
| members 컬렉션 그룹 조회 노출 범위 | 본인 문서만 | `{path=**}/members` list `resource.data.uid == me()`. create가 `uid` 필드 = 문서 이름 = 나를 강제 |
| `get()`/`exists()` 호출 수 | 한도 안 | 최대 3회, 공식 한도(단일 문서·쿼리 요청 10회) |
| 원칙 5 sandbox | 성립(화면 쪽) | 슬라이드 30 프롬프트가 값 없는 `sandbox` + `srcdoc` + innerHTML 금지 |
| 비밀키 | 통과 | firebaseConfig만 브라우저, AI 키는 `defineSecret`/`secrets:set`, 복구 폴더에 비밀 값 없음 |

### 9-1c. 지금도 유효한 확인
| 확인 | 방법 | 결과 |
|---|---|---|
| CDN 주소 `https://www.gstatic.com/firebasejs/12.19.0/firebase-{app,auth,firestore,functions}.js` | `curl`(검수 단계에서 다시 확인) | 4개 모두 HTTP 200 |
| 공식 문서로 확인된 사실: 2025-04-28 이후 프로젝트에 `localhost` 기본 미포함, 문서 최대 1MiB, 규칙 호출 한도 10회, Functions 배포에 Blaze 필요, 색인 삭제 질문 원문 | 검수 보고서 2절 대조표 | 확인됨 |

### 9-2. 미검증 (실제 Firebase 프로젝트·콘솔·결제가 필요해 확인하지 못함)

1. **색인:** 에뮬레이터는 색인을 요구하지 않는다. 학생 목록의 컬렉션 그룹 조회(`members.uid`)가 실제 프로젝트에서 색인 오류를 내는지, 오류 문구·링크 모양, 색인 생성 소요 시간, `firestore.indexes.json`의 `fieldOverrides` 배포가 그 색인을 만드는지.
2. 색인 삭제 질문: 문구는 firebase-tools 소스로 확인됨("The following indexes are defined in your project but are not present in your firestore indexes file … Would you like to delete these indexes? Selecting no will continue the rest of the deployment."). 실제 프로젝트에서 이 질문이 나오는지, `--only firestore:rules`가 색인을 건드리지 않는지는 미검증.
3. 실제 프로젝트에 규칙을 게시했을 때 규칙 편집기(콘솔)가 이 규칙을 문법 오류 없이 받는지. (당시 에뮬레이터 통과 기록은 9-1에 따라 재확인 필요)
4. 승인된 도메인: **2025-04-28 이후 만든 프로젝트에는 `localhost`가 기본으로 없다(공식 문서로 확인).** 그래서 슬라이드 12에서 참가자가 직접 추가한다. 미검증으로 남는 것은 구글 팝업 로그인 실제 동작, Hosting 배포 후 `*.web.app`·`*.firebaseapp.com` 자동 등록 여부다.
5. file:// 로 열었을 때 로그인·모듈 로딩이 실패하는 정확한 증상(크롬 기준 모듈 스크립트 CORS 차단으로 예상).
6. 90만 바이트(UTF-8) 제한으로 충분한지(슬라이드 29 기준. 문서 최대 1MiB = 1,048,576바이트는 공식 문서로 확인됨. "한글 위주 약 30만 글자"는 노트용 환산).
7. 한국어 콘솔 메뉴 이름(공식 문서 영문 기준 `Security > Authentication`, `Databases & Storage > Firestore`), 규칙 탭 게시 버튼의 한국어 이름, 문서 삭제 메뉴, 테스트 모드 공개 기간 표현.
8. sandbox iframe(값 없음)에서 샘플 자료의 버튼이 실제로 동작하지 않는지 크롬 최신판에서 눈으로 확인. `allow-scripts`+`allow-same-origin` 동시 부여 시 sandbox 해제 가능은 MDN 경고 문구 기준(브라우저 실측 아님).
9. 심화(슬라이드 45): Blaze 필요, `asia-northeast3` 지역, 비밀 값 등록 명령은 공식 문서로 확인됨. 무료 사용량·AI API 비용, 함수의 실제 배포·호출은 미검증(예전 함수 코드 `reference-app/advanced-ai-feedback/`은 삭제됨).
10. 규칙 `get()`/`exists()` 호출 수: 검수자 정적 검토로 최대 3회, 공식 한도 10회 안(9-1b). 실측은 하지 않음.

(예전 항목 "대안 B(D2 명세 미승인 시)"는 명세가 승인·반영되어 삭제했다.)
