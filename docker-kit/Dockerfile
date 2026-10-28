FROM node:22-bookworm-slim

# 기본 도구: git(하네스 플러그인 설치에 필요), gh(GitHub), 편집기·검색 도구
RUN apt-get update && apt-get install -y --no-install-recommends \
      git ca-certificates curl less nano jq ripgrep gh \
    && rm -rf /var/lib/apt/lists/*

# Claude Code와 Firebase CLI 설치 (이미지를 만들 때 한 번만 실행됨)
ARG CLAUDE_CODE_VERSION=latest
RUN npm install -g @anthropic-ai/claude-code@${CLAUDE_CODE_VERSION} firebase-tools

# 로그인 정보가 저장될 폴더를 일반 사용자(node) 소유로 미리 만들어 둠
RUN mkdir -p /workspace /home/node/.claude /home/node/.config \
    && chown -R node:node /workspace /home/node/.claude /home/node/.config

# 컨테이너 안에서는 이미지가 버전을 고정하므로 자동 업데이트는 끈다
ENV DISABLE_AUTOUPDATER=1 \
    CLAUDE_CONFIG_DIR=/home/node/.claude

USER node
WORKDIR /workspace
CMD ["claude"]
