(function () {
  var STORE = "gs-site-lang";
  var TITLES = {
    ko: "Graph Styler — 옵시디언 그래프, 클릭 한 번으로",
    en: "Graph Styler — Your Obsidian graph, one click away"
  };
  var DESCRIPTIONS = {
    ko: "옵시디언 그래프 뷰를 클릭 한 번으로 예쁘게. 14가지 프리셋 + 나만의 테마. CSS도, 설정도 필요 없어요.",
    en: "Make your Obsidian graph view beautiful in one click. 14 presets, custom themes, no CSS setup."
  };

  function setLang(lang) {
    document.documentElement.lang = lang;
    document.title = TITLES[lang] || TITLES.ko;
    var desc = document.querySelector('meta[name="description"]');
    if (desc) desc.setAttribute("content", DESCRIPTIONS[lang] || DESCRIPTIONS.ko);
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
      if (!text) {
        var wrap = btn.closest(".snippet") || btn.closest(".prompt") || btn.parentElement;
        var el = wrap && (wrap.querySelector(".prompt-text") || wrap.querySelector("code"));
        text = el ? el.textContent : "";
      }
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

  var urlLang = "";
  try {
    var params = new URLSearchParams(window.location.search);
    urlLang = params.get("lang") || "";
  } catch (e) {}

  var pathLang = window.location.pathname.indexOf("/en") === 0 ? "en" : "";
  var saved = pathLang || urlLang || "ko";
  try { saved = localStorage.getItem(STORE) || "ko"; } catch (e) {}
  if (pathLang || urlLang) saved = pathLang || urlLang;
  if (saved === "en") setLang("en");
})();
