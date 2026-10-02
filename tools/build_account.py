# Account pages (exec'd from build.py; shares its helpers)
I.update({"user":"M12 12a4 4 0 100-8 4 4 0 000 8zM4 21a8 8 0 0116 0","edit":"M4 20h4L19 9l-4-4L4 16zM13.5 6.5l4 4","upload":"M12 16V4m0 0L7 9m5-5l5 5M5 20h14","doc":"M7 3h8l4 4v14H7zM14 3v5h5M10 13h6M10 17h6","gear":"M12 15a3 3 0 100-6 3 3 0 000 6zM4 12h2m12 0h2M12 4v2m0 12v2"})
def F(id, label, ctl, hint="", full=False):
    return f'<div class="{"full" if full else ""}"><label for="{id}">{label}</label>{ctl}{f"<p class=hint>{hint}</p>" if hint else ""}<p class="ferr" id="{id}Err" hidden></p></div>'
def sw(id, t, d): return f'<div class="trow"><div><b>{t}</b><span class="d">{d}</span></div><label class="switch"><input type="checkbox" id="{id}" aria-label="{t}"><span></span></label></div>'
def ahero(crumb, h1, lead, act=""):
    return phero(crumb, h1, lead, act)
AP = dict(protected=True, scripts="common.js")

# ---- profile ----
body = ahero("Profile","My profile","Your account information.", f'<div class="cta"><a class="btn primary" href="profile-edit.html">{ic("edit")} Edit Profile</a><a class="btn" href="settings.html">Settings</a><button class="btn danger" id="pfLogout" type="button">{ic("out")} Log out</button></div>') + f'''<section class="section tight"><div class="wrap"><div class="profile-tiles-scroll" aria-label="Profile details"><div class="grid" id="pfGrid">
<div class="card"><div class="profile-head"><div id="pfAvatar"></div><div><h2 id="pfName"></h2><p class="muted" id="pfEmail" style="margin:0"></p></div></div>
<hr style="border:0;border-top:1px solid var(--line);margin:26px 0"><h3>Personal information</h3><dl class="kv" style="margin-top:16px"><dt>Full name</dt><dd id="pfName2"></dd><dt>Email</dt><dd id="pfEmail2"></dd><dt>Country</dt><dd id="pfCountry"></dd><dt>Preferred language</dt><dd id="pfLang"></dd></dl></div>
<div class="card"><h3>Account information</h3><dl class="kv" style="margin-top:16px;grid-template-columns:130px 1fr"><dt>Member since</dt><dd id="pfSince"></dd><dt>Reports submitted</dt><dd><a href="my-reports.html" id="pfReports"></a></dd><dt>Readings saved</dt><dd><a href="analytics.html" id="pfReadings"></a></dd><dt>Unread alerts</dt><dd><a href="notifications.html" id="pfUnread"></a></dd><dt>Data storage</dt><dd>This browser only</dd></dl></div></div></div></section><style>.profile-tiles-scroll{{max-height:520px;overflow-y:auto;overscroll-behavior:contain;padding:2px 10px 10px 2px;scrollbar-width:thin;scrollbar-color:var(--pri) var(--surface-2)}}.profile-tiles-scroll::-webkit-scrollbar{{width:10px}}.profile-tiles-scroll::-webkit-scrollbar-thumb{{background:var(--pri);border:3px solid var(--surface-2);border-radius:99px}}#pfGrid{{grid-template-columns:1fr;gap:18px}}@media(max-width:900px){{#pfGrid{{grid-template-columns:1fr}}}}</style>
<script>document.addEventListener("DOMContentLoaded",function(){{["Name","Email"].forEach(function(k){{var a=document.getElementById("pf"+k),b=document.getElementById("pf"+k+"2");if(a&&b)b.textContent=a.textContent}})}});</script>'''
page("profile.html","My Profile | SmartNoise","Your SmartNoise profile and account information.",body,pg="profile",**AP)

# ---- edit profile ----
body = ahero('<a href="profile.html">Profile</a> / Edit',"Edit profile","Update your photo and personal information.") + f'''<section class="section tight"><div class="wrap" style="max-width:760px"><form class="card" id="editForm" novalidate>
<div class="uploader"><div id="epAvatar"></div><div><label class="btn sm" for="epPhoto" style="margin:0;cursor:pointer">{ic("upload")} Upload photo</label><input id="epPhoto" type="file" accept="image/jpeg,image/png,image/webp,image/gif" class="sr"><button class="btn sm ghost" type="button" id="epRemove" hidden style="margin-left:8px">Remove</button><p class="hint">JPG, PNG, WebP or GIF up to 8 MB. Cropped to a square and stored privately in this browser.</p><p class="ferr" id="epPhotoErr" hidden></p></div></div>
<hr style="border:0;border-top:1px solid var(--line);margin:26px 0 4px">
<div class="form-grid">{F("epName","Full name",'<input id="epName" type="text" autocomplete="name" maxlength="60" required>')}{F("epEmail","Email",'<input id="epEmail" type="email" autocomplete="email" required>',"Changing your email requires your current password.")}
<div class="full" id="epPwBox" hidden>{F("epPw","Current password",'<input id="epPw" type="password" autocomplete="current-password">')}</div>
{F("epCountry","Country",'<select id="epCountry"></select>')}{F("epLang","Preferred language",'<select id="epLang"></select>',"Stored for future translations. The site is currently in English.")}</div>
<p class="error" id="epErr" role="alert" hidden></p>
<div class="cta"><button class="btn primary" type="submit" id="epSave">Save Changes</button><button class="btn" type="button" id="epCancel">Cancel</button></div></form></div></section>'''
page("profile-edit.html","Edit Profile | SmartNoise","Update your SmartNoise profile picture, name, email, country and language.",body,pg="profile-edit",**AP)

# ---- submit data ----
body = ahero("Submit Data","Submit noise data","Record a noise observation with its location, level and source. Reports are saved to your account.") + f'''<section class="section tight"><div class="wrap split" style="align-items:start"><form class="card" id="sdForm" novalidate>
<div class="form-grid">{F("sdLoc","Location",'<input id="sdLoc" type="text" maxlength="200" placeholder="Street, area or landmark" required>',full=True)}
{F("sdLevel","Noise level (dB)",'<input id="sdLevel" type="number" min="20" max="140" step="0.1" required>',"Estimated or measured, 20 to 140 dB.")}
<div style="display:flex;align-items:end;padding-bottom:22px"><button class="btn sm" type="button" id="sdLatest">Use my latest saved reading</button></div>
{F("sdDate","Date",'<input id="sdDate" type="date" required>')}{F("sdTime","Time",'<input id="sdTime" type="time" required>')}
{F("sdCat","Noise category / source",'<select id="sdCat" required></select>',full=True)}
{F("sdDesc","Description",'<textarea id="sdDesc" maxlength="1000" placeholder="What did you hear, for how long, and how often?" required></textarea><p class="hint" id="sdCount" style="text-align:right">0 / 1000</p>',full=True)}
{F("sdImg","Evidence image (optional)",'<input id="sdImg" type="file" accept="image/jpeg,image/png,image/webp,image/gif">',"Resized and stored privately in this browser.",full=True)}</div>
<div class="uploader" id="sdPrev" style="margin-top:6px"></div><p class="error" id="sdErr" role="alert" hidden></p>
<div class="cta"><button class="btn primary lg" type="submit">Submit report</button><a class="btn lg" href="my-reports.html">Cancel</a></div></form>
<div class="card">{ico("flag")}<h3>Before you submit</h3><ul class="ticks" style="margin-top:12px"><li>Reports are saved to your SmartNoise account on this device.</li><li>They are <b>not</b> sent to any authority. For a formal complaint use the <a href="complaints.html">official portals</a>.</li><li>For a live disturbance call <a href="helplines.html">112</a>.</li></ul></div></div></section><style>@media(max-width:640px){{#sdForm .form-grid>div[style]{{padding-bottom:0!important;margin-bottom:14px}}}}</style>'''
page("submit-data.html","Submit Data | SmartNoise","Submit a noise observation with location, level, date, time, category and optional evidence.",body,pg="submit-data",**AP)

# ---- my reports ----
body = ahero("My Reports","My reports","Track the reports you have submitted and their current status.", f'<div class="cta"><a class="btn primary" href="submit-data.html">{ic("upload")} Submit new data</a></div>') + f'''<section class="section tight"><div class="wrap">
<div class="filters" id="rpFilters" hidden>{"".join(f'<button class="chip" data-flt="{x}" aria-pressed="false">{x}</button>' for x in ["All","Submitted","Under Review","Resolved"])}</div>
<div id="rpList"></div>
<div class="card empty-state" id="rpEmpty" hidden>{ico("doc")}<h3>No reports yet</h3><p>Reports you submit will appear here with their status: Submitted, Under Review, Resolved.</p><div class="cta" style="justify-content:center"><a class="btn primary" href="submit-data.html">Submit your first report</a></div></div>
<p class="note">Status changes need a reviewing service, which this static version does not have. Use "Simulate next status (demo)" to preview how updates and notifications behave.</p></div></section>'''
page("my-reports.html","My Reports | SmartNoise","Your submitted noise reports and their review status.",body,pg="my-reports",**AP)

# ---- notifications ----
body = ahero("Notifications","Notifications","Noise alerts, complaint updates and account messages.") + f'''<section class="section tight"><div class="wrap" style="max-width:820px">
<div class="row" id="ntBar" hidden><div class="filters" style="margin:0">{"".join(f'<button class="chip" data-nf="{k}" aria-pressed="false">{v}</button>' for k,v in [("all","All"),("unread","Unread")])}</div><div class="cta" style="margin:0"><button class="btn sm" id="ntReadAll">Mark all as read</button><button class="btn sm danger ghost" id="ntClear">Clear all</button></div></div>
<div id="ntList"></div>
<div class="card empty-state" id="ntEmpty" hidden>{ico("bell")}<h3>No notifications</h3><p>Noise alerts from the Live Monitor and updates on your reports will appear here.</p></div>
<p class="note">Choose which notifications you receive in <a href="settings.html">Settings</a>.</p></div></section>'''
page("notifications.html","Notifications | SmartNoise","Your SmartNoise noise alerts, complaint updates and account notifications.",body,pg="notifications",**AP)

# ---- settings ----
body = ahero("Settings","Settings","Manage your account, preferences, notifications and security.") + f'''<section class="section tight"><div class="wrap" style="max-width:820px;display:grid;gap:20px">
<div class="card"><h3>Account</h3><div class="profile-head" style="margin-top:16px"><div id="stAvatar"></div><div style="flex:1;min-width:200px"><b id="stName"></b><p class="muted" id="stEmail" style="margin:0"></p></div></div>
<div class="cta"><label class="btn sm" for="stPhoto" style="margin:0;cursor:pointer">{ic("upload")} Change picture</label><input id="stPhoto" type="file" accept="image/jpeg,image/png,image/webp,image/gif" class="sr"><button class="btn sm ghost" id="stRemovePhoto" type="button">Remove picture</button><a class="btn sm" href="profile-edit.html">Edit name and email</a></div><p class="ferr" id="stPhotoErr" hidden></p></div>
<form class="card" id="stPrefs"><h3>Preferences</h3><div class="form-grid">{F("stLang","Language",'<select id="stLang"></select>',"Stored for future translations. The site is currently in English.")}{F("stCountry","Country",'<select id="stCountry"></select>')}{F("stTheme","Theme",'<select id="stTheme"><option value="day">Light</option><option value="dark">Dark</option></select>')}</div>
<h3 style="margin-top:28px">Notifications</h3>{sw("tNoise","Noise alerts","Notify me when the Live Monitor exceeds the reference limit.")}{sw("tComplaint","Complaint updates","Notify me about status changes to my reports.")}{sw("tEmail","Email notifications","Saved as a preference. Sending email needs a server, which this version does not have.")}
<h3 style="margin-top:28px">Privacy</h3>{sw("tHistory","Save monitoring history","Record readings in this browser. Turn off to stop saving new readings.")}
<div class="cta"><button class="btn primary" type="submit">Save preferences</button></div></form>
<form class="card" id="pwForm" novalidate><h3>Security</h3><p class="muted">Change your password. Passwords are salted and hashed in this browser and are never stored in plain text.</p><div class="form-grid">{F("pwCur","Current password",'<input id="pwCur" type="password" autocomplete="current-password">',full=True)}{F("pwNew","New password",'<input id="pwNew" type="password" autocomplete="new-password">')}{F("pwNew2","Confirm new password",'<input id="pwNew2" type="password" autocomplete="new-password">')}</div><div class="cta" style="margin-top:0"><button class="btn primary" type="submit">Update password</button></div></form>
<div class="card"><h3>Your data</h3><p class="muted">Your profile is private: it is visible only to you and stored on this device. There is no public profile.</p><div class="cta"><button class="btn" id="exportData" type="button">Download my data (JSON)</button></div></div>
<form class="card danger-card" id="delForm" novalidate><h3>Delete account</h3><p class="muted">Permanently removes your account, reports, notifications and history from this browser.</p>{F("delPw","Confirm with your password",'<input id="delPw" type="password" autocomplete="current-password">')}<div class="cta" style="margin-top:0"><button class="btn danger" type="submit">Delete my account</button></div></form>
</div></section>'''
page("settings.html","Settings | SmartNoise","Manage your SmartNoise account, preferences, notifications and security.",body,pg="settings",**AP)
