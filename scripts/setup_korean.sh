#!/bin/bash
set -e

# 현재 로케일 확인
CURRENT_LOCALE=$(locale | grep "^LANG=" | cut -d= -f2)

if [ "$CURRENT_LOCALE" = "ko_KR.UTF-8" ]; then
    echo "이미 한국어(ko_KR.UTF-8)로 설정되어 있습니다."
    exit 0
fi

echo "한국어(ko_KR.UTF-8)로 변경합니다."

# 한국어 설치 및 변경
sudo apt update && sudo apt install -y locales
sudo locale-gen ko_KR.UTF-8
sudo update-locale LANG=ko_KR.UTF-8

echo "변경 완료. 3초 후 재부팅합니다..."
for i in 3 2 1
do
    echo "$i..."
    sleep 1
done

sudo reboot