/* ResumeCraft 2.0 — app.js
   Lightweight, dependency-free JavaScript.
   Handles: password toggle, mobile sidebar, scroll reveal,
            auto-dismiss messages, mobile nav.
*/

(function () {
  "use strict";

  // ─── Password Toggle ──────────────────────────────────
  function initPasswordToggle() {
    document.querySelectorAll(".pw-wrap").forEach(function (wrap) {
      var input  = wrap.querySelector("input[type=password], input[type=text]");
      var toggle = wrap.querySelector(".pw-toggle");
      if (!input || !toggle) return;

      toggle.setAttribute("aria-label", "Show password");
      toggle.setAttribute("type", "button");

      toggle.addEventListener("click", function () {
        var visible = input.type === "text";
        input.type  = visible ? "password" : "text";
        toggle.innerHTML = visible ? eyeHide() : eyeShow();
        toggle.setAttribute("aria-label", visible ? "Show password" : "Hide password");
      });

      // Set initial icon
      toggle.innerHTML = eyeShow();
    });
  }

  function eyeShow() {
    return '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>';
  }
  function eyeHide() {
    return '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/></svg>';
  }

  // ─── Navigation Drawer (overlay, no layout shift) ─────
  function initNavDrawer() {
    var drawer   = document.getElementById("navDrawer");
    var backdrop = document.getElementById("navBackdrop");
    var toggle   = document.getElementById("navToggle");
    if (!drawer || !toggle) return;

    function openDrawer() {
      drawer.classList.add("is-open");
      drawer.setAttribute("aria-hidden", "false");
      toggle.setAttribute("aria-expanded", "true");
      toggle.setAttribute("aria-label", "Close navigation");
      toggle.classList.add("is-open");
      if (backdrop) {
        backdrop.classList.add("is-visible");
        backdrop.setAttribute("aria-hidden", "false");
      }
      document.body.style.overflow = "hidden";
    }

    function closeDrawer() {
      drawer.classList.remove("is-open");
      drawer.setAttribute("aria-hidden", "true");
      toggle.setAttribute("aria-expanded", "false");
      toggle.setAttribute("aria-label", "Open navigation");
      toggle.classList.remove("is-open");
      if (backdrop) {
        backdrop.classList.remove("is-visible");
        backdrop.setAttribute("aria-hidden", "true");
      }
      document.body.style.overflow = "";
    }

    toggle.addEventListener("click", function () {
      if (drawer.classList.contains("is-open")) {
        closeDrawer();
      } else {
        openDrawer();
      }
    });

    // Backdrop click closes drawer
    if (backdrop) {
      backdrop.addEventListener("click", closeDrawer);
    }

    // Escape key closes drawer
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && drawer.classList.contains("is-open")) {
        closeDrawer();
        toggle.focus();
      }
    });

    // Clicking a nav link closes drawer
    drawer.querySelectorAll(".side-link").forEach(function (link) {
      link.addEventListener("click", function () {
        closeDrawer();
      });
    });
  }

  // ─── Scroll Reveal ────────────────────────────────────
  function initScrollReveal() {
    if (!("IntersectionObserver" in window)) {
      document.querySelectorAll(".reveal").forEach(function (el) {
        el.classList.add("visible");
      });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add("visible");
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.12 });
    document.querySelectorAll(".reveal").forEach(function (el) { io.observe(el); });
  }

  // ─── Auto-dismiss Messages ────────────────────────────
  function initMessages() {
    document.querySelectorAll(".message").forEach(function (msg) {
      setTimeout(function () {
        msg.style.transition = "opacity 0.4s ease, transform 0.4s ease";
        msg.style.opacity = "0";
        msg.style.transform = "translateX(20px)";
        setTimeout(function () { msg.remove(); }, 420);
      }, 4200);
    });
  }

  // ─── Mobile Nav (home page links) ────────────────────
  function initMobileNav() {
    var toggle  = document.querySelector(".nav-toggle");
    var navMenu = document.querySelector(".nav-links");
    if (!toggle || !navMenu) return;

    navMenu.style.display = "none";
    var open = false;

    toggle.addEventListener("click", function () {
      open = !open;
      if (open) {
        navMenu.style.cssText = "display:flex; flex-direction:column; position:absolute; top:68px; left:0; right:0; background:var(--bg-surface); border-bottom:1px solid var(--border); padding:1.5rem 5%; gap:1rem; z-index:200;";
      } else {
        navMenu.style.display = "none";
      }
      toggle.innerHTML = open ? "✕" : "☰";
    });

    // Close when clicking a link
    navMenu.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () {
        open = false;
        navMenu.style.display = "none";
        toggle.innerHTML = "☰";
      });
    });
  }

  // ─── Progress bar animation ───────────────────────────
  function animateProgressBars() {
    document.querySelectorAll(".progress-bar-fill, .progress-fill").forEach(function (bar) {
      var target = bar.style.width || bar.getAttribute("data-width") || "0%";
      bar.style.width = "0%";
      requestAnimationFrame(function () {
        setTimeout(function () { bar.style.width = target; }, 80);
      });
    });
  }

  // ─── Init ─────────────────────────────────────────────
  document.addEventListener("DOMContentLoaded", function () {
    initPasswordToggle();
    initNavDrawer();
    initScrollReveal();
    initMessages();
    initMobileNav();
    animateProgressBars();
  });
}());
