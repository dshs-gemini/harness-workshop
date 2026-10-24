---
name: firebase-classroom-spec
description: Firebase + 구글 로그인 + 수업코드 수강신청 + HTML 수업자료 등록 + 웹 학습지 + 개인별 맞춤 피드백으로 구성된 온라인 클래스룸의 기능 명세, 데이터 모델, 보안 규칙 원칙을 제공한다. 클래스룸 연수 콘텐츠나 실습 코드를 만들거나 검수할 때 반드시 사용한다.
---

# 온라인 클래스룸 기능 명세

연수 콘텐츠의 모든 에이전트는 이 명세를 단일 기준으로 삼는다. 기준이 하나여야 슬라이드, 프롬프트, 완성본이 어긋나지 않는다.

## 기능과 모듈 대응
| 기능 | 핵심 개념(정의) | 산출물 |
|---|---|---|
| 구글 로그인 | Firebase Authentication (사용자 인증, uid 발급) | 로그인/로그아웃, 역할(교사/학생) 구분 |
| 수업코드 수강신청 | Firestore + 코드 입력 (수업 문서 이름=수업코드로 조회) | 교사가 수업 생성 → 코드 발급, 학생이 코드로 가입 |
| HTML 수업자료 등록 | Firestore 문서 또는 Storage | 교사가 HTML 업로드, 학생이 수업별 열람 |
| 웹 학습지 | 문항 문서 + 제출 문서 | 문항 작성, 학생 제출, 교사 확인 |
| 개인별 맞춤 피드백 | 서버 함수에서 AI 호출 | 제출 답안 기반 개인 피드백 저장·표시 |

## 데이터 모델 (Firestore)
- `users/{uid}`: name, email, role
- `classes/{classId}`: title, teacherUid, joinCode (문서 이름 classId를 수업코드와 같게 한다. 학생은 `classes/{코드}` 1건만 읽는다)
- `classes/{classId}/members/{uid}`: uid, joinedAt (uid 필드는 '내가 가입한 수업' 목록을 컬렉션 그룹 조회로 찾기 위한 것이며 색인 1개가 필요하다)
- `classes/{classId}/materials/{id}`: title, html, createdAt
- `classes/{classId}/worksheets/{id}`: title, questions[]
- `classes/{classId}/worksheets/{id}/submissions/{uid}`: answers, feedback, submittedAt

## 보안 규칙 원칙 (슬라이드에서 반드시 설명)
1. 학생은 자신이 가입한 수업의 자료만 읽는다.
2. 학생은 자기 제출물만 읽고 쓴다. 다른 학생의 제출물은 읽을 수 없다.
3. 수업·자료·학습지 작성은 해당 수업 교사만 한다.
4. 수업코드 조회는 가입 시점에만 허용하고, 수업 목록 전체 열람은 막는다.
5. 교사가 올린 HTML은 sandbox iframe으로 보여준다. 이유: 자료 속 스크립트가 로그인 정보에 접근하지 못하게 한다.

## 비밀 정보 원칙
- Firebase 웹 설정값은 공개되어도 되며 보안은 보안 규칙이 담당한다.
- AI API 키는 브라우저에 두지 않는다. Cloud Functions 같은 서버 쪽에 보관한다. (Cloud Functions 배포에는 Blaze(종량제) 요금제가 필요하다. 공식 문서로 확인됨. 무료 사용량과 최신 정책만 `[확인필요]`로 둔다.)

## 개인정보
학생 이름·이메일은 최소 수집하고, 연수 실습은 테스트 계정으로 진행하도록 안내한다. 실제 학생 데이터는 소속 기관의 개인정보 지침을 따른다.
