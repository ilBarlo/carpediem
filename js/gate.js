/* Passa a true quando il sito è pronto per il pubblico. */
var SITE_OPEN = true;
if (SITE_OPEN) document.documentElement.classList.add('site-open');

(function () {
  if (!SITE_OPEN) return;

  var COLORS = ['#8A3149', '#5F2033', '#55693F', '#F5F3EE', '#E3E0D8'];

  function reduced() {
    return window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  function already() {
    try { return sessionStorage.getItem('cd_open_confetti') === '1'; } catch (e) { return false; }
  }

  function mark() {
    try { sessionStorage.setItem('cd_open_confetti', '1'); } catch (e) {}
  }

  function burst() {
    if (reduced() || already()) return;
    mark();

    var canvas = document.createElement('canvas');
    canvas.className = 'site-confetti';
    canvas.setAttribute('aria-hidden', 'true');
    document.body.appendChild(canvas);
    var ctx = canvas.getContext('2d');
    var pieces = [];
    var w = 0;
    var h = 0;
    var dpr = 1;
    var running = true;

    function size() {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      w = window.innerWidth;
      h = window.innerHeight;
      canvas.width = Math.floor(w * dpr);
      canvas.height = Math.floor(h * dpr);
      canvas.style.width = w + 'px';
      canvas.style.height = h + 'px';
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }
    size();

    var n = Math.min(160, Math.max(80, Math.floor(w / 7)));
    var i;
    for (i = 0; i < n; i++) {
      pieces.push({
        x: w * 0.5 + (Math.random() - 0.5) * w * 0.4,
        y: -16 - Math.random() * 90,
        vx: (Math.random() - 0.5) * 12,
        vy: 2.2 + Math.random() * 6.5,
        ww: 4 + Math.random() * 8,
        hh: 7 + Math.random() * 11,
        rot: Math.random() * Math.PI,
        vr: (Math.random() - 0.5) * 0.28,
        color: COLORS[i % COLORS.length],
        g: 0.11 + Math.random() * 0.09
      });
    }

    var start = performance.now();
    var dur = 4200;

    function frame(now) {
      if (!running) return;
      ctx.clearRect(0, 0, w, h);
      for (i = 0; i < pieces.length; i++) {
        var p = pieces[i];
        p.vy += p.g;
        p.x += p.vx;
        p.y += p.vy;
        p.rot += p.vr;
        p.vx *= 0.996;
        ctx.save();
        ctx.translate(p.x, p.y);
        ctx.rotate(p.rot);
        ctx.fillStyle = p.color;
        ctx.fillRect(-p.ww / 2, -p.hh / 2, p.ww, p.hh);
        ctx.restore();
      }
      if (now - start < dur) {
        requestAnimationFrame(frame);
      } else {
        running = false;
        window.removeEventListener('resize', size);
        canvas.remove();
      }
    }
    window.addEventListener('resize', size);
    requestAnimationFrame(frame);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', burst);
  } else {
    burst();
  }
})();
