/* SmartNoise dashboard logic. Shared by dashboard / monitor / analytics / zones / controls pages;
   each page only wires up the elements it contains. Estimates only; not a calibrated sound-level meter. */
(function () {
  "use strict";
  var D = window.SN_DATA, $ = function (id) { return document.getElementById(id); };
  function histKey() { return "smartnoise_history_" + (window.SN_USER || "guest"); }
  var st = { mode: null, stream: null, ctx: null, analyser: null, buf: null, timer: null, start: 0, vals: [], alerts: 0, over: false, lastSave: 0, last: 0 };

  /* ---------- helpers ---------- */
  function pad(n) { return String(n).padStart(2, "0"); }
  function fmt(s) { return pad(Math.floor(s / 60)) + ":" + pad(s % 60); }
  function esc(t) { var d = document.createElement("div"); d.textContent = t; return d.innerHTML; }
  function setText(id, v) { var e = $(id); if (e) e.textContent = v; }
  function showErr(m) { var e = $("error"); if (e) { e.textContent = m; e.hidden = !m; } }
  function cssVar(n) { return getComputedStyle(document.documentElement).getPropertyValue(n).trim(); }
  function loadHist() { try { var h = JSON.parse(localStorage.getItem(histKey())); return Array.isArray(h) ? h : []; } catch (e) { return []; } }
  function saveHist(h) { try { localStorage.setItem(histKey(), JSON.stringify(h.slice(-500))); } catch (e) { showErr("Could not save history (storage unavailable)."); } }

  /* ---------- shared settings (kept across dashboard pages) ---------- */
  var cfg = { area: "residential", period: "day", calib: 90 };
  try { var s = JSON.parse(localStorage.getItem("sn_settings")); if (s && D.limits[s.area]) cfg.area = s.area; if (s && (s.period === "day" || s.period === "night")) cfg.period = s.period; if (s && isFinite(s.calib)) cfg.calib = +s.calib; } catch (e) {}
  function saveCfg() { try { localStorage.setItem("sn_settings", JSON.stringify(cfg)); } catch (e) {} }
  function limit() { return D.limits[cfg.area][cfg.period]; }
  function areaName() { return D.limits[cfg.area].name; }
  function bindSettings() {
    var a = $("area"), p = $("period"), c = $("calib");
    if (a) { a.value = cfg.area; a.onchange = function () { cfg.area = a.value; saveCfg(); refreshSettings(); }; }
    if (p) { p.value = cfg.period; p.onchange = function () { cfg.period = p.value; saveCfg(); refreshSettings(); }; }
    if (c) { c.value = cfg.calib; c.onchange = function () { cfg.calib = parseFloat(c.value) || 90; saveCfg(); }; }
  }

  /* ---------- status ---------- */
  function statusOf(v) {
    var l = limit();
    if (v < l - 10) return ["low", "LOW"];
    if (v <= l) return ["moderate", "MODERATE"];
    if (v <= l + 10) return ["high", "HIGH"];
    return ["veryhigh", "VERY HIGH"];
  }

  /* ---------- microphone / demo (monitor page) ---------- */
  function readMic() {
    st.analyser.getFloatTimeDomainData(st.buf);
    var sum = 0, i; for (i = 0; i < st.buf.length; i++) sum += st.buf[i] * st.buf[i];
    var rms = Math.sqrt(sum / st.buf.length);
    if (rms < 1e-5) return null;
    // Transparent estimate: dBFS = 20*log10(rms) plus a user-adjustable offset. NOT calibrated dB SPL.
    var est = 20 * Math.log10(rms) + cfg.calib;
    return Math.max(20, Math.min(120, est));
  }
  function startMic() {
    showErr("");
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) return showErr("This browser does not support microphone access. Please use Demo Mode or a modern browser over HTTPS/localhost.");
    stop(true); setText("micStatus", "Requesting permission...");
    navigator.mediaDevices.getUserMedia({ audio: true }).then(function (stream) {
      var AC = window.AudioContext || window.webkitAudioContext;
      if (!AC) { stream.getTracks().forEach(function (t) { t.stop(); }); return showErr("Web Audio API is not supported. Please use Demo Mode."); }
      st.stream = stream; st.ctx = new AC(); st.analyser = st.ctx.createAnalyser(); st.analyser.fftSize = 1024;
      st.buf = new Float32Array(st.analyser.fftSize); st.ctx.createMediaStreamSource(stream).connect(st.analyser);
      begin("mic");
    }).catch(function (e) {
      setText("micStatus", "Unavailable");
      var n = e && e.name;
      showErr(n === "NotAllowedError" || n === "SecurityError" ? "Microphone permission was denied. Allow access in your browser, or launch Demo Mode."
        : n === "NotFoundError" ? "No microphone was found on this device. Try Demo Mode."
        : "Could not start the microphone (" + (n || "unknown error") + "). Try Demo Mode.");
    });
  }
  function demoValue() {
    var base = D.demoBase[cfg.area] + (cfg.period === "night" ? -4 : 0);
    var drift = (st.last || base) + (Math.random() - 0.5) * 5 + (base - (st.last || base)) * 0.1;
    if (Math.random() < 0.04) drift += 12 + Math.random() * 8; // occasional simulated loud event
    return Math.max(30, Math.min(110, drift));
  }
  function begin(mode) {
    st.mode = mode; st.start = Date.now(); st.vals = []; st.alerts = 0; st.over = false; st.last = 0; st.lastSave = 0;
    var sim = mode === "demo";
    $("simTag").hidden = !sim; $("dot").className = "dot " + (sim ? "sim" : "on");
    setText("modeLabel", sim ? "DEMO MODE" : "MICROPHONE LIVE");
    setText("micStatus", sim ? "Not used (simulated)" : "Active");
    $("stop").disabled = false; $("alertBox").hidden = true;
    st.timer = setInterval(tick, 500); tick();
  }
  function tick() {
    var v = st.mode === "demo" ? demoValue() : readMic();
    var sec = Math.floor((Date.now() - st.start) / 1000); setText("duration", fmt(sec)); setText("sTime", fmt(sec));
    if (v === null) { showErr("No audio input detected. Check that your microphone is not muted."); return; }
    showErr(""); v = Math.round(v * 10) / 10; st.last = v; st.vals.push(v); if (st.vals.length > 120) st.vals.shift();
    var s = statusOf(v); setText("level", Math.round(v)); setText("status", s[1]); $("status").dataset.s = s[0];
    var over = v > limit(); if (over && !st.over) { st.alerts++; showAlert(v); notifyAlert(v); } st.over = over;
    var all = st.vals; setText("sCur", Math.round(v));
    setText("sAvg", Math.round(all.reduce(function (a, b) { return a + b; }, 0) / all.length));
    setText("sMax", Math.round(Math.max.apply(null, all))); setText("sMin", Math.round(Math.min.apply(null, all))); setText("sAlerts", st.alerts);
    if (Date.now() - st.lastSave > 5000) { st.lastSave = Date.now(); record(v, s[1], over); }
    drawChart(); drawWave(v);
  }
  function stop(silent) {
    clearInterval(st.timer); st.timer = null;
    if (st.stream) st.stream.getTracks().forEach(function (t) { t.stop(); });
    if (st.ctx && st.ctx.close) st.ctx.close().catch(function () {});
    st.stream = st.ctx = st.analyser = null; st.mode = null;
    if (!$("dot")) return;
    $("dot").className = "dot"; setText("modeLabel", "IDLE"); $("simTag").hidden = true; $("stop").disabled = true;
    if (!silent) { setText("micStatus", "Off"); setText("status", "NOT MONITORING"); $("status").dataset.s = "idle"; }
  }
  var lastNote = 0;
  function notifyAlert(v) {
    if (!window.SN_notify || Date.now() - lastNote < 60000) return; lastNote = Date.now();
    SN_notify({ type: "alert", title: (st.mode === "demo" ? "Demo: " : "") + "Elevated noise detected", body: "Estimated " + Math.round(v) + " dB in a " + areaName() + " area, above the " + limit() + " dB(A) reference limit." });
  }
  function showAlert(v) {
    var box = $("alertBox"), sim = st.mode === "demo";
    box.innerHTML = "<h3>&#9888; Elevated noise detected" + (sim ? " <span class='tag sim'>SIMULATED</span>" : "") + "</h3>" +
      "<p>Estimated level: <b>" + Math.round(v) + " dB</b> &middot; Area: <b>" + esc(areaName()) + "</b> &middot; Reference threshold: <b>" + limit() + " dB(A)</b> &middot; Time: <b>" + new Date().toLocaleTimeString() + "</b></p>" +
      "<p>Recommended action: " + esc(D.tips[cfg.area][0]) + "</p><button class='btn sm' id='dismiss'>Dismiss</button>";
    box.hidden = false; $("dismiss").onclick = function () { box.hidden = true; };
  }

  /* ---------- drawing (plain canvas, no libraries) ---------- */
  function lineChart(c, vals, maxPts, withLimit) {
    var g = c.getContext("2d"), W = c.width, H = c.height, p = 36, lo = 20, hi = 120, grid = cssVar("--line") || "#ccc", txt = cssVar("--mut") || "#888", pri = cssVar("--pri") || "#4f46e5", warn = cssVar("--hi") || "#ea580c";
    g.clearRect(0, 0, W, H); g.font = "600 12px 'Plus Jakarta Sans',system-ui,sans-serif"; g.fillStyle = txt; g.strokeStyle = grid; g.lineWidth = 1;
    for (var y = lo; y <= hi; y += 20) { var py = H - p - (y - lo) / (hi - lo) * (H - 2 * p); g.beginPath(); g.moveTo(p, py); g.lineTo(W - 10, py); g.stroke(); g.fillText(y, 4, py + 4); }
    if (withLimit) { var ly = H - p - (limit() - lo) / (hi - lo) * (H - 2 * p); g.setLineDash([6, 5]); g.strokeStyle = warn; g.beginPath(); g.moveTo(p, ly); g.lineTo(W - 10, ly); g.stroke(); g.setLineDash([]); }
    if (vals.length < 2) return;
    g.strokeStyle = pri; g.lineWidth = 2.5; g.lineJoin = "round"; g.beginPath();
    vals.forEach(function (v, i) { var x = p + i / (maxPts - 1) * (W - p - 10), yy = H - p - (Math.max(lo, Math.min(hi, v)) - lo) / (hi - lo) * (H - 2 * p); i ? g.lineTo(x, yy) : g.moveTo(x, yy); }); g.stroke();
  }
  function drawChart() { var c = $("chart"); if (!c || !c.getContext) return; lineChart(c, st.vals, 120, true); }
  function drawWave(v) {
    var c = $("wave"); if (!c) return;
    var g = c.getContext("2d"), W = c.width, H = c.height, t = Date.now() / 200, amp = ((v || 20) - 20) / 100 * (H / 2);
    g.clearRect(0, 0, W, H); g.strokeStyle = cssVar("--acc") || "#06b6d4"; g.lineWidth = 2.5; g.beginPath();
    for (var x = 0; x < W; x += 3) { var y = H / 2 + Math.sin(x / 18 + t) * amp * Math.sin(x / W * Math.PI); x ? g.lineTo(x, y) : g.moveTo(x, y); } g.stroke();
  }

  /* ---------- history ---------- */
  function record(v, status, over) {
    if (window.SN_prefs && SN_prefs().saveHistory === false) return;
    var h = loadHist(), d = new Date();
    h.push({ id: d.getTime() + Math.random(), date: d.toLocaleDateString(), time: d.toLocaleTimeString(), area: areaName(), period: cfg.period, level: Math.round(v), status: status, over: !!over, type: st.mode === "demo" ? "Simulated" : "Mic estimate" });
    saveHist(h); renderHist(); renderOverview();
  }
  function renderHist() {
    var b = $("histBody"); if (!b) return;
    var h = loadHist(); b.innerHTML = "";
    $("histEmpty").hidden = h.length > 0;
    h.slice(-20).reverse().forEach(function (r) {
      var tr = document.createElement("tr");
      tr.innerHTML = "<td>" + esc(r.date) + "</td><td>" + esc(r.time) + "</td><td>" + esc(r.area) + "</td><td>" + r.level + " dB</td><td>" + esc(r.status) + "</td><td>" + esc(r.type) + "</td><td><button class='btn sm' aria-label='Delete record'>&times;</button></td>";
      tr.querySelector("button").onclick = function () { saveHist(loadHist().filter(function (x) { return x.id !== r.id; })); renderHist(); renderOverview(); };
      b.appendChild(tr);
    });
  }
  function renderOverview() {
    var h = loadHist(), lv = h.map(function (r) { return r.level; });
    var avg = lv.length ? Math.round(lv.reduce(function (a, b) { return a + b; }, 0) / lv.length) : "--";
    setText("ovCount", h.length); setText("ovAvg", avg); setText("ovMax", lv.length ? Math.max.apply(null, lv) : "--"); setText("ovMin", lv.length ? Math.min.apply(null, lv) : "--");
    setText("ovAlerts", h.filter(function (r) { return r.status === "HIGH" || r.status === "VERY HIGH"; }).length);
    setText("ovLast", h.length ? h[h.length - 1].level + " dB" : "--");
    var rc = $("recent"); if (rc) {
      rc.innerHTML = ""; $("recentEmpty").hidden = h.length > 0;
      h.slice(-5).reverse().forEach(function (r) { var tr = document.createElement("tr"); tr.innerHTML = "<td>" + esc(r.date) + "</td><td>" + esc(r.time) + "</td><td>" + esc(r.area) + "</td><td>" + r.level + " dB</td><td>" + esc(r.status) + "</td><td>" + esc(r.type) + "</td>"; rc.appendChild(tr); });
    }
    var hc = $("hchart"); if (hc && hc.getContext) { var vs = lv.slice(-60); lineChart(hc, vs, Math.max(vs.length, 2), false); setText("hchartMsg", vs.length < 2 ? "Record at least two readings on the Live Monitor to see a trend." : "Last " + vs.length + " saved readings (estimated dB)."); }
  }
  function exportCsv() {
    var h = loadHist(); if (!h.length) return showErr("No history to export yet.");
    var rows = [["Date", "Time", "Area", "Day/Night", "Estimated Level (dB)", "Status", "Data Type"]].concat(h.map(function (r) { return [r.date, r.time, r.area, r.period, r.level, r.status, r.type]; }));
    var csv = rows.map(function (r) { return r.map(function (c) { return '"' + String(c).replace(/"/g, '""') + '"'; }).join(","); }).join("\r\n");
    var url = URL.createObjectURL(new Blob([csv], { type: "text/csv;charset=utf-8;" })), a = document.createElement("a");
    a.href = url; a.download = "smartnoise-history.csv"; document.body.appendChild(a); a.click(); a.remove(); setTimeout(function () { URL.revokeObjectURL(url); }, 500);
  }

  /* ---------- UI refresh ---------- */
  function refreshSettings() {
    setText("areaLabel", areaName()); setText("recArea", areaName()); setText("periodLabel", cfg.period === "day" ? "Day" : "Night");
    setText("limit", limit() + " dB(A)");
    var rl = $("recList"); if (rl) rl.innerHTML = D.tips[cfg.area].map(function (t) { return "<li>" + esc(t) + "</li>"; }).join("");
    st.over = false; drawChart();
  }
  function buildZones() {
    var z = $("zoneGrid"); if (!z) return;
    z.innerHTML = D.zones.map(function (x) {
      var c = x.v > 70 ? "#dc2626" : x.v > 60 ? "#ea580c" : x.v > 50 ? "#b45309" : "#059669";
      return "<div class='zone' style='border-top-color:" + c + "'><div class='ic'>" + x.icon + "</div><h3>" + x.name + "</h3><b>" + x.v + " dB</b><span class='tag sim'>DEMO / SIMULATED</span></div>";
    }).join("");
  }

  /* ---------- wiring (only what exists on this page) ---------- */
  bindSettings();
  if ($("startMic")) { $("startMic").onclick = startMic; $("startDemo").onclick = function () { showErr(""); stop(true); begin("demo"); }; $("stop").onclick = function () { stop(false); }; drawWave(0); }
  if ($("exportCsv")) $("exportCsv").onclick = exportCsv;
  if ($("clearHist")) $("clearHist").onclick = function () { if (confirm("Delete all saved history?")) { saveHist([]); renderHist(); renderOverview(); } };
  buildZones(); refreshSettings(); renderHist(); renderOverview();
  window.addEventListener("beforeunload", function () { stop(true); });
  new MutationObserver(function () { drawChart(); renderOverview(); }).observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
})();
