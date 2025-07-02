const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const captureBtn = document.getElementById("capture-btn");
const uploadedPhoto = document.getElementById("uploaded-photo");
const matchedPhotos = document.getElementById("matched-photos");
const toleranceSlider = document.getElementById("tolerance");
const toleranceValue = document.getElementById("tolerance-value");

toleranceSlider.addEventListener("input", () => {
    toleranceValue.textContent = toleranceSlider.value;
});

navigator.mediaDevices.getUserMedia({ video: true })
    .then((stream) => {
        video.srcObject = stream;
    })
    .catch((err) => {
        alert("Camera access denied: " + err.message);
    });

captureBtn.addEventListener("click", () => {
    const ctx = canvas.getContext("2d");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    // flip image (mirror)
    ctx.translate(canvas.width, 0);
    ctx.scale(-1, 1);
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    const dataURL = canvas.toDataURL("image/jpeg");
    const blob = dataURLtoBlob(dataURL);
    const formData = new FormData();
    formData.append("file", blob, "capture.jpg");
    formData.append("tolerance", toleranceSlider.value);

    uploadedPhoto.innerHTML = `<img src="${dataURL}" alt="Captured Photo">`;
    matchedPhotos.innerHTML = `<i class="fas fa-spinner fa-spin"></i><p>Matching...</p>`;

    fetch("/api/upload", {
        method: "POST",
        body: formData,
    })
        .then((res) => res.json())
        .then((data) => {
            if (data.matches.length > 0) {
                matchedPhotos.innerHTML = data.matches.map(
                    (img) => `<img src="${img}" alt="Match">`
                ).join("");
            } else {
                matchedPhotos.innerHTML = `<i class="fas fa-search"></i><p>No matches found</p>`;
            }
        })
        .catch((err) => {
            console.error(err);
            matchedPhotos.innerHTML = `<p>Error: ${err.message}</p>`;
        });
});

function dataURLtoBlob(dataurl) {
    const arr = dataurl.split(",");
    const mime = arr[0].match(/:(.*?);/)[1];
    const bstr = atob(arr[1]);
    let n = bstr.length;
    const u8arr = new Uint8Array(n);
    while (n--) {
        u8arr[n] = bstr.charCodeAt(n);
    }
    return new Blob([u8arr], { type: mime });
}
