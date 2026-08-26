(function () {
  document.addEventListener('DOMContentLoaded', function () {
    var toggle = document.querySelector('.nav-toggle');
    var nav = document.querySelector('.topnav');
    var lockY = 0;
    if (!toggle || !nav) return;

    function label(isOpen) {
      var en = document.documentElement.lang === 'en';
      if (isOpen) return en ? 'Close menu' : 'Chiudi menù';
      return en ? 'Menu' : 'Menù';
    }

    function setOpen(isOpen) {
      nav.classList.toggle('nav-open', isOpen);
      toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
      toggle.setAttribute('aria-label', label(isOpen));
      if (isOpen) {
        lockY = window.scrollY || window.pageYOffset || 0;
        document.body.style.position = 'fixed';
        document.body.style.top = '-' + lockY + 'px';
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
        window.scrollTo(0, lockY);
      }
    }

    toggle.addEventListener('click', function () {
      setOpen(!nav.classList.contains('nav-open'));
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('nav-open')) {
        setOpen(false);
        toggle.focus();
      }
    });

    nav.querySelectorAll('.nav-list a, .nav-ig').forEach(function (link) {
      link.addEventListener('click', function () {
        setOpen(false);
      });
    });

    window.addEventListener('resize', function () {
      if (window.matchMedia('(min-width: 781px)').matches && nav.classList.contains('nav-open')) {
        setOpen(false);
      }
    });
  });
})();
