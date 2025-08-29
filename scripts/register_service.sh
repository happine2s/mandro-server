#!/bin/bash
set -euo pipefail

log() {
    echo -e "\n[ $(date '+%Y-%m-%d %H:%M:%S') ] $1"
}

svc=$1
port=$2

# 인자가 비어있는지 확인
if [ -z "${svc}" ] || [ -z "${port}" ]; then
    echo "실행방법; $0 <서비스명> <포트번호>"
    exit 1
fi
log "스크립트 시작 - 서비스: ${svc}, 포트: ${port}"


# uvicorn 설치 경로 어딘지 저장
cd "/home/$(whoami)/Desktop/mandro-server"
source venv/bin/activate

uvicorn_path=$(which uvicorn)

if [ ! -f "${uvicorn_path}" ]; then
  log "uvicorn 실행 파일이 존재하지 않습니다: ${uvicorn_path}"
  exit 1
fi

log "uvicorn 경로: ${uvicorn_path}"

# systemd 유닛 생성
log "systemd 유닛 파일 생성"
cat <<EOF | sudo tee /etc/systemd/system/${svc}.service > /dev/null
[Unit]
Description=Mandro FastAPI Server
After=network.target

[Service]
WorkingDirectory=/home/$(whoami)/Desktop/mandro-server
ExecStart=${uvicorn_path} app.main:app \
  --host 0.0.0.0 \
  --port ${port}
Restart=always
User=$(whoami)

[Install]
WantedBy=multi-user.target
EOF
log "systemd 유닛 파일 생성 완료"


# 서비스 등록 및 실행
log "서비스 등록 및 시작"
sudo systemctl daemon-reload
sudo systemctl enable "${svc}"
sudo systemctl restart ${svc}.service
log "서비스 등록 및 실행 완료"

# 상태 확인
sudo systemctl status "${svc}" --no-pager -l
