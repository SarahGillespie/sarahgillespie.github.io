// darkmode.js (this is an ES6 Module)
export function initDarkMode() {
  const toggle = document.getElementById("darkModeToggle");
  const body = document.body;

  toggle.addEventListener("click", () => {
    body.classList.toggle("dark-mode");
    toggle.textContent = body.classList.contains("dark-mode")
      ? "Light Mode"
      : "Dark Mode";
  });
}
