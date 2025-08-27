# 듀얼 카메라 스트리밍 서비스

라즈베리파이에 연결된 **카메라 모듈 2개**를 FastAPI 서버로 제어하고 WebView를 통해 실시간 스트리밍과 설정 조작을 할 수 있는 시스템입니다. 모든 환경 구성은 제공된 셸 스크립트로 자동화할 수 있습니다.

---

## 📌 프로젝트 개요

Raspberry Pi와 FastAPI를 이용해 **듀얼 카메라 스트리밍 서버**를 구성합니다.  
제공된 스크립트(`setup_korean.sh`, `setup_env.sh`, `register_service.sh`)로 환경을 구성할 수 있으며, 이후 systemd 서비스로 등록되어 부팅 시 자동 실행됩니다.

카메라 영상은 WebSocket을 통해 실시간으로 스트리밍되며, `/config` API를 통해 다양한 카메라 상태(간격, 반전, 회전, 해상도, 순서 등)를 제어하고 저장할 수 있습니다.
또한 `/health`, `/version` API를 제공해 서버 상태와 버전을 확인할 수 있습니다.


## 🚀 주요 기능

- **실시간 카메라 스트리밍**
  - WebSocket(`/ws/stream/0`, `/ws/stream/1`)을 통해 바이너리 전송
  - UI에서 두 카메라를 동시에 확인 가능
- **카메라 상태 제어 및 저장**
  - `POST /config`, `GET /config`  
  - 제어 가능한 항목:
    - **간격 (gap)**: 카메라 화면 간 여백(px 단위) 조절
    - **좌우 반전 (flip)**: 영상 좌우 반전
    - **화면 회전 (rotate)**: 90° 단위 회전
    - **해상도 (resolution)**: 4:3 비율 (320×240, 640×480, 960×720)
    - **카메라 순서 (order)**: 두 카메라 화면 순서 교체
  - 모든 설정은 서버에 저장되어 재접속 시에도 유지됨
- **health 체킹**
  - `GET /health` → `{ "status": "ok" }`
  - `GET /version` → `{ "project": "camera", "mode": "V1" }`


## 🛠 기술 스택

| 구분         | 사용 기술 |
|--------------|--------------------------|
| **하드웨어** | Raspberry Pi, Picamera2 |
| **프레임워크** | FastAPI, uvicorn |
| **라이브러리** | OpenCV (cv2), libcamera, numpy, python-multipart |
| **빌드/운영** | systemd, Bash Shell Script |

## 🗺️ 아키텍처 다이어그램
![mandro (1)](https://github.com/user-attachments/assets/ed9564c3-a10d-46e7-84fc-8a5825109512)


## 📂 프로젝트 구조

```bash
mandro-server/
├── app/
│   ├── camera/
│   │   └── camera_manager.py   # Picamera2 제어
│   ├── routers/
│   │   ├── config.py           # /config API
│   │   ├── health.py           # /health, /version API
│   │   └── stream.py           # /, /ws/stream/{index}
│   ├── services/
│   │   └── config_service.py   # 설정 저장/조회 로직
│   ├── static/
│   │   ├── stream.html         # 스트리밍 UI
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── app.js
│   └── storage/
│       └── config.json         # 설정값 저장 파일
│   └── __init__.py
├── scripts/
│   ├── register_service.sh     # systemd 서비스 등록 및 실행
│   ├── setup_env.sh            # 환경 세팅 (apt, pip, venv 등)
│   └── setup_korean.sh         # 한글 환경 세팅
├── main.py                     # FastAPI 앱 실행 진입점
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
