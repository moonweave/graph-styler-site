(function () {
  var STORE = "gs-site-lang";

  function setLang(lang) {
    document.documentElement.lang = lang;
    document.querySelectorAll("[data-" + lang + "]").forEach(function (el) {
      var val = el.getAttribute("data-" + lang);
      if (val !== null) el.innerHTML = val;
    });
    document.querySelectorAll(".lang-btn").forEach(function (b) {
      b.classList.toggle("active", b.dataset.lang === lang);
    });
    try { localStorage.setItem(STORE, lang); } catch (e) {}
  }

  document.querySelectorAll(".lang-btn").forEach(function (btn) {
    btn.addEventListener("click", function () { setLang(btn.dataset.lang); });
  });

  document.querySelectorAll(".copy").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var text = btn.getAttribute("data-copy");
      navigator.clipboard.writeText(text).then(function () {
        var lang = document.documentElement.lang;
        var label = btn.textContent;
        btn.textContent = lang === "en" ? "Copied ✓" : "복사됨 ✓";
        btn.classList.add("done");
        setTimeout(function () {
          btn.textContent = btn.getAttribute("data-" + lang) || label;
          btn.classList.remove("done");
        }, 1400);
      });
    });
  });

  var saved = "ko";
  try { saved = localStorage.getItem(STORE) || "ko"; } catch (e) {}
  if (saved === "en") setLang("en");
})();
