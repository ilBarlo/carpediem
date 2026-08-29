(function () {
  var COPY = {
    it: {
      open: 'Fai una domanda',
      close: 'Chiudi',
      hint: 'Domande?',
      title: 'Carpe Diem',
      hello: 'Ciao — dimmi cosa ti serve.',
      more: 'Altra domanda?',
      wa: 'Scrivici su WhatsApp',
      qs: [
        { id: 'order', q: 'Come si ordina?', a: 'In bottega, via WhatsApp o dal modulo contatti. Indicaci il pezzo e ti confermiamo disponibilità, tempi e spedizione.' },
        { id: 'where', q: 'Dove ci troviamo?', a: 'Via L. da Vinci, 12 — Grottaglie (TA), nel Quartiere delle Ceramiche.' },
        { id: 'what', q: 'Cosa fate?', a: 'Ceramica fatta a mano: pumi, arredo e tavola, arte sacra, Natale, Pasqua ed Estate. Su richiesta anche bomboniere e pezzi su misura.' },
        { id: 'ship', q: 'Spedite?', a: 'Sì, in tutta Italia e nel mondo, con imballaggi sicuri.' },
        { id: 'hours', q: 'Quali sono gli orari?', a: 'Tutti i giorni, 8:30–13:00 / 14:30–21:00.' },
        { id: 'custom', q: 'Pezzi personalizzati?', a: 'Sì. Bomboniere, eventi e idee su misura: raccontaci l’occasione e lo realizziamo insieme.' }
      ]
    },
    en: {
      open: 'Ask a question',
      close: 'Close',
      hint: 'Questions?',
      title: 'Carpe Diem',
      hello: 'Hello — tell me what you need.',
      more: 'Another question?',
      wa: 'Message us on WhatsApp',
      qs: [
        { id: 'order', q: 'How do I order?', a: 'In the workshop, via WhatsApp, or through the contact form. Tell us the piece and we’ll confirm availability, timing and shipping.' },
        { id: 'where', q: 'Where are you?', a: 'Via L. da Vinci, 12 — Grottaglie (TA), in the Ceramics Quarter.' },
        { id: 'what', q: 'What do you make?', a: 'Handmade ceramics: pumi, home & table, sacred art, Christmas, Easter and Summer. Wedding favors and custom pieces on request.' },
        { id: 'ship', q: 'Do you ship?', a: 'Yes — across Italy and worldwide, with secure packaging.' },
        { id: 'hours', q: 'What are your hours?', a: 'Every day, 8:30–13:00 / 14:30–21:00.' },
        { id: 'custom', q: 'Custom pieces?', a: 'Yes. Favors, events and one-off ideas: tell us the occasion and we’ll make it together.' }
      ]
    }
  };

  var WA = 'https://wa.me/393400657599?text=' + encodeURIComponent('Ciao, vorrei informazioni sulla vostra ceramica.');

  function lang() {
    return document.documentElement.lang === 'en' ? 'en' : 'it';
  }

  function t() { return COPY[lang()]; }

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text) n.textContent = text;
    return n;
  }

  document.addEventListener('DOMContentLoaded', function () {
    var root = el('div', 'ask');
    root.innerHTML =
      '<button class="ask-fab" type="button" aria-expanded="false">' +
        '<span class="ask-hint"></span>' +
        '<span class="ask-dot">' +
          '<img src="assets/img/mascotte-ink.png" alt="">' +
          '<span class="ask-fab-x" aria-hidden="true">×</span>' +
        '</span>' +
      '</button>' +
      '<div class="ask-panel" hidden role="dialog" aria-modal="false" aria-labelledby="ask-title">' +
        '<div class="ask-head">' +
          '<strong id="ask-title"></strong>' +
          '<button class="ask-x" type="button">×</button>' +
        '</div>' +
        '<div class="ask-thread"></div>' +
        '<div class="ask-chips"></div>' +
        '<a class="ask-wa" href="' + WA + '" target="_blank" rel="noopener"></a>' +
      '</div>';
    document.body.appendChild(root);

    var fab = root.querySelector('.ask-fab');
    var panel = root.querySelector('.ask-panel');
    var thread = root.querySelector('.ask-thread');
    var chips = root.querySelector('.ask-chips');
    var title = root.querySelector('#ask-title');
    var wa = root.querySelector('.ask-wa');

    function paintChrome() {
      var c = t();
      title.textContent = c.title;
      wa.textContent = c.wa;
      root.querySelector('.ask-hint').textContent = c.hint;
      fab.setAttribute('aria-label', panel.hidden ? c.open : c.close);
      root.querySelector('.ask-x').setAttribute('aria-label', c.close);
    }

    function renderChips() {
      var c = t();
      chips.innerHTML = '';
      c.qs.forEach(function (item) {
        var b = el('button', 'ask-chip', item.q);
        b.type = 'button';
        b.addEventListener('click', function () { ask(item); });
        chips.appendChild(b);
      });
    }

    function bubble(kind, text) {
      var b = el('div', 'ask-bubble is-' + kind, text);
      thread.appendChild(b);
      thread.scrollTop = thread.scrollHeight;
    }

    function ask(item) {
      bubble('me', item.q);
      window.setTimeout(function () {
        bubble('bot', item.a);
      }, 220);
    }

    function reset() {
      thread.innerHTML = '';
      bubble('bot', t().hello);
      renderChips();
    }

    function setOpen(open) {
      panel.hidden = !open;
      root.classList.toggle('is-open', open);
      fab.setAttribute('aria-expanded', open ? 'true' : 'false');
      paintChrome();
      if (open) {
        reset();
        panel.querySelector('.ask-x').focus();
      }
    }

    fab.addEventListener('click', function () { setOpen(panel.hidden); });
    root.querySelector('.ask-x').addEventListener('click', function () { setOpen(false); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !panel.hidden) setOpen(false);
    });
    document.querySelectorAll('.lang-btn').forEach(function (btn) {
      btn.addEventListener('click', function () {
        window.setTimeout(function () {
          paintChrome();
          if (!panel.hidden) reset();
        }, 0);
      });
    });

    paintChrome();
  });
})();
