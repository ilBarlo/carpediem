(function () {
  document.addEventListener('DOMContentLoaded', function () {
    var pills = document.querySelectorAll('.filter-pill');
    var cards = document.querySelectorAll('.prod-card');
    var grid = document.querySelector('.prod-grid');
    if (!pills.length || !cards.length) return;

    function apply(cat) {
      pills.forEach(function (p) {
        p.classList.toggle('active', p.dataset.cat === cat);
      });
      cards.forEach(function (c) {
        c.hidden = !(cat === 'all' || c.dataset.cat === cat);
      });
      if (grid) grid.classList.toggle('is-all', cat === 'all');
    }

    pills.forEach(function (p) {
      p.addEventListener('click', function () {
        var cat = p.dataset.cat || 'all';
        apply(cat);
        if (history.replaceState) {
          history.replaceState(null, '', cat === 'all' ? location.pathname : '#' + cat);
        }
      });
    });

    var hash = (location.hash || '#all').replace('#', '');
    var valid = Array.prototype.some.call(pills, function (p) { return p.dataset.cat === hash; });
    apply(valid ? hash : 'all');
  });
})();
