(function () {
  document.addEventListener('DOMContentLoaded', function () {
    var pills = document.querySelectorAll('.filter-pill');
    var cards = document.querySelectorAll('.prod-card');
    var grid = document.querySelector('.prod-grid');
    var look = document.getElementById('look');
    if (!pills.length || !cards.length) return;

    var currentCat = 'all';
    var lookIndex = 0;
    var lookLockY = 0;
    var lookGen = 0;
    var swipeX = 0;
    var swiping = false;

    function apply(cat) {
      currentCat = cat;
      pills.forEach(function (p) {
        p.classList.toggle('active', p.dataset.cat === cat);
      });
      cards.forEach(function (c) {
        c.hidden = !(cat === 'all' || c.dataset.cat === cat);
      });
      if (grid) grid.classList.toggle('is-all', cat === 'all');
    }

    function visibleCards() {
      return Array.prototype.filter.call(cards, function (c) {
        return !c.hidden && c.querySelector('.frame img');
      });
    }

    function langIsEn() {
      return document.documentElement.lang === 'en';
    }

    function cardText(el, enAttr) {
      if (!el) return '';
      if (langIsEn() && el.getAttribute(enAttr)) return el.getAttribute(enAttr);
      return (el.dataset.it || el.textContent || '').trim();
    }

    function lockPage(on) {
      if (on) {
        lookLockY = window.scrollY || window.pageYOffset || 0;
        document.body.style.position = 'fixed';
        document.body.style.top = '-' + lookLockY + 'px';
        document.body.style.left = '0';
        document.body.style.right = '0';
        document.body.style.width = '100%';
        document.documentElement.classList.add('nav-lock');
      } else {
        document.documentElement.classList.remove('nav-lock');
        document.body.style.position = '';
        document.body.style.top = '';
        document.body.style.left = '';
        document.body.style.right = '';
        document.body.style.width = '';
        window.scrollTo(0, lookLockY);
      }
    }

    function renderLook(dir) {
      var list = visibleCards();
      if (!list.length) return;
      if (lookIndex < 0) lookIndex = list.length - 1;
      if (lookIndex >= list.length) lookIndex = 0;
      var gen = ++lookGen;
      var card = list[lookIndex];
      var img = card.querySelector('.frame img');
      var stageImg = look.querySelector('.look-stage img');
      var catEl = card.querySelector('.cat-tag');
      var nameEl = card.querySelector('.name');
      var wa = card.querySelector('.ask-wa');
      var cat = cardText(catEl, 'data-en');
      var name = cardText(nameEl, 'data-en');

      function paint() {
        if (gen !== lookGen) return;
        stageImg.src = img.currentSrc || img.src;
        stageImg.alt = img.alt || name;
        look.querySelector('.look-cat').textContent = cat;
        look.querySelector('.look-name').textContent = name;
        look.querySelector('.look-count').textContent = (lookIndex + 1) + ' / ' + list.length;
        var waLink = look.querySelector('.look-wa');
        if (wa && waLink) {
          waLink.href = wa.getAttribute('href');
          waLink.textContent = langIsEn() ? (wa.getAttribute('data-en') || 'Ask on WhatsApp') : (wa.dataset.it || wa.textContent);
        }
        stageImg.style.setProperty('--look-dir', (dir || 1) * 18 + 'px');
        stageImg.classList.remove('is-leave');
        stageImg.classList.add('is-enter');
        requestAnimationFrame(function () {
          requestAnimationFrame(function () {
            stageImg.classList.remove('is-enter');
          });
        });
      }

      if (dir && stageImg.src) {
        stageImg.style.setProperty('--look-dir', dir * 18 + 'px');
        stageImg.classList.add('is-leave');
        window.setTimeout(paint, 160);
      } else {
        paint();
      }
    }

    function openLook(card) {
      var list = visibleCards();
      var i = list.indexOf(card);
      if (i < 0) return;
      lookIndex = i;
      look.hidden = false;
      lockPage(true);
      renderLook(0);
      look.querySelector('.look-close').setAttribute('aria-label', langIsEn() ? 'Close' : 'Chiudi');
      look.querySelector('.look-nav.prev').setAttribute('aria-label', langIsEn() ? 'Previous' : 'Precedente');
      look.querySelector('.look-nav.next').setAttribute('aria-label', langIsEn() ? 'Next' : 'Successiva');
      look.querySelector('.look-close').focus();
    }

    function closeLook() {
      if (look.hidden) return;
      look.hidden = true;
      lockPage(false);
    }

    function step(dir) {
      lookIndex += dir;
      renderLook(dir);
    }

    pills.forEach(function (p) {
      p.addEventListener('click', function () {
        closeLook();
        var cat = p.dataset.cat || 'all';
        apply(cat);
        if (history.replaceState) {
          history.replaceState(null, '', cat === 'all' ? location.pathname : '#' + cat);
        }
      });
    });

    cards.forEach(function (card) {
      var frame = card.querySelector('.frame');
      var img = card.querySelector('.frame img');
      if (!frame || !img) return;
      frame.setAttribute('role', 'button');
      frame.setAttribute('tabindex', '0');
      frame.addEventListener('click', function () { openLook(card); });
      frame.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          openLook(card);
        }
      });
    });

    if (look) {
      look.querySelector('.look-close').addEventListener('click', closeLook);
      look.querySelector('.look-nav.prev').addEventListener('click', function () { step(-1); });
      look.querySelector('.look-nav.next').addEventListener('click', function () { step(1); });

      var stage = look.querySelector('.look-stage');
      stage.addEventListener('click', function (e) {
        if (e.target === stage) closeLook();
      });
      stage.addEventListener('touchstart', function (e) {
        if (!e.changedTouches[0]) return;
        swiping = true;
        swipeX = e.changedTouches[0].clientX;
      }, { passive: true });
      stage.addEventListener('touchend', function (e) {
        if (!swiping || !e.changedTouches[0]) return;
        var dx = e.changedTouches[0].clientX - swipeX;
        swiping = false;
        if (Math.abs(dx) > 50) step(dx < 0 ? 1 : -1);
      });
    }

    document.addEventListener('keydown', function (e) {
      if (look && !look.hidden) {
        if (e.key === 'Escape') closeLook();
        if (e.key === 'ArrowLeft') step(-1);
        if (e.key === 'ArrowRight') step(1);
        return;
      }
    });

    document.querySelectorAll('.lang-btn').forEach(function (btn) {
      btn.addEventListener('click', function () {
        if (look && !look.hidden) renderLook(0);
      });
    });

    var hash = (location.hash || '#all').replace('#', '');
    var valid = Array.prototype.some.call(pills, function (p) { return p.dataset.cat === hash; });
    apply(valid ? hash : 'all');
  });
})();
