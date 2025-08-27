document.addEventListener("DOMContentLoaded", () => {
  const cam0 = document.getElementById("cam0");
  const cam1 = document.getElementById("cam1");
  const gapSlider = document.getElementById("gapSlider");
  const gapValue = document.getElementById("gapValue");

  // 상태를 JS에서도 관리
  let cameraState = {
    gap: 0,
    cameras: {
      cam0: { order: 1, rotation: 0, flipped: false },
      cam1: { order: 2, rotation: 0, flipped: false }
    }
  };

  // 📌 1. 서버에서 설정 불러오기
  async function loadConfig() {
    const res = await fetch("/config");
    const data = await res.json();
    cameraState = data;

    // gap 반영
    gapSlider.value = cameraState.gap;
    gapValue.textContent = cameraState.gap;

    applyCameraStyles();
  }

  // 📌 2. DOM에 상태 반영
  function applyCameraStyles() {
    Object.entries(cameraState.cameras).forEach(([id, state]) => {
      const cam = document.getElementById(id);
      cam.style.order = state.order;
      cam.style.transform = `
        rotate(${state.rotation}deg)
        scaleX(${state.flipped ? -1 : 1})
      `;
    });
  }

  // 📌 이벤트 핸들러
  gapSlider.addEventListener("input", (e) => {
    cameraState.gap = parseInt(e.target.value, 10);
    gapValue.textContent = cameraState.gap;
    document.querySelector(".container").style.gap = `${cameraState.gap}px`;
  });

  document.getElementById("rotateCam0").addEventListener("click", () => {
    cameraState.cameras.cam0.rotation = (cameraState.cameras.cam0.rotation + 90) % 360;
    applyCameraStyles();
  });

  document.getElementById("rotateCam1").addEventListener("click", () => {
    cameraState.cameras.cam1.rotation = (cameraState.cameras.cam1.rotation + 90) % 360;
    applyCameraStyles();
  });

  document.getElementById("distortedToggle").addEventListener("change", (e) => {
    // 좌우 반전 → 두 카메라 모두 적용한다고 가정
    cameraState.cameras.cam0.flipped = e.target.checked;
    cameraState.cameras.cam1.flipped = e.target.checked;
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

  // 📌 3. 서버에 저장
  document.getElementById("saveBtn").addEventListener("click", async () => {
    const formData = new FormData();
    formData.append("gap", cameraState.gap);

    formData.append("cam0_order", cameraState.cameras.cam0.order);
    formData.append("cam0_rotation", cameraState.cameras.cam0.rotation);
    formData.append("cam0_flipped", cameraState.cameras.cam0.flipped);

    formData.append("cam1_order", cameraState.cameras.cam1.order);
    formData.append("cam1_rotation", cameraState.cameras.cam1.rotation);
    formData.append("cam1_flipped", cameraState.cameras.cam1.flipped);

    const res = await fetch("/config", {
      method: "POST",
      body: formData
    });
    const data = await res.json();
    alert(data.message);
  });

  // 페이지 로드 시 서버 상태 불러오기
  loadConfig();
});
