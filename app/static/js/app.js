document.addEventListener("DOMContentLoaded", () => {
  const cam0 = document.getElementById("cam0");
  const cam1 = document.getElementById("cam1");
  const gapSlider = document.getElementById("gapSlider");
  const gapValue = document.getElementById("gapValue");
  const controls = document.querySelector(".controls");
  const isMobile = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
  let hideTimeout;

  // 상태를 JS에서 관리
  let cameraState = {
    gap: 0,
    cameras: {
      cam0: { order: 1, rotation: 0 },
      cam1: { order: 2, rotation: 0 }
    },
    stream: {
      resolution: [640, 480],
      quality: 80,
      fps: 30
    }
  };

  // 카메라 WebSocket 연결
  function connectCamera(index) {
    const ws = new WebSocket(`ws://${location.host}/ws/stream/${index}`);
    const img = document.getElementById(`cam${index}`);

    ws.binaryType = "arraybuffer";
    ws.onmessage = (event) => {
      const bytes = new Uint8Array(event.data);
      const blob = new Blob([bytes], { type: "image/jpeg" });
      img.src = URL.createObjectURL(blob);
    };

    ws.onclose = () => {
      console.warn(`Camera ${index} 연결 종료됨, 재연결 시도...`);
      setTimeout(() => connectCamera(index), 2000);
    };
  }

  // 서버에서 설정 불러오기
  async function loadConfig() {
    try {
      const res = await fetch("/config");
      const data = await res.json();
      cameraState = data;
      
      // gap UI 동기화
      gapSlider.value = cameraState.gap;
      gapValue.textContent = cameraState.gap;

      // 해상도 UI 값 동기화
      const [w, h] = cameraState.stream.resolution;
      document.getElementById("resolutionSelect").value = `${w}x${h}`;

      // 순서 UI 값 동기화
      const orderToggle = document.getElementById("orderToggle");
      orderToggle.checked = (cameraState.cameras.cam0.order === 2);

      applyCameraStyles();
    } catch (err) {
      console.error("설정 불러오기 실패:", err);
    }
  }

  // 카메라 상태 적용 (order, rotation, gap, crop)
  function applyCameraStyles() {
    const container = document.querySelector(".container");

    // gap > 0 → flex gap, gap < 0 → crop 후 밀착
    if (cameraState.gap > 0) {
      container.style.gap = `${cameraState.gap}px`;
    } else {
      container.style.gap = "0px"; // 음수일 때는 밀착
    }

    Object.entries(cameraState.cameras).forEach(([id, state]) => {
      const cam = document.getElementById(id);

      // 순서 적용
      cam.style.order = state.order;

      // 회전 적용
      cam.style.transform = `rotate(${state.rotation}deg)`;

      // @margin 초기화
      cam.style.margin = "0";

      // crop 적용 (gap < 0일 때만)
      if (cameraState.gap < 0) {
        const crop = Math.abs(cameraState.gap) / 2;
        let top = 0, right = 0, bottom = 0, left = 0;

        if (state.order === 1) { // 왼쪽 카메라
          if (state.rotation === 0) right = crop;
          if (state.rotation === 90) top = crop;
          if (state.rotation === 180) left = crop;
          if (state.rotation === 270) bottom = crop;
          
          // @왼쪽 카메라는 오른쪽으로 당김
          cam.style.marginRight = `${cameraState.gap}px`;

        } else { // 오른쪽 카메라
          if (state.rotation === 0) left = crop;
          if (state.rotation === 90) bottom = crop;
          if (state.rotation === 180) right = crop;
          if (state.rotation === 270) top = crop;

          // @오른쪽 카메라는 왼쪽으로 당김
          cam.style.marginLeft = `${cameraState.gap}px`;
        }

        cam.style.clipPath = `inset(${top}px ${right}px ${bottom}px ${left}px)`;
      } else {
        cam.style.clipPath = "none"; // crop 해제
      }
    });
  }

  // 이벤트 핸들러
  gapSlider.addEventListener("input", (e) => {
    cameraState.gap = parseInt(e.target.value, 10);
    gapValue.textContent = cameraState.gap;
    applyCameraStyles();
  });

  document.getElementById("rotateCam0").addEventListener("click", () => {
    cameraState.cameras.cam0.rotation =
      (cameraState.cameras.cam0.rotation + 90) % 360;
    applyCameraStyles();
  });

  document.getElementById("rotateCam1").addEventListener("click", () => {
    cameraState.cameras.cam1.rotation =
      (cameraState.cameras.cam1.rotation + 90) % 360;
    applyCameraStyles();
  });

  document.getElementById("orderToggle").addEventListener("change", (e) => {
    if (e.target.checked) {
      cameraState.cameras.cam0.order = 2;
      cameraState.cameras.cam1.order = 1;
    } else {
      cameraState.cameras.cam0.order = 1;
      cameraState.cameras.cam1.order = 2;
    }
    applyCameraStyles();
  });

  // 해상도 이벤트 핸들러
  document.getElementById("resolutionSelect").addEventListener("change", (e) => {
    const [w, h] = e.target.value.split("x").map(Number);
    cameraState.stream.resolution = [w, h];
  });

  // 서버에 설정 저장
  document.getElementById("saveBtn").addEventListener("click", async () => {
    try {
      const formData = new FormData();
      formData.append("gap", cameraState.gap);

      formData.append("cam0_order", cameraState.cameras.cam0.order);
      formData.append("cam0_rotation", cameraState.cameras.cam0.rotation);

      formData.append("cam1_order", cameraState.cameras.cam1.order);
      formData.append("cam1_rotation", cameraState.cameras.cam1.rotation);

      // stream 관련 값 추가
      formData.append("stream_width", cameraState.stream.resolution[0]);
      formData.append("stream_height", cameraState.stream.resolution[1]);
      formData.append("stream_quality", cameraState.stream.quality);
      formData.append("stream_fps", cameraState.stream.fps);

      const res = await fetch("/config", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();

      console.log("설정 저장 완료:", data);
      showToast("설정이 저장되었습니다.");
    } catch (err) {
      console.error("저장 실패:", err);
      showToast("저장 실패. 서버를 확인하세요.");
    }
  });

  // 토스트 메시지
  function showToast(message) {
    let toast = document.querySelector(".toast");
    if (!toast) {
      toast = document.createElement("div");
      toast.className = "toast";
      document.body.appendChild(toast);
    }
    toast.textContent = message;
    toast.classList.add("show");
    setTimeout(() => toast.classList.remove("show"), 2000);
  }

  // 실행
  connectCamera(0);
  connectCamera(1);
  loadConfig();

  if (isMobile) {
    function showControls() {
      controls.classList.remove("hidden");
      clearTimeout(hideTimeout);
      hideTimeout = setTimeout(() => {
        controls.classList.add("hidden");
      }, 3000); // 3초 후 숨김
    }

    window.addEventListener("load", showControls);
    document.addEventListener("touchstart", showControls);
  }
});
