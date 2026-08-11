// HUMMUSHEIKHS VENTURES: site behaviour
document.addEventListener("DOMContentLoaded", function() {
  "use strict";

  // Mobile menu toggle
  var menuToggle = document.querySelector(".menu-toggle");
  var navLinks = document.querySelector(".nav-links");
  if (menuToggle && navLinks) {
    menuToggle.addEventListener("click", function () {
      var open = navLinks.classList.toggle("is-open");
      menuToggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  // Mobile dropdown expand (tap to open submenu instead of hover)
  document.querySelectorAll(".has-dropdown > a").forEach(function (link) {
    link.addEventListener("click", function (e) {
      if (window.innerWidth <= 900) {
        var parent = link.parentElement;
        var isOpen = parent.classList.contains("is-open");
        if (!isOpen) {
          e.preventDefault();
          document.querySelectorAll(".has-dropdown.is-open").forEach(function (el) {
            el.classList.remove("is-open");
          });
          parent.classList.add("is-open");
        }
      }
    });
  });

  // Search panel toggle
  var searchToggle = document.querySelector(".search-toggle");
  var searchPanel = document.querySelector(".search-panel");
  if (searchToggle && searchPanel) {
    searchToggle.addEventListener("click", function () {
      var open = searchPanel.classList.toggle("is-open");
      searchToggle.setAttribute("aria-expanded", open ? "true" : "false");
      if (open) {
        var input = searchPanel.querySelector("input");
        if (input) input.focus();
      }
    });
  }

  // Site search: redirect to bookshelf with query
  var siteSearchForm = document.querySelector("[data-site-search]");
  if (siteSearchForm) {
    siteSearchForm.addEventListener("submit", function (e) {
      e.preventDefault();
      var q = siteSearchForm.querySelector("input").value.trim();
      var base = siteSearchForm.getAttribute("data-target") || "bookshelf.html";
      window.location.href = base + (q ? "?q=" + encodeURIComponent(q) : "");
    });
  }

  // FAQ accordion
  document.querySelectorAll(".faq-item").forEach(function (item) {
    var btn = item.querySelector(".faq-q");
    var answer = item.querySelector(".faq-a");
    if (!btn || !answer) return;
    btn.addEventListener("click", function () {
      var isOpen = item.classList.contains("is-open");
      document.querySelectorAll(".faq-item.is-open").forEach(function (el) {
        el.classList.remove("is-open");
        el.querySelector(".faq-a").style.maxHeight = null;
        el.querySelector(".faq-q").setAttribute("aria-expanded", "false");
      });
      if (!isOpen) {
        item.classList.add("is-open");
        answer.style.maxHeight = answer.scrollHeight + "px";
        btn.setAttribute("aria-expanded", "true");
      }
    });
  });

  // Bookshelf: search + category filter (client-side, works on bookshelf.html)
  var shelf = document.querySelector("[data-bookshelf]");
  if (shelf) {
    var cards = Array.prototype.slice.call(shelf.querySelectorAll(".book-card"));
    var searchInput = document.querySelector("[data-shelf-search]");
    var chips = Array.prototype.slice.call(document.querySelectorAll("[data-shelf-chip]"));
    var emptyState = document.querySelector("[data-shelf-empty]");
    var activeCategory = "all";

    function applyFilters() {
      var term = (searchInput && searchInput.value || "").toLowerCase().trim();
      var visibleCount = 0;
      cards.forEach(function (card) {
        var cats = (card.getAttribute("data-categories") || "").toLowerCase();
        var text = (card.getAttribute("data-search") || "").toLowerCase();
        var matchesCategory = activeCategory === "all" || cats.indexOf(activeCategory) !== -1;
        var matchesTerm = term === "" || text.indexOf(term) !== -1;
        var show = matchesCategory && matchesTerm;
        card.style.display = show ? "" : "none";
        if (show) visibleCount++;
      });
      if (emptyState) emptyState.style.display = visibleCount === 0 ? "block" : "none";
    }

    // Pre-fill from ?q= param
    var params = new URLSearchParams(window.location.search);
    if (params.get("q") && searchInput) {
      searchInput.value = params.get("q");
    }

    if (searchInput) searchInput.addEventListener("input", applyFilters);
    chips.forEach(function (chip) {
      chip.addEventListener("click", function () {
        chips.forEach(function (c) { c.classList.remove("is-active"); });
        chip.classList.add("is-active");
        activeCategory = chip.getAttribute("data-shelf-chip");
        applyFilters();
      });
    });
    applyFilters();
  }

  // Contact + newsletter forms (no backend attached, so show a clear inline confirmation)
  document.querySelectorAll("[data-static-form]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var note = form.querySelector("[data-form-note]");
      if (note) {
        note.textContent = "This form isn't wired to a live inbox yet. See the note below, or reach us directly on WhatsApp or email.";
        note.style.color = "#a9812f";
      }
    });
  });

  // Footer year
  document.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });
});
