(function () {
  document.addEventListener('DOMContentLoaded', function () {
    var track = document.getElementById('reviewsTrack');
    var dotsWrap = document.getElementById('reviewsDots');
    var prevBtn = document.querySelector('.rev-nav.prev');
    var nextBtn = document.querySelector('.rev-nav.next');
    if (!track || !dotsWrap) return;

    var cards = Array.prototype.slice.call(track.children);
    var dots = cards.map(function (card, i) {
      var d = document.createElement('button');
      d.className = 'dot' + (i === 0 ? ' active' : '');
      d.setAttribute('aria-label', 'Recensione ' + (i + 1));
      d.addEventListener('click', function () { scrollToCard(i); });
      dotsWrap.appendChild(d);
      return d;
    });

    function scrollToCard(i) {
      track.scrollTo({ left: cards[i].offsetLeft - track.offsetLeft, behavior: 'smooth' });
    }

    function activeIndex() {
      var scrollLeft = track.scrollLeft;
      var best = 0, bestDist = Infinity;
      cards.forEach(function (card, i) {
        var dist = Math.abs((card.offsetLeft - track.offsetLeft) - scrollLeft);
        if (dist < bestDist) { bestDist = dist; best = i; }
      });
      return best;
    }

    if (prevBtn) prevBtn.addEventListener('click', function () {
      scrollToCard(Math.max(0, activeIndex() - 1));
    });
    if (nextBtn) nextBtn.addEventListener('click', function () {
      scrollToCard(Math.min(cards.length - 1, activeIndex() + 1));
    });

    var ticking = false;
    track.addEventListener('scroll', function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        var idx = activeIndex();
        dots.forEach(function (d, i) { d.classList.toggle('active', i === idx); });
        ticking = false;
      });
    }, { passive: true });
  });
})();
