(function () {
  document.addEventListener('DOMContentLoaded', function () {
    var toggle = document.querySelector('.nav-toggle');
    var nav = document.querySelector('.topnav');
    if (!toggle || !nav) return;

    toggle.addEventListener('click', function () {
      var isOpen = nav.classList.toggle('nav-open');
      toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });

    nav.querySelectorAll('.navlinks a').forEach(function (link) {
      link.addEventListener('click', function () {
        nav.classList.remove('nav-open');
        toggle.setAttribute('aria-expanded', 'false');
      });
    });
  });
})();
