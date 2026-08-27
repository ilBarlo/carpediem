(function () {
  document.addEventListener('DOMContentLoaded', function () {
    var els = document.querySelectorAll('.reveal, .reveal-stagger');
    if (!els.length) return;

    if ('IntersectionObserver' in window) {
      var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            observer.unobserve(entry.target);
          }
        });
        }, { threshold: 0, rootMargin: '80px 0px 80px 0px' });
        els.forEach(function (el) { observer.observe(el); });
        requestAnimationFrame(function () {
          els.forEach(function (el) {
            var r = el.getBoundingClientRect();
            if (r.bottom > 0 && r.top < window.innerHeight) {
              el.classList.add('is-visible');
              observer.unobserve(el);
            }
          });
        });
    } else {
      els.forEach(function (el) { el.classList.add('is-visible'); });
    }
  });
})();
