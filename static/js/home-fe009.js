
document.documentElement.classList.add("js");
document.addEventListener("DOMContentLoaded", () => {
  const panel = document.getElementById("sip-capture");
  const triggers = [...document.querySelectorAll("[data-layer='sip']")];
  const collapse = document.querySelector("[data-collapse]");
  if (!panel || !triggers.length) return;

  const setExpanded = (expanded, moveFocus = false) => {
    panel.classList.toggle("is-expanded", expanded);
    panel.classList.toggle("is-focus", expanded);
    triggers.forEach((button) => button.setAttribute("aria-expanded", String(expanded)));
    if (expanded && moveFocus) {
      panel.scrollIntoView({behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth", block: "center"});
      panel.focus({preventScroll:true});
    }
  };

  triggers.forEach((button) => button.addEventListener("click", () => setExpanded(!panel.classList.contains("is-expanded"), true)));
  collapse?.addEventListener("click", () => setExpanded(false, false));
  if (location.hash === "#sip-capture") setExpanded(true, false);
});
