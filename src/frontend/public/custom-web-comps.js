document.addEventListener("DOMContentLoaded", () => {
  // Mutation observer callback
  const observerCallback = (mutationsList) => {
    for (const mutation of mutationsList) {
      const uploadButton = document.getElementById("upload-button");
      if (uploadButton) {
        uploadButton.remove();
      }

      const watermark = document.querySelector(".watermark");
      if (watermark && !watermark.querySelector("span.made-by")) {
        watermark.innerHTML = '<span class="made-by">This is a Proof of Concept</span>';
      }
    }
  };

  // Create and start the observer
  const observer = new MutationObserver(observerCallback);
  observer.observe(document.body, {
    childList: true,
    subtree: true
  });

  // Run the logic once on initial load
  observerCallback();
});
