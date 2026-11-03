/* HGS · carrusel curvo + entrada + menú + formulario */
(function () {
  "use strict";
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Menú celular ---------- */
  var sheet = document.querySelector(".sheet");
  document.querySelectorAll("[data-menu]").forEach(function (b) {
    b.addEventListener("click", function () {
      if (!sheet) return;
      var open = !sheet.classList.contains("open");
      sheet.classList.toggle("open", open);
      document.body.style.overflow = open ? "hidden" : "";
      if (open) { var c = sheet.querySelector(".close-btn"); if (c) c.focus(); }
    });
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && sheet && sheet.classList.contains("open")) {
      sheet.classList.remove("open"); document.body.style.overflow = "";
    }
  });

  /* ---------- Formulario ---------- */
  var form = document.getElementById("contact-form");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.checkValidity()) { form.classList.add("invalid"); form.reportValidity(); return; }
      form.classList.remove("invalid");
      var d = new FormData(form), lines = [];
      form.querySelectorAll("[name]").forEach(function (el) {
        if (lines.some(function (l) { return l.k === el.name; })) return;
        var lab = el.getAttribute("data-label") || el.name;
        lines.push({ k: el.name, t: lab + ": " + (d.get(el.name) || "") });
      });
      var to = form.getAttribute("data-to");
      var subj = form.getAttribute("data-subject") + " · " + (d.get("empresa") || "");
      var body = lines.map(function (l) { return l.t; }).join("\n");
      var href = "mailto:" + to + "?subject=" + encodeURIComponent(subj) + "&body=" + encodeURIComponent(body);
      var link = document.getElementById("mail-link");
      if (link) link.href = href;
      document.querySelector(".contact-main").classList.add("sent");
      window.location.href = href;
    });
  }

  /* ---------- Carrusel curvo ---------- */
  var hero = document.querySelector(".hero");
  if (!hero) return;
  var track = hero.querySelector(".cards");
  var cards = Array.prototype.slice.call(track.querySelectorAll(".card"));
  var N = cards.length, PITCH = 196, L = N * PITCH;

  cards.forEach(function (c) {
    var img = c.querySelector("img");
    var done = function () { img.classList.add("ready"); };
    if (img.complete && img.naturalWidth) done(); else img.addEventListener("load", done);
    img.addEventListener("error", done);
    img.style.animationDelay = (-Math.random() * 14).toFixed(2) + "s";
  });

  var mobile, u, C, R, cyBase, halfVis;
  function measure() {
    mobile = window.innerWidth <= 820;
    if (mobile) {
      u = track.clientWidth / 640; C = 320; R = 314;
      cyBase = (track.clientHeight / 2) / u + 6;
      halfVis = 320;
    } else {
      u = Math.min(window.innerWidth / 1440, window.innerHeight / 1080);
      C = 720; R = 706; cyBase = 687;
      halfVis = (window.innerWidth / u) / 2;
    }
  }
  measure();
  window.addEventListener("resize", measure);

  function rq(p, r) {
    // polígono de 4 puntos con esquinas redondeadas
    var n = p.length, s = "";
    for (var i = 0; i < n; i++) {
      var a = p[(i + n - 1) % n], b = p[i], c = p[(i + 1) % n];
      var d1 = Math.hypot(a[0] - b[0], a[1] - b[1]), d2 = Math.hypot(c[0] - b[0], c[1] - b[1]);
      var r1 = Math.min(r, d1 / 2), r2 = Math.min(r, d2 / 2);
      var p1 = [b[0] + (a[0] - b[0]) * r1 / d1, b[1] + (a[1] - b[1]) * r1 / d1];
      var p2 = [b[0] + (c[0] - b[0]) * r2 / d2, b[1] + (c[1] - b[1]) * r2 / d2];
      s += (i ? "L" : "M") + p1[0].toFixed(1) + " " + p1[1].toFixed(1) + "Q" + b[0].toFixed(1) + " " + b[1].toFixed(1) + " " + p2[0].toFixed(1) + " " + p2[1].toFixed(1);
    }
    return s + "Z";
  }

  var off = 0, vel = 0, dragging = false, lastX = 0, lastT = 0, pid = null;
  var clock = null;
  try { clock = document.documentElement.animate([{ opacity: 1 }, { opacity: 1 }], { duration: 1e9 }); } catch (e) { clock = null; }
  function now() { return clock && clock.currentTime != null ? clock.currentTime : performance.now(); }
  var prev = now();

  function layout() {
    var maxD = mobile ? 1.15 : 1.35;
    for (var i = 0; i < N; i++) {
      var x0 = (((i * PITCH - off) % L) + L) % L;
      var t = x0 - L / 2;
      var x = C + t * (1 + 0.083 * Math.pow(t / R, 2));
      var el = cards[i];
      if (Math.abs(x - C) > halfVis + 320) { el.style.visibility = "hidden"; continue; }
      el.style.visibility = "";
      var d = Math.min(Math.abs(x - C) / R, maxD);
      var w = 170 + 48 * d * d;
      var xl = x - w / 2, xr = x + w / 2;
      var ql = Math.min(Math.abs(xl - C) / R, maxD), qr = Math.min(Math.abs(xr - C) / R, maxD);
      var hl = 280 + 92 * Math.pow(ql, 2.6), hr = 280 + 92 * Math.pow(qr, 2.6);
      var cy = cyBase - 12 * d * d;
      var H = Math.max(hl, hr);
      var top = cy - H / 2;
      var W = w * u, Hp = H * u;
      el.style.width = W.toFixed(1) + "px";
      el.style.height = Hp.toFixed(1) + "px";
      el.style.transform = "translate(" + (xl * u).toFixed(1) + "px," + (top * u).toFixed(1) + "px)";
      var yl0 = (H - hl) / 2 * u, yr0 = (H - hr) / 2 * u;
      var path = rq([[0, yl0], [W, yr0], [W, Hp - yr0], [0, Hp - yl0]], 15 * u);
      el.style.clipPath = "path('" + path + "')";
      el.style.webkitClipPath = "path('" + path + "')";
      var tag = el.querySelector(".tag");
      if (tag) tag.style.bottom = (yl0 + 10 * Math.max(u, .6) * (mobile ? 1.2 : 1)).toFixed(1) + "px";
    }
  }

  function frame() {
    var t = now(), dt = Math.min(0.05, Math.max(0, (t - prev) / 1000)); prev = t;
    if (!dragging) {
      if (!reduce) off += 50 * dt;
      if (Math.abs(vel) > 0.5) { off += vel * dt; vel *= Math.pow(0.05, dt); } else vel = 0;
    }
    layout();
    requestAnimationFrame(frame);
  }

  track.addEventListener("pointerdown", function (e) {
    if (e.button !== undefined && e.button !== 0) return;
    dragging = true; pid = e.pointerId; vel = 0; lastX = e.clientX; lastT = performance.now();
    track.classList.add("dragging");
    try { track.setPointerCapture(pid); } catch (er) {}
  });
  track.addEventListener("pointermove", function (e) {
    if (!dragging || e.pointerId !== pid) return;
    var tt = performance.now(), dx = e.clientX - lastX, dts = Math.max(1, tt - lastT) / 1000;
    off -= dx / u;
    var v = -dx / u / dts;
    vel = vel * 0.6 + v * 0.4;
    lastX = e.clientX; lastT = tt;
  });
  function end(e) {
    if (!dragging || (e && e.pointerId !== pid)) return;
    dragging = false; track.classList.remove("dragging");
    if (performance.now() - lastT > 90) vel = 0;
    vel = Math.max(-4000, Math.min(4000, vel));
  }
  track.addEventListener("pointerup", end);
  track.addEventListener("pointercancel", end);
  track.addEventListener("dragstart", function (e) { e.preventDefault(); });

  layout();
  requestAnimationFrame(frame);

  /* ---------- Entrada ---------- */
  if (reduce || !document.body.animate) return;
  function A(sel, kf, o) {
    hero.querySelectorAll(sel).forEach(function (el, i) {
      el.animate(kf, Object.assign({ fill: "backwards", easing: "cubic-bezier(.2,.7,.2,1)" }, o, { delay: (o.delay || 0) + i * (o.stagger || 0) }));
    });
  }
  var desk = !mobile;
  A(".f-logo, .f-nav, .f-acts", [{ opacity: 0, transform: "translateY(-14px)" }, { opacity: 1, transform: "none" }], { duration: 700, delay: 0, stagger: 80 });
  A(".f-badge", [{ opacity: 0, transform: (desk ? "translateX(-50%) " : "") + "scale(.7)" }, { opacity: 1, transform: (desk ? "translateX(-50%) " : "") + "scale(1)" }], { duration: 600, delay: 250, easing: "cubic-bezier(.3,1.5,.5,1)" });
  A(".f-h1 span", [{ opacity: 0, transform: "translateY(28px)", filter: "blur(10px)" }, { opacity: 1, transform: "none", filter: "blur(0)" }], { duration: 900, delay: 380, stagger: 140 });
  A(".f-sub", [{ opacity: 0, transform: "translateY(16px)" }, { opacity: 1, transform: "none" }], { duration: 800, delay: 700 });
  A(".cards", [{ opacity: 0, transform: "translateY(80px)" }, { opacity: 1, transform: "none" }], { duration: 1200, delay: 850 });
  A(".f-cta", [{ opacity: 0, transform: (desk ? "translateX(-50%) " : "") + "scale(.8)" }, { opacity: 1, transform: (desk ? "translateX(-50%) " : "") + "scale(1)" }], { duration: 700, delay: 1250, easing: "cubic-bezier(.3,1.4,.5,1)" });
  hero.querySelectorAll(".doodles path").forEach(function (p, i) {
    p.style.strokeDasharray = "1"; p.style.strokeDashoffset = "0";
    p.animate([{ strokeDashoffset: 1 }, { strokeDashoffset: 0 }], { duration: 1100, delay: 1500 + i * 220, fill: "backwards", easing: "ease-in-out" });
  });
  A(".f-note1, .f-note2", [{ opacity: 0 }, { opacity: 1 }], { duration: 800, delay: 1700, stagger: 250 });
})();
