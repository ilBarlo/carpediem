(function () {
  var KEY = 'cd_consent';
  var COPY = {
    it: {
      text: 'Usiamo solo quanto serve al sito. La mappa Google si carica se accetti i cookie di terze parti.',
      accept: 'Accetta',
      needed: 'Solo necessari',
      more: 'Privacy e cookie',
      map: 'La mappa è di Google e usa cookie di terze parti.',
      mapBtn: 'Mostra mappa'
    },
    en: {
      text: 'We only use what the site needs. The Google map loads if you accept third-party cookies.',
      accept: 'Accept',
      needed: 'Necessary only',
      more: 'Privacy & cookies',
      map: 'The map is provided by Google and uses third-party cookies.',
      mapBtn: 'Show map'
    }
  };

  function lang() {
    return document.documentElement.lang === 'en' ? 'en' : 'it';
  }

  function t() { return COPY[lang()]; }

  function getConsent() {
    try { return localStorage.getItem(KEY); } catch (e) { return null; }
  }

  function setConsent(value) {
    try { localStorage.setItem(KEY, value); } catch (e) {}
  }

  function allowed() {
    return getConsent() === 'all';
  }

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text) n.textContent = text;
    return n;
  }

  document.addEventListener('DOMContentLoaded', function () {
    var bar = el('div', 'cookie-bar');
    bar.setAttribute('role', 'dialog');
    bar.setAttribute('aria-live', 'polite');
    bar.innerHTML =
      '<p class="cookie-text"></p>' +
      '<div class="cookie-actions">' +
        '<button type="button" class="cookie-accept"></button>' +
        '<button type="button" class="cookie-needed"></button>' +
        '<a class="cookie-more" href="privacy.html"></a>' +
      '</div>';
    document.body.appendChild(bar);
    bar.hidden = true;

    var textEl = bar.querySelector('.cookie-text');
    var acceptBtn = bar.querySelector('.cookie-accept');
    var neededBtn = bar.querySelector('.cookie-needed');
    var moreLink = bar.querySelector('.cookie-more');

    function paintBar() {
      var c = t();
      textEl.textContent = c.text;
      acceptBtn.textContent = c.accept;
      neededBtn.textContent = c.needed;
      moreLink.textContent = c.more;
    }

    function showBar(show) {
      bar.hidden = !show;
    }

    function paintMaps() {
      var c = t();
      document.querySelectorAll('iframe[data-map-src]').forEach(function (frame) {
        var wrap = frame.parentElement;
        if (!wrap) return;
        wrap.classList.add('map-wrap');
        var cover = wrap.querySelector('.map-cover');
        if (!cover) {
          cover = el('div', 'map-cover');
          cover.innerHTML = '<p></p><button type="button" class="btn-primary"></button>';
          wrap.appendChild(cover);
          cover.querySelector('button').addEventListener('click', function () {
            setConsent('all');
            showBar(false);
            apply();
          });
        }
        cover.querySelector('p').textContent = c.map;
        cover.querySelector('button').textContent = c.mapBtn;

        if (allowed()) {
          if (!frame.getAttribute('src')) frame.src = frame.getAttribute('data-map-src');
          cover.hidden = true;
        } else {
          frame.removeAttribute('src');
          cover.hidden = false;
        }
      });
    }

    function apply() {
      paintBar();
      paintMaps();
      var choice = getConsent();
      showBar(!choice);
    }

    acceptBtn.addEventListener('click', function () {
      setConsent('all');
      apply();
    });
    neededBtn.addEventListener('click', function () {
      setConsent('needed');
      apply();
    });
    document.querySelectorAll('.lang-btn').forEach(function (btn) {
      btn.addEventListener('click', function () {
        window.setTimeout(apply, 0);
      });
    });

    apply();
  });
})();
