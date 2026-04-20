// Main entry point for Sarah Gillespie's homepage
import { initDarkMode } from "./darkmode.js";

document.addEventListener("DOMContentLoaded", () => {
  console.log("Homepage JavaScript initialized");

  // Initialize dark mode toggle
  initDarkMode();

  // Log confirmation
  console.log("All features loaded successfully");
});

// Export for potential use elsewhere
export { initDarkMode };
