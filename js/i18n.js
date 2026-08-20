(function () {
  function applyLang(lang) {
    document.documentElement.lang = lang;
    document.querySelectorAll('[data-en]').forEach(function (el) {
      if (el.dataset.it === undefined) { el.dataset.it = el.innerHTML; }
      el.innerHTML = lang === 'en' ? el.dataset.en : el.dataset.it;
    });
    document.querySelectorAll('[data-en-placeholder]').forEach(function (el) {
      if (el.dataset.itPlaceholder === undefined) { el.dataset.itPlaceholder = el.getAttribute('placeholder') || ''; }
      el.setAttribute('placeholder', lang === 'en' ? el.dataset.enPlaceholder : el.dataset.itPlaceholder);
    });
    document.querySelectorAll('.lang-btn').forEach(function (btn) {
      btn.classList.toggle('active', btn.dataset.lang === lang);
    });
    try { localStorage.setItem('cd_lang', lang); } catch (e) {}
  }

  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.lang-btn').forEach(function (btn) {
      btn.addEventListener('click', function () { applyLang(btn.dataset.lang); });
    });
    var saved = 'it';
    try { saved = localStorage.getItem('cd_lang') || 'it'; } catch (e) {}
    applyLang(saved);
  });
})();
