# 듀얼 카메라 스트리밍 서비스

라즈베리파이에 연결된 **카메라 모듈 2개**를 FastAPI 서버로 제어하고 WebView를 통해 실시간 스트리밍과 설정 조작을 할 수 있는 시스템입니다. 모든 환경 구성은 제공된 셸 스크립트로 자동화할 수 있습니다.

---

## 📌 프로젝트 개요

Raspberry Pi와 FastAPI를 이용해 **듀얼 카메라 스트리밍 서버**를 구성합니다.  
제공된 스크립트(`setup_korean.sh`, `setup_env.sh`, `register_service.sh`)로 환경을 구성할 수 있으며, 이후 systemd 서비스로 등록되어 부팅 시 자동 실행됩니다.

카메라 영상은 WebSocket을 통해 실시간으로 스트리밍되며, `/config` API로 간격(gap)과 좌우 반전(distorted) 설정을 제어할 수 있습니다.  
또한 `/health`, `/version` API를 제공해 서버 상태와 버전을 확인할 수 있습니다.


## 🚀 주요 기능

- **실시간 카메라 스트리밍**
  - WebSocket(`/ws/stream/0`, `/ws/stream/1`)을 통해 Base64 JPEG 전송
- **보정값 설정**
  - `POST /config` (Form 데이터)
  - `GET /config`
  - gap(px 단위 간격), 좌우반전(distorted) 값 적용
- **health 체킹**
  - `GET /health` → `{ "status": "ok" }`
  - `GET /version` → `{ "project": "camera", "mode": "V1" }`

---

## 🛠 기술 스택

| 구분         | 사용 기술 |
|--------------|--------------------------|
| **하드웨어** | Raspberry Pi, Picamera2 |
| **프레임워크** | FastAPI, uvicorn |
| **라이브러리** | OpenCV (cv2), libcamera, numpy, python-multipart |
| **빌드/운영** | systemd, Bash Shell Script |

## 🗺️ 아키텍처 다이어그램
![mandro](https://github.com/user-attachments/assets/a42afb2d-4d1e-4083-8b8f-c9ad35eabb6c)


## 📂 프로젝트 구조

```bash
mandro-server/
├── app/
│   ├── routers/
│   │   ├── config.py          # /config API
│   │   ├── health.py          # /health, /version
│   │   └── stream.py          # /, /ws/stream/{index}
│   ├── camera/
│   │   └── camera_manager.py  # Picamera2 제어
│   └── static/
│       └── stream.html        # 스트리밍 UI
├── scripts/
│   ├── register_service.sh    # systemd 서비스 등록 및 실행
│   ├── setup_env.sh           # 환경 세팅 (apt, pip, venv 등)
│   └── setup_korean.sh        # 한글 환경 세팅
├── main.py                    # FastAPI 앱 실행 진입점
└── README.md
```

---

## ⚡️ 환경 구성 방법
### 1. 프로젝트 클론
```bash
cd ~/Desktop
git clone https://github.com/happine2s/mandro-server.git
cd mandro-server
```
### 2. 스크립트 실행 권한 부여
```bash
chmod +x scripts/setup_korean.sh
chmod +x scripts/setup_env.sh
chmod +x scripts/register_service.sh
```

### 3. 한글 환경 세팅(선택)
```bash
./scripts/setup_korean.sh
```
재부팅 후 프로젝트 경로로 이동
```bash
cd mandro-server
```

### 4. 개발 환경 세팅
```bash
./scripts/setup_env.sh
```

### 5. systemd 서비스 등록 및 실행
```bash
./scripts/register_service.sh <서비스명> <포트번호>
```
- <서비스명>: systemd에 등록할 이름 (ex: mandro)
- <포트번호>: FastAPI 서버 포트 (ex: 8000)
