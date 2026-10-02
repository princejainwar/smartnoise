/* SmartNoise login / create-account page logic (browser-only demo accounts).
   Passwords are salted and hashed (PBKDF2); nothing leaves the browser. */
(function () {
  "use strict";
  var $ = function (id) { return document.getElementById(id); };
  var USERS = "smartnoise_users", SESSION = "smartnoise_session";
  function readUsers() { try { var u = JSON.parse(localStorage.getItem(USERS)); return u && typeof u === "object" && !Array.isArray(u) ? u : {}; } catch (e) { return {}; } }
  function hex(b) { return Array.prototype.map.call(new Uint8Array(b), function (x) { return x.toString(16).padStart(2, "0"); }).join(""); }
  function cryptoOk() { return !!(window.crypto && crypto.subtle && window.TextEncoder); }
  function derive(pw, salt) {
    var enc = new TextEncoder();
    return crypto.subtle.importKey("raw", enc.encode(pw), "PBKDF2", false, ["deriveBits"]).then(function (k) {
      return crypto.subtle.deriveBits({ name: "PBKDF2", salt: enc.encode(salt), iterations: 100000, hash: "SHA-256" }, k, 256);
    }).then(hex);
  }
  function err(m) { $("authErr").textContent = m; $("authErr").hidden = !m; }
  function tr(key, fallback) { try { var d = window.SN_I18N && window.SN_I18N.dict; return d && d.errors && d.errors[key] || fallback; } catch (e) { return fallback; } }
  function enter(email) {
    try { localStorage.setItem(SESSION, email); sessionStorage.setItem("sn_celebrate", "1"); } catch (e) {}
    location.href = "dashboard.html";
  }
  function tab(t) {
    var login = t !== "signup"; err("");
    $("forgotForm").hidden = true; $("loginForm").hidden = !login; $("signupForm").hidden = login;
    $("tabLogin").hidden = false; $("tabSignup").hidden = false;
    
    $("tabLogin").setAttribute("aria-selected", login); $("tabSignup").setAttribute("aria-selected", !login);
  }
  $("loginForm").addEventListener("submit", function (e) {
    e.preventDefault(); err("");
    var email = $("liEmail").value.trim().toLowerCase(), pw = $("liPass").value, u = readUsers()[email];
    if (!email || !pw) return err(tr("emailPass", "Please enter your email and password."));
    if (!cryptoOk()) return err(tr("secureLogin", "Secure login needs HTTPS or localhost. Please open the site that way."));
    if (!u) return err(tr("noAccount", "No account found for this email in this browser. Please create an account first."));
    derive(pw, u.salt).then(function (h) { if (h !== u.hash) return err(tr("incorrect", "Incorrect password.")); enter(email); }).catch(function () { err(tr("loginFailed", "Login failed. Please try again.")); });
  });
  $("showForgot").onclick = function () {
    err(""); $("loginForm").hidden = true; $("signupForm").hidden = true; $("forgotForm").hidden = false;
    $("tabLogin").hidden = true; $("tabSignup").hidden = true; $("frEmail").value = $("liEmail").value.trim();
  };
  $("cancelForgot").onclick = function () { tab("login"); };
  $("forgotForm").addEventListener("submit", function (e) {
    e.preventDefault(); err("");
    var email = $("frEmail").value.trim().toLowerCase(), name = $("frName").value.trim(), p1 = $("frPass").value, p2 = $("frPass2").value, users = readUsers(), u = users[email];
    if (!u || !name || String(u.name || "").trim().toLowerCase() !== name.toLowerCase()) return err("We could not match that email and name in this browser.");
    if (p1.length < 8) return err("Password must be at least 8 characters.");
    if (p1 !== p2) return err("Passwords do not match.");
    if (!cryptoOk()) return err("Password reset needs HTTPS or localhost. Please open the site that way.");
    var a = new Uint8Array(16); crypto.getRandomValues(a); var salt = hex(a);
    derive(p1, salt).then(function (h) {
      users[email].salt = salt; users[email].hash = h;
      try { localStorage.setItem(USERS, JSON.stringify(users)); } catch (x) { return err("Could not save the new password (browser storage is unavailable)."); }
      $("liEmail").value = email; $("liPass").value = ""; $("forgotForm").reset(); tab("login"); err("Password reset on this browser. You can now log in.");
    }).catch(function () { err("Could not reset the password. Please try again."); });
  });
  $("signupForm").addEventListener("submit", function (e) {
    e.preventDefault(); err("");
    var name = $("suName").value.trim(), email = $("suEmail").value.trim().toLowerCase(), pw = $("suPass").value;
    if (!name) return err(tr("name", "Please enter your name."));
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return err(tr("validEmail", "Please enter a valid email address."));
    if (pw.length < 8) return err(tr("minPass", "Password must be at least 8 characters."));
    if (pw !== $("suPass2").value) return err(tr("match", "Passwords do not match."));
    if (!cryptoOk()) return err("Secure sign-up needs HTTPS or localhost. Please open the site that way.");
    var users = readUsers(); if (users[email]) return err(tr("exists", "An account with this email already exists. Please login."));
    var a = new Uint8Array(16); crypto.getRandomValues(a); var salt = hex(a);
    derive(pw, salt).then(function (h) {
      users[email] = { name: name, salt: salt, hash: h, created: new Date().toISOString(), language: (window.SN_i18nGet ? window.SN_i18nGet() : "en") };
      try { localStorage.setItem(USERS, JSON.stringify(users)); } catch (x) { return err(tr("storage", "Could not save your account (browser storage is unavailable).")); }
      enter(email);
    }).catch(function () { err(tr("signupFailed", "Could not create the account. Please try again.")); });
  });
  /* eye buttons: show / hide password */
  document.querySelectorAll(".eye").forEach(function (b) {
    b.addEventListener("click", function () {
      var i = $(b.dataset.for), show = i.type === "password"; i.type = show ? "text" : "password";
      b.setAttribute("aria-pressed", show); b.setAttribute("aria-label", show ? "Hide password" : "Show password");
      b.querySelector("path").setAttribute("d", show ? "M3 3l18 18M10.6 6.2A9 9 0 0121 12a13 13 0 01-3 3.7M6.6 6.6A13 13 0 003 12s3.5 7 9 7a9 9 0 004.4-1.2M9.9 9.9a3 3 0 004.2 4.2" : "M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12zM12 15a3 3 0 100-6 3 3 0 000 6z");
    });
  });
  $("tabLogin").onclick = function () { tab("login"); }; $("tabSignup").onclick = function () { tab("signup"); };
  tab(new URLSearchParams(location.search).get("tab"));
  if (localStorage.getItem(SESSION) && readUsers()[localStorage.getItem(SESSION)]) location.replace("dashboard.html");
})();
