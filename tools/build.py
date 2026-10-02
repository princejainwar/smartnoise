# Generates the static multi-page site. Run from SmartNoise/: python3 ../tools/build.py
import html, os
OWNER = "princejainwar43@gmail.com"
LOGIN_TEMPLATE = open("login.html", encoding="utf-8").read() if os.path.exists("login.html") else None
I = {
 "phone":"M5 4h4l2 5-2.5 1.5a11 11 0 005 5L15 13l5 2v4a2 2 0 01-2 2A16 16 0 013 6a2 2 0 012-2z",
 "flag":"M5 21V4m0 0h12l-2 4 2 4H5","gauge":"M3 17a9 9 0 1118 0M12 17l4-6","mic":"M12 3a3 3 0 00-3 3v6a3 3 0 006 0V6a3 3 0 00-3-3zM6 11a6 6 0 0012 0M12 17v4",
 "chart":"M4 20V4M4 20h16M8 16l4-5 3 3 5-7","pin":"M12 21s7-6 7-12a7 7 0 10-14 0c0 6 7 12 7 12zM12 11a2 2 0 100-4 2 2 0 000 4z","bulb":"M9 18h6M10 21h4M12 3a6 6 0 00-4 10c1 1 1 2 1 3h6c0-1 0-2 1-3a6 6 0 00-4-10z",
 "mail":"M3 6h18v12H3zM3 7l9 7 9-7","bell":"M6 8a6 6 0 1112 0c0 7 3 8 3 8H3s3-1 3-8zM10 20a2 2 0 004 0","download":"M12 4v11m0 0l-4-4m4 4l4-4M5 20h14","play":"M7 4l13 8-13 8z",
 "shield":"M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z","arrow":"M5 12h14M13 6l6 6-6 6","grid":"M4 4h7v7H4zM13 4h7v7h-7zM4 13h7v7H4zM13 13h7v7h-7z","moon":"M20 14.5A8 8 0 019.5 4 8 8 0 1020 14.5z",
 "sun":"M12 17a5 5 0 100-10 5 5 0 000 10zM12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4","menu":"M4 7h16M4 12h16M4 17h16","out":"M15 3h4a2 2 0 012 2v14a2 2 0 01-2 2h-4M10 17l5-5-5-5M15 12H3","clock":"M12 21a9 9 0 100-18 9 9 0 000 18zM12 7v5l3 2","book":"M4 5a2 2 0 012-2h13v16H6a2 2 0 00-2 2zM4 19a2 2 0 012-2h13",
}
def ic(n, cls=""): return f'<svg viewBox="0 0 24 24" aria-hidden="true"{(" class=%s" % chr(34)+cls+chr(34)) if cls else ""}><path d="{I[n]}"/></svg>'
def ico(n): return f'<div class="ico">{ic(n)}</div>'

NAV = [("dashboard.html","Dashboard"),("monitor.html","Live Monitor"),("analytics.html","Analytics"),("awareness.html","Awareness"),("complaints.html","Help & reports")]
SUB = [("dashboard.html","Overview"),("monitor.html","Live Monitor"),("analytics.html","Analytics"),("zones.html","Noise Zones"),("controls.html","Smart Controls")]

def head(title, desc, extra=""):
    t = html.escape(title); d = html.escape(desc)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#4f46e5">
<link rel="icon" href="assets/icons/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="style.css">
<script>try{{document.documentElement.dataset.theme=localStorage.getItem("sn_theme")||"day"}}catch(e){{document.documentElement.dataset.theme="day"}}</script>
{extra}</head>
'''

def navbar(cur):
    links = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h==cur else ""} data-i18n="{n}">{n}</a>' for h,n in NAV)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="nav"><div class="wrap">
<a class="brand" href="dashboard.html" aria-label="SmartNoise dashboard"><img src="assets/images/logo.svg" alt="" width="34" height="34">SmartNoise</a>
<nav class="links" id="navLinks" aria-label="Main navigation">{links}<a class="mobile-only" data-guest hidden href="login.html?tab=signup">Create Account</a></nav>
<div class="nav-right">
<button class="icon-btn" id="themeBtn" aria-label="Switch to dark mode" aria-pressed="false"><span class="moon">{ic("moon")}</span><span class="sun">{ic("sun")}</span></button>
<div class="acct" id="acct" data-state="loading" aria-live="polite"><span class="sk sk-circle"></span><span class="sk sk-line"></span><noscript><a class="btn primary" href="login.html">Login</a></noscript></div>
<button class="icon-btn burger" id="burger" aria-label="Open menu" aria-expanded="false" aria-controls="navLinks">{ic("menu")}</button>
</div></div><div class="header-tile-row"><div class="wrap"><a class="header-tile" href="research.html"><span class="header-tile-mark">LEARN</span><span><b>Learning</b><small>Research &amp; study notes</small></span></a><a class="header-tile" href="team.html"><span class="header-tile-mark team-mark">TEAM</span><span><b>Team</b><small>About the project</small></span></a></div></div></header>
'''

def subnav(cur):
    return '<nav class="subnav" aria-label="Dashboard"><div class="wrap">' + "".join(f'<a href="{h}"{" aria-current=\"page\"" if h==cur else ""}>{n}</a>' for h,n in SUB) + '</div></nav>\n'

FOOT = f'''<footer class="foot"><div class="wrap">
<div class="foot-grid">
<div><a class="brand" href="dashboard.html"><img src="assets/images/logo.svg" alt="" width="34" height="34">SmartNoise</a><p style="margin-top:14px">A citizen noise portal and monitoring dashboard for urban India. Find the right helpline, understand the rules, and track noise levels.</p></div>
<div><h4>Product</h4><ul><li><a href="features.html">Features</a></li><li><a href="dashboard.html">Dashboard</a></li><li><a href="monitor.html">Live Monitor</a></li><li><a href="zones.html">Noise Zones</a></li></ul></div>
<div><h4>Help</h4><ul><li><a href="awareness.html">Noise awareness</a></li><li><a href="research.html">Research &amp; learning</a></li><li><a href="helplines.html">Helplines</a></li><li><a href="complaints.html">File a Complaint</a></li><li><a href="limits.html">Noise Limits</a></li></ul></div>
<div><h4>Company</h4><ul><li><a href="about.html">About</a></li><li><a href="contact.html">Contact</a></li><li><a href="login.html">Login</a></li><li><a href="login.html?tab=signup">Create account</a></li></ul></div>
<div><h4>Team</h4><ul><li><b>Owner: Prince Jainwar</b></li><li><a href="mailto:{OWNER}">{OWNER}</a></li><li><a href="team.html">Team page</a></li></ul></div>
</div>
<div class="foot-bottom"><span>&copy; 2026 Prince Jainwar. SmartNoise.</span><span>Microphone readings are estimates, not certified measurements. <a href="mailto:{OWNER}">{OWNER}</a></span></div>
</div></footer>
'''

def page(fn, title, desc, body, cur=None, sub=False, protected=False, scripts="common.js", extra="", pg=None):
    cur = cur or fn
    scripts = scripts.replace("common.js","common.js,i18n.js,account.js")
    guard = '<script>try{var snEmail=localStorage.getItem("smartnoise_session"),snUsers=JSON.parse(localStorage.getItem("smartnoise_users")||"{}");if(!snEmail||!snUsers[snEmail])location.replace("login.html")}catch(e){location.replace("login.html")}</script>' if fn != "login.html" else ""
    out = head(title, desc, extra + guard) + f'<body{" data-protected=\"1\"" if protected else ""}{(" data-page=\""+pg+"\"") if pg else ""}>\n' + navbar(cur if not sub else "")
    if sub: out += subnav(fn)
    out += f'<main id="main">\n{body}\n</main>\n' + FOOT
    out += "".join(f'<script src="{s}"></script>' for s in scripts.split(",")) + "\n</body>\n</html>\n"
    open(fn, "w", encoding="utf-8").write(out)

def phero(crumb, h1, lead, extra=""):
    return f'<section class="page-hero"><div class="wrap"><p class="crumbs"><a href="dashboard.html">Dashboard</a> / {crumb}</p><h1>{h1}</h1><p class="lead">{lead}</p>{extra}</div></section>'

def dhero(crumb, h1, lead):
    return phero(f'<a href="dashboard.html">Dashboard</a> / {crumb}' if crumb != "Overview" else "Dashboard", h1, lead)

# ============ HOME ============
bars = "".join(f'<i style="height:{h}%"></i>' for h in [40,62,48,78,56,92,66,50,84,60,44,72])
home = f'''
<section class="hero"><div class="wrap split">
<div>
<span class="eyebrow">Citizen Noise Portal &middot; India</span>
<h1>Report noise. Understand it. <span class="hl">Protect your neighbourhood.</span></h1>
<p class="lead">Disturbed by a late-night party or loudspeaker? Find the right helpline and complaint portal in seconds, then track noise around you with a free monitoring dashboard.</p>
<div class="cta"><a class="btn primary lg" href="login.html?tab=signup" data-auth-cta>Create free account {ic("arrow")}</a><a class="btn lg" href="complaints.html">How to file a complaint</a></div>
<div class="trust"><span>Free to use</span><span>No hardware needed</span><span>Data stays in your browser</span></div>
</div>
<div class="preview reveal" aria-label="Sample preview of the live monitor">
<div class="preview-top"><span class="live"><span class="dot sim"></span>LIVE MONITOR</span><span class="tag sim">SAMPLE PREVIEW</span></div>
<div class="big">52<small>dB</small></div>
<div class="bars" aria-hidden="true">{bars}</div>
<div class="muted" style="font-size:.84rem;font-weight:600">Residential &middot; Day &middot; Reference limit 55 dB(A)</div>
</div>
</div></section>

<section class="section alt"><div class="wrap">
<div class="sec-head"><span class="eyebrow">Get help now</span><h2>Everything you need to act on noise</h2><p>Three quick routes to resolve a disturbance, from a live emergency to a formal complaint.</p></div>
<div class="grid g3">
<a class="card reveal" href="helplines.html">{ico("phone")}<h3>Helplines</h3><p>112, 100 and city helplines for disturbances that are happening right now.</p><span class="more">View helplines {ic("arrow")}</span></a>
<a class="card reveal" href="complaints.html">{ico("flag")}<h3>File a complaint</h3><p>Direct links to official government grievance portals, with a clear step-by-step guide.</p><span class="more">See how to complain {ic("arrow")}</span></a>
<a class="card reveal" href="limits.html">{ico("gauge")}<h3>Noise limits</h3><p>Day and night reference limits for industrial, commercial, residential and silence zones.</p><span class="more">Check the limits {ic("arrow")}</span></a>
</div></div></section>

<section class="section"><div class="wrap">
<div class="sec-head"><span class="eyebrow">The dashboard</span><h2>Track noise with your own device</h2><p>Use your microphone or Demo Mode to estimate noise levels and compare them with official reference limits.</p></div>
<div class="grid g4">
<div class="card reveal">{ico("mic")}<h3>Live monitor</h3><p>Real-time estimate from your microphone using the Web Audio API.</p></div>
<div class="card reveal">{ico("chart")}<h3>Analytics</h3><p>Trends, history and CSV export of every recorded reading.</p></div>
<div class="card reveal">{ico("pin")}<h3>Noise zones</h3><p>A conceptual smart-city view of typical noise by zone type.</p></div>
<div class="card reveal">{ico("bulb")}<h3>Smart controls</h3><p>Practical recommendations tailored to the selected area type.</p></div>
</div>
<div class="cta"><a class="btn" href="features.html">Explore all features</a></div>
</div></section>

<section class="section alt"><div class="wrap split">
<div><span class="eyebrow">Late-night noise</span><h2>Party, DJ or loudspeaker after hours?</h2>
<p class="lead">Loudspeakers and public address systems are generally restricted from 10 PM to 6 AM, with limited exceptions. Rules can vary by state.</p>
<div class="cta"><a class="btn primary" href="helplines.html">See helplines</a><a class="btn" href="limits.html">Noise limits</a></div></div>
<div class="card"><h3>What to do</h3><ol class="steps" style="margin-top:14px"><li>Note the address, the time and the source of the noise.</li><li>For a live disturbance, call <b>112</b>.</li><li>For repeated noise, file an online complaint with CPCB or your State Pollution Control Board.</li><li>Save any complaint number you receive.</li></ol></div>
</div></section>

<section class="section"><div class="wrap"><div class="card" style="text-align:center;padding:52px 24px;background:linear-gradient(160deg,var(--pri-soft),var(--surface))">
<h2>Start monitoring in under a minute</h2><p class="lead" style="margin:0 auto">Create a free account, open the Live Monitor and try Demo Mode with no microphone required.</p>
<div class="cta" style="justify-content:center"><a class="btn primary lg" href="login.html?tab=signup" data-auth-cta>Create free account {ic("arrow")}</a><a class="btn lg" href="about.html">Learn more</a></div></div></div></section>
'''
page("index.html","SmartNoise | Report Noise Pollution & Find Helplines in India","Find official helplines and complaint portals for noise pollution and late-night disturbances in India, and use the free SmartNoise noise-monitoring dashboard.",home)

# ============ FEATURES ============
def feat(i, n, t, p, pts, link=None):
    rev = " style=\"direction:rtl\"" if i % 2 else ""
    lk = f'<div class="cta"><a class="btn" href="{link[0]}">{link[1]}</a></div>' if link else ""
    return f'<div class="split reveal" style="padding:34px 0;{"border-top:1px solid var(--line)" if i else ""}"><div{"" if not i%2 else " style=\"order:2\""}><span class="eyebrow">{n}</span><h2>{t}</h2><p class="lead">{p}</p>{lk}</div><div class="card" style="order:{1 if i%2 else 0}"><ul class="ticks">{"".join(f"<li>{x}</li>" for x in pts)}</ul></div></div>'
feats = [
 ("01","Live noise monitor","Estimate the noise level around you in real time using your device microphone, with a clear status from low to very high.",["RMS-based estimate converted to dB with an adjustable calibration offset","Animated waveform and live trend chart","Status updates against the selected reference limit","Microphone is released as soon as you stop or leave the page"],("monitor.html","Open Live Monitor")),
 ("02","Demo Mode","No microphone? Launch Demo Mode to explore the full dashboard with realistic simulated values for your chosen area.",["Always clearly labelled as SIMULATED DATA","Includes occasional simulated loud events to test alerts","Ideal for presentations and first-time exploration"],("monitor.html","Try Demo Mode")),
 ("03","Reference limits and alerts","Pick an area type and time of day. SmartNoise compares readings with the CPCB / MoEFCC limits and raises an alert when they are exceeded.",["Industrial, commercial, residential and silence zones","Separate day (6 AM to 10 PM) and night (10 PM to 6 AM) limits","Alert with level, area, threshold, time and recommended action"],("limits.html","View noise limits")),
 ("04","History, analytics and export","Readings are recorded roughly every five seconds while monitoring and stored privately in your browser.",["Summary statistics: count, average, maximum, minimum, alerts","Trend chart across saved readings and a searchable history table","One-click CSV export; delete single records or clear everything"],("analytics.html","Open Analytics")),
 ("05","Noise zones and recommendations","See typical noise by zone type in a conceptual smart-city view, and get practical recommendations for the selected area.",["Residential, hospital, school, junction, market and industrial zones","Illustrative values, always labelled as demo data","Tailored guidance for every area type"],("zones.html","View Noise Zones")),
 ("06","Guidance and official links","Beyond the dashboard, SmartNoise brings together the numbers and portals you need when noise becomes a problem.",["112, 100 and Delhi 155271 helplines","Links to CPCB, CPGRAMS, 112 India and the Delhi noise portal","Plain-language steps for reporting a late-night disturbance"],("helplines.html","See helplines")),
]
body = phero("Features","Everything in one noise toolkit","Guidance for residents and a monitoring dashboard for anyone who wants to measure and understand noise, all in a single free product.") + '<section class="section tight"><div class="wrap">' + "".join(feat(i,*f) for i,f in enumerate(feats)) + '<p class="note">SmartNoise microphone readings are prototype estimates, not calibrated dB SPL. Actual environmental noise measurement requires a calibrated sound-level meter.</p></div></section>'
body += f'<section class="section alt"><div class="wrap"><div class="sec-head"><span class="eyebrow">How it works</span><h2>From sound to insight in four steps</h2></div><div class="grid g4">' + "".join(f'<div class="card reveal"><div class="num">{n}</div><h3>{t}</h3><p>{p}</p></div>' for n,t,p in [("1","Create an account","Sign up free. Accounts are stored in your browser."),("2","Choose your area","Select the area type and day or night period."),("3","Start monitoring","Use the microphone or Demo Mode."),("4","Review and act","Check analytics, export data and follow recommendations.")]) + '</div></div></section>'
page("features.html","Features | SmartNoise","Live noise monitoring, Demo Mode, reference limits, analytics, CSV export, noise zones and smart recommendations in one free platform.",body)

# ============ ABOUT ============
about = phero("About","About SmartNoise","SmartNoise is an independent project that helps people in India respond to noise pollution with clear information and simple monitoring tools.") + f'''
<section class="section"><div class="wrap split">
<div><span class="eyebrow">Our mission</span><h2>Make noise pollution easier to understand and act on</h2>
<p class="lead">Urban noise is a daily problem, but the steps to address it are often hard to find. SmartNoise puts helplines, official complaint portals and reference limits in one place.</p>
<p class="lead">It pairs this guidance with a lightweight dashboard so anyone can see how loud their surroundings are, using only a browser.</p></div>
<div class="grid g2"><div class="card reveal">{ico("shield")}<h3>Privacy first</h3><p>No server. Accounts and readings stay in your browser.</p></div><div class="card reveal">{ico("book")}<h3>Official sources</h3><p>Limits follow the Noise Pollution (Regulation and Control) Rules, 2000.</p></div><div class="card reveal">{ico("mic")}<h3>Transparent method</h3><p>Estimates are labelled as such, with an open calculation.</p></div><div class="card reveal">{ico("grid")}<h3>Free and open</h3><p>Plain HTML, CSS and JavaScript with no external libraries.</p></div></div>
</div></section>
<section class="section alt"><div class="wrap"><div class="sec-head"><span class="eyebrow">Vision</span><h2>Where SmartNoise is headed</h2><p>Planned improvements for future versions of the platform.</p></div>
<div class="grid g3"><div class="card reveal"><h3>IoT sensor nodes</h3><p>Connect dedicated low-cost sensors for continuous, location-based monitoring.</p></div><div class="card reveal"><h3>Calibration and A-weighting</h3><p>Calibrate against a reference meter and add A-weighting for closer dB(A) accuracy.</p></div><div class="card reveal"><h3>Cloud sync and maps</h3><p>Optional shared accounts and map views of noise across a city.</p></div></div></div></section>
<section class="section"><div class="wrap"><div class="card"><div class="row"><div><h3>What SmartNoise is not</h3><p>SmartNoise is not a certified measurement tool and its readings cannot prove a violation of the Noise Rules. For legal matters, rely on calibrated measurements by the authorities.</p></div><a class="btn primary" href="contact.html">Contact the owner</a></div></div></div></section>
'''
page("about.html","About SmartNoise | Mission, Approach and Vision","Learn about SmartNoise, an independent citizen noise portal and monitoring dashboard for India.",about)

# ============ HELPLINES ============
def hl(t,num,p,l=""): return f'<article class="card reveal">{ico("phone")}<h3>{t}</h3><p class="num">{num}</p><p>{p} {l}</p></article>'
body = phero("Helplines","Noise helplines","Call these numbers when noise is happening right now.") + '<section class="section tight"><div class="wrap"><div class="grid g3">' + hl("112 &middot; Emergency (ERSS)","112","National emergency number. Use it for ongoing late-night parties, DJs and loudspeakers.",'<a href="https://112.gov.in/" target="_blank" rel="noopener">112.gov.in &#8599;</a>') + hl("100 &middot; Police","100","The older police number, still working in many areas. If it does not connect, use 112.") + hl("Delhi noise complaints","155271","Delhi government grievance helpline from its noise portal (Delhi only).",'<a href="https://ngms.delhi.gov.in/" target="_blank" rel="noopener">ngms.delhi.gov.in &#8599;</a>') + '</div><p class="note">Other states and cities have their own police and pollution-control-board numbers. Please confirm numbers on official websites before relying on them.</p><div class="cta"><a class="btn primary" href="complaints.html">File a formal complaint</a><a class="btn" href="limits.html">Check noise limits</a></div></div></section>'
page("helplines.html","Noise Complaint Helplines India | SmartNoise","Emergency and helpline numbers to report noise pollution and late-night disturbances in India: 112, 100 and Delhi 155271.",body)

# ============ COMPLAINTS ============
def pl(t,p,u): return f'<a class="card reveal" href="{u}" target="_blank" rel="noopener"><h3>{t} &#8599;</h3><p>{p}</p></a>'
body = phero("Complaints","File a complaint","Official portals open in a new tab.") + '<section class="section tight"><div class="wrap"><div class="grid g3">' + pl("CPCB Grievance Portal","Central Pollution Control Board online grievance redressal. Choose the noise category.","https://cpcb.nic.in/grievance-redressal/") + pl("Noise Rules: Authority List","CPCB list of authorities who implement the Noise Rules in each state.","https://cpcb.nic.in/displaypdf.php?id=Tm9pc2UtU3RhbmRhcmRzL0F1dGhvcml0eUxpc3QucGRm") + pl("CPGRAMS Grievances","Government of India portal for public grievances.","https://pgportal.gov.in/") + pl("112 India","Official ERSS site and the 112 India mobile app.","https://112.gov.in/") + pl("Delhi Noise Portal","Delhi government portal to lodge and track noise complaints.","https://ngms.delhi.gov.in/") + '</div></div></section>' + '''<section class="section alt"><div class="wrap split"><div><span class="eyebrow">Step by step</span><h2>How to report a late-night disturbance</h2><p class="lead">Follow these steps to give your complaint the best chance of action.</p></div>
<div class="card"><ol class="steps"><li>Note the address or map link, the time and the source (party, DJ, loudspeaker, construction, vehicle).</li><li>For a live disturbance, call <b>112</b>.</li><li>For repeated or industrial noise, file an online complaint with the CPCB portal or your State Pollution Control Board.</li><li>Keep brief evidence and save any complaint number you receive.</li></ol><p class="note">Under the Noise Pollution (Regulation and Control) Rules, 2000, loudspeakers and public address systems are generally restricted between 10 PM and 6 AM, with limited exceptions. Rules can vary by state.</p></div></div></section>'''
page("complaints.html","File a Noise Pollution Complaint | SmartNoise","Official government portals and steps to file a noise pollution complaint in India, including CPCB, CPGRAMS and 112.",body)

# ============ LIMITS ============
rows = [("Industrial",75,70),("Commercial",65,55),("Residential",55,45),("Silence Zone",50,40)]
tbl = '<div class="scroll"><table><thead><tr><th>Area category</th><th>Day (6 AM-10 PM)</th><th>Night (10 PM-6 AM)</th></tr></thead><tbody>' + "".join(f'<tr><td><b>{a}</b></td><td>{d} dB(A) Leq</td><td>{n} dB(A) Leq</td></tr>' for a,d,n in rows) + '</tbody></table></div>'
body = phero("Noise Limits","Noise limits by area","Reference limits from the Noise Pollution (Regulation and Control) Rules, 2000 (MoEFCC / CPCB).") + f'<section class="section tight"><div class="wrap split"><div>{tbl}<p class="note">These limits apply to calibrated measurements. SmartNoise microphone readings are estimates only and cannot prove a violation. Verify against the latest official notification.</p></div><div class="card">{ico("gauge")}<h3>Compare against your surroundings</h3><p>Use the dashboard to estimate noise and see it against the limit for your area type.</p><div class="cta"><a class="btn primary" href="login.html?tab=signup" data-auth-cta>Use the dashboard {ic("arrow")}</a></div></div></div></section>'
page("limits.html","Indian Noise Limits by Area | SmartNoise","Day and night reference noise limits for industrial, commercial, residential and silence zones from the Noise Pollution (Regulation and Control) Rules, 2000.",body)

# ============ CONTACT ============
body = phero("Contact","Contact SmartNoise","Questions, feedback or corrections? Write to the owner.") + f'''<section class="section tight"><div class="wrap split" style="align-items:start">
<div class="card"><h3>Send a message</h3><p>This opens your email app with the message ready to send.</p>
<form id="contactForm" novalidate><label for="cName">Your name</label><input id="cName" type="text" autocomplete="name" required>
<label for="cTopic">Topic</label><select id="cTopic"><option>Feedback</option><option>Correction</option><option>Question</option><option>Other</option></select>
<label for="cMsg">Message</label><textarea id="cMsg" required></textarea>
<p class="error" id="cErr" role="alert" hidden></p><div class="cta"><button class="btn primary" type="submit">Open in email app</button></div></form></div>
<div class="grid"><div class="card">{ico("mail")}<h3>Owner</h3><p>Email: <a href="mailto:{OWNER}">{OWNER}</a></p><div class="cta" style="margin-top:16px"><a class="btn" href="mailto:{OWNER}?subject=SmartNoise%20feedback">Send email</a><button class="btn" id="copyMail" type="button">Copy email</button></div><p class="success" id="copyMsg" role="status"></p></div>
<div class="card">{ico("clock")}<h3>Before you write</h3><p>For urgent noise issues, call <a href="helplines.html">112</a> or use the <a href="complaints.html">official portals</a>. The owner cannot act on complaints.</p></div></div>
</div></section>
<script>document.addEventListener("DOMContentLoaded",function(){{var T="{OWNER}",b=document.getElementById("copyMail"),m=document.getElementById("copyMsg"),f=document.getElementById("contactForm"),e=document.getElementById("cErr");
b.onclick=function(){{if(navigator.clipboard&&navigator.clipboard.writeText){{navigator.clipboard.writeText(T).then(function(){{m.textContent="Email copied."}},function(){{m.textContent="Could not copy. Please select the email above."}})}}else{{m.textContent="Copy is not supported here. Please select the email above."}}}};
f.addEventListener("submit",function(ev){{ev.preventDefault();var n=document.getElementById("cName").value.trim(),g=document.getElementById("cMsg").value.trim(),t=document.getElementById("cTopic").value;
if(!n||!g){{e.textContent="Please enter your name and a message.";e.hidden=false;return}}e.hidden=true;
location.href="mailto:"+T+"?subject="+encodeURIComponent("SmartNoise "+t)+"&body="+encodeURIComponent(g+"\\n\\n"+n)}});}});</script>'''
page("contact.html","Contact SmartNoise | Owner & Feedback","Contact the owner of SmartNoise by email for feedback, corrections or questions.",body)

# ============ LOGIN ============
eye = '<button type="button" class="eye" data-for="%s" aria-label="Show password" aria-pressed="false"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12zM12 15a3 3 0 100-6 3 3 0 000 6z"/></svg></button>'
body = f'''<div class="auth"><aside class="auth-side"><span class="eyebrow" style="color:#a5b4fc">Free account</span><h2>Your noise dashboard, one login away</h2><p>Sign in to monitor noise, review analytics and export your history.</p><ul class="ticks" style="margin-top:20px"><li>Live microphone monitor and Demo Mode</li><li>History, analytics and CSV export</li><li>Data stays in your browser</li></ul></aside>
<div class="auth-main"><section class="authbox"><h1 style="font-size:2rem">Welcome</h1><p class="muted">Login or create a free account to open your dashboard.</p>
<div class="tabs" role="tablist"><button id="tabLogin" role="tab" type="button">Login</button><button id="tabSignup" role="tab" type="button">Create account</button></div>
<form id="loginForm" novalidate><label for="liEmail">Email</label><input id="liEmail" type="email" autocomplete="email" required>
<label for="liPass">Password</label><div class="pw"><input id="liPass" type="password" autocomplete="current-password" required>{eye % "liPass"}</div><div class="cta"><button class="btn primary lg" style="width:100%" type="submit">Login</button></div></form>
<form id="signupForm" novalidate hidden><label for="suName">Full name</label><input id="suName" type="text" autocomplete="name" required>
<label for="suEmail">Email</label><input id="suEmail" type="email" autocomplete="email" required>
<label for="suPass">Password (min 8 characters)</label><div class="pw"><input id="suPass" type="password" autocomplete="new-password" required>{eye % "suPass"}</div>
<label for="suPass2">Confirm password</label><div class="pw"><input id="suPass2" type="password" autocomplete="new-password" required>{eye % "suPass2"}</div><div class="cta"><button class="btn primary lg" style="width:100%" type="submit">Create account</button></div></form>
<p class="error" id="authErr" role="alert" hidden></p>
<p class="note">This is a static site with no server. Accounts and history are saved only in this browser on this device. Do not reuse an important password.</p></section></div></div>'''
page("login.html","Login or Create Account | SmartNoise","Login or create a free SmartNoise account to use the noise monitoring dashboard.",body,scripts="common.js,auth.js")

# ============ DASHBOARD PAGES ============
DS = "common.js,data/demo-data.js,script.js"
def stat(l,i,v="--"): return f'<div class="card stat"><span>{l}</span><b id="{i}">{v}</b></div>'
qa = [("monitor.html","mic","Live Monitor","Start the microphone or Demo Mode."),("analytics.html","chart","Analytics","Trends, history and CSV export."),("zones.html","pin","Noise Zones","Typical noise by zone type."),("controls.html","bulb","Smart Controls","Recommendations for your area.")]
body = dhero("Overview","Dashboard","Your saved readings at a glance, with quick access to every tool.") + f'''<section class="section tight"><div class="wrap">
<div class="stats">{stat("Readings","ovCount","0")}{stat("Average (dB)","ovAvg")}{stat("Maximum (dB)","ovMax")}{stat("Minimum (dB)","ovMin")}{stat("High readings","ovAlerts","0")}{stat("Latest","ovLast")}</div>
<div class="grid g4">{"".join(f'<a class="card" href="{h}">{ico(i)}<h3>{t}</h3><p>{p}</p><span class="more">Open {ic("arrow")}</span></a>' for h,i,t,p in qa)}</div>
<div class="card" style="margin-top:20px"><div class="row"><h3>Recent readings</h3><a class="btn sm" href="analytics.html">View all</a></div>
<div class="scroll"><table><thead><tr><th>Date</th><th>Time</th><th>Area</th><th>Level</th><th>Status</th><th>Data type</th></tr></thead><tbody id="recent"></tbody></table></div><p class="empty" id="recentEmpty">No readings yet. Open the Live Monitor or try Demo Mode.</p></div>
</div></section>'''
page("dashboard.html","Dashboard | SmartNoise","SmartNoise noise monitoring dashboard overview.",body,sub=True,protected=True,scripts=DS)

body = dhero("Live Monitor","Live Monitor","Estimate noise with your microphone or try Demo Mode.") + f'''<section class="section tight"><div class="wrap">
<div class="grid" style="grid-template-columns:1.5fr 1fr;align-items:start" id="monGrid">
<div class="card"><div class="live"><span class="dot" id="dot"></span><span id="modeLabel">IDLE</span><span class="tag sim" id="simTag" hidden>SIMULATED DATA</span></div>
<p class="muted" style="margin:14px 0 0;font-size:.8rem;font-weight:700;letter-spacing:.06em">LIVE NOISE LEVEL</p>
<div class="level"><span id="level">--</span><small>dB</small></div><span class="tag" id="estTag">ESTIMATED</span><span class="status" id="status" data-s="idle">NOT MONITORING</span>
<canvas id="wave" width="600" height="70" aria-label="Audio wave visualization" role="img" style="margin-top:18px"></canvas>
<div class="cta"><button class="btn primary" id="startMic">{ic("mic")} Start Microphone</button><button class="btn" id="startDemo">{ic("play")} Launch Demo Mode</button><button class="btn" id="stop" disabled>Stop</button></div>
<p class="error" id="error" role="alert" hidden></p>
<p class="note">Prototype estimate based on microphone audio. Actual environmental noise measurement requires a calibrated sound-level meter. Monitoring stops when you leave this page.</p></div>
<div class="card"><h3>Settings</h3><label for="area">Area type</label><select id="area"><option value="residential">Residential</option><option value="commercial">Commercial</option><option value="industrial">Industrial</option><option value="silence">Silence Zone</option></select>
<label for="period">Time period</label><select id="period"><option value="day">Day (6 AM - 10 PM)</option><option value="night">Night (10 PM - 6 AM)</option></select>
<label for="calib">Calibration offset (dB, adjustable)</label><input id="calib" type="number" value="90" min="40" max="130">
<dl class="info"><dt>Microphone</dt><dd id="micStatus">Off</dd><dt>Duration</dt><dd id="duration">00:00</dd><dt>Selected area</dt><dd id="areaLabel">Residential</dd><dt>Period</dt><dd id="periodLabel">Day</dd><dt>Reference limit</dt><dd id="limit">55 dB(A)</dd></dl></div></div>
<div id="alertBox" class="alert" role="alert" hidden></div>
<div class="stats" style="margin-top:20px">{stat("Current (dB)","sCur")}{stat("Average (dB)","sAvg")}{stat("Maximum (dB)","sMax")}{stat("Minimum (dB)","sMin")}{stat("Alerts","sAlerts","0")}{stat("Session time","sTime","00:00")}</div>
<div class="card"><h3>Noise trend (estimated dB)</h3><canvas id="chart" width="1000" height="300" aria-label="Noise trend line chart" role="img"></canvas><p class="muted" id="chartMsg" style="margin:8px 0 0;font-size:.88rem">Start monitoring to see the trend. Dashed line = reference limit.</p></div>
</div></section><style>@media(max-width:900px){{#monGrid{{grid-template-columns:1fr!important}}}}</style>'''
page("monitor.html","Live Monitor | SmartNoise","Estimate noise with your microphone or Demo Mode and compare it with reference limits.",body,sub=True,protected=True,scripts=DS)

body = dhero("Analytics","Analytics","Review trends, browse your history and export it as CSV.") + f'''<section class="section tight"><div class="wrap">
<div class="stats">{stat("Readings","ovCount","0")}{stat("Average (dB)","ovAvg")}{stat("Maximum (dB)","ovMax")}{stat("Minimum (dB)","ovMin")}{stat("High readings","ovAlerts","0")}{stat("Latest","ovLast")}</div>
<div class="card" style="margin-bottom:20px"><h3>Noise trend (estimated dB)</h3><canvas id="hchart" width="1000" height="300" aria-label="Saved readings trend chart" role="img"></canvas><p class="muted" id="hchartMsg" style="margin:8px 0 0;font-size:.88rem"></p></div>
<div class="card"><div class="row"><h3>Monitoring history</h3><div class="cta" style="margin:0"><button class="btn sm" id="exportCsv">{ic("download")} Export CSV</button><button class="btn sm" id="clearHist">Clear history</button></div></div>
<div class="scroll"><table><thead><tr><th>Date</th><th>Time</th><th>Area</th><th>Level</th><th>Status</th><th>Data type</th><th><span class="sr">Delete</span></th></tr></thead><tbody id="histBody"></tbody></table></div>
<p class="empty" id="histEmpty">No readings yet. Start monitoring or Demo Mode to record history.</p><p class="error" id="error" role="alert" hidden></p></div>
</div></section>'''
page("analytics.html","Analytics | SmartNoise","Trends, history and CSV export of your SmartNoise readings.",body,sub=True,protected=True,scripts=DS)

body = dhero("Noise Zones","Noise Zones","Conceptual smart-city view of typical noise by zone type.") + '<section class="section tight"><div class="wrap"><p><span class="tag sim">DEMO / SIMULATED DATA</span></p><div class="grid g3" id="zoneGrid"></div><p class="note">Values are illustrative only and are not real city measurements.</p></div></section>'
page("zones.html","Noise Zones | SmartNoise","Conceptual smart-city view of typical noise by zone type (simulated data).",body,sub=True,protected=True,scripts=DS)

body = dhero("Smart Controls","Smart Controls","Practical recommendations for the selected area and time of day.") + '''<section class="section tight"><div class="wrap split" style="align-items:start">
<div class="card"><h3>Recommendations for <span id="recArea">Residential</span></h3><ul class="ticks" id="recList" style="margin-top:16px"></ul></div>
<div class="card"><h3>Area settings</h3><label for="area">Area type</label><select id="area"><option value="residential">Residential</option><option value="commercial">Commercial</option><option value="industrial">Industrial</option><option value="silence">Silence Zone</option></select>
<label for="period">Time period</label><select id="period"><option value="day">Day (6 AM - 10 PM)</option><option value="night">Night (10 PM - 6 AM)</option></select>
<dl class="info"><dt>Period</dt><dd id="periodLabel">Day</dd><dt>Reference limit</dt><dd id="limit">55 dB(A)</dd></dl><p class="muted" style="font-size:.85rem;margin:14px 0 0">Settings are shared with the Live Monitor.</p></div></div></section>'''
page("controls.html","Smart Controls | SmartNoise","Recommendations to reduce noise for residential, commercial, industrial and silence zones.",body,sub=True,protected=True,scripts=DS)

account_builder = "tools/build_account.py" if os.path.exists("tools/build_account.py") else "../tools/build_account.py"
exec(open(account_builder, encoding="utf-8").read())

# ============ AWARENESS ============
awareness = phero("Awareness","Protect hearing. Reduce noise at the source.","Understand how repeated loud exposure can damage hearing, learn simple ways to reduce risk, and find trusted help.", '<div class="cta"><a class="btn primary" href="research.html">Read the Research &amp; Learning Desk</a></div>') + f'''
<section class="section tight"><div class="wrap awareness-grid">
<div class="awareness-lead card"><div class="eyebrow">HEARING HEALTH · PRACTICAL GUIDANCE</div><h2 data-i18n="Noise damage can build quietly over time.">Noise damage can build quietly over time.</h2><p>Very loud sounds can injure the inner ear in one event. Repeated exposure to loud sound can damage sensory structures over time and may cause permanent hearing loss or tinnitus. Risk depends on both sound level and time exposed.</p><div class="awareness-callout"><b>Use the right context</b><span>NIOSH's 85 dBA over 8 hours is an occupational recommended exposure limit. It is not a universal guarantee of safety for every person or every setting.</span></div><div class="cta"><a class="btn primary" href="#take-action" data-i18n="What can I do?">What can I do?</a><a class="btn" href="submit-data.html">Record a noise incident</a></div></div>
<figure class="card awareness-figure"><img src="assets/images/hearing-health.svg" alt="Illustration of sound waves reaching the ear, with hearing protection and a quiet space as ways to reduce exposure"><figcaption>Illustration: reduce exposure, take quiet breaks, and use hearing protection where appropriate.</figcaption></figure>
</div></section>
<section class="section alt"><div class="wrap"><div class="sec-head"><span class="eyebrow">What research says</span><h2 data-i18n="How harmful noise can affect people">How harmful noise can affect people</h2><p>Health outcomes depend on the type of noise and exposure. Avoid assuming every effect applies to every person.</p></div><div class="grid g3 awareness-cards">
<article class="card"><span class="aw-icon">01</span><h3>Hearing and tinnitus</h3><p>Loud noise can damage hearing; tinnitus is ringing, buzzing, or similar sound without an outside source. Noise-induced hearing loss can be permanent.</p><a href="https://www.who.int/news-room/questions-and-answers/item/deafness-and-hearing-loss-safe-listening" target="_blank" rel="noopener">WHO safe-listening guidance ↗</a></article>
<article class="card"><span class="aw-icon">02</span><h3>Sleep and wellbeing</h3><p>Environmental noise is associated with sleep disturbance and annoyance. WHO summaries also describe links with cardiovascular and cognitive health outcomes.</p><a href="https://www.who.int/tools/compendium-on-health-and-environment/environmental-noise/" target="_blank" rel="noopener">WHO environmental-noise overview ↗</a></article>
<article class="card"><span class="aw-icon">03</span><h3>Safety and communication</h3><p>Noise can mask alarms, warnings, and conversation, which may make it harder to notice hazards or coordinate with others.</p><a href="https://www.cdc.gov/niosh/noise/prevent/" target="_blank" rel="noopener">CDC/NIOSH prevention guide ↗</a></article>
</div></div></section>
<section class="section"><div class="wrap"><div class="sec-head"><span class="eyebrow">Quick explainer</span><h2 data-i18n="Learn from public-health experts">Learn from public-health experts</h2><p>Videos are hosted by CDC/NIOSH. Use the controls to play; captions and transcripts are available from the original source where provided.</p></div><div class="grid g2 video-grid">
<article class="card video-card"><div class="video-frame"><iframe src="https://www.youtube-nocookie.com/embed/GEyC112dO44" title="CDC: Protecting Against Noise Hazards at My Job" loading="lazy" referrerpolicy="strict-origin-when-cross-origin" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe></div><h3>Protecting against noise hazards</h3><p>CDC/NIOSH overview for workers on noise hazards and practical hearing-loss prevention.</p><a href="https://www.cdc.gov/niosh/noise/about/noise.html" target="_blank" rel="noopener">Open CDC/NIOSH article and transcript ↗</a></article>
<article class="card video-card"><div class="video-frame"><iframe src="https://www.youtube-nocookie.com/embed/U4us4Ut2J7I" title="CDC: Protecting workers against noise hazards" loading="lazy" referrerpolicy="strict-origin-when-cross-origin" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe></div><h3>Protecting workers from noise hazards</h3><p>CDC/NIOSH guidance for managers on reducing hazardous noise at work.</p><a href="https://www.cdc.gov/niosh/noise/prevent/" target="_blank" rel="noopener">Open CDC/NIOSH prevention resources ↗</a></article>
</div></div></section>
<section class="section alt" id="take-action"><div class="wrap"><div class="sec-head"><span class="eyebrow">Practical actions</span><h2 data-i18n="Small changes can lower exposure">Small changes can lower exposure</h2></div><div class="grid g4 action-grid">
<div class="card"><span class="aw-icon">A</span><h3>Move away</h3><p>Increase distance from the source and choose quieter routes or rooms when possible.</p></div><div class="card"><span class="aw-icon">B</span><h3>Reduce time</h3><p>Take quiet breaks and limit time around loud activities. Louder sound generally means less safe exposure time.</p></div><div class="card"><span class="aw-icon">C</span><h3>Protect hearing</h3><p>Use suitable, correctly fitted hearing protection for unavoidable loud work or events. Follow product instructions.</p></div><div class="card"><span class="aw-icon">D</span><h3>Reduce noise at source</h3><p>For workplaces and communities, address the source, maintenance, barriers, scheduling, and quieter equipment.</p></div>
</div><p class="note">For sudden hearing loss, severe ear pain, or distressing symptoms after a loud event, seek prompt advice from a qualified health professional. This site does not diagnose or replace clinical care.</p></div></section>
<section class="section"><div class="wrap split awareness-tools"><div><span class="eyebrow" data-i18n="Exposure learning tool">Exposure learning tool</span><h2>Explore a workplace reference example</h2><p class="lead">Estimate an illustrative daily noise dose using the NIOSH 3 dB exchange-rate model. This is for learning only: it is not a medical assessment, measurement, or legal compliance result.</p><p><a href="https://www.cdc.gov/niosh/noise/prevent/understand.html" target="_blank" rel="noopener">Read the method and limits ↗</a></p></div><form class="card dose-tool" id="doseForm"><label for="doseLevel">Exposure level (dBA)</label><input id="doseLevel" type="number" min="70" max="120" step="1" value="85" required><label for="doseHours">Time exposed (hours)</label><input id="doseHours" type="number" min="0.1" max="24" step="0.1" value="8" required><button class="btn primary" type="submit" data-i18n="Calculate example dose">Calculate example dose</button><output id="doseResult" class="dose-result" aria-live="polite">At 85 dBA for 8 hours: 100% of the NIOSH reference daily dose.</output></form></div></section>
<section class="section alt"><div class="wrap split"><div><span class="eyebrow" data-i18n="Make a useful report">Make a useful report</span><h2>Help your community act on recurring noise</h2><p>Keep a factual log: dates, start/end times, location area, type of source, pattern, and any steps tried. Do not put yourself at risk to collect evidence.</p><div class="cta"><a class="btn primary" href="submit-data.html" data-i18n="Create a local report">Create a local report</a><a class="btn" href="complaints.html">Find official complaint channels</a></div></div><div class="card"><h3>Before you submit</h3><ul class="ticks"><li>Describe what happened without guessing who is responsible.</li><li>Record time and duration; avoid recording private conversations.</li><li>Keep copies of reference numbers from official portals.</li><li>For immediate danger, contact local emergency services.</li></ul></div></div></section>
<section class="section tight"><div class="wrap"><div class="sec-head"><span class="eyebrow">Trusted resources</span><h2 data-i18n="Continue learning">Continue learning</h2></div><div class="grid g3 resource-grid"><a class="card" href="https://www.who.int/news-room/questions-and-answers/item/deafness-and-hearing-loss-safe-listening" target="_blank" rel="noopener"><h3>WHO · Safe listening</h3><p>How loudness, duration, and repeated exposure affect hearing.</p><span class="more">Visit WHO ↗</span></a><a class="card" href="https://www.cdc.gov/hearing-loss/prevention/" target="_blank" rel="noopener"><h3>CDC · Hearing-loss prevention</h3><p>Practical tips for protecting hearing from loud sound.</p><span class="more">Visit CDC ↗</span></a><a class="card" href="https://www.cdc.gov/niosh/noise/about/app.html" target="_blank" rel="noopener"><h3>NIOSH · Sound Level Meter</h3><p>Validated iOS workplace sound meter details and limitations.</p><span class="more">Visit NIOSH ↗</span></a></div><p class="note">Noise readings from this SmartNoise prototype are not calibrated sound-level measurements. Do not use them to diagnose hearing risk, prove a violation, or substitute for a certified instrument.</p></div></section>
'''
page("awareness.html","Noise Awareness & Hearing Health | SmartNoise","Evidence-based noise awareness, hearing health resources, worker protection and community reporting tools.",awareness,pg="awareness",scripts="common.js,awareness.js")

# ============ Team ============
team = phero("Team", "The people behind SmartNoise", "A small independent project built to make noise awareness and learning easier to explore.") + '<section class="section tight"><div class="wrap" style="max-width:760px"><article class="card"><div class="profile-head"><img src="assets/images/team-prince.svg" alt="Illustrated profile avatar for Prince Jainwar" width="88" height="88" style="border-radius:50%"><div><span class="tag">OWNER</span><h2 style="margin-top:8px">Prince Jainwar</h2><a href="mailto:princejainwar43@gmail.com">princejainwar43@gmail.com</a></div></div><hr style="border:0;border-top:1px solid var(--line);margin:24px 0"><p>SmartNoise is an independent educational prototype for understanding environmental noise, hearing health, and community reporting. Its readings and local reports stay in the browser and are not official measurements or submissions.</p><a class="btn" href="contact.html">Contact the project</a></article></div></section>'
page("team.html", "Team | SmartNoise", "Meet the creator of the SmartNoise independent noise awareness project.", team)

# ============ Research & learning desk ============
research = phero("Research & learning", "The noise desk", "Research notes, study guides and practical lessons on sound, health, learning and quieter communities.") + '''
<section class="section tight"><div class="wrap"><div class="paper-masthead"><span>SMARTNOISE · THE LEARNING DESK</span><span>RESEARCH NOTES / ISSUE 01</span></div><div class="paper-lead"><div><span class="eyebrow">Evidence, explained</span><h2>What does the research say about everyday noise?</h2><p class="lead">A reading guide to studies and public-health sources. Each cutting is a short, plain-language summary with a link to the original source.</p></div><figure class="paper-cover"><img src="assets/images/noise-city.svg" alt="Illustration of a city soundscape, with buildings, sound waves, and a quiet green space"><figcaption>A soundscape has sources, pathways and places where people listen, rest and learn.</figcaption></figure></div>
<div class="learning-desk-layout"><aside class="learning-rail" aria-label="Learning desk sections"><h2>Explore</h2><a class="learning-tile" href="#learning-guide"><span>01</span><b>Learning guide</b><small>Sound level, time and context</small></a><a class="learning-tile" href="#paper-cuttings"><span>02</span><b>Research cuttings</b><small>Newspaper-style paper summaries</small></a><a class="learning-tile" href="#study-task"><span>03</span><b>Study activity</b><small>Map a soundscape near you</small></a><p class="learning-rail-note">Start with the learning guide, then browse the studies and original sources.</p></aside><div class="learning-desk-content"><section id="learning-guide" class="learning-intro"><span class="eyebrow">Study material · beginner</span><h2>First, learn what a sound reading can tell you</h2><p>Sound level describes how strong a sound is at a place and time. A reading alone does not tell you who made the sound, how long it lasted, whether it disturbed sleep, or how a person experienced it. Good observation includes source, time, duration and setting.</p><div class="learning-points"><article><b>Level</b><p>Decibels use a logarithmic scale. Small numeric changes can represent meaningful changes in sound energy; compare readings only when the meter and method are suitable.</p></article><article><b>Duration</b><p>A short peak and a steady exposure are different patterns. Record how long the sound continues and whether quiet breaks occur.</p></article><article><b>Context</b><p>Indoor and outdoor readings, day and night, and occupational and community guidance answer different questions. Do not mix their limits.</p></article></div><p><b>Remember:</b> SmartNoise microphone estimates are for learning patterns only. They are not calibrated measurements or proof of a legal violation.</p></section><section id="paper-cuttings"><div class="paper-section-heading"><span class="eyebrow">Research &amp; newspaper cuttings</span><h2>Five short reads from the evidence desk</h2><p>These are paraphrased study summaries, not reproduced paper pages. Open the source links to read the authors' methods and limitations.</p></div><div class="paper-grid"><article class="paper-story"><div class="paper-kicker">HEARING · WORKPLACE REFERENCE</div><h3>Why a 3 dB rise can halve recommended exposure time</h3><p class="paper-deck">NIOSH uses 85 dBA over an 8-hour work shift as its occupational recommended exposure limit.</p><figure><img src="assets/images/noise-dose.svg" alt="Illustration showing sound level rising as safe reference duration falls"><figcaption>Illustration of the occupational 3 dB exchange-rate concept.</figcaption></figure><p>For occupational noise, NIOSH’s 3 dB exchange rate means each 3 dB increase halves the recommended duration: 85 dBA for 8 hours, 88 dBA for 4 hours, and 91 dBA for 2 hours. This is a workplace reference, not a general outdoor or personal safety guarantee.</p><p><b>Study note:</b> dBA accounts for frequency weighting; exposure duration matters alongside level. Phone microphones are not calibrated instruments.</p><a href="https://www.cdc.gov/niosh/noise/prevent/understand.html" target="_blank" rel="noopener">Read CDC/NIOSH guidance ↗</a><span class="paper-source">Source: US National Institute for Occupational Safety and Health (NIOSH), Understand Noise Exposure.</span></article>
<article class="paper-story"><div class="paper-kicker">SLEEP · ENVIRONMENTAL NOISE</div><h3>Night noise and sleep: a guideline is not a personal diagnosis</h3><p class="paper-deck">WHO guidance links night-time road-traffic exposure above its recommended level with adverse sleep effects.</p><figure><img src="assets/images/quiet-night.svg" alt="Illustration of a sleeping neighborhood beneath a moon, with traffic sound kept at a distance"><figcaption>Quiet-at-night illustration; the actual sound at a home depends on place and measurement.</figcaption></figure><p>WHO’s European Region guideline strongly recommends reducing average road-traffic noise at night below 45 dB L<sub>night</sub>. That indicator is a long-term average outdoors, not a quick phone reading or a limit that predicts an individual’s sleep.</p><p><b>What to learn:</b> separate a population guideline from a personal measurement. Sleep can also be affected by timing, peaks, building insulation, health and individual sensitivity.</p><a href="https://www.who.int/europe/publications/i/item/9789289053563" target="_blank" rel="noopener">Read the WHO guideline ↗</a><span class="paper-source">Source: WHO Regional Office for Europe, Environmental Noise Guidelines (2018).</span></article>
<article class="paper-story"><div class="paper-kicker">SCHOOLS · LEARNING</div><h3>Noise can make listening and reading harder—but evidence varies by source</h3><p class="paper-deck">Systematic reviews examine how transport and classroom noise relate to children’s cognition.</p><figure><img src="assets/images/classroom.svg" alt="Illustration of a student reading in a classroom with sound waves outside the window"><figcaption>Learning depends on audibility, room acoustics and many factors beyond noise.</figcaption></figure><p>A 2018 review prepared for WHO examined studies on environmental noise and cognition in children. It found moderate evidence for some outcomes, including aircraft-noise effects on reading comprehension and long-term memory, while results differed by outcome and noise source. The authors called for stronger, more consistent research.</p><p><b>Study note:</b> association does not prove that noise alone caused an outcome. Look for study design, population, measured exposure and uncertainty before drawing conclusions.</p><a href="https://pubmed.ncbi.nlm.nih.gov/29414890/" target="_blank" rel="noopener">Read the systematic review (PubMed) ↗</a><span class="paper-source">Source: Clark &amp; Paunović, International Journal of Environmental Research and Public Health, 2018.</span></article>
<article class="paper-story"><div class="paper-kicker">COGNITION · SYSTEMATIC REVIEW + META-ANALYSIS</div><h3>Noise and cognition: a broad review finds mixed certainty across outcomes</h3><p class="paper-deck">A 2022 review combined recent studies with an earlier evidence set and graded the strength of findings.</p><figure><img src="assets/images/research-forest.svg" alt="Illustration of study estimates around an evidence line, showing varied findings and uncertainty"><figcaption>Illustration only: each research outcome has a different evidence estimate and uncertainty.</figcaption></figure><p>The review included 16 newer studies alongside 32 studies from a prior review. It reported high-quality evidence for an association between residential noise and cognitive impairment in middle-to-older adults, and moderate evidence for some aircraft-noise and child reading outcomes. Evidence for many other outcomes remained low or very low quality.</p><p><b>How to read it:</b> pooled findings do not mean every person is affected in the same way. The authors called for more consistent studies and better estimates.</p><a href="https://pubmed.ncbi.nlm.nih.gov/34649047/" target="_blank" rel="noopener">Read Thompson et al., Environment International (2022) ↗</a><span class="paper-source">Source: Thompson et al., “Noise pollution and human cognition: An updated systematic review and meta-analysis of recent evidence,” 2022.</span></article>
<article class="paper-story"><div class="paper-kicker">RESEARCH METHODS · HOW TO READ</div><h3>Four questions to ask before believing a noise headline</h3><p class="paper-deck">A quick checklist for reading studies and news coverage critically.</p><ol><li><b>What was measured?</b> Sound level, duration, source, timing and location?</li><li><b>Who was studied?</b> Workers, children, residents, or a different group?</li><li><b>What kind of study?</b> A review, cohort, experiment, or one-time survey?</li><li><b>How certain is it?</b> Check sample size, confidence intervals, limitations and whether other studies agree.</li></ol><p>A headline may compress a complex result. Read the abstract and limitations, and distinguish an observed association from a causal effect.</p><a href="https://pubmed.ncbi.nlm.nih.gov/34649047/" target="_blank" rel="noopener">Example: systematic review of noise and cognition ↗</a><span class="paper-source">Learning guide · SmartNoise editorial summary.</span></article></div></section></div></div>
<aside class="study-box" id="study-task"><div><span class="eyebrow">Take it into your day</span><h2>Mini study guide: map a soundscape</h2><p>Choose a familiar place and observe without recording private conversations. Note the time, likely sound sources, whether sound is steady or intermittent, and where a quieter spot is available. Repeat at another time and compare.</p><p>For a useful record, write down method and limits. A phone estimate can help illustrate patterns, but it cannot prove a regulatory violation or replace a calibrated meter.</p></div><img src="assets/images/sound-map.svg" alt="Illustrated neighborhood map with marked loud and quiet listening spots"></aside>
<p class="note">Educational material only. It is not medical advice, legal advice, an official measurement, or an endorsement of any product. Research summaries are paraphrased; use the linked original sources for details.</p></div></section>'''
page("research.html", "Research & Learning Desk | SmartNoise", "Plain-language research cuttings and study material about environmental noise, hearing, sleep and learning.", research)

# ============ sitemap ============
base = "https://YOUR-USERNAME.github.io/SmartNoise/"
pages = ["login.html", "research.html", "team.html"]
open("sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f'<url><loc>{base}{p}</loc></url>\n' for p in pages) + '</urlset>\n')
# Keep the entry point auth-only; all other routes are guarded in the document head.
open("index.html", "w", encoding="utf-8").write("<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><title>SmartNoise — AI-Powered Noise Monitoring</title><script>location.replace(\"login.html\")</script></head><body><a href=\"login.html\">Continue to SmartNoise</a></body></html>")
if LOGIN_TEMPLATE is not None:
    open("login.html", "w", encoding="utf-8").write(LOGIN_TEMPLATE)
print("built")
