#!/bin/bash
set -euo pipefail

dir=$1

log() {
    echo -e "\n[ $(date '+%Y-%m-%d %H:%M:%S') ] $1"
}


# 인자가 비어있는지 확인
if [ -z "${dir}" ]; then
    echo "실행방법; $0 <프로젝트 폴더명>"
    exit 1
fi
log "스크립트 시작 - 프로젝트 폴더명: ${dir}"


# 시스템 패키지 설치
sudo apt update
sudo apt install -y \
  git curl \
  build-essential python3-dev pkg-config \
  libopus-dev libvpx-dev \
  libffi-dev libssl-dev \
  ffmpeg libavdevice-dev libavfilter-dev libavformat-dev \
  libavcodec-dev libswscale-dev libavutil-dev \
  libsrtp2-dev \
  python3-venv
log "필수 시스템 패키지(apt) 설치 완료"


# 프로젝트 폴더 생성
cd ~/Desktop
# 기존 폴더가 있으면 삭제
if [ -d "${dir}" ]; then
    log "기존 폴더 ${dir} 삭제"
    rm -rf "${dir}"
fi
mkdir -p "${dir}"

# 깃허브 레포지토리 클론
git clone https://github.com/happine2s/mandro-server.git "${dir}"
log "깃허브 레포지토리 클론 완료"

# 파이썬 가상환경 만들기
log "파이썬 가상환경 생성"
cd "${dir}"
python3 -m venv --system-site-packages venv
source venv/bin/activate
log "가상환경 활성화됨"

# include-system-site-packages = true 확인
cd "venv"
cfg_file="pyvenv.cfg"
value=$(grep "^include-system-site-packages" "$cfg_file" | awk -F= '{print $2}' | tr -d '[:space:]')

if [ "${value}" != "true" ]; then
    log "include-system-site-packages 값이 true가 아님 (현재: ${value})"
    exit 1
fi
log "include-system-site-packages = true 확인 완료"


# 필요한 패키지 설치
log "필요한 패키지 설치 시작"
pip install \
aiortc==1.10.0 \
av==13.0.0 \
flask \
pyee \
google-crc32c \
pylibsrtp \
pyopenssl \
aioice \
dnspython \
typing-extensions \
"numpy<2" \
opencv-python-headless==4.7.0.72 \
fastapi \
"uvicorn[standard]" \
python-multipart
log "패키지 설치 완료"

# 카메라 모듈 패키지 정상작동 확인
log "카메라 모듈 패키지 정상작동 확인"
result=$(python3 -c "import libcamera; print('OK')" || echo "FAIL")
if [ ${result} == "OK" ]; then
	log "카메라 모듈 정상작동"
else
	log "카메라 모듈 오류 - 스크립트 종료"
	exit 1
fi
