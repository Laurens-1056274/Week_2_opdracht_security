window.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("iframe").forEach((iframe) => {
    iframe.addEventListener("load", () => {
      try {
        const doc = iframe.contentDocument || iframe.contentWindow.document;
        const navbar = doc.querySelector(".navbar");
        if (navbar) {
          navbar.style.display = "none";
        }
      } catch (e) {
        console.warn("Cannot access iframe:", e);
      }
    });
  });
});
