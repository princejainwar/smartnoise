/* SmartNoise account system: header user area, profile menu, notifications, reports, settings.
   Static demo architecture: everything is stored per account in this browser's localStorage.
   Every read/write is scoped to the signed-in account (window.SN_USER), so one account never touches another's data.
   For real multi-device accounts, move these functions behind a backend that authorises each request. */
(function () {
  "use strict";
  var $ = function (id) { return document.getElementById(id); };
  var email = window.SN_USER || null;
  if (document.body.dataset.protected && !email) return; // common.js is redirecting to login

  /* ---------- storage helpers ---------- */
  function jget(k, d) { try { var v = JSON.parse(localStorage.getItem(k)); return v == null ? d : v; } catch (e) { return d; } }
  function jset(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); return true; } catch (e) { return false; } }
  function users() { var u = jget("smartnoise_users", {}); return u && typeof u === "object" && !Array.isArray(u) ? u : {}; }
  function me() { return email ? users()[email] || null : null; }
  function saveMe(patch) { var all = users(); if (!email || !all[email]) return false; Object.keys(patch).forEach(function (k) { all[email][k] = patch[k]; }); return jset("smartnoise_users", all); }
  function key(kind, e) { return "smartnoise_" + kind + "_" + (e || email); }
  function esc(t) { var d = document.createElement("div"); d.textContent = t == null ? "" : String(t); return d.innerHTML; }
  function pad(n) { return String(n).padStart(2, "0"); }
  var ICONS = {
    user: "M12 12a4 4 0 100-8 4 4 0 000 8zM4 21a8 8 0 0116 0", edit: "M4 20h4L19 9l-4-4L4 16zM13.5 6.5l4 4", upload: "M12 16V4m0 0L7 9m5-5l5 5M5 20h14", doc: "M7 3h8l4 4v14H7zM14 3v5h5M10 13h6M10 17h6",
    bell: "M6 8a6 6 0 1112 0c0 7 3 8 3 8H3s3-1 3-8zM10 20a2 2 0 004 0", gear: "M12 15a3 3 0 100-6 3 3 0 000 6zM19 12a7 7 0 00-.1-1.2l2-1.5-2-3.4-2.3 1a7 7 0 00-2-1.2L14.2 3h-4l-.4 2.7a7 7 0 00-2 1.2l-2.3-1-2 3.4 2 1.5A7 7 0 005 12c0 .4 0 .8.1 1.2l-2 1.5 2 3.4 2.3-1a7 7 0 002 1.2l.4 2.7h4l.4-2.7a7 7 0 002-1.2l2.3 1 2-3.4-2-1.5c.1-.4.1-.8.1-1.2z",
    dash: "M4 4h7v7H4zM13 4h7v4h-7zM13 11h7v9h-7zM4 14h7v6H4z", out: "M15 3h4a2 2 0 012 2v14a2 2 0 01-2 2h-4M10 17l5-5-5-5M15 12H3", moon: "M20 14.5A8 8 0 019.5 4 8 8 0 1020 14.5z", chev: "M6 9l6 6 6-6",
    alert: "M12 3l10 18H2zM12 10v5M12 18v.01", flag: "M5 21V4m0 0h12l-2 4 2 4H5", info: "M12 21a9 9 0 100-18 9 9 0 000 18zM12 11v5M12 8v.01", check: "M5 12l5 5 9-10", trash: "M4 7h16M9 7V4h6v3M6 7l1 13h10l1-13"
  };
  function ic(n) { return '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="' + ICONS[n] + '"/></svg>'; }

  /* ---------- toast ---------- */
  function toast(msg, bad) {
    var w = $("toasts"); if (!w) { w = document.createElement("div"); w.id = "toasts"; w.className = "toast-wrap"; w.setAttribute("role", "status"); w.setAttribute("aria-live", "polite"); document.body.appendChild(w); }
    var t = document.createElement("div"); t.className = "toast" + (bad ? " err" : ""); t.textContent = msg; w.appendChild(t); setTimeout(function () { t.remove(); }, 4200);
  }
  window.SN_toast = toast;
  try { var pt = sessionStorage.getItem("sn_toast"); if (pt) { sessionStorage.removeItem("sn_toast"); toast(pt); } } catch (e) {}
  function flash(msg) { try { sessionStorage.setItem("sn_toast", msg); } catch (e) {} }

  /* ---------- per-account data ---------- */
  var DEF = { noiseAlerts: true, complaintUpdates: true, emailNotifs: false, saveHistory: true };
  function prefs() { var p = jget(key("prefs"), {}), o = {}; Object.keys(DEF).forEach(function (k) { o[k] = typeof p[k] === "boolean" ? p[k] : DEF[k]; }); return o; }
  function savePrefs(p) { return jset(key("prefs"), p); }
  function notifs() { var n = jget(key("notifs"), []); return Array.isArray(n) ? n : []; }
  function saveNotifs(n) { return jset(key("notifs"), n.slice(0, 100)); }
  function reports() { var r = jget(key("reports"), []); return Array.isArray(r) ? r : []; }
  function history() { var h = jget(key("history"), []); return Array.isArray(h) ? h : []; }
  window.SN_prefs = prefs;
  function notify(n) {
    if (!email) return; var p = prefs();
    if (n.type === "alert" && !p.noiseAlerts) return; if (n.type === "complaint" && !p.complaintUpdates) return;
    var all = notifs(); all.unshift({ id: Date.now() + "-" + Math.random().toString(36).slice(2, 6), type: n.type, title: n.title, body: n.body, at: Date.now(), read: false });
    saveNotifs(all); updateBadge();
  }
  window.SN_notify = notify;
  function unread() { return notifs().filter(function (n) { return !n.read; }).length; }
  if (email && localStorage.getItem(key("notifs")) === null) { saveNotifs([{ id: "welcome", type: "account", title: "Welcome to SmartNoise", body: "Your account is ready. Try the Live Monitor, or submit your first noise report.", at: Date.now(), read: false }]); }

  /* ---------- avatar ---------- */
  function initials(name) { var p = String(name || "?").trim().split(/\s+/); return ((p[0] || "?")[0] + (p.length > 1 ? p[p.length - 1][0] : "")).toUpperCase(); }
  function avatar(u, cls) {
    if (u && typeof u.avatar === "string" && /^data:image\/jpeg;base64,[A-Za-z0-9+\/=]+$/.test(u.avatar)) return '<img class="avatar ' + (cls || "") + '" alt="" src="' + u.avatar + '">';
    return '<span class="avatar ' + (cls || "") + '" aria-hidden="true">' + esc(initials(u && u.name)) + "</span>";
  }
  function processImage(file, max, square) {
    return new Promise(function (res, rej) {
      if (!file) return rej(new Error("No file selected."));
      if (!/^image\/(jpeg|png|webp|gif)$/.test(file.type)) return rej(new Error("Please choose a JPG, PNG, WebP or GIF image."));
      if (file.size > 8 * 1048576) return rej(new Error("The image is too large (maximum 8 MB)."));
      var r = new FileReader(); r.onerror = function () { rej(new Error("Could not read the image.")); };
      r.onload = function () {
        var i = new Image(); i.onerror = function () { rej(new Error("That file is not a valid image.")); };
        i.onload = function () {
          var c = document.createElement("canvas"), w = i.width, h = i.height, sx = 0, sy = 0, sw = w, sh = h;
          if (square) { var s = Math.min(w, h); sx = (w - s) / 2; sy = (h - s) / 2; sw = sh = s; c.width = c.height = max; }
          else { var k = Math.min(1, max / Math.max(w, h)); c.width = Math.round(w * k); c.height = Math.round(h * k); }
          var g = c.getContext("2d"); g.fillStyle = "#fff"; g.fillRect(0, 0, c.width, c.height); g.drawImage(i, sx, sy, sw, sh, 0, 0, c.width, c.height);
          res(c.toDataURL("image/jpeg", .85));
        };
        i.src = r.result;
      };
      r.readAsDataURL(file);
    });
  }

  /* ---------- crypto (same PBKDF2 scheme as auth.js) ---------- */
  function hex(b) { return Array.prototype.map.call(new Uint8Array(b), function (x) { return x.toString(16).padStart(2, "0"); }).join(""); }
  function cryptoOk() { return !!(window.crypto && crypto.subtle && window.TextEncoder); }
  function derive(pw, salt) { var enc = new TextEncoder(); return crypto.subtle.importKey("raw", enc.encode(pw), "PBKDF2", false, ["deriveBits"]).then(function (k) { return crypto.subtle.deriveBits({ name: "PBKDF2", salt: enc.encode(salt), iterations: 100000, hash: "SHA-256" }, k, 256); }).then(hex); }
  function verify(pw) { var u = me(); if (!cryptoOk()) return Promise.reject(new Error("Secure operations need HTTPS or localhost.")); if (!pw) return Promise.reject(new Error("Please enter your current password.")); return derive(pw, u.salt).then(function (h) { if (h !== u.hash) throw new Error("Current password is incorrect."); }); }
  function changeEmail(next, pw) {
    var all = users(), old = email;
    return verify(pw).then(function () {
      if (all[next]) throw new Error("Another account already uses this email.");
      all[next] = all[old]; delete all[old]; if (!jset("smartnoise_users", all)) throw new Error("Could not save your account (storage unavailable).");
      ["history", "prefs", "reports", "notifs"].forEach(function (k) { var v = localStorage.getItem(key(k, old)); if (v !== null) { localStorage.setItem(key(k, next), v); localStorage.removeItem(key(k, old)); } });
      localStorage.setItem("smartnoise_session", next); email = window.SN_USER = next;
    });
  }

  /* ---------- reference lists ---------- */
  var COUNTRIES = "Australia,Bangladesh,Bhutan,Brazil,Canada,China,Denmark,Egypt,France,Germany,Indonesia,India,Ireland,Italy,Japan,Kenya,Malaysia,Maldives,Mexico,Myanmar,Nepal,Netherlands,New Zealand,Nigeria,Norway,Pakistan,Philippines,Qatar,Russia,Saudi Arabia,Singapore,South Africa,South Korea,Spain,Sri Lanka,Sweden,Switzerland,Thailand,Turkey,United Arab Emirates,United Kingdom,United States,Vietnam,Other".split(",");
  var LANGS = ["en", "hi", "es", "fr", "de", "pt", "ja"]; var LANG_LABELS={en:"English",hi:"हिन्दी",es:"Español",fr:"Français",de:"Deutsch",pt:"Português",ja:"日本語"};
  function fillSelect(el, list, val, ph) { if (!el) return; el.innerHTML = (ph ? '<option value="">' + ph + "</option>" : "") + list.map(function (c) { return '<option value="' + esc(c) + '">' + esc(LANG_LABELS[c] || c) + "</option>"; }).join(""); el.value = val || ""; }
  function rel(t) { var s = Math.floor((Date.now() - t) / 1000); if (s < 60) return "Just now"; if (s < 3600) return Math.floor(s / 60) + " min ago"; if (s < 86400) return Math.floor(s / 3600) + " h ago"; if (s < 604800) return Math.floor(s / 86400) + " d ago"; return new Date(t).toLocaleDateString(); }
  function field(id, msg) { var e = $(id), m = $(id + "Err"); if (e) e.classList.toggle("bad", !!msg); if (m) { m.textContent = msg || ""; m.hidden = !msg; } return !msg; }
  var EMAIL_RE = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;

  /* ================= HEADER ================= */
  var here = location.pathname.split("/").pop() || "index.html", menu, btn, scrim;
  function updateBadge() {
    var n = unread(), b = $("bellBadge"); if (b) { b.textContent = n > 99 ? "99+" : n; b.hidden = n === 0; }
    var c = $("menuCnt"); if (c) { c.textContent = n; c.hidden = n === 0; }
    var bell = $("bellLink"); if (bell) bell.setAttribute("aria-label", n ? "Notifications, " + n + " unread" : "Notifications");
  }
  function item(href, icon, label, extra) { return '<a role="menuitem" href="' + href + '"' + (here === href ? ' aria-current="page"' : "") + ">" + ic(icon) + label + (extra || "") + "</a>"; }
  function renderHeader() {
    var box = $("acct"); if (!box) return; var u = me();
    if (!u) { box.innerHTML = '<a class="btn ghost nav-login" href="login.html">Login</a><a class="btn primary nav-signup" href="login.html?tab=signup">Create Account</a>'; box.dataset.state = "out"; document.querySelectorAll("[data-guest]").forEach(function (a) { a.hidden = false; }); return; }
    document.querySelectorAll("[data-guest]").forEach(function (a) { a.remove(); });
    box.dataset.state = "in";
    box.innerHTML = '<a class="icon-btn bell" id="bellLink" href="notifications.html" aria-label="Notifications">' + ic("bell") + '<span class="badge" id="bellBadge" hidden>0</span></a>' +
      '<button class="acct-btn" id="acctBtn" type="button" aria-haspopup="menu" aria-expanded="false" aria-controls="acctMenu" aria-label="Account menu for ' + esc(u.name) + '">' + avatar(u) + '<span class="acct-name">' + esc(u.name) + '</span><svg class="chev" viewBox="0 0 24 24" aria-hidden="true"><path d="' + ICONS.chev + '"/></svg></button>' +
      '<div class="scrim" id="acctScrim"></div>' +
      '<div class="menu" id="acctMenu" role="menu" aria-label="Account"><div class="menu-head">' + avatar(u, "md") + "<div><b>" + esc(u.name) + "</b><span>" + esc(email) + "</span></div></div>" +
      item("profile.html", "user", "Profile") + item("profile-edit.html", "edit", "Edit Profile") + '<div class="menu-sep"></div>' +
      item("awareness.html", "info", "Noise Awareness") + item("helplines.html", "bell", "Helplines") + item("complaints.html", "flag", "Official Complaint Links") + item("limits.html", "alert", "Noise Limits") + item("zones.html", "pin", "Noise Zones") + item("controls.html", "gear", "Smart Controls") + item("submit-data.html", "upload", "Submit Data") + item("my-reports.html", "doc", "My Reports") + item("notifications.html", "bell", "Notifications", '<span class="cnt" id="menuCnt" hidden>0</span>') + '<div class="menu-sep"></div>' +
      item("settings.html", "gear", "Settings") + item("dashboard.html", "dash", "Dashboard") +
      '<button role="menuitem" type="button" id="menuTheme">' + ic("moon") + '<span id="menuThemeTxt">Dark mode</span></button><div class="menu-sep"></div>' +
      '<button role="menuitem" type="button" class="danger" id="menuLogout">' + ic("out") + "Log out</button></div>";
    menu = $("acctMenu"); btn = $("acctBtn"); scrim = $("acctScrim"); updateBadge(); syncTheme();
    btn.onclick = function (e) { e.stopPropagation(); toggle(); }; scrim.onclick = function () { toggle(false); };
    menu.addEventListener("click", function (e) { if (e.target.closest("a")) toggle(false); });
    $("menuTheme").onclick = function () { var t = document.documentElement.dataset.theme === "dark" ? "day" : "dark"; window.SN_setTheme ? SN_setTheme(t) : (document.documentElement.dataset.theme = t); syncTheme(); };
    $("menuLogout").onclick = function () { try { localStorage.removeItem("smartnoise_session"); } catch (e) {} location.replace("login.html"); };
    document.addEventListener("click", function (e) { if (menu.classList.contains("open") && !menu.contains(e.target)) toggle(false); });
    document.addEventListener("keydown", function (e) {
      if (!menu.classList.contains("open")) return;
      if (e.key === "Escape") { toggle(false); btn.focus(); }
      if (e.key === "ArrowDown" || e.key === "ArrowUp") { e.preventDefault(); var its = [].slice.call(menu.querySelectorAll("[role=menuitem]")), i = its.indexOf(document.activeElement); its[(i + (e.key === "ArrowDown" ? 1 : -1) + its.length) % its.length].focus(); }
    });
  }
  function toggle(open) {
    var o = open === undefined ? !menu.classList.contains("open") : open;
    menu.classList.toggle("open", o); scrim.classList.toggle("open", o); btn.setAttribute("aria-expanded", o);
    if (o) { var f = menu.querySelector("[role=menuitem]"); f && f.focus({ preventScroll: true }); }
  }
  function syncTheme() { var t = $("menuThemeTxt"); if (t) t.textContent = document.documentElement.dataset.theme === "dark" ? "Light mode" : "Dark mode"; }
  new MutationObserver(syncTheme).observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
  renderHeader();

  /* ================= PAGES ================= */
  var page = document.body.dataset.page, u = me();
  if (!page || !u) return;

  function setAvatar(id, size) { var el = $(id); if (el) el.innerHTML = avatar(me(), size); }

  /* ---- profile ---- */
  if (page === "profile") {
    var profileLogout = $("pfLogout");
    if (profileLogout) profileLogout.onclick = function () { try { localStorage.removeItem("smartnoise_session"); } catch (e) {} location.replace("login.html"); };
    setAvatar("pfAvatar", "lg"); $("pfName").textContent = u.name; $("pfEmail").textContent = email;
    $("pfCountry").textContent = u.country || "Not set"; var lp={en:"English",hi:"हिन्दी",es:"Español",fr:"Français",de:"Deutsch",pt:"Português",ja:"日本語"}; $("pfLang").textContent = lp[u.language] || u.language || "English (default)";
    $("pfSince").textContent = u.created ? new Date(u.created).toLocaleDateString(undefined, { year: "numeric", month: "long", day: "numeric" }) : "Not available";
    $("pfReports").textContent = reports().length; $("pfReadings").textContent = history().length; $("pfUnread").textContent = unread();
  }

  /* ---- edit profile ---- */
  if (page === "profile-edit") {
    var newAvatar = u.avatar || null, f = $("editForm");
    fillSelect($("epCountry"), COUNTRIES, u.country, "Select country"); fillSelect($("epLang"), LANGS, ({English:"en",Hindi:"hi",Spanish:"es",French:"fr",German:"de",Portuguese:"pt",Japanese:"ja"}[u.language] || u.language || "en"));
    $("epName").value = u.name; $("epEmail").value = email;
    function paint() { $("epAvatar").innerHTML = avatar({ name: $("epName").value || u.name, avatar: newAvatar }, "lg"); $("epRemove").hidden = !newAvatar; }
    paint(); $("epName").addEventListener("input", paint);
    $("epPhoto").onchange = function () { var file = this.files[0]; field("epPhoto", ""); if (!file) return; processImage(file, 256, true).then(function (d) { newAvatar = d; paint(); }).catch(function (e) { field("epPhoto", e.message); }); this.value = ""; };
    $("epRemove").onclick = function () { newAvatar = null; paint(); };
    function togglePw() { var ch = $("epEmail").value.trim().toLowerCase() !== email; $("epPwBox").hidden = !ch; }
    $("epEmail").addEventListener("input", togglePw);
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var name = $("epName").value.trim(), em = $("epEmail").value.trim().toLowerCase(), changed = em !== email, ok = true;
      ok = field("epName", !name ? "Please enter your name." : name.length > 60 ? "Name must be 60 characters or fewer." : "") && ok;
      ok = field("epEmail", !EMAIL_RE.test(em) ? "Please enter a valid email address." : "") && ok;
      if (changed) ok = field("epPw", !$("epPw").value ? "Enter your current password to change your email." : "") && ok;
      if (!ok) return;
      var btnS = $("epSave"); btnS.disabled = true;
      var p = changed ? changeEmail(em, $("epPw").value) : Promise.resolve();
      p.then(function () {
        if (!saveMe({ name: name, avatar: newAvatar, country: $("epCountry").value, language: $("epLang").value })) throw new Error("Could not save (browser storage is full or unavailable). Try a smaller photo."); if(window.SN_i18nSet)window.SN_i18nSet($("epLang").value);
        flash("Profile updated successfully."); location.href = "profile.html";
      }).catch(function (er) { btnS.disabled = false; var m = er.message; if (/password/i.test(m)) field("epPw", m); else if (/email/i.test(m)) field("epEmail", m); else { var g = $("epErr"); g.textContent = m; g.hidden = false; } });
    });
    $("epCancel").onclick = function () { location.href = "profile.html"; };
  }

  /* ---- submit data ---- */
  if (page === "submit-data") {
    var evidence = null, now = new Date(), sf = $("sdForm");
    var CATS = ["Traffic and vehicle horns", "Construction", "Loudspeaker, music or events", "Industrial or factory", "Generator or machinery", "Commercial or market", "Neighbours or residential", "Other"];
    fillSelect($("sdCat"), CATS, "", "Select a category");
    $("sdDate").value = now.getFullYear() + "-" + pad(now.getMonth() + 1) + "-" + pad(now.getDate()); $("sdDate").max = $("sdDate").value; $("sdTime").value = pad(now.getHours()) + ":" + pad(now.getMinutes());
    $("sdDesc").addEventListener("input", function () { $("sdCount").textContent = this.value.length + " / 1000"; });
    $("sdLatest").onclick = function () { var h = history(); if (!h.length) return toast("No saved monitor readings yet. Record some on the Live Monitor.", true); $("sdLevel").value = h[h.length - 1].level; toast("Filled with your latest saved reading (" + h[h.length - 1].level + " dB, " + h[h.length - 1].type + ")."); };
    $("sdImg").onchange = function () {
      var file = this.files[0]; field("sdImg", ""); if (!file) return;
      processImage(file, 900, false).then(function (d) { evidence = d; $("sdPrev").innerHTML = '<img src="' + d + '" alt="Evidence preview"><span><b>' + esc(file.name) + '</b><br><button type="button" class="btn sm" id="sdRm">Remove</button></span>'; $("sdRm").onclick = function () { evidence = null; $("sdPrev").innerHTML = ""; $("sdImg").value = ""; }; })
        .catch(function (e) { field("sdImg", e.message); });
    };
    sf.addEventListener("submit", function (e) {
      e.preventDefault();
      var loc = $("sdLoc").value.trim(), lv = parseFloat($("sdLevel").value), d = $("sdDate").value, t = $("sdTime").value, c = $("sdCat").value, ds = $("sdDesc").value.trim(), ok = true;
      ok = field("sdLoc", loc.length < 3 ? "Enter the address or area where the noise occurred." : loc.length > 200 ? "Location is too long." : "") && ok;
      ok = field("sdLevel", isNaN(lv) || lv < 20 || lv > 140 ? "Enter a level between 20 and 140 dB." : "") && ok;
      ok = field("sdDate", !d ? "Choose the date." : new Date(d + "T" + (t || "00:00")) > new Date() ? "The date and time cannot be in the future." : "") && ok;
      ok = field("sdTime", !t ? "Choose the time." : "") && ok;
      ok = field("sdCat", !c ? "Select a noise category." : "") && ok;
      ok = field("sdDesc", ds.length < 10 ? "Please describe the noise in at least 10 characters." : ds.length > 1000 ? "Description must be 1000 characters or fewer." : "") && ok;
      if (!ok) { var b = sf.querySelector(".bad"); b && b.focus(); return; }
      var ref = "SN-" + Date.now().toString(36).toUpperCase().slice(-6), all = reports();
      all.unshift({ id: ref, loc: loc, level: lv, date: d, time: t, cat: c, desc: ds, image: evidence, status: "Submitted", created: Date.now(), log: [{ s: "Submitted", at: Date.now() }] });
      if (!jset(key("reports"), all)) { var g = $("sdErr"); g.textContent = "Could not save the report (browser storage is full). Remove the image or delete older reports."; g.hidden = false; return; }
      notify({ type: "complaint", title: "Report " + ref + " submitted", body: c + " at " + loc + ". Track its status in My Reports." });
      flash("Report " + ref + " submitted."); location.href = "my-reports.html";
    });
  }

  /* ---- my reports ---- */
  if (page === "my-reports") {
    var STEPS = ["Submitted", "Under Review", "Resolved"], flt = "All";
    function drawReports() {
      var all = reports(), list = all.filter(function (r) { return flt === "All" || r.status === flt; }), box = $("rpList");
      $("rpEmpty").hidden = all.length > 0; $("rpFilters").hidden = all.length === 0;
      document.querySelectorAll("[data-flt]").forEach(function (c) { c.setAttribute("aria-pressed", c.dataset.flt === flt); });
      box.innerHTML = all.length && !list.length ? '<p class="empty">No reports with this status.</p>' : "";
      list.forEach(function (r) {
        var idx = STEPS.indexOf(r.status), el = document.createElement("article"); el.className = "card report";
        el.innerHTML = '<div class="report-top"><div><h3>' + esc(r.cat) + '</h3><div class="meta"><span>' + esc(r.id) + "</span><span>" + esc(r.loc) + "</span><span>" + esc(r.level) + " dB</span><span>" + esc(r.date) + " " + esc(r.time) + '</span></div></div><span class="pill" data-s="' + esc(r.status) + '">' + esc(r.status) + "</span></div>" +
          '<ol class="tracker" aria-label="Status: ' + esc(r.status) + '">' + STEPS.map(function (s, i) { return '<li class="' + (i <= idx ? "done" : "") + '">' + s + "</li>"; }).join("") + "</ol>" +
          '<div class="rdetail" hidden><p>' + esc(r.desc).replace(/\n/g, "<br>") + "</p>" + (r.image && /^data:image\/jpeg;base64,/.test(r.image) ? '<img src="' + r.image + '" alt="Evidence for report ' + esc(r.id) + '">' : "") + '<p class="hint">Submitted ' + new Date(r.created).toLocaleString() + "</p></div>" +
          '<div class="cta" style="margin-top:16px"><button class="btn sm" data-a="d">View details</button>' + (idx < 2 ? '<button class="btn sm ghost" data-a="s" title="Demo only: there is no server reviewing reports">Simulate next status (demo)</button>' : "") + '<button class="btn sm danger ghost" data-a="x">Delete</button></div>';
        el.querySelector('[data-a="d"]').onclick = function () { var d = el.querySelector(".rdetail"); d.hidden = !d.hidden; this.textContent = d.hidden ? "View details" : "Hide details"; };
        var sb = el.querySelector('[data-a="s"]'); if (sb) sb.onclick = function () { var a = reports(), x = a.filter(function (q) { return q.id === r.id; })[0]; if (!x) return; x.status = STEPS[Math.min(2, STEPS.indexOf(x.status) + 1)]; x.log.push({ s: x.status, at: Date.now() }); jset(key("reports"), a); notify({ type: "complaint", title: "Report " + x.id + ": " + x.status, body: "Your " + x.cat.toLowerCase() + " report is now " + x.status.toLowerCase() + "." }); drawReports(); toast("Status updated (demo)."); };
        el.querySelector('[data-a="x"]').onclick = function () { if (confirm("Delete report " + r.id + "? This cannot be undone.")) { jset(key("reports"), reports().filter(function (q) { return q.id !== r.id; })); drawReports(); toast("Report deleted."); } };
        box.appendChild(el);
      });
    }
    document.querySelectorAll("[data-flt]").forEach(function (c) { c.onclick = function () { flt = c.dataset.flt; drawReports(); }; });
    drawReports();
  }

  /* ---- notifications ---- */
  if (page === "notifications") {
    var nf = "all", TI = { alert: "alert", complaint: "flag", system: "info", account: "user" };
    function drawNotifs() {
      var all = notifs(), list = all.filter(function (n) { return nf === "all" || !n.read; }), box = $("ntList");
      $("ntEmpty").hidden = all.length > 0; $("ntBar").hidden = all.length === 0;
      document.querySelectorAll("[data-nf]").forEach(function (c) { c.setAttribute("aria-pressed", c.dataset.nf === nf); });
      box.innerHTML = all.length && !list.length ? '<p class="empty">You are all caught up.</p>' : "";
      list.forEach(function (n) {
        var el = document.createElement("div"); el.className = "nitem" + (n.read ? "" : " unread");
        el.innerHTML = '<div class="ico">' + ic(TI[n.type] || "info") + '</div><div><b>' + esc(n.title) + "</b><p>" + esc(n.body) + "</p><small>" + rel(n.at) + " &middot; " + ({ alert: "Noise alert", complaint: "Complaint update", system: "System", account: "Account" }[n.type] || "System") + '</small></div><div class="acts"><button class="icon-btn" data-a="r" aria-label="' + (n.read ? "Mark as unread" : "Mark as read") + '" title="' + (n.read ? "Mark as unread" : "Mark as read") + '">' + ic("check") + '</button><button class="icon-btn" data-a="x" aria-label="Delete notification">' + ic("trash") + "</button></div>";
        el.querySelector('[data-a="r"]').onclick = function () { var a = notifs(); a.forEach(function (x) { if (x.id === n.id) x.read = !x.read; }); saveNotifs(a); updateBadge(); drawNotifs(); };
        el.querySelector('[data-a="x"]').onclick = function () { saveNotifs(notifs().filter(function (x) { return x.id !== n.id; })); updateBadge(); drawNotifs(); };
        box.appendChild(el);
      });
    }
    document.querySelectorAll("[data-nf]").forEach(function (c) { c.onclick = function () { nf = c.dataset.nf; drawNotifs(); }; });
    $("ntReadAll").onclick = function () { var a = notifs(); a.forEach(function (x) { x.read = true; }); saveNotifs(a); updateBadge(); drawNotifs(); };
    $("ntClear").onclick = function () { if (confirm("Delete all notifications?")) { saveNotifs([]); updateBadge(); drawNotifs(); } };
    drawNotifs();
  }

  /* ---- settings ---- */
  if (page === "settings") {
    var p = prefs();
    setAvatar("stAvatar", "lg"); $("stName").textContent = u.name; $("stEmail").textContent = email;
    fillSelect($("stLang"), LANGS, ({English:"en",Hindi:"hi",Spanish:"es",French:"fr",German:"de",Portuguese:"pt",Japanese:"ja"}[u.language] || u.language || "en")); fillSelect($("stCountry"), COUNTRIES, u.country, "Select country"); $("stTheme").value = document.documentElement.dataset.theme === "dark" ? "dark" : "day";
    $("tNoise").checked = p.noiseAlerts; $("tComplaint").checked = p.complaintUpdates; $("tEmail").checked = p.emailNotifs; $("tHistory").checked = p.saveHistory;
    $("stPhoto").onchange = function () { var file = this.files[0]; field("stPhoto", ""); if (!file) return; processImage(file, 256, true).then(function (d) { if (!saveMe({ avatar: d })) throw new Error("Could not save the photo (storage unavailable)."); setAvatar("stAvatar", "lg"); renderHeader(); toast("Profile picture updated."); }).catch(function (e) { field("stPhoto", e.message); }); this.value = ""; };
    $("stRemovePhoto").onclick = function () { saveMe({ avatar: null }); setAvatar("stAvatar", "lg"); renderHeader(); toast("Profile picture removed."); };
    $("stPrefs").addEventListener("submit", function (e) {
      e.preventDefault();
      var ok = saveMe({ language: $("stLang").value, country: $("stCountry").value }) && savePrefs({ noiseAlerts: $("tNoise").checked, complaintUpdates: $("tComplaint").checked, emailNotifs: $("tEmail").checked, saveHistory: $("tHistory").checked });
      window.SN_setTheme ? SN_setTheme($("stTheme").value) : 0; if(window.SN_i18nSet){window.SN_i18nSet($("stLang").value)} syncTheme(); toast(ok ? "Settings saved." : "Could not save settings (storage unavailable).", !ok);
    });
    $("pwForm").addEventListener("submit", function (e) {
      e.preventDefault(); var cur = $("pwCur").value, n1 = $("pwNew").value, n2 = $("pwNew2").value, ok = true;
      ok = field("pwCur", !cur ? "Enter your current password." : "") && ok; ok = field("pwNew", n1.length < 8 ? "Password must be at least 8 characters." : "") && ok; ok = field("pwNew2", n1 !== n2 ? "Passwords do not match." : "") && ok; if (!ok) return;
      verify(cur).then(function () { var a = new Uint8Array(16); crypto.getRandomValues(a); var salt = hex(a); return derive(n1, salt).then(function (h) { if (!saveMe({ salt: salt, hash: h })) throw new Error("Could not save the new password."); }); })
        .then(function () { $("pwForm").reset(); toast("Password changed."); notify({ type: "account", title: "Password changed", body: "Your SmartNoise password was updated on this device." }); })
        .catch(function (er) { field("pwCur", er.message); });
    });
    $("exportData").onclick = function () {
      var c = me(), d = { profile: { name: c.name, email: email, country: c.country || null, language: c.language || null, created: c.created }, preferences: prefs(), reports: reports(), notifications: notifs(), monitoringHistory: history() };
      var url = URL.createObjectURL(new Blob([JSON.stringify(d, null, 2)], { type: "application/json" })), a = document.createElement("a"); a.href = url; a.download = "smartnoise-my-data.json"; document.body.appendChild(a); a.click(); a.remove(); setTimeout(function () { URL.revokeObjectURL(url); }, 500);
    };
    $("delForm").addEventListener("submit", function (e) {
      e.preventDefault();
      verify($("delPw").value).then(function () {
        if (!confirm("Permanently delete your account and all data stored on this device?")) return;
        var all = users(); delete all[email]; jset("smartnoise_users", all); ["history", "prefs", "reports", "notifs"].forEach(function (k) { localStorage.removeItem(key(k)); }); localStorage.removeItem("smartnoise_session"); location.replace("login.html");
      }).catch(function (er) { field("delPw", er.message); });
    });
  }
})();
