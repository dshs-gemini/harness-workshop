# Claude Code Docker 키트

Windows에서 네이티브 설치가 막힐 때, Docker 컨테이너 안에서 Claude Code를 실행하는 키트입니다.
자세한 설명은 상위 폴더의 `클로드코드_Docker_사용가이드.html`을 보세요.

## 구성

| 파일 | 역할 |
| --- | --- |
| `Dockerfile` | Node 22 + git + gh + Claude Code + Firebase CLI가 든 이미지 설계도 |
| `compose.yaml` | `work` 폴더 공유, 로그인 정보 볼륨 2개 |
| `work/` | 실습 파일을 두는 폴더 (컨테이너의 `/workspace`) |

## 사용

Docker Desktop을 켠 뒤, 이 폴더에서:

```
docker compose build          # 처음 한 번
docker compose run --rm claude                                   # Claude Code 시작
docker compose run --rm claude firebase login --no-localhost     # Firebase 로그인
```

## 검증 범위

macOS(Apple Silicon), Docker Desktop 29.4에서 빌드·실행 확인. Windows 실기와 계정 로그인 완료는 미검증.
