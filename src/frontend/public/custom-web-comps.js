document.addEventListener("DOMContentLoaded", () => {
  const intervalId = setInterval(() => {
    // 1. Remove the #upload-button element if it exists
    const uploadButton = document.getElementById("upload-button");
    if (uploadButton) {
      uploadButton.remove();
    }

    // 2. Modify the watermark text if not already modified
    const watermark = document.querySelector(".watermark");
    if (watermark && !watermark.querySelector("span.made-by")) {
      watermark.innerHTML = '<span class="made-by">A PoC by TheComputerScientist</span>';
      clearInterval(intervalId);
    }
  }, 500);
});
