# 02. 슬라이드 원고: M1 도입 · Claude Code 첫 대화 (슬라이드 1–9, 13분)

<!-- 연수 전체: 총 71장, 180분 -->

## 검수 반영
- (재검수 2회차) 슬라이드 4 노트·가정의 설치 명령 `[확인필요]` 삭제(공식 setup 문서와 일치, 검수 확인). 슬라이드 2 노트에 OS 요구사항(macOS 13.0 이상, Windows 10 1809 이상) 한 줄 추가. 번호·유형·분은 그대로.
- 복구 지점 안내 삭제
- (2026-10-28) Windows 설치가 막힐 때의 대안으로 Docker 경로 슬라이드 3장(5 개념, 6 빌드, 7 실행·로그인)을 4번 뒤에 추가. 기존 5·6은 8·9로, 뒤 모듈 번호는 모두 +3. 시간은 4번 4→2분, 8번(옛 5) 4→3분으로 줄여 M1 13분 유지. 원본은 `클로드코드_Docker_사용가이드.html`(보충 자료). Windows 실기 미검증은 `[확인필요]`.

## 가정
- 설계서 7절 M1 지시표의 번호·유형·분을 그대로 썼다(1+1+2+2+1+1+1+3+1 = 13분, 설명 5 / 실습 8). 5번(개념 1분)은 설명, 6~7번은 해당자만 4번·8번 시간에 병행하는 실습이다..
- 모듈 내용 모두 원본 `intro`, `t1-what`, `t1-install`에서 가져왔다. 원본 문장을 바꾼 곳은 노트에 "원본 대비 변경"을 남겼다.
- 연수 총 시간은 180분(원본의 3.5~4시간을 압축). 슬라이드 2의 "7개 모듈"은 설계서 모듈표(M1~M5, M6, M7)를 따른다.
- 확인필요 항목: 학교 PC 설치 권한, 학교 Workspace 계정의 프로젝트 생성 제한. (설치 명령 3종은 검수에서 공식 setup 문서와 일치 확인되어 태그 제거)

---

## [슬라이드 1] Claude Code로 배우는 하네스 엔지니어링
- 유형: 정리
- 본문: 클로드 코드 기반 하네스 엔지니어링 교원 연수 (180분)
  오늘 가져갈 것 3개: ① 하네스로 만든 팀을 쓰고 말로 고치는 경험(나의 Claude Code 작업 폴더) ② 우리 교과 단원 수업 패키지(슬라이드와 학생 워크북)를 Firebase Hosting 주소로 배포·확인한 결과 ③ Firebase 기능 지도
- 도식: 표지. 제목 아래에 "가져갈 것" 카드 3장을 가로로 나란히(폴더 아이콘 / 배포 주소 아이콘 / 지도 아이콘).
- 노트: 환영 인사. "오늘은 앱을 만드는 날이 아니라, 에이전트형 코딩 도구를 잘 쓰는 방법과 하네스 플러그인으로 에이전트 팀을 만들어 쓰고 고치는 방법을 배우는 날입니다." 오늘 끝나면 손에 남는 것 세 가지를 짚는다. 원본 intro의 목표(Track 1: 혼자 쓰기, Track 2: 하네스 활용)를 한 문장으로 요약해 말한다. 이 연수는 멀티 에이전트의 원리를 배우는 것이 아니라 하네스를 활용하는 연수라고 한 줄로 말한다. 원본 대비 변경: 원본의 책·오픈소스 소개 문단은 슬라이드 71(참고 자료)로 넘긴다. (1분)

## [슬라이드 2] 오늘의 지도
- 유형: 개념
- 본문: 앱은 예시 소재일 뿐, 배우는 것은 방법입니다.
  준비물 점검: 유료 Claude 계정 · 개인 구글 계정 · Git(하네스 설치에) · 결제 수단(Blaze 요금제에) · 실제 학생 정보는 쓰지 않기
- 도식: `.flow` 가로 도식, 8칸(휴식 포함). 첫 다섯 칸은 Claude Code 기본(M1 첫 대화 → M2 프롬프트 → M3 CLAUDE.md·스킬 → M4 하네스 입문 → M5 하네스가 만든 파일 고치기), 휴식, 이어서 M6 Firebase 지도(27분) → M7 수업 패키지 프로젝트(50분). 현재 위치(M1)를 강조색으로 표시.
- 노트: 로드맵을 한 번만 훑는다. 앞 절반은 "혼자 쓰는 법과 하네스로 팀 만들기·고치기", 뒤 절반은 "Firebase 기능 지도와 수업 패키지 프로젝트". 마지막 M7은 50분 동안 각자 자기 교과 단원의 슬라이드와 학생 워크북을 만드는 프로젝트이며, 전체는 180분이다. 클래스룸 앱은 "예를 들면"으로만 나온다고 못박는다. 사전 준비 점검(손들기): ① Claude Code는 Pro·Max·Team·Enterprise 또는 Console(API) 계정이 필요하고 무료 claude.ai 계정으로는 쓸 수 없다 ② Firebase 실습용 개인 구글 계정(학교 관리 계정은 프로젝트 생성이 막혀 있을 수 있음 `[확인필요]`) ③ 실제 학생 이름·계정은 쓰지 않는다 ④ Git: Claude Code 설치에는 필요 없지만 하네스 플러그인 설치(M4 25번)에는 필수다. `git --version`으로 확인하고, Windows는 없으면 Git for Windows를 설치한다(슬라이드 4) ⑤ Node.js·Firebase CLI는 M6 50번에서 함께 설치하고 로그인한다. 미리 설치해 두면 시간이 남는다. 없으면 50번 막힐 때를 따른다 `[확인필요: 학교 PC 설치 권한]`. ⑥ 결제 수단: M6 45번에서 Firebase 테스트 프로젝트를 Blaze 요금제로 바꾸고 Storage·Cloud Functions를 함께 해 본다. Blaze는 결제 수단 등록이 필수이므로 **본인 개인 계정에 본인 결제 수단**을 준비해 오게 한다(학교 카드·타인 카드 금지). 무료 사용량 안에서는 비용이 0일 수 있으나 예산 알림을 먼저 걸고, 연수 후 테스트 프로젝트를 삭제한다. 결제 수단을 쓰고 싶지 않은 참가자는 짝 화면을 보며 따라간다. 학교 관리 PC는 관리자 권한 설치 제한이 있을 수 있다(원본 intro). ⑦ Windows에서 설치 명령이 막히면: Docker Desktop을 쓰는 대안 경로(슬라이드 5~7)가 있다. Docker Desktop 설치(약 10~15분, WSL 2·가상화 필요)는 연수 시간에 하기에 길어서 사전 과제로 안내한다 `[확인필요: 학교 PC 설치 권한·가상화]`. OS 요구사항: macOS 13.0 이상, Windows 10(1809) 이상. 원본 대비 변경: 원본의 "3.5~4시간, Track 1·2" 구성은 180분 7개 모듈(총 71장)로 재구성했다. (1분)

## [슬라이드 3] 채팅 AI와 Claude Code는 무엇이 다른가
- 유형: 개념
- 본문: 채팅 AI는 답을 주고, Claude Code는 직접 해 봅니다.
  Claude Code는 터미널에서 동작하는 에이전트형 코딩 도구로, 파일 읽기·수정과 명령 실행을 도구 호출로 수행합니다.
  (에이전틱 루프 = 모델이 도구를 호출하고, 결과를 관찰해 다음 행동을 정하는 반복)
- 도식: 카드 2장 비교. 왼쪽 "일반 채팅 AI: 묻고, 복사하고, 붙여넣는다"(회색 태그), 오른쪽 "Claude Code: 직접 읽고, 쓰고, 실행한다"(초록 `good` 태그). 아래에 순환 화살표 한 줄: 해 보기 → 결과 보기 → 다음 행동.
- 노트: 채팅 AI는 텍스트로 답을 돌려주고, Claude Code는 도구 호출로 작업을 직접 수행한다. 채팅은 결과를 내가 저장·실행하고 오류도 내가 다시 붙여넣어야 한다. Claude Code는 내 컴퓨터의 실제 폴더에서 파일을 읽고 쓰고 명령을 실행하며 오류까지 스스로 확인한다. 사람은 결과를 검토하고 승인하는 역할이다. 이 루프를 에이전틱 루프라고 부른다. 반드시 말할 것: "이름은 코드지만 수업 자료(HTML, 문항)를 만드는 데 쓴다." 예: 만든 HTML 파일의 문법 오류를 명령줄에서 검사하게 시킬 수 있다. 터미널 CLI 외에 데스크톱 앱, VS Code·JetBrains 확장, 웹(claude.ai/code)도 있으나 오늘은 터미널 CLI 기준이다(한 번 익히면 다른 형태로 넘어가기 쉽다). (2분)

## [슬라이드 4] 터미널을 열고 설치 확인하기
- 유형: 실습
- 본문: ① 터미널 열기: macOS는 `⌘+Space`에서 "터미널", Windows는 시작 메뉴에서 "PowerShell"
  ② 아래 명령으로 버전이 보이면 이미 설치된 것입니다.
  (터미널 = 말로 시키는 대신 글자로 명령하는 창)
  ③ Git도 필요합니다. Claude Code 설치에는 필요 없지만, 하네스 플러그인 설치(M4)에 필수입니다. `git --version`에 버전이 보이면 준비 완료. Windows에서 없으면 Git for Windows를 먼저 설치합니다.
- 도식: OS 탭 없이 터미널 화면 예시 1장(커서 깜빡이는 창). 아래에 "미설치자용 설치 명령" `.code-block` + OS 탭 3개(macOS / Linux, Windows PowerShell, Windows CMD).
- 프롬프트: (터미널에 입력. Claude Code에 붙여넣는 문장이 아니라 터미널 명령)
  ```
  claude --version
  git --version
  ```
  미설치자용 설치 명령(OS 탭):
  - macOS / Linux: `curl -fsSL https://claude.ai/install.sh | bash`
  - Windows PowerShell: `irm https://claude.ai/install.ps1 | iex`
  - Windows CMD: `curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd`
- 예상 결과:
  ```
  $ claude --version
  2.1.211 (Claude Code)
  $ git --version
  git version 2.45.0
  ```
  `2.1.211`과 `2.45.0`은 예시 숫자입니다. 내 화면의 번호는 달라도 됩니다. 두 명령 모두 버전 번호가 보이면 성공입니다.
- 막힐 때:
  - `command not found` → 터미널을 완전히 닫았다가 다시 엽니다.
  - `git`을 찾을 수 없다고 나옴 → Windows는 Git for Windows(git-scm.com/downloads/win)를 설치하고 터미널을 새로 엽니다. 설치하지 않으면 M4 25번 플러그인 설치에서 `Failed to clone marketplace repository: Command 'git' not found`로 막힙니다.
  - Windows에서 `irm`이 "인식할 수 없는 명령" → CMD입니다(프롬프트가 `C:\>`). PowerShell(`PS C:\>`)에서 PowerShell 탭 명령을 씁니다.
  - 설치 명령이 계속 오류(`403`, TLS, PATH 등) → 다음 슬라이드 5~7의 Docker 경로(이미지 만들기와 실행)로 바꿉니다.
- 노트: 이미 설치한 분이 대부분이므로 `claude --version`만 확인시키고 끝낸다. 미설치자는 OS 탭에서 자기 명령을 복사해 붙여넣고 Enter. Git은 Claude Code 설치에는 필요 없지만, 이 연수의 하네스 플러그인 설치(M4 25번의 `/plugin marketplace add revfactory/harness`)에는 필수다. 마켓플레이스를 GitHub 저장소에서 git으로 내려받기 때문이다. 공식 문서(plugin 문서와 troubleshooting, 2026-10-25 확인)에 따르면 Windows에서 git이 없으면 마켓플레이스 등록이 `Failed to clone marketplace repository: Command 'git' not found or is in an unsafe location`로 실패하고, 해결은 Git for Windows(https://git-scm.com/downloads/win) 설치 후 다시 시도하는 것이다. 그래서 M1에서 `git --version`으로 미리 확인시킨다. macOS·Linux도 같은 명령으로 확인하고, 없으면 설치 방법을 Claude Code나 강사에게 묻는다 `[확인필요: OS별 git 기본 설치 여부]`. Git for Windows가 있으면 Claude Code가 Git Bash로 Bash 도구를 쓸 수 있다(없으면 PowerShell 도구로 대신). 학교 PC에서 설치 권한이 없으면 짝 화면을 함께 보거나 강사 화면을 따라 본다. macOS는 공식 설치 스크립트(네이티브 설치)를 권장하며 Node.js를 먼저 깔 필요가 없다(원본). 프롬프트가 `PS`로 시작하면 PowerShell, `C:\>`만 보이면 CMD. 설치 명령 3종은 원본 그대로 옮겼고 공식 setup 문서와 일치한다(검수 확인). 학교 관리 PC에서 설치가 막히면 짝 화면 함께 보기, 강사 화면 따라 보기로 전환한다. 원본 대비 변경: 원본 1~3단계를 한 장으로 합쳤고 1단계 터미널 열기는 본문으로 압축. 설치 오류가 계속되는 Windows 참가자는 여기서 멈추지 말고 슬라이드 5~7의 Docker 경로로 안내한다. (2분)

## [슬라이드 5] Windows 설치가 막히면: Docker로 쓰는 대안
- 유형: 개념
- 본문: 설치 스크립트 대신, 작은 리눅스 환경(컨테이너) 안에서 Claude Code를 실행합니다.
  Dockerfile로 이미지를 한 번 만들면(빌드) Claude Code·Git·Node.js·Firebase CLI가 들어 있어 설치 오류, PATH, Git Bash 문제가 생길 자리가 없습니다.
  대신 Docker Desktop 설치가 필요합니다. 4번 설치가 막힌 Windows 참가자만 6~7번을 따라 하고, 이미 설치한 분은 8번으로 갑니다.
  단계별 설명서: [dshs-gemini.github.io/harness-workshop/docker](https://dshs-gemini.github.io/harness-workshop/docker/)
- 도식: 2열 카드. 왼쪽 `good` "사라지는 문제": 설치 명령 오류(`irm`·`403`·TLS), `claude`를 못 찾음(PATH), Git for Windows 설치, Node.js·Firebase CLI 설치. 오른쪽 "새로 생기는 조건": Docker Desktop 설치(WSL 2·가상화), 디스크 약 3GB와 RAM 8GB 이상, 학교 네트워크 차단은 그대로. 아래에 가로 한 줄: 내 PC의 `work` 폴더 ⇄ 컨테이너의 `/workspace`(이 폴더만 공유).
- 노트: 4번에서 설치가 막힌 Windows 참가자를 위한 대안 경로다. 나머지 참가자는 8번으로 바로 간다. 핵심 한 문장: "Docker는 설치 문제를 없애는 것이 아니라 'Docker Desktop 설치 한 번'으로 모아 준다." 컨테이너는 내 PC 안의 작은 리눅스 환경이고, Claude Code는 그 안에서 실행된다. 내 PC에서는 지정한 폴더(`work`) 하나만 공유되며, Claude Code가 만든 파일은 그 폴더에 그대로 나타난다. 이 경로는 두 단계다: 이미지를 한 번 만들고(빌드, 6번), 그 이미지로 Claude Code를 실행한다(7번). 이미지에 Git이 들어 있으므로 M4 25번의 하네스 플러그인 설치(`/plugin marketplace add`)도 Git for Windows 없이 된다. 한계: ① Docker Desktop은 Windows 10 22H2(빌드 19045) 이상 또는 Windows 11 23H2(빌드 22631) 이상, RAM 8GB, BIOS 가상화 사용이 필요하다(Docker 공식 문서). 가상화가 꺼져 있고 바꿀 수 없는 학교 PC에서는 Docker Desktop도 설치되지 않으므로 이때는 짝 화면을 함께 보거나 Claude 데스크톱 앱·웹 버전을 쓴다. ② Docker Desktop은 교육 목적에는 무료이지만 정부 기관은 유료 구독이 필요하다고 Docker 문서에 적혀 있어, 소속 기관 정책 확인이 필요하다 `[확인필요]`. ③ 학교 네트워크가 Docker Hub·npm·claude.ai를 막으면 똑같이 실패한다. Docker Hub는 로그인 없이 IP당 6시간에 100회까지만 내려받을 수 있어, 여러 명이 동시에 빌드하면 한도에 걸릴 수 있다. 그래서 빌드가 막히면 강사가 만든 이미지 파일(`claude-workshop.tar`)로 `docker load`를 쓴다(6번 막힐 때). 사전 준비: Docker Desktop 설치는 연수 전 과제로 안내한다. 이 경로의 파일(Dockerfile·compose.yaml)과 단계별 설명은 보충 자료 "Docker 사용 가이드"(https://dshs-gemini.github.io/harness-workshop/docker/)와 저장소의 `docker-kit/` 폴더에 있다. 슬라이드에서 링크를 누르면 열린다. 원본 대비 변경: 원본 HTML에 없는 내용으로, 공식 문서(Claude Code devcontainer·sandbox-environments·setup, Docker Desktop for Windows)와 macOS에서의 빌드 확인을 근거로 추가했다. Windows 실기 확인은 아직 하지 못했다 `[확인필요]`. (1분)

## [슬라이드 6] Docker 이미지 만들기: 빌드 (해당자만)
- 유형: 실습
- 본문: ① Docker Desktop을 켜고 'Engine running'이 보일 때까지 기다립니다.
  ② 강사가 준 `docker-kit` 폴더(Dockerfile, compose.yaml, work)를 `C:\claude-docker`에 두고, 그 폴더에서 PowerShell을 엽니다.
  ③ `docker compose build`를 실행합니다. Dockerfile대로 이미지를 만드는 과정이며, 처음 한 번만 합니다. 몇 분 걸립니다.
  ④ 마지막에 `Image claude-workshop Built`가 보이면 완료입니다.
- 도식: 가로 흐름 3칸. `Dockerfile`(설계도: Node 22 + Git·gh + Claude Code·Firebase CLI) → `docker compose build`(한 번 실행) → 이미지 `claude-workshop`(설치 완료본). 아래에 작은 글씨로 "이미지 = 설치 완료본, 컨테이너 = 그 이미지를 실행한 것(7번)".
- 프롬프트: (PowerShell에 입력)
  ```
  cd C:\claude-docker
  docker compose build
  docker images
  ```
  강사에게 이미지 파일(`claude-workshop.tar`)을 받았다면 빌드 대신 아래 명령으로 불러옵니다(빌드를 건너뜁니다).
  ```
  docker load -i claude-workshop.tar
  ```
- 예상 결과:
  ```
  Image claude-workshop Built
  REPOSITORY         TAG      SIZE
  claude-workshop    latest   1.8GB
  ```
  크기와 진행 로그는 PC마다 다를 수 있습니다. 중간에 진행 표시가 오래 멈춘 것처럼 보여도 정상일 수 있으니 몇 분은 기다립니다. 막히면 설명서: [dshs-gemini.github.io/harness-workshop/docker](https://dshs-gemini.github.io/harness-workshop/docker/)
- 막힐 때:
  - `docker`를 인식하지 못함 → Docker Desktop을 설치·실행했는지 확인하고 PowerShell을 새로 엽니다.
  - `Cannot connect to the Docker daemon` → Docker Desktop이 꺼져 있습니다. 켜고 'Engine running'이 될 때까지 기다립니다.
  - `no configuration file provided` 또는 Dockerfile을 못 찾음 → `Dockerfile`, `compose.yaml`이 있는 폴더에서 실행했는지 확인합니다. 메모장으로 만들었다면 `Dockerfile.txt`처럼 `.txt`가 붙지 않았는지 봅니다.
  - 빌드가 오류·시간 초과(`apt`·`npm`·`toomanyrequests`) → 학교 네트워크 차단이나 Docker Hub 한도일 수 있습니다. 개인 핫스팟으로 다시 하거나 강사의 이미지 파일로 `docker load`를 씁니다.
- 노트: 이 슬라이드는 4번에서 설치가 막힌 Windows 참가자만 따라 한다. 나머지는 8번으로 간다. 해당자는 4번과 8번 시간에 병행해서 하고, 진행자가 안내하는 시간은 1분이다. 키트 폴더는 강사가 미리 나눠 준다. 강조할 점: 빌드는 처음 한 번만 하면 되고, 이후에는 7번의 `docker compose run`만 쓴다. Dockerfile이 하는 일을 한 줄씩만 말한다: Node.js 22가 든 리눅스에서 시작 → Git·gh 설치 → npm으로 Claude Code와 Firebase CLI 설치 → 일반 사용자(root가 아님)로 실행. 이 파일들을 직접 쓰는 법은 다루지 않는다(복사해서 쓴다). 이미지는 설치 완료본이고 컨테이너는 그 이미지를 실행한 것이다. 이 Mac에서는 빌드가 약 1분 걸렸고 이미지가 1.8GB였다. 학교 네트워크나 Windows에서는 더 걸릴 수 있으므로 시간이 길어지면 앞 슬라이드 설명을 이어가며 기다린다. 이미지 파일을 쓰는 경우: Apple Silicon Mac에서 만든 이미지 파일은 Intel/AMD Windows에서 실행되지 않으므로, 강사는 Windows x64 PC에서 빌드해 `docker save claude-workshop -o claude-workshop.tar`로 만들거나 `--platform linux/amd64`로 빌드한다(약 487MB). 검증 범위: macOS(Apple Silicon)의 Docker Desktop 29.4에서 `docker compose build`, 실행, `docker save`/`docker load`를 확인했다. Windows 실기 빌드는 확인하지 못했다 `[확인필요: Windows 리허설]`. 원본 대비 변경: 원본에 없는 내용. (1분)

## [슬라이드 7] Docker로 Claude Code 시작하기 (해당자만)
- 유형: 실습
- 본문: ① Docker Desktop이 켜져 있는지 확인하고, 키트 폴더에서 PowerShell을 엽니다.
  ② 아래 명령으로 Claude Code를 시작합니다. 6번에서 만든 이미지로 새 컨테이너가 열립니다.
  ③ 터미널에 나온 로그인 주소를 복사해 브라우저에서 열고, 화면에 나온 코드를 터미널에 붙여넣습니다.
  ④ 종료는 `/exit`. 로그인과 `work` 폴더의 파일은 남습니다.
- 도식: 터미널 2단 화면. 위: `cd C:\claude-docker` → `docker compose run --rm claude`. 아래: Claude Code 입력 줄. 오른쪽에 폴더 연결 그림: `C:\claude-docker\work` ⇄ `/workspace`.
- 프롬프트: (PowerShell에 입력)
  ```
  cd C:\claude-docker
  docker compose run --rm claude
  ```
- 예상 결과: Claude Code 시작 화면이 나오고, 로그인하면 8번과 같은 첫 문장을 그대로 붙여넣을 수 있다. 컨테이너를 닫아도 로그인과 `work` 폴더의 파일은 남는다. 다음부터는 이 명령만 쓰면 된다(빌드는 다시 하지 않는다). 막히면 설명서: [dshs-gemini.github.io/harness-workshop/docker](https://dshs-gemini.github.io/harness-workshop/docker/)
- 막힐 때:
  - `Cannot connect to the Docker daemon` → Docker Desktop이 꺼져 있습니다. 켜고 'Engine running'이 될 때까지 기다립니다.
  - 이미지를 찾을 수 없다고 나오거나 빌드가 다시 시작됨 → 6번 빌드(또는 `docker load`)가 끝났는지 확인합니다.
  - 로그인 브라우저가 자동으로 안 뜸 → 정상입니다. 터미널의 주소를 직접 복사해 열고, 나온 코드를 터미널에 붙여넣습니다.
  - `docker compose down -v`는 쓰지 않습니다. 로그인 정보까지 지워집니다.
- 노트: 4번에서 설치가 막힌 Windows 참가자만 따라 한다. 나머지는 8번으로 간다. 해당자는 8번 시간에 병행하며, 진행자가 안내하는 시간은 1분이다. 작업 폴더는 `C:\claude-docker\work`이고 컨테이너 안에서는 `/workspace`다. 이 폴더의 파일만 내 PC와 공유되므로 수업 자료는 여기에 만든다. `--rm`은 닫을 때 컨테이너를 지운다는 뜻이며, 로그인 정보(`claude-config` 볼륨)와 `work` 폴더는 따로 보관되어 남는다. 로그인은 컨테이너에 브라우저가 없어서 주소를 직접 복사해 열어야 한다. 브라우저가 완료되지 않으면 화면에 코드가 나오며, 그 코드를 터미널의 `Paste code here if prompted`에 붙여넣는다(공식 devcontainer 문서 안내). 이 경로로 시작한 참가자는 이후 8번 첫 대화를 같은 화면에서 한다. Firebase CLI·Git·gh는 이미지에 들어 있어 M4 25번·M6 50번에서 따로 설치하지 않는다. `firebase login`은 브라우저가 없으므로 `firebase login --no-localhost`를 쓴다(M6 50번 막힐 때 참고). 검증 범위: macOS(Apple Silicon)의 Docker Desktop 29.4에서 실행을 확인했다(`claude --version` 2.1.312, Git·gh·Firebase CLI 동작, `work` 폴더 공유, 로그인 폴더 유지). Windows 실기와 계정 로그인 완료, 하네스 플러그인 설치, Firebase 로그인 완료는 확인하지 못했다 `[확인필요: Windows 리허설]`. 원본 대비 변경: 원본에 없는 내용. (1분)

## [슬라이드 8] 실습 폴더에서 첫 대화
- 유형: 실습
- 본문: 실습 폴더로 이동(`cd`)하고 `claude`를 실행합니다.
  처음이면 브라우저에서 로그인하고 터미널로 돌아옵니다.
  첫 문장을 그대로 붙여넣고 Enter.
- 도식: 터미널 2단 화면. 위: `cd` + `claude` 실행. 아래: `>` 입력 줄에 첫 문장 입력. 오른쪽에 "빈 폴더 `claude-training`"을 폴더 아이콘으로 표시.
- 프롬프트: (터미널에서 먼저 아래 두 줄 실행, 그 뒤 Claude Code 화면에 붙여넣기)
  ```
  cd Desktop/claude-training
  claude
  ```
  ```
  너는 지금 이 폴더에서 무엇을 할 수 있어? 교사인 내가 수업 자료를 만드는 걸 어떻게 도와줄 수 있는지 3가지만 예를 들어줘
  ```
- 예상 결과: Claude가 "이 폴더는 비어 있다", "파일을 만들고 실행할 수 있다"를 바탕으로 수업 자료 제작 예시 3가지를 구체적으로 제안한다. 이것이 이번 모듈의 산출물(실습 폴더에서 실행한 첫 대화 화면)이다. 응답 문구는 사람마다 다르다.
- 막힐 때:
  - 로그인 브라우저 창이 안 뜸 → 방화벽·보안 프로그램이 원인인 경우가 많습니다. 개인 핫스팟으로 잠시 시도합니다.
  - `cd`가 안 됨(폴더 없음) → 실습 폴더 `claude-training`을 바탕화면에 먼저 만듭니다. 경로가 다르면 폴더 위치를 확인합니다.
  - Docker 경로(5~7번)로 시작한 경우 → `cd`는 건너뜁니다. 7번에서 연 Claude Code 화면에 아래 첫 문장을 그대로 붙여넣습니다. 작업 폴더는 `C:\claude-docker\work`입니다.
- 노트: `cd`는 폴더를 이동하는 명령이다. 첫 실행 때 브라우저에서 Claude 계정으로 로그인하고 터미널로 돌아오면 현재 폴더 이름과 함께 대화 준비 화면이 나온다. 아직 파일이 없는 빈 폴더라서 "무엇을 할 수 있는지"를 묻는 것이 좋은 첫 질문이다. 프롬프트는 원본 그대로. 대화 중 화면을 잘 보도록 안내: 사람은 결과를 검토하고 승인하는 쪽이다. 폴더 이름 `claude-training`은 사전에 만들어 둔 것(원본 intro). 원본 대비 변경: 없음(4~5단계 압축). (3분)

## [슬라이드 9] 막히면 이렇게
- 유형: 정리
- 본문: 로그인 창이 안 뜨면 → 핫스팟 · `command not found` → 터미널 재시작
  Windows 설치 오류가 계속되면 → Docker 경로(5~7번), 설명서: [dshs-gemini.github.io/harness-workshop/docker](https://dshs-gemini.github.io/harness-workshop/docker/)
  대화를 끝낼 때는 `/exit` (또는 `Ctrl+D` 두 번)
- 도식: 3칸 표. 증상 / 해결 / 종료법. Windows 설치 오류 행의 해결 칸은 "Docker 경로(5~7번)". 아래 작은 상자에 짝 화면 함께 보기, 강사 화면 따라 보기 안내.
- 노트: 이 슬라이드는 실습 시간으로 센다. 막힌 참가자를 돌아보며 확인한다. 설치·로그인이 끝내 안 되는 분은 짝 화면을 함께 보거나 강사 화면을 따라 본다. 다음 모듈 예고: 잘 시키는 법(구체적 프롬프트, 컨텍스트, 플랜 모드). (1분)
