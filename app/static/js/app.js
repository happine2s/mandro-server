const cam0 = document.getElementById("cam0");
const cam1 = document.getElementById("cam1");
const gapSlider = document.getElementById("gapSlider");
const gapValue = document.getElementById("gapValue");
const distortedToggle = document.getElementById("distortedToggle");
const saveBtn = document.getElementById("saveBtn");
const app = document.getElementById("app");
const controls = document.querySelector(".controls");

let gap = 0;
let distorted = false;
let cameraOrder = "01";

const applyConfig = () => {
    const halfGap = gap / 2;

    if (cameraOrder === "01") {
        cam0.style.marginRight = `${halfGap}px`;
        cam0.style.marginLeft = "0";
        cam1.style.marginLeft = `${halfGap}px`;
        cam1.style.marginRight = "0";
    } else {
        cam1.style.marginRight = `${halfGap}px`;
        cam1.style.marginLeft = "0";
        cam0.style.marginLeft = `${halfGap}px`;
        cam0.style.marginRight = "0";
    }

    cam0.style.transform = distorted ? "scaleX(-1)" : "none";
    cam1.style.transform = distorted ? "scaleX(-1)" : "none";

    const isLandscape = window.innerWidth > window.innerHeight;
    app.classList.toggle("vertical", !isLandscape);
};

window.addEventListener("resize", applyConfig);

const wsScheme = location.protocol === 'https:' ? 'wss' : 'ws';
const ws0 = new WebSocket(`${wsScheme}://${location.host}/ws/stream/0`);
const ws1 = new WebSocket(`${wsScheme}://${location.host}/ws/stream/1`);

ws0.binaryType = "arraybuffer";
ws1.binaryType = "arraybuffer";

ws0.onmessage = (event) => {
    const blob = new Blob([event.data], { type: "image/jpeg" });
    const url = URL.createObjectURL(blob);
    cam0.src = url;
    cam0.onload = () => URL.revokeObjectURL(url);
};

ws1.onmessage = (event) => {
    const blob = new Blob([event.data], { type: "image/jpeg" });
    const url = URL.createObjectURL(blob);
    cam1.src = url;
    cam1.onload = () => URL.revokeObjectURL(url);
};

document.body.addEventListener("click", () => {
    const elem = document.documentElement;
    if (elem.requestFullscreen) elem.requestFullscreen();
    else if (elem.webkitRequestFullscreen) elem.webkitRequestFullscreen();
    else if (elem.msRequestFullscreen) elem.msRequestFullscreen();
}, { once: true });

// 초기 설정 불러오기
async function fetchAndApplyConfig() {
    try {
        const res = await fetch("/config");
        const config = await res.json();

        gap = Number(config.gap) || 0;
        distorted = config.distorted === true;
        cameraOrder = config.order || "01";

        gapSlider.value = gap;
        gapValue.textContent = gap;
        distortedToggle.checked = distorted;
        orderToggle.checked = (cameraOrder === "10");

        if (cameraOrder === "10") {
        app.insertBefore(cam1, cam0);
        } else {
        app.insertBefore(cam0, cam1);
        }

        applyConfig();
    } catch (e) {
        console.error("Failed to fetch /config", e);
    }
}

// 저장 버튼 클릭 → 서버에 POST 요청
saveBtn.addEventListener("click", async () => {
    const formData = new FormData();
    formData.append("gap", gapSlider.value);
    formData.append("distorted", distortedToggle.checked);
    formData.append("order", cameraOrder);

    try {
        const res = await fetch("/config", {
        method: "POST",
        body: formData,
        });

        if (res.ok) {
        const result = await res.json();
        console.log("Saved:", result);

        gap = Number(gapSlider.value);
        distorted = distortedToggle.checked;
        gapValue.textContent = gap;

        applyConfig();

        showToast("설정이 저장되었습니다.");
        } else {
        showToast("저장 실패했습니다. 서버 오류");
        }
    } catch (e) {
        console.error("Failed to save config", e);
        showToast("저장 실패했습니다. 네트워크 오류");
    }
});

function showToast(message) {
    const toast = document.createElement("div");
    toast.className = "toast";
    toast.textContent = message;
    document.body.appendChild(toast);

    setTimeout(() => toast.classList.add("show"), 10);

    setTimeout(() => {
        toast.classList.remove("show");
        setTimeout(() => document.body.removeChild(toast), 500);
    }, 2500);
    }

    gapSlider.addEventListener("input", () => {
    gap = Number(gapSlider.value);
    gapValue.textContent = gap;
    applyConfig();
    });

    distortedToggle.addEventListener("change", () => {
    distorted = distortedToggle.checked;
    applyConfig();
    });

    orderToggle.addEventListener("change", () => {
    if (orderToggle.checked) {
        app.insertBefore(cam1, cam0);
        cameraOrder = "10";
    } else {
        app.insertBefore(cam0, cam1);
        cameraOrder = "01";
    }
    applyConfig();
});

fetchAndApplyConfig();

// 모바일에서만 자동 숨김 기능
const isMobile = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
let hideTimeout;

if (isMobile) {
    function showControls() {
        controls.classList.remove("hidden");
        clearTimeout(hideTimeout);
        hideTimeout = setTimeout(() => {
        controls.classList.add("hidden");
        }, 3000);
    }

    window.addEventListener("load", showControls);
    document.addEventListener("touchstart", showControls);
}
