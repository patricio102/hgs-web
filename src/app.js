(function () {
  var btn = document.querySelector('.menu-btn');
  var nav = document.getElementById('nav');
  if (btn && nav) {
    btn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  document.querySelectorAll('.copy').forEach(function (b) {
    b.addEventListener('click', function () {
      var target = document.getElementById(b.getAttribute('data-copy'));
      var text = target ? target.textContent.trim() : '';
      var done = function () { var t = b.textContent; b.textContent = b.getAttribute('data-ok'); setTimeout(function () { b.textContent = t; }, 1600); };
      var fallback = function () {
        var r = document.createRange(); r.selectNodeContents(target);
        var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
      };
      try {
        navigator.clipboard.writeText(text).then(done, fallback);
      } catch (e) { fallback(); }
    });
  });

  var form = document.getElementById('contact-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var ok = true;
      form.querySelectorAll('[data-req]').forEach(function (f) {
        var err = f.querySelector('.err');
        var inputs = f.querySelectorAll('input, select');
        var filled = false;
        inputs.forEach(function (i) {
          if ((i.type === 'radio' && i.checked) || (i.type !== 'radio' && i.value.trim() !== '')) filled = true;
        });
        if (err) err.hidden = filled;
        if (!filled) ok = false;
      });
      if (!ok) {
        var first = form.querySelector('.err:not([hidden])');
        if (first) first.parentElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
        return;
      }
      form.hidden = true;
      var t = document.getElementById('thanks');
      t.hidden = false;
      t.focus();
    });
  }
})();
