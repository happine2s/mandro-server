#!/bin/bash
set -e

# 현재 로케일 확인
CURRENT_LOCALE=$(locale | grep "^LANG=" | cut -d= -f2)

if [ "$CURRENT_LOCALE" = "ko_KR.UTF-8" ]; then
    echo "이미 한국어(ko_KR.UTF-8)로 설정되어 있습니다."
else
    echo "한국어(ko_KR.UTF-8)로 변경합니다."

    # locales 패키지 설치
    sudo apt update && sudo apt install -y locales

    # /etc/locale.gen에서 ko_KR.UTF-8 주석 해제
    if ! grep -q "^ko_KR.UTF-8 UTF-8" /etc/locale.gen; then
        sudo sed -i 's/^# *ko_KR.UTF-8 UTF-8/ko_KR.UTF-8 UTF-8/' /etc/locale.gen
    fi

    # 로케일 생성
    sudo locale-gen

    # 시스템 기본 로케일 변경
    sudo update-locale LANG=ko_KR.UTF-8
fi

# 한글 폰트 설치
echo "한글 폰트(Nanum, Unfonts)를 설치합니다."
sudo apt install -y fonts-nanum fonts-unfonts-core

# LXTerminal 폰트 설정
LXCONF="$HOME/.config/lxterminal/lxterminal.conf"
mkdir -p "$(dirname "$LXCONF")"

if grep -q "^font_name=" "$LXCONF" 2>/dev/null; then
    sed -i 's/^font_name=.*/font_name=NanumGothic 12/' "$LXCONF"
else
    echo "font_name=NanumGothic 12" >> "$LXCONF"
fi

echo "LXTerminal 기본 폰트를 NanumGothic 12로 설정했습니다."

echo "변경 완료. 3초 후 재부팅합니다..."
for i in 3 2 1
do
    echo "$i..."
    sleep 1
done

sudo reboot