/* SmartNoise shared script: theme, mobile menu, session-aware nav, scroll reveal, welcome celebration. */
(function () {
  "use strict";
  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); if (v === null) localStorage.removeItem(k); else localStorage.setItem(k, v); } catch (e) {} return null; }
  function users() { try { var u = JSON.parse(store("smartnoise_users")); return u && typeof u === "object" && !Array.isArray(u) ? u : {}; } catch (e) { return {}; } }

  /* ---- session ---- */
  var email = store("smartnoise_session"), me = email && users()[email] ? users()[email] : null;
  if (!me) email = null;
  window.SN_USER = email;
  /* ---- persistent language selector for authenticated application ---- */
  function addLanguageControl() {
    if (!email || document.getElementById("snLangControl")) return;
    var host = document.querySelector(".nav-right") || document.querySelector("header .wrap"); if (!host) return;
    var wrap = document.createElement("div"); wrap.id = "snLangControl"; wrap.className = "sn-lang-control";
    wrap.innerHTML = '<label class="sr" for="snLang">Language</label><select id="snLang" aria-label="Language"><option value="en">English</option><option value="hi">हिन्दी</option><option value="es">Español</option><option value="fr">Français</option><option value="de">Deutsch</option><option value="pt">Português</option><option value="ja">日本語</option></select>';
    host.insertBefore(wrap, host.firstChild);
    var sel = wrap.querySelector("select"), code = window.SN_i18nGet ? window.SN_i18nGet() : (store("sn_language") || "en"); sel.value = code;
    sel.addEventListener("change", function(){ try{localStorage.setItem("sn_language", this.value)}catch(e){}; if(window.SN_i18nSet) window.SN_i18nSet(this.value); });
  }
  addLanguageControl();
  if (document.body.dataset.protected && !me) { location.replace("login.html"); return; }

  /* ---- theme ---- */
  var themeBtn = document.getElementById("themeBtn");
  function setTheme(t) {
    document.documentElement.dataset.theme = t; store("sn_theme", t);
    if (themeBtn) { themeBtn.setAttribute("aria-pressed", t === "dark"); themeBtn.setAttribute("aria-label", t === "dark" ? "Switch to light mode" : "Switch to dark mode"); }
  }
  window.SN_setTheme = setTheme;
  setTheme(document.documentElement.dataset.theme || "day");
  if (themeBtn) themeBtn.onclick = function () { setTheme(document.documentElement.dataset.theme === "dark" ? "day" : "dark"); };

  /* ---- mobile menu ---- */
  var burger = document.getElementById("burger"), links = document.getElementById("navLinks");
  if (burger && links) {
    burger.onclick = function () { var o = links.classList.toggle("open"); burger.setAttribute("aria-expanded", o); };
    links.addEventListener("click", function (e) { if (e.target.closest("a")) links.classList.remove("open"); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") links.classList.remove("open"); });
  }

  /* ---- session-aware nav ---- */
  var cta = document.getElementById("navCta"), hello = document.getElementById("hello");
  if (me) {
    if (cta) { cta.textContent = "Dashboard"; cta.href = "dashboard.html"; }
    if (hello) { hello.textContent = me.name; hello.hidden = false; }
    var lo = document.getElementById("navLogout"); if (lo) lo.hidden = false;
  }
  var logout = document.getElementById("navLogout");
  if (logout) logout.onclick = function () { store("smartnoise_session", null); location.replace("login.html"); };
  document.querySelectorAll("[data-auth-cta]").forEach(function (a) { if (me) { a.href = "dashboard.html"; a.firstChild.textContent = "Open dashboard "; } });

  /* ---- scroll reveal ---- */
  var rv = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } }); }, { threshold: .1 });
    rv.forEach(function (r) { io.observe(r); });
  } else rv.forEach(function (r) { r.classList.add("in"); });

  /* ---- welcome celebration: confetti, fireworks, party poppers ---- */
  window.SN_celebrate = function (name) {
    var box = document.createElement("div"); box.id = "party"; box.setAttribute("role", "dialog"); box.setAttribute("aria-label", "Welcome");
    box.innerHTML = '<canvas></canvas><div class="pbox"><h2>Welcome aboard!</h2><p>Your SmartNoise account is ready, <b></b>.</p><button class="btn primary lg" id="partyGo">Continue to dashboard</button></div>';
    box.querySelector("b").textContent = name; document.body.appendChild(box);
    var cv = box.querySelector("canvas"), g = cv.getContext("2d"), P = [], cols = ["#818cf8", "#22d3ee", "#fde047", "#f472b6", "#a78bfa", "#4ade80"], t0 = Date.now(), alive = true;
    function size() { cv.width = innerWidth; cv.height = innerHeight; } size(); addEventListener("resize", size);
    function burst(x, y, n, speed, grav) { for (var i = 0; i < n; i++) { var a = Math.random() * 6.283, s = Math.random() * speed; P.push({ x: x, y: y, vx: Math.cos(a) * s, vy: Math.sin(a) * s - 2, c: cols[i % 6], l: 90 + Math.random() * 50, g: grav, w: 4 + Math.random() * 5 }); } }
    function popper(x, dir) { for (var i = 0; i < 70; i++) { var a = -Math.PI / 2 + dir * (0.2 + Math.random() * 0.7), s = 8 + Math.random() * 12; P.push({ x: x, y: innerHeight, vx: Math.cos(a) * s * dir * dir, vy: Math.sin(a) * s, c: cols[i % 6], l: 140, g: .25, w: 6 }); } }
    popper(0, 1); popper(innerWidth, -1); setTimeout(function () { popper(0, 1); popper(innerWidth, -1); }, 900);
    var fw = setInterval(function () { burst(innerWidth * (.15 + Math.random() * .7), innerHeight * (.15 + Math.random() * .4), 60, 7, .08); }, 450);
    function frame() {
      if (!alive) return; g.clearRect(0, 0, cv.width, cv.height);
      P = P.filter(function (p) { p.x += p.vx; p.y += p.vy; p.vy += p.g; p.vx *= .985; p.l--; g.globalAlpha = Math.max(p.l / 60, 0); g.fillStyle = p.c; g.fillRect(p.x, p.y, p.w, p.w * .6); return p.l > 0; });
      requestAnimationFrame(frame);
    }
    frame();
    function close() { alive = false; clearInterval(fw); box.remove(); removeEventListener("keydown", esc); removeEventListener("resize", size); }
    function esc(e) { if (e.key === "Escape") close(); }
    addEventListener("keydown", esc); box.querySelector("#partyGo").onclick = close; box.querySelector("#partyGo").focus(); setTimeout(function () { if (Date.now() - t0 > 5500) close(); }, 6000);
  };
  if (me && sessionStorage.getItem("sn_celebrate")) { try { sessionStorage.removeItem("sn_celebrate"); } catch (e) {} window.SN_celebrate(me.name.split(" ")[0]); }
})();
