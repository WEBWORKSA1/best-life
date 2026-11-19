#!/usr/bin/env python3
"""Best.Life static site generator. Run: python3 build.py  (stdlib only).
Writes plain HTML into the repo root so GitHub Pages can serve the main branch directly."""
import json, os, datetime, html as H, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "content"))
from guides import PILLARS, ARTICLES

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://best.life/"
SITE = "Best.Life"
ADS = "ca-pub-6620975821265271"
CONTACT = "https://web.works/contact"
TODAY = datetime.date.today().isoformat()
TOPBAR = "Contact, if you are interested in this website/domain name/Sponsorship/Advertisement/Partnership"
PAGES = []  # (url, title, desc, kind) for sitemap + search

LOGO = '<svg viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="20" r="19" fill="#1F5C4A"/><path d="M6 25a14 14 0 0 1 28 0z" fill="#E9B44C"/><circle cx="20" cy="25" r="6.5" fill="#F26B3A"/><path d="M4 25h32" stroke="#FBF7F0" stroke-width="2.2" stroke-linecap="round"/></svg>'

NAV = [("life-score.html", "Life Score"), ("tools/index.html", "Tools"), ("guides/index.html", "Guides"),
       ("videos.html", "Videos"), ("challenges.html", "Challenges"), ("support.html", "Support")]

def e(s): return H.escape(s, quote=True)

def write(path, text):
    full = os.path.join(HERE, path)
    os.makedirs(os.path.dirname(full) or ".", exist_ok=True)
    with open(full, "w", encoding="utf-8") as f: f.write(text)

def page(path, title, desc, body, kind="Page", scripts=(), jsonld=None, index=True, section=None, head_extra=""):
    depth = path.count("/"); R = "../" * depth
    url = BASE + ("" if path == "index.html" else path)
    full_title = title if path == "index.html" else f"{title} — {SITE}"
    cur = ' aria-current="page"'
    nav = "".join(f'<a href="{R}{u}"{cur if (section or path) == u else ""}>{t}</a>' for u, t in NAV)
    ld = [{"@context": "https://schema.org", "@type": "WebSite", "name": SITE, "url": BASE}] if path == "index.html" else []
    if jsonld: ld.append(jsonld)
    ldtag = "".join(f'<script type="application/ld+json">{json.dumps(x)}</script>' for x in ld)
    sc = "".join(f'<script src="{R}assets/js/{s}" defer></script>' for s in ("app.js",) + tuple(scripts))
    out = f"""<!DOCTYPE html>
<html lang="en" data-root="{R}">
<head>
<meta charset="utf-8">{head_extra}
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full_title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
{'' if index else '<meta name="robots" content="noindex">'}
<meta name="google-adsense-account" content="{ADS}">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADS}" crossorigin="anonymous"></script>
<meta property="og:type" content="{'article' if kind == 'Guide' else 'website'}">
<meta property="og:site_name" content="{SITE}">
<meta property="og:title" content="{e(full_title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}assets/img/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#1F5C4A">
<link rel="icon" href="{R}assets/img/favicon.svg" type="image/svg+xml">
<link rel="manifest" href="{R}manifest.webmanifest">
<link rel="alternate" type="application/rss+xml" title="{SITE} guides" href="{R}feed.xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600;9..40,700&family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;0,9..144,700;1,9..144,600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{R}assets/css/style.css">
{ldtag}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><a href="{CONTACT}" target="_blank" rel="noopener">{TOPBAR}</a></div>
<header class="site-head"><div class="wrap">
<a class="brand" href="{R}index.html" aria-label="{SITE} home">{LOGO}<span>Best<i>.</i>Life</span></a>
<button class="icon-btn menu-btn" data-menu aria-controls="nav" aria-expanded="false" aria-label="Menu">☰</button>
<nav class="nav" id="nav" aria-label="Main">{nav}<a href="{R}search.html" aria-label="Search">Search</a>
<button class="icon-btn" data-theme-toggle aria-label="Toggle dark mode">◐</button>
<a class="btn btn-primary btn-sm" href="{R}blueprint.html">Free Blueprint</a></nav>
</div></header>
<main id="main">
{body.replace('{R}', R)}
</main>
<footer class="site-foot"><div class="wrap">
<div class="foot-grid">
<div><a class="brand" href="{R}index.html" style="color:#fff">{LOGO}<span>Best<i>.</i>Life</span></a>
<p style="margin-top:12px;max-width:34ch">Free tools and plain-language guides for a healthier, calmer, more purposeful life. Independent and reader-supported.</p>
<p><a class="btn btn-primary btn-sm" href="{R}support.html">Support the project</a></p></div>
<div><h4>Explore</h4><ul><li><a href="{R}life-score.html">Life Score</a></li><li><a href="{R}tools/index.html">All tools</a></li><li><a href="{R}guides/index.html">Guides</a></li><li><a href="{R}videos.html">Videos</a></li><li><a href="{R}research.html">Research feed</a></li><li><a href="{R}challenges.html">Challenges &amp; contest</a></li></ul></div>
<div><h4>Get involved</h4><ul><li><a href="{R}blueprint.html">Free 30-Day Blueprint</a></li><li><a href="{R}support.html">Donate / sponsor</a></li><li><a href="{R}careers.html">Work with us</a></li><li><a href="{CONTACT}" target="_blank" rel="noopener">Advertise &amp; partner</a></li><li><a href="{R}contact.html">Contact</a></li></ul></div>
<div><h4>Trust</h4><ul><li><a href="{R}about.html">About</a></li><li><a href="{R}editorial-policy.html">Editorial policy</a></li><li><a href="{R}privacy.html">Privacy &amp; cookies</a></li><li><a href="{R}terms.html">Terms of use</a></li><li><a href="{R}disclaimer.html">Disclaimer &amp; trademarks</a></li></ul></div>
</div>
<div class="legal"><p>© <span id="year">{TODAY[:4]}</span> {SITE}. Original content, all rights reserved. Content is for general education and is not medical, psychological, financial or legal advice.</p>
<p><strong>Trademark notice:</strong> “{SITE}” is the internet domain name of this independent website and is used descriptively. This site is not affiliated with, endorsed by or connected to any magazine, media brand, company, product or programme that uses similar words in its name. All third-party names, marks, videos and headlines belong to their respective owners. <a href="{R}disclaimer.html">Full disclosure</a>.</p></div>
</div></footer>
<div class="cookie" id="cookie" role="dialog" aria-label="Cookie notice"><p>We use cookies and local storage to remember your preferences and, through Google AdSense, to show and measure ads. See our <a href="{R}privacy.html">privacy &amp; cookie policy</a>.</p><button class="btn btn-ghost btn-sm" data-c="essential">Essential only</button><button class="btn btn-primary btn-sm" data-c="all">Accept</button></div>
{sc}
</body>
</html>
"""
    write(path, out)
    if index: PAGES.append((path, title, desc, kind))

def hero(eyebrow, title, lede, crumbs=()):
    c = '<div class="crumbs"><a href="{R}index.html">Home</a>' + "".join(f' › <a href="{{R}}{u}">{t}</a>' for u, t in crumbs) + "</div>"
    return f'<section class="page-hero"><div class="wrap">{c}<span class="eyebrow">{eyebrow}</span><h1>{title}</h1><p class="lede">{lede}</p></div></section>'

def form(kind, fields, button, ok, note="We reply personally. Your details are never sold.", attrs=""):
    return f'''<form data-form="{kind}" data-ok="{e(ok)}" {attrs}>
{fields}
<div class="hp" aria-hidden="true"><label>Leave empty<input type="text" name="_honey" tabindex="-1" autocomplete="off"></label></div>
<div class="field"><label style="font-weight:400;font-size:.88rem"><input type="checkbox" name="consent" value="yes" required> I agree to be contacted about this request and accept the <a href="{{R}}privacy.html">privacy policy</a>.</label></div>
<button class="btn btn-primary" type="submit">{button}</button>
<p class="form-note" style="margin-top:10px">{note}</p>
<div class="form-msg" role="status" aria-live="polite"></div>
</form>'''

def f_text(name, label, typ="text", req=True, ph="", extra=""):
    return f'<div class="field"><label for="f-{name}">{label}</label><input id="f-{name}" name="{name}" type="{typ}" placeholder="{ph}" {"required" if req else ""} {extra}></div>'
def f_area(name, label, req=False, ph=""):
    return f'<div class="field"><label for="f-{name}">{label}</label><textarea id="f-{name}" name="{name}" rows="4" placeholder="{ph}" {"required" if req else ""}></textarea></div>'
def f_sel(name, label, opts):
    return f'<div class="field"><label for="f-{name}">{label}</label><select id="f-{name}" name="{name}">' + "".join(f"<option>{o}</option>" for o in opts) + "</select></div>"

AREAS = ["Health", "Mind", "Relationships", "Work", "Money", "Growth", "Play", "Purpose"]
LEAD_FIELDS = '<div class="row">' + f_text("name", "First name", ph="Alex") + f_text("email", "Email", "email", ph="you@example.com") + "</div>" + f_sel("focus", "Area I most want to improve", AREAS)
LEAD_OK = "You are in. Your printable 30-Day Blueprint is unlocked below — and a copy of this confirmation is on its way."

def lead_band(title="Get the free 30-Day Blueprint", sub="One small, specific action a day across all eight life areas — printable, free, and built to be finished."):
    return f'''<section id="join"><div class="wrap"><div class="lead reveal">
<div><span class="eyebrow">Free · no spam · unsubscribe anytime</span><h2>{title}</h2><p>{sub}</p>
<ul><li>A day-by-day plan you can print and tick off</li><li>Occasional notes when new tools and challenges launch</li><li>First access to contest rounds and prizes</li></ul></div>
<div class="card">{form("Blueprint signup", LEAD_FIELDS, "Send me the Blueprint", LEAD_OK, "Join free. One-click unsubscribe by replying “stop”.")}
<p class="form-note"><a href="{{R}}blueprint.html">See what is inside →</a></p></div>
</div></div></section>'''

# ------------------------------------------------------------------ TOOLS
TOOLS = [
dict(slug="sleep-calculator", js="sleep", icon="🌙", name="Sleep Calculator", area="Health",
 desc="Find the best time to go to bed or wake up, based on 90-minute sleep cycles and how long you take to fall asleep.",
 ui='''<div class="seg" role="tablist"><button class="on" data-m="wake">I know my wake-up time</button><button data-m="bed">I know my bedtime</button></div>
<div class="row"><div class="field"><label id="sl-label" for="sl-time">I need to wake up at</label><input type="time" id="sl-time" value="07:00"></div>
<div class="field"><label for="sl-lat">Minutes I take to fall asleep</label><input type="number" id="sl-lat" value="15" min="0" max="90"></div></div>
<div class="out" id="sl-out" aria-live="polite"></div>''',
 how='''<h2>How the sleep calculator works</h2><p>Sleep moves through repeating cycles of lighter sleep, deep sleep and REM sleep. A full cycle lasts roughly 90 minutes on average, though it varies between people and across the night. Waking near the end of a cycle, when sleep is lighter, tends to feel easier than being pulled out of deep sleep.</p><p>The calculator counts backward (or forward) in 90-minute steps and adds the time you usually need to drift off. It then highlights the options that give five or six cycles — about 7.5 to 9 hours — which matches the seven-plus hours widely recommended for adults.</p><h2>Getting more from the result</h2><ul><li>Pick one wake-up time and hold it every day for two weeks, weekends included.</li><li>If you wake before your alarm feeling fine, you have probably found your natural length.</li><li>Still groggy? Move bedtime 15 minutes earlier for a week before judging.</li></ul>''',
 faq=[("Is a sleep cycle always 90 minutes?", "No. Ninety minutes is an average; individual cycles commonly range from about 70 to 120 minutes. Treat the times as a starting window and adjust by 15 minutes based on how you feel."),
      ("How much sleep do adults need?", "Most healthy adults do best with at least seven hours a night, and many need eight or nine. Teenagers and children need more."),
      ("Does this replace medical advice?", "No. Persistent trouble sleeping, loud snoring or daytime sleepiness should be discussed with a doctor.")]),
dict(slug="habit-tracker", js="habits", icon="✅", name="Habit Tracker", area="Growth",
 desc="A private, no-signup habit tracker with streaks and a 30-day consistency score. Your data stays in your browser.",
 ui='''<form id="hb-add" class="row" style="grid-template-columns:1fr auto;align-items:end"><div class="field" style="margin:0"><label for="hb-name">New habit</label><input id="hb-name" maxlength="60" placeholder="e.g. Read 10 pages"></div><button class="btn btn-green" type="submit">Add habit</button></form>
<div class="out" id="hb-out"></div><p style="margin-top:14px"><button class="btn btn-ghost btn-sm" id="hb-export" type="button">Export my data</button> <span class="form-note">Stored only on this device.</span></p>''',
 how='''<h2>How to use the habit tracker</h2><p>Add up to a handful of habits, then tap the box for each day you complete one. The tracker shows the last seven days, your current streak and how consistent you have been over the past 30 days. Nothing is sent to a server — entries live in your browser's local storage, so they stay private and work offline.</p><h2>Three rules that make tracking work</h2><ol><li><strong>Track few.</strong> Three habits tracked honestly beat ten tracked for a week.</li><li><strong>Make them tiny.</strong> "Read one page" is a better entry than "read more".</li><li><strong>Never miss twice.</strong> One empty box is life. Two in a row is the signal to shrink the habit.</li></ol>''',
 faq=[("Do I need an account?", "No. There is no signup and no login. Your habits are saved in this browser only."),
      ("Will I lose my data?", "Clearing your browser data or switching devices will remove it. Use the export button to keep a backup file."),
      ("How long does it take to form a habit?", "It varies widely with the person and the behaviour — from a few weeks to many months. Focus on consistency instead of a magic number of days.")]),
dict(slug="life-in-weeks", js="weeks", icon="🗓️", name="Life in Weeks", area="Purpose",
 desc="See your whole life as a grid of weeks — lived and still ahead. A gentle nudge to spend them on purpose.",
 ui='''<div class="row"><div class="field"><label for="wk-dob">Date of birth</label><input type="date" id="wk-dob"></div><div class="field"><label for="wk-exp">Planning horizon (years)</label><input type="number" id="wk-exp" value="85" min="40" max="110"></div></div>
<div class="stats" id="wk-stats"></div><div class="out" style="text-align:center"><canvas id="wk-cv" aria-label="Grid of weeks"></canvas><p class="form-note">Each square is one week. Each row is one year.</p><button class="btn btn-ghost btn-sm" id="wk-dl" style="display:none" type="button">Download as image</button></div>''',
 how='''<h2>Why look at life in weeks?</h2><p>Years feel abstract; weeks are something you can picture. A long life holds only around four thousand of them, and they fit on a single screen. Seeing the grid is not meant to be gloomy. People who use it tend to report the opposite — a clearer sense of what deserves a square and what does not.</p><h2>How to use it</h2><ul><li>Enter your date of birth and choose a planning horizon. The number is not a prediction, just a frame.</li><li>Notice how many summers and weekends are ahead and decide what one of them is for.</li><li>Download the image and keep it where you plan your week.</li></ul><p>Your date of birth is processed only in your browser and is never transmitted or stored on a server.</p>''',
 faq=[("Is this a life-expectancy prediction?", "No. The horizon is a number you choose for planning. It does not estimate how long anyone will live."),
      ("Is my date of birth saved?", "No. The calculation happens on your device and nothing is uploaded.")]),
dict(slug="compound-growth", js="compound", icon="📈", name="Compound Growth Calculator", area="Money",
 desc="See how regular saving grows over time, with a chart, yearly table and an inflation-adjusted figure.",
 ui='''<div class="row"><div class="field"><label for="cg-start">Starting amount</label><input type="number" id="cg-start" value="1000" min="0"></div><div class="field"><label for="cg-month">Added every month</label><input type="number" id="cg-month" value="200" min="0"></div></div>
<div class="row"><div class="field"><label for="cg-rate">Assumed yearly growth (%)</label><input type="number" id="cg-rate" value="6" step="0.1"></div><div class="field"><label for="cg-years">Years</label><input type="number" id="cg-years" value="25" min="1" max="60"></div></div>
<div class="field"><label for="cg-inf">Assumed inflation (%)</label><input type="number" id="cg-inf" value="2.5" step="0.1"></div>
<div class="stats" id="cg-stats" aria-live="polite"></div><div class="out"><canvas id="cg-cv" aria-label="Chart of contributions and balance over time"></canvas><p class="form-note">Gold: what you put in. Green: total balance.</p></div>
<div class="tablewrap" style="margin-top:14px"><table id="cg-table"></table></div>''',
 how='''<h2>What compounding means</h2><p>Compounding is growth earning its own growth. In the early years almost all of your balance is money you put in; later, the growth itself becomes the larger part. That is why the curve looks flat for a long time and then bends upward.</p><h2>How this calculator works</h2><p>It applies the yearly rate monthly, adds your contribution each month, and reports the final balance, the total you contributed and the growth earned. The "today's money" figure discounts the result by your inflation assumption so you can judge real buying power.</p><h2>Using it wisely</h2><ul><li>Try changing the number of years before you change the amount. Time is the strongest input.</li><li>Returns are never smooth or guaranteed; use a conservative rate.</li><li>Fees and taxes, which vary by country and product, are not included.</li></ul><p class="form-note">For education only. This is not financial advice and not a forecast.</p>''',
 faq=[("What growth rate should I use?", "That depends on what you hold and nobody can know future returns. Many people test a cautious, a middle and an optimistic rate to see a range."),
      ("Does it include fees and tax?", "No. Subtract your expected annual fees from the growth rate for a closer estimate.")]),
dict(slug="daily-energy", js="energy", icon="🔥", name="Daily Energy & Water Estimator", area="Health",
 desc="Estimate your resting and maintenance energy needs and a daily water guide, using the Mifflin–St Jeor equation.",
 ui='''<div class="row"><div class="field"><label for="en-unit">Units</label><select id="en-unit"><option value="metric">Metric (kg, cm)</option><option value="imperial">Imperial (lb, in)</option></select></div><div class="field"><label for="en-sex">Sex used for the formula</label><select id="en-sex"><option value="f">Female</option><option value="m">Male</option></select></div></div>
<div class="row"><div class="field"><label for="en-age">Age</label><input type="number" id="en-age" value="35" min="18" max="100"></div><div class="field"><label id="en-wl" for="en-w">Weight (kg)</label><input type="number" id="en-w" value="70"></div></div>
<div class="row"><div class="field"><label id="en-hl" for="en-h">Height (cm)</label><input type="number" id="en-h" value="170"></div><div class="field"><label for="en-act">Typical activity</label><select id="en-act"><option value="1.2">Mostly sitting</option><option value="1.375" selected>Light (1–3 active days)</option><option value="1.55">Moderate (3–5 active days)</option><option value="1.725">Very active (6–7 days)</option></select></div></div>
<div class="out" id="en-out" aria-live="polite"></div>''',
 how='''<h2>What the numbers mean</h2><p><strong>Resting energy</strong> is an estimate of what your body uses in a day at complete rest — breathing, circulation, keeping warm. <strong>Maintenance</strong> multiplies that by an activity factor to approximate a normal day. The water guide is a simple body-weight rule of thumb; needs rise in heat and with exercise, and food and other drinks count too.</p><h2>How to use it</h2><p>Treat the output as a ballpark for understanding your body, not a target to hit. Appetite, sleep, stress and muscle mass all shift real needs from day to day. If you want to change your weight or have a health condition, a doctor or registered dietitian can give guidance fitted to you.</p><p class="form-note">Designed for adults. Not suitable during pregnancy or for anyone with, or recovering from, an eating disorder — please seek professional support instead.</p>''',
 faq=[("Which formula is used?", "The Mifflin–St Jeor equation, a widely used method for estimating resting energy expenditure in adults."),
      ("How accurate is it?", "It is an estimate. Individual results commonly differ by ten percent or more from measured values.")]),
dict(slug="breathing-timer", js="breath", icon="🫁", name="Breathing Timer", area="Mind",
 desc="A guided breathing pacer with box breathing, 4-7-8 and steady calm patterns. Two minutes to a slower heart rate.",
 ui='''<div class="center"><div class="seg"><button class="on" data-p="box">Box 4-4-4-4</button><button data-p="478">4-7-8</button><button data-p="calm">Calm 5-5</button></div>
<div class="breath"><div class="orb" id="br-orb">Ready</div></div><p id="br-count" class="form-note" aria-live="polite">Press start and follow the circle.</p><button class="btn btn-primary" id="br-go" type="button">Start</button></div>''',
 how='''<h2>Why slow breathing helps</h2><p>Breathing is one of the few body functions that runs automatically and can also be steered on purpose. Slowing it down, especially the out-breath, shifts the nervous system toward its rest-and-digest state. Many people notice a calmer pulse and looser shoulders within a couple of minutes.</p><h2>The three patterns</h2><ul><li><strong>Box (4-4-4-4):</strong> inhale, hold, exhale, hold — four counts each. Steadying before a difficult moment.</li><li><strong>4-7-8:</strong> inhale 4, hold 7, exhale 8. The long exhale suits winding down at night.</li><li><strong>Calm (5-5):</strong> about six breaths a minute with no holds. Easy to sustain for ten minutes.</li></ul><p>Breathe through your nose if you can, sit comfortably and stop if you feel dizzy. People with respiratory or heart conditions should check with a clinician before breath-hold exercises.</p>''',
 faq=[("How long should I practise?", "Two to five minutes is enough to feel a difference. Daily practice makes the skill available when you are under pressure."),
      ("What if holding my breath is uncomfortable?", "Use the Calm 5-5 pattern, which has no holds, or shorten the counts.")]),
dict(slug="focus-timer", js="focus", icon="⏱️", name="Focus Timer", area="Work",
 desc="A clean focus-and-break timer for deep work sessions, with a daily session count. No signup, no clutter.",
 ui='''<div class="center"><span class="tag" id="fc-mode">Focus</span><div class="timer" id="fc-time" aria-live="off">25:00</div><p class="form-note" id="fc-today"></p>
<p><button class="btn btn-primary" id="fc-go" type="button">Start</button> <button class="btn btn-ghost" id="fc-reset" type="button">Reset</button></p></div>
<div class="row"><div class="field"><label for="fc-f">Focus minutes</label><input type="number" id="fc-f" value="25" min="1" max="120"></div><div class="field"><label for="fc-b">Break minutes</label><input type="number" id="fc-b" value="5" min="1" max="60"></div></div>''',
 how='''<h2>How timed focus works</h2><p>Working against a visible clock does two useful things: it makes starting easier, because the commitment is small, and it makes distractions easier to postpone, because a break is always close. The classic rhythm is 25 minutes on and 5 off; many people doing demanding work prefer 50 and 10.</p><h2>Make each session count</h2><ol><li>Write down the one outcome for this session before you press start.</li><li>Put your phone out of reach and close email and chat.</li><li>When the chime sounds, stand up. Look out of a window. Do not open a feed.</li><li>After four sessions, take a longer break of 20–30 minutes.</li></ol><p>The counter records completed focus sessions for today in your browser so you can see real effort, not just hours at a desk.</p>''',
 faq=[("What session length is best?", "Start with 25 minutes. If you regularly feel you are stopped mid-flow, move to 45 or 50 minutes with a 10-minute break."),
      ("Does the timer work in the background?", "Yes, while the tab stays open. The remaining time also shows in the tab title.")]),
dict(slug="gratitude-journal", js="gratitude", icon="📝", name="Gratitude Journal", area="Play",
 desc="A private daily gratitude journal with a fresh prompt each day. Entries stay on your device and can be exported.",
 ui='''<form id="gr-form"><div class="field"><label for="gr-text">Today's prompt: <span id="gr-prompt"></span></label><textarea id="gr-text" rows="4" maxlength="2000" placeholder="Write one to three things, and why they mattered…"></textarea></div><button class="btn btn-green" type="submit">Save entry</button> <button class="btn btn-ghost btn-sm" id="gr-export" type="button">Export all</button> <span class="form-note" id="gr-n"></span></form><div style="margin-top:20px" id="gr-out"></div>''',
 how='''<h2>Why write down what went well?</h2><p>Attention naturally drifts toward problems. A short gratitude practice deliberately points it at what is working. Studies in positive psychology have repeatedly linked this kind of writing with better mood and sleep, with the clearest effects when people are specific and explain <em>why</em> something was good.</p><h2>Tips for a practice that lasts</h2><ul><li>Two or three times a week can work as well as daily — avoid making it a chore.</li><li>Be concrete: "the neighbour who carried my shopping" beats "people".</li><li>Include small things. Small things are most of life.</li></ul><p>Entries are stored only in this browser. Export them whenever you like.</p>''',
 faq=[("Is my journal private?", "Yes. Entries are saved in your browser's local storage and are never uploaded."),
      ("How often should I write?", "Aim for a few times a week. Consistency over months matters more than daily perfection.")]),
dict(slug="goal-builder", js="goal", icon="🎯", name="Goal Builder", area="Purpose",
 desc="Turn a vague wish into a clear goal with a deadline, measure, checkpoints, a daily minimum and an if-then plan.",
 ui='''<form id="gl-form"><div class="field"><label for="gl-what">What do you want to achieve?</label><input id="gl-what" required placeholder="run 5 km without stopping"></div>
<div class="row"><div class="field"><label for="gl-meas">How will you measure it?</label><input id="gl-meas" placeholder="a timed 5 km on my usual route"></div><div class="field"><label for="gl-weeks">In how many weeks?</label><input type="number" id="gl-weeks" value="12" min="1" max="52"></div></div>
<div class="field"><label for="gl-why">Why does it matter to you?</label><input id="gl-why" placeholder="I want energy to play with my kids"></div>
<div class="row"><div class="field"><label for="gl-small">Smallest daily version</label><input id="gl-small" placeholder="put on shoes and walk 5 minutes"></div><div class="field"><label for="gl-block">Most likely obstacle</label><input id="gl-block" placeholder="a late day at work"></div></div>
<button class="btn btn-primary" type="submit">Build my goal</button></form><div id="gl-out" style="margin-top:20px"></div>''',
 how='''<h2>What makes a goal work</h2><p>Goals fail for predictable reasons: they are vague, they have no deadline, nobody checks progress, and the first bad day ends them. The builder answers each of those. It writes a single clear statement, sets four checkpoints, defines a daily minimum for difficult days and prepares an if-then plan for your most likely obstacle.</p><h2>After you build it</h2><ul><li>Print the plan or copy the statement somewhere you will see it daily.</li><li>Put the four checkpoint dates in your calendar now.</li><li>Tell one person. A little accountability goes a long way.</li><li>Track the daily minimum in the Habit Tracker.</li></ul>''',
 faq=[("How many goals should I have at once?", "One to three. Each additional goal divides your attention."),
      ("What if I miss a checkpoint?", "Adjust the plan, not your self-worth. Shorten the scope or extend the date, and keep the daily minimum going.")]),
]

def build_tools():
    cards = "".join(f'<a class="card reveal" href="{{R}}tools/{t["slug"]}.html"><span class="ico">{t["icon"]}</span><span class="tag">{t["area"]}</span><h3>{t["name"]}</h3><p>{t["desc"]}</p></a>' for t in TOOLS)
    score_card = '<a class="card reveal" href="{R}life-score.html" style="border-color:var(--accent)"><span class="ico">🧭</span><span class="tag">Start here</span><h3>Life Score</h3><p>Rate eight areas of life in four minutes and get a radar chart plus a 30-day plan.</p></a>'
    page("tools/index.html", "Free Life Tools", "Free, private, no-signup tools for sleep, habits, focus, money, calm and purpose. Everything runs in your browser.",
         hero("Tools", "Free tools for a better day", "No signup. No app. Your entries never leave your device.", [("tools/index.html", "Tools")]) +
         f'<section><div class="wrap"><div class="grid g3">{score_card}{cards}</div></div></section>' + lead_band(), section="tools/index.html")
    for t in TOOLS:
        faq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in t["faq"])
        others = "".join(f'<li><a href="{{R}}tools/{o["slug"]}.html">{o["icon"]} {o["name"]}</a></li>' for o in TOOLS if o["slug"] != t["slug"])[:2000]
        guide = next(p for p in PILLARS if p["area"] == t["area"] or (t["area"] == "Health" and p["slug"] == "health"))
        body = hero(t["area"] + " tool", f'{t["icon"]} {t["name"]}', t["desc"], [("tools/index.html", "Tools")]) + f'''
<section><div class="wrap layout"><div>
<div class="tool" data-tool="{t["js"]}">{t["ui"]}</div>
<div class="prose" style="margin-top:40px">{t["how"]}<h2>Frequently asked questions</h2><div class="faq">{faq}</div>
<p style="margin-top:28px">Next: read the <a href="{{R}}guides/{guide["slug"]}.html">{guide["area"]} guide</a> or take the <a href="{{R}}life-score.html">Life Score</a>.</p></div>
</div><aside class="aside"><div class="card"><span class="tag">4 minutes</span><h3>What is your Life Score?</h3><p>Rate eight life areas and get a personal 30-day plan.</p><p style="margin-top:12px"><a class="btn btn-primary btn-sm" href="{{R}}life-score.html">Take it free</a></p></div>
<div class="card"><h3>More tools</h3><ul style="padding-left:18px;margin:0">{others}</ul></div></aside></div></section>''' + lead_band()
        ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in t["faq"]]}
        page(f'tools/{t["slug"]}.html', t["name"], t["desc"], body, kind="Tool · " + t["area"], scripts=("tools.js",), jsonld=ld, section="tools/index.html")

# ------------------------------------------------------------------ GUIDES
def aside_for(tool):
    return f'''<aside class="aside"><div class="card"><span class="tag">Try the tool</span><h3>{tool[1]}</h3><p>Put this guide into practice in two minutes.</p><p style="margin-top:12px"><a class="btn btn-green btn-sm" href="{{R}}{tool[0]}">Open tool</a></p></div>
<div class="card"><span class="tag">4 minutes</span><h3>Take the Life Score</h3><p>See which of eight life areas needs you most.</p><p style="margin-top:12px"><a class="btn btn-primary btn-sm" href="{{R}}life-score.html">Start free</a></p></div>
<div class="card"><h3>Free 30-Day Blueprint</h3><p>One small action a day. Printable.</p><p style="margin-top:12px"><a href="{{R}}blueprint.html">Get it →</a></p></div></aside>'''

AREA_TOOL = {"Health": ("tools/sleep-calculator.html", "Sleep Calculator"), "Mind": ("tools/breathing-timer.html", "Breathing Timer"), "Love": ("life-score.html", "Life Score"),
             "Work": ("tools/focus-timer.html", "Focus Timer"), "Money": ("tools/compound-growth.html", "Compound Growth Calculator"), "Growth": ("tools/habit-tracker.html", "Habit Tracker"), "Purpose": ("tools/goal-builder.html", "Goal Builder")}

def words(htmltext):
    import re
    return len(re.sub(r"<[^>]+>", " ", htmltext).split())

def build_guides():
    pc = "".join(f'<a class="card reveal" href="{{R}}guides/{p["slug"]}.html"><span class="ico">{p["icon"]}</span><span class="tag">Pillar guide</span><h3>{p["area"]}</h3><p>{p["desc"]}</p></a>' for p in PILLARS)
    ac = "".join(f'<a class="card reveal" href="{{R}}guides/{a["slug"]}.html"><span class="tag">{a["area"]}</span><h3>{a["title"]}</h3><p>{a["desc"]}</p></a>' for a in ARTICLES)
    page("guides/index.html", "Guides", "Plain-language, evidence-informed guides to health, mind, relationships, work, money, growth, play and purpose.",
         hero("Guides", "Eight areas. One well-lived life.", "Start with the pillar guide for your lowest Life Score area, then go deeper.", [("guides/index.html", "Guides")]) +
         f'<section><div class="wrap"><h2>The eight pillars</h2><div class="grid g4">{pc}</div></div></section><section class="section-alt"><div class="wrap"><h2>Practical reads</h2><div class="grid g3">{ac}</div></div></section>' + lead_band(), section="guides/index.html")
    for p in PILLARS:
        mins = max(3, round(words(p["body"]) / 220))
        take = "".join(f"<li>{t}</li>" for t in p["take"])
        rel = "".join(f'<li><a href="{{R}}guides/{a["slug"]}.html">{a["title"]}</a></li>' for a in ARTICLES if a["area"] == p["area"])
        body = hero(f'{p["area"]} · pillar guide', p["title"], p["desc"], [("guides/index.html", "Guides")]) + f'''
<section><div class="wrap layout"><article class="prose"><p class="meta">By the {SITE} editorial team · {mins} min read · Reviewed {TODAY}</p>
<div class="key"><h3>Key takeaways</h3><ul>{take}</ul></div>{p["body"]}
{"<h2>Keep reading</h2><ul>" + rel + "</ul>" if rel else ""}</article>{aside_for(p["tool"])}</div></section>''' + lead_band()
        ld = {"@context": "https://schema.org", "@type": "Article", "headline": p["title"], "description": p["desc"], "dateModified": TODAY, "author": {"@type": "Organization", "name": SITE}, "publisher": {"@type": "Organization", "name": SITE}, "mainEntityOfPage": BASE + f'guides/{p["slug"]}.html'}
        page(f'guides/{p["slug"]}.html', p["title"], p["desc"], body, kind="Guide", jsonld=ld, section="guides/index.html")
    for a in ARTICLES:
        mins = max(2, round(words(a["body"]) / 220))
        pillar = next(p for p in PILLARS if p["area"] == a["area"])
        body = hero(a["area"], a["title"], a["desc"], [("guides/index.html", "Guides"), (f'guides/{pillar["slug"]}.html', pillar["area"])]) + f'''
<section><div class="wrap layout"><article class="prose"><p class="meta">By the {SITE} editorial team · {mins} min read · Reviewed {TODAY}</p>{a["body"]}
<p style="margin-top:28px">Part of the <a href="{{R}}guides/{pillar["slug"]}.html">{pillar["area"]} pillar guide</a>.</p></article>{aside_for(AREA_TOOL[a["area"]])}</div></section>''' + lead_band()
        ld = {"@context": "https://schema.org", "@type": "Article", "headline": a["title"], "description": a["desc"], "dateModified": TODAY, "author": {"@type": "Organization", "name": SITE}, "publisher": {"@type": "Organization", "name": SITE}}
        page(f'guides/{a["slug"]}.html', a["title"], a["desc"], body, kind="Guide", jsonld=ld, section="guides/index.html")

# ------------------------------------------------------------------ CORE PAGES
BLUEPRINT_DAYS = [
 ("Health", "Set one wake-up time and keep it for the whole month."), ("Mind", "Three minutes of slow breathing before you check your phone."), ("Love", "Message someone you have not spoken to in a month."),
 ("Work", "Write tomorrow's most important task before you finish today."), ("Money", "List every subscription you pay for."), ("Growth", "Read ten pages."), ("Play", "Do twenty minutes of something purely for fun."),
 ("Purpose", "Write your top five values."), ("Health", "Walk ten minutes after your largest meal."), ("Mind", "Write three things that went well today."), ("Love", "Have one conversation with your phone in another room."),
 ("Work", "Protect one 25-minute focus block."), ("Money", "Cancel one subscription."), ("Growth", "Choose one skill for the next 90 days."), ("Play", "Plan something small to look forward to this weekend."),
 ("Purpose", "Do one unrequested favour."), ("Health", "Add a portion of vegetables to dinner."), ("Mind", "Turn off all non-human notifications."), ("Love", "Give one specific, sincere compliment."),
 ("Work", "Say a polite no to one request."), ("Money", "Set up a small automatic transfer to savings."), ("Growth", "Run a 15-minute weekly review: keep, stop, start."), ("Play", "Revive a hobby for thirty minutes."),
 ("Purpose", "Describe a great ordinary day five years from now."), ("Health", "Do two sets of squats and push-ups at your level."), ("Mind", "Spend one hour entirely offline."), ("Love", "Schedule a recurring weekly call or meal."),
 ("Work", "Write three lines: shipped, learned, next."), ("Money", "Name one financial goal and its next step."), ("All", "Retake the Life Score and compare."),
]

def build_core():
    # HOME
    pill = "".join(f'<a class="card reveal" href="{{R}}guides/{p["slug"]}.html"><span class="ico">{p["icon"]}</span><h3>{p["area"]}</h3><p>{p["desc"]}</p></a>' for p in PILLARS)
    tl = "".join(f'<a class="card reveal" href="{{R}}tools/{t["slug"]}.html"><span class="ico">{t["icon"]}</span><h3>{t["name"]}</h3><p>{t["desc"]}</p></a>' for t in TOOLS[:6])
    ar3 = "".join(f'<a class="card reveal" style="padding:18px" href="{{R}}guides/{a["slug"]}.html"><span class="tag">{a["area"]}</span><h3>{a["title"]}</h3><p>{a["desc"]}</p></a>' for a in (ARTICLES[0], ARTICLES[3], ARTICLES[8]))
    home = f'''<section class="hero"><div class="wrap"><div>
<span class="eyebrow">Free · private · no signup</span>
<h1>Know where you stand. <em>Improve what matters.</em></h1>
<p class="lede">Best.Life is a free toolkit for a healthier, calmer and more purposeful life. Take the four-minute Life Score, see your eight life areas on one chart, and get a 30-day plan you can actually finish.</p>
<div class="hero-cta"><a class="btn btn-primary" href="{{R}}life-score.html">Take the Life Score →</a><a class="btn btn-ghost" href="{{R}}tools/index.html">Explore the tools</a></div>
<ul class="hero-points"><li>24 questions, 4 minutes</li><li>Instant radar chart</li><li>Nothing leaves your device</li></ul></div>
<div class="dial reveal"><canvas id="demo-radar" aria-label="Example Life Score radar chart"></canvas><small id="demo-cap">Example result — yours takes four minutes.</small></div>
</div></section>

<section><div class="wrap"><div class="daily reveal"><div><h3>Thought for today</h3><blockquote id="daily-quote"></blockquote></div>
<div><h3>Today's two-minute challenge</h3><p class="challenge" id="daily-challenge"></p><p><button class="btn btn-primary btn-sm" id="daily-done" type="button">Mark as done</button> <span id="daily-streak" style="margin-left:10px;color:#BFDCD0"></span></p></div></div></div></section>

<section class="section-alt"><div class="wrap"><div class="center"><span class="eyebrow">How it works</span><h2>Measure. Focus. Repeat.</h2><p class="lede">Most self-improvement fails because it tries to fix everything at once. This does the opposite.</p></div>
<div class="grid g3" style="margin-top:30px"><div class="card reveal"><span class="ico">①</span><h3>Measure</h3><p>Answer 24 honest statements. Your Life Score shows eight areas side by side so the real gap is obvious.</p></div>
<div class="card reveal"><span class="ico">②</span><h3>Focus</h3><p>Work only on your two lowest areas for 30 days, using one guide and one tool for each.</p></div>
<div class="card reveal"><span class="ico">③</span><h3>Repeat</h3><p>Retake the score monthly. Your history is saved on your device so you can watch the shape change.</p></div></div></div></section>

<section><div class="wrap"><span class="eyebrow">The eight areas</span><h2>A whole life, not just a productive one</h2><div class="grid g4" style="margin-top:24px">{pill}</div></div></section>

<section class="section-alt"><div class="wrap"><span class="eyebrow">Tools</span><h2>Small tools that earn a daily visit</h2><div class="grid g3" style="margin-top:24px">{tl}</div><p style="margin-top:24px"><a class="btn btn-ghost" href="{{R}}tools/index.html">See all tools</a></p></div></section>

<section><div class="wrap"><span class="eyebrow">Watch</span><h2>Talks worth your time</h2><p class="lede">Hand-picked talks on happiness, habits, sleep and purpose, plus a feed that refreshes automatically.</p><div class="grid g3" style="margin-top:24px" data-videos="6"></div><p style="margin-top:24px"><a class="btn btn-ghost" href="{{R}}videos.html">All videos</a></p></div></section>

<section class="section-alt"><div class="wrap"><div class="grid g2"><div><span class="eyebrow">Read</span><h2>Practical guides</h2><div class="grid" style="margin-top:20px">{ar3}</div><p style="margin-top:20px"><a class="btn btn-ghost" href="{{R}}guides/index.html">All guides</a></p></div>
<div><span class="eyebrow">Fresh daily</span><h2>Wellbeing research feed</h2><ul class="news" data-news="6"></ul><p style="margin-top:20px"><a class="btn btn-ghost" href="{{R}}research.html">Full feed</a></p></div></div></div></section>
{lead_band()}
<section class="section-alt"><div class="wrap"><div class="grid g3"><a class="card reveal" href="{{R}}challenges.html"><span class="ico">🏆</span><h3>Challenges &amp; contest</h3><p>Join a 30-day challenge and enter the community prize draw.</p></a>
<a class="card reveal" href="{{R}}support.html"><span class="ico">💚</span><h3>Support the project</h3><p>Keep the tools free. Pledge a donation or sponsor a challenge.</p></a>
<a class="card reveal" href="{{R}}careers.html"><span class="ico">✍️</span><h3>Work with us</h3><p>Writers, reviewers, developers and designers — help build the toolkit.</p></a></div></div></section>'''
    page("index.html", "Best.Life — Free Life Score, Tools & Guides for a Better Life", "Take the free four-minute Life Score, see eight life areas on one chart, and use private no-signup tools and guides for sleep, habits, money, calm and purpose.", home)

    # LIFE SCORE
    ls = hero("Free assessment · 4 minutes", "The Life Score", "Rate 24 statements across eight life areas. Get an instant radar chart, your life shape and a focused 30-day plan. No signup; answers stay on your device.", [("life-score.html", "Life Score")]) + f'''
<section><div class="wrap" data-tool="score" style="max-width:880px">
<form id="score-form" class="tool"><p><strong>How true is each statement for you right now?</strong> 1 = not true, 5 = very true. Answer for the last month, not your ideal self.</p>
<div class="progress"><i id="score-prog"></i></div><p class="form-note" id="score-count" aria-live="polite">0 of 24 answered</p>
<div id="score-qs"></div><button class="btn btn-primary" type="submit">Show my Life Score</button></form>
<div id="score-result" aria-live="polite"></div>
<div class="lead no-print" style="margin-top:40px"><div><span class="eyebrow">Keep your result</span><h2>Email me my score and plan</h2><p>Get your eight scores and focus areas in your inbox, plus the printable 30-Day Blueprint.</p></div>
<div class="card">{form("Life Score result", LEAD_FIELDS, "Email my result", "Sent. Check your inbox — and your printable Blueprint is at best.life/blueprint.html", "Take the score first so your numbers are included.", 'id="score-lead"')}</div></div>
<div class="prose" style="margin-top:48px"><h2>How the Life Score works</h2><p>The Life Score is a structured self-reflection based on the long-established coaching practice of rating satisfaction across the major areas of life. Each of the eight areas — Health, Mind, Love, Work, Money, Growth, Play and Purpose — has three statements. Your answers are converted to a 0–100 score per area and averaged into an overall score.</p>
<p>The number matters less than the shape. A lopsided chart tells you where a small effort will have the largest effect, which is why the plan targets only your two lowest areas.</p>
<h2>What it is not</h2><p>It is not a clinical or diagnostic test, and it does not measure your worth. It is a mirror for a single moment. If your answers reflect serious distress, please speak with a health professional.</p>
<div class="faq"><details><summary>Is it really free and private?</summary><p>Yes. There is no account. Scores are calculated and stored in your browser only, unless you choose to email them to yourself.</p></details>
<details><summary>How often should I retake it?</summary><p>Every 30 days is ideal. Your previous result is kept on your device so you can see the change.</p></details>
<details><summary>Can I share my result?</summary><p>Use “Copy share link”. The link contains only the eight numbers, no personal details.</p></details></div></div>
</div></section>'''
    page("life-score.html", "Life Score: Free 4-Minute Life Assessment", "Free Life Score assessment: rate eight life areas in four minutes, get an instant radar chart, your life shape and a personal 30-day plan. No signup.", ls, kind="Tool · Assessment", scripts=("tools.js",))

    # BLUEPRINT (dedicated lead-gen page)
    days = "".join(f'<tr><td><strong>{i+1}</strong></td><td><span class="tag" style="margin:0">{a}</span></td><td>{t}</td><td style="text-align:center">☐</td></tr>' for i, (a, t) in enumerate(BLUEPRINT_DAYS))
    bp = hero("Free download", "The 30-Day Blueprint", "Thirty small actions — one a day — across all eight life areas. Designed to take under fifteen minutes and to be finished, not admired.", [("blueprint.html", "Blueprint")]) + f'''
<section><div class="wrap"><div class="lead"><div><span class="eyebrow">Join free</span><h2>Get the Blueprint and join the list</h2><p>Sign up and the full printable plan unlocks instantly on this page.</p>
<ul><li>30 daily actions, each under 15 minutes</li><li>Balanced across Health, Mind, Love, Work, Money, Growth, Play and Purpose</li><li>News of new tools, challenges and prize rounds</li></ul></div>
<div class="card">{form("Blueprint signup", LEAD_FIELDS + f_area("challenge", "Biggest challenge right now (optional)", ph="One sentence is plenty"), "Unlock the Blueprint", LEAD_OK, "Free. No spam. Reply “stop” to any email to unsubscribe.")}</div></div>
<div class="grid g3" style="margin-top:36px"><div class="card"><span class="ico">🧩</span><h3>Small on purpose</h3><p>Every action is sized to succeed on a bad day. Momentum first, intensity later.</p></div><div class="card"><span class="ico">⚖️</span><h3>Balanced</h3><p>Rotates through all eight areas so no part of life is left behind.</p></div><div class="card"><span class="ico">🔁</span><h3>Measured</h3><p>Starts and ends with the Life Score so you can see what changed.</p></div></div>
<div id="bp-plan" style="margin-top:44px;display:none"><h2>Your 30-Day Blueprint</h2><p class="no-print"><button class="btn btn-ghost btn-sm" onclick="print()">Print / save as PDF</button></p><div class="tablewrap"><table><thead><tr><th>Day</th><th>Area</th><th>Action</th><th>Done</th></tr></thead><tbody>{days}</tbody></table></div></div>
<div id="bp-locked" class="card center" style="margin-top:44px"><h3>🔒 The full plan unlocks when you join</h3><p>Preview — Day 1: {BLUEPRINT_DAYS[0][1]} Day 2: {BLUEPRINT_DAYS[1][1]} Day 3: {BLUEPRINT_DAYS[2][1]}</p></div>
</div></section>
<script>document.addEventListener('DOMContentLoaded',function(){{function open(){{document.getElementById('bp-plan').style.display='';document.getElementById('bp-locked').style.display='none';}}
try{{if(localStorage.getItem('bl_lead'))open();}}catch(e){{}}
new MutationObserver(function(){{if(document.querySelector('.form-msg.ok'))open();}}).observe(document.body,{{subtree:true,attributes:true,attributeFilter:['class']}});}});</script>'''
    page("blueprint.html", "Free 30-Day Blueprint", "Get the free printable 30-Day Blueprint: one small daily action across eight life areas. Join the Best.Life list to unlock it instantly.", bp, kind="Lead")

    # VIDEOS
    vd = hero("Watch", "Videos", "Standout talks on happiness, habits, sleep, stress and purpose — embedded from their creators' official YouTube channels. The latest feed refreshes automatically.", [("videos.html", "Videos")]) + '''
<section><div class="wrap"><h2>Editor's picks</h2><div class="seg" id="video-filter"><button class="on" data-t="">All</button><button data-t="Health">Health</button><button data-t="Mind">Mind</button><button data-t="Love">Love</button><button data-t="Work">Work</button><button data-t="Purpose">Purpose</button></div>
<div class="grid g3" data-videos="60" data-only="featured"></div></div></section>
<section class="section-alt"><div class="wrap"><h2>Latest from channels we follow</h2><p class="form-note" data-updated></p><div class="grid g3" data-videos="60" data-only="latest"></div>
<p class="form-note" style="margin-top:24px">Videos are streamed through YouTube's embedded player in privacy-enhanced mode and remain the property of their creators. Best.Life is not affiliated with the channels shown. Rights holders may request removal through our <a href="{R}contact.html">contact page</a>.</p></div></section>''' + lead_band()
    page("videos.html", "Videos on Happiness, Habits, Sleep & Purpose", "Curated talks and an auto-updating video feed on happiness, habits, sleep, stress, relationships and purpose.", vd, section="videos.html")

    # RESEARCH FEED
    rs = hero("Fresh daily", "Wellbeing research feed", "Headlines on health, psychology and wellbeing from established publishers, refreshed automatically every day. Each links to the original source.", [("research.html", "Research feed")]) + '''
<section><div class="wrap layout"><div><p class="form-note" data-news-updated></p><ul class="news" data-news="60"></ul>
<p class="form-note" style="margin-top:20px">Headlines are shown with attribution and link to the publisher. Best.Life does not reproduce the articles and is not affiliated with these publishers. A headline appearing here is not an endorsement or medical advice.</p></div>
<aside class="aside"><div class="card"><h3>How to read health news</h3><p>One study is a clue, not a verdict. Look for size, whether it was in people, and whether others have found the same.</p></div><div class="card"><span class="tag">4 minutes</span><h3>Take the Life Score</h3><p style="margin-bottom:12px">Find your focus area first.</p><a class="btn btn-primary btn-sm" href="{R}life-score.html">Start free</a></div></aside></div></section>''' + lead_band()
    page("research.html", "Wellbeing Research Feed", "An auto-updating feed of health, psychology and wellbeing headlines from established publishers, with links to the original sources.", rs)

    # CHALLENGES + CONTEST
    CH = [("🌅", "30 Days of Mornings", "Health", "Same wake-up time, daylight within an hour, a glass of water before coffee."), ("📵", "30-Day Digital Declutter", "Mind", "Notifications off, phone out of the bedroom, two check-in windows a day."),
          ("💌", "30 Days of Connection", "Love", "One genuine message, call or conversation every day."), ("💸", "30-Day No-Waste Money Month", "Money", "Track every expense and cancel what you would not buy again."),
          ("📖", "10 Pages a Day", "Growth", "Read ten pages daily — about one book by the end of the month."), ("🚶", "Walk After Meals", "Health", "Ten minutes on foot after your largest meal, every day.")]
    cc = "".join(f'<div class="card reveal"><span class="ico">{i}</span><span class="tag">{a}</span><h3>{n}</h3><p>{d}</p></div>' for i, n, a, d in CH)
    cf = '<div class="row">' + f_text("name", "Name") + f_text("email", "Email", "email") + "</div>" + f_sel("challenge", "Challenge I am taking on", [c[1] for c in CH]) + f_text("country", "Country", req=True) + f_area("pledge", "My one-sentence commitment", ph="For the next 30 days I will…")
    chp = hero("Join in", "30-day challenges & community contest", "Pick one challenge, commit in public, and enter the prize draw for people who finish.", [("challenges.html", "Challenges")]) + f'''
<section><div class="wrap"><h2>Choose your challenge</h2><div class="grid g3">{cc}</div></div></section>
<section class="section-alt"><div class="wrap layout"><div class="prose"><span class="eyebrow">Community contest</span><h2>The Finisher's Draw</h2>
<p>Each contest round runs for one calendar month. Register for a challenge, track it with the <a href="{{R}}tools/habit-tracker.html">Habit Tracker</a>, and at the end tell us how it went. Everyone who completes a round and sends a short reflection is entered in that round's prize draw.</p>
<p><strong>Prizes</strong> are funded by supporters and sponsors and are announced on this page before each round opens. Register now and you will be notified when the next round and its prize are confirmed.</p>
<h3>Official rules (summary)</h3><ul><li>No purchase or donation is necessary to enter or win. A purchase does not improve your chances.</li><li>Open to adults aged 18+ where such promotions are lawful; void where prohibited or restricted.</li><li>One entry per person per round. Winners are chosen at random from eligible finishers and contacted by email.</li><li>The prize, entry dates, eligibility and odds for each round are published here before it opens.</li><li>Entry details are used only to run the contest — see the <a href="{{R}}privacy.html">privacy policy</a>.</li><li>Not sponsored, endorsed or administered by Google, YouTube or any social network.</li></ul>
<p>Want to fund a prize? <a href="{{R}}support.html">Sponsor a round</a>.</p></div>
<div><div class="card"><h3>Register for the next round</h3>{form("Challenge registration", cf, "Register me", "You are registered. We will email you when the next round and its prize are announced.", "Free to enter. 18+. See rules.")}</div></div></div></section>'''
    page("challenges.html", "30-Day Challenges & Contest", "Join a free 30-day challenge for mornings, focus, money, reading or connection, and enter the community Finisher's Draw.", chp, section="challenges.html")

    # SUPPORT / DONATIONS
    tiers = [("Friend", "5", ["Keeps one tool online for a month", "Our thanks by email"]), ("Builder", "25", ["Funds a new guide or tool feature", "Name on the supporters list (optional)"]), ("Champion", "100", ["Funds a contest prize or a contributor's work", "Early look at new tools"]), ("Sponsor", "Custom", ["Sponsor a challenge round, tool or guide series", "Clearly labelled sponsor credit"])]
    tc = "".join(f'<div class="card tier reveal"><h3>{n}</h3><div class="price">{"$" + p if p != "Custom" else "Custom"}</div><ul>{"".join("<li>" + x + "</li>" for x in li)}</ul><a class="btn btn-primary btn-sm" href="#pledge" data-amt="{p}">Pledge</a></div>' for n, p, li in tiers)
    sf = '<div class="row">' + f_text("name", "Name") + f_text("email", "Email", "email") + '</div><div class="row">' + f_text("amount", "Amount (USD) or “custom”", ph="25") + f_sel("frequency", "Frequency", ["One-time", "Monthly", "Yearly"]) + "</div>" + f_sel("purpose", "Put my support toward", ["Wherever it is needed most", "Ongoing operations & hosting", "Promotion & marketing", "Hiring writers, reviewers & developers", "Contests & prizes", "Sponsorship of a tool or challenge"]) + f_area("message", "Message (optional)")
    sp = hero("Reader-supported", "Support Best.Life", "The tools are free and stay free. Donations and sponsorships pay for hosting, new tools, expert contributors, promotion and contest prizes.", [("support.html", "Support")]) + f'''
<section><div class="wrap"><div class="grid g4">{tc}</div></div></section>
<section class="section-alt"><div class="wrap layout"><div class="prose"><h2>Where your support goes</h2>
<ul><li><strong>Ongoing operations</strong> — hosting, domains, maintenance and accessibility work.</li><li><strong>Promotion &amp; marketing</strong> — reaching people who would benefit from free tools.</li><li><strong>Hiring talent</strong> — paying writers, subject reviewers, designers and developers.</li><li><strong>Contests &amp; prizes</strong> — funding rewards for people who finish a 30-day challenge.</li></ul>
<h2>How pledging works</h2><ol><li>Send a pledge with the form. No card details are collected on this website.</li><li>We reply personally with a secure payment link from an established payment provider.</li><li>You receive a receipt and, if you wish, a place on the supporters list.</li></ol>
<p>Donations are voluntary contributions to an independent project. They are not purchases, do not buy editorial influence, and unless we tell you otherwise in writing are not tax-deductible.</p>
<h2>Sponsorship, advertising &amp; partnerships</h2><p>Brands and organisations can sponsor a tool, a guide series or a contest round. Sponsored material is always labelled. <a href="{CONTACT}" target="_blank" rel="noopener">Start a sponsorship or partnership conversation →</a></p></div>
<div id="pledge"><div class="card"><h3>Make a pledge</h3>{form("Donation pledge", sf, "Send my pledge", "Thank you — pledge received. We will email you a secure payment link shortly.", "No payment is taken on this page.")}</div></div></div></section>
<script>document.addEventListener('click',function(e){{var a=e.target.closest('[data-amt]');if(a){{var i=document.getElementById('f-amount');if(i)i.value=a.getAttribute('data-amt').toLowerCase();}}}});</script>'''
    page("support.html", "Support, Donate & Sponsor", "Support Best.Life: pledge a donation or sponsor a tool or contest to fund free tools, contributors, promotion and prizes.", sp, section="support.html")

    # CAREERS
    roles = [("✍️", "Contributing writer", "Write clear, practical, well-sourced guides in one of the eight life areas."), ("🔬", "Subject reviewer", "Qualified health, psychology or finance professionals who check guides for accuracy."), ("💻", "Front-end developer", "Build fast, accessible, privacy-first tools in plain JavaScript."), ("🎨", "Designer / illustrator", "Shape the visual language of tools, printables and social content."), ("📣", "Community & growth lead", "Run challenges, contests and partnerships that bring the tools to more people.")]
    rc = "".join(f'<div class="card reveal"><span class="ico">{i}</span><h3>{n}</h3><p>{d}</p></div>' for i, n, d in roles)
    cf2 = '<div class="row">' + f_text("name", "Name") + f_text("email", "Email", "email") + "</div>" + f_sel("role", "Role", [r[1] for r in roles] + ["Something else"]) + f_text("portfolio", "Link to portfolio, profile or samples", "url", req=False, ph="https://") + f_area("about", "Why you, in a few sentences", req=True)
    cp = hero("Work with us", "Help build the toolkit", "Best.Life is a small independent project that works with freelance and part-time contributors around the world. Roles open as supporter funding allows.", [("careers.html", "Work with us")]) + f'''
<section><div class="wrap"><div class="grid g3">{rc}</div></div></section>
<section class="section-alt"><div class="wrap layout"><div class="prose"><h2>How we work</h2><ul><li>Remote, asynchronous and outcome-based.</li><li>Paid per project or on a part-time retainer; terms are agreed in writing before work starts.</li><li>Evidence first: claims are sourced, and health and money content is reviewed.</li><li>Readers before revenue: no dark patterns, no fake urgency.</li></ul><p>Send a short application. We read every one and keep strong profiles on file for upcoming projects.</p></div>
<div class="card"><h3>Apply</h3>{form("Contributor application", cf2, "Send application", "Application received — thank you. We will reply if there is a fit.")}</div></div></section>'''
    page("careers.html", "Work With Us", "Open calls for writers, subject reviewers, developers, designers and community leads at Best.Life.", cp)

    # CONTACT
    ctf = '<div class="row">' + f_text("name", "Name") + f_text("email", "Email", "email") + "</div>" + f_sel("topic", "Topic", ["General question", "Feedback on a tool or guide", "Correction request", "Content or video removal request", "Press", "Donation or sponsorship", "Something else"]) + f_area("message", "Message", req=True)
    ct = hero("Contact", "Get in touch", "Questions, corrections, feedback and ideas are all welcome. We read everything.", [("contact.html", "Contact")]) + f'''
<section><div class="wrap layout"><div class="card">{form("Contact", ctf, "Send message", "Message sent — thank you. We usually reply within a few working days.")}</div>
<aside class="aside"><div class="card"><h3>Business enquiries</h3><p>Interested in this website, the domain name, sponsorship, advertising or a partnership?</p><p style="margin-top:12px"><a class="btn btn-green btn-sm" href="{CONTACT}" target="_blank" rel="noopener">Open the enquiry page</a></p></div>
<div class="card"><h3>In a crisis?</h3><p>This site cannot provide emergency help. Contact your local emergency number or a crisis line in your country.</p></div></aside></div></section>'''
    page("contact.html", "Contact", "Contact the Best.Life team with questions, corrections, feedback or partnership enquiries.", ct)

    # SEARCH
    page("search.html", "Search", "Search Best.Life tools and guides.", hero("Search", "Find a tool or guide", "Type at least two letters.", [("search.html", "Search")]) + '<section><div class="wrap"><div class="field"><label for="search-q">Search</label><input id="search-q" type="search" placeholder="sleep, habits, money, purpose…" autofocus></div><div class="grid g3" id="search-out" aria-live="polite"></div></div></section>')

    # LEGAL / TRUST
    def legal(path, title, desc, inner):
        page(path, title, desc, hero("Trust", title, desc, [(path, title)]) + f'<section><div class="wrap"><div class="prose">{inner}<p class="meta" style="margin-top:30px">Last updated {TODAY}.</p></div></div></section>')

    legal("about.html", "About Best.Life", "Who we are, what we publish and how the project is funded.", f'''
<p>Best.Life is an independent website that publishes free self-reflection tools and plain-language guides to living well. It exists for one reason: most advice about improving your life is either locked inside an app subscription or scattered across thousands of articles that contradict each other. We wanted one calm place that helps a person see where they stand and take the next small step.</p>
<h2>What you will find here</h2><ul><li><strong>The Life Score</strong> — a four-minute self-assessment across eight life areas.</li><li><strong>Tools</strong> — private, no-signup utilities for sleep, habits, focus, money, calm and goals.</li><li><strong>Guides</strong> — practical reading for each life area.</li><li><strong>Videos and a research feed</strong> — curated and refreshed automatically.</li><li><strong>Challenges</strong> — 30-day programmes and a community contest.</li></ul>
<h2>Our principles</h2><ul><li><strong>Private by design.</strong> Tools run in your browser. We do not collect what you type into them.</li><li><strong>Evidence-informed.</strong> We favour well-established findings over trends and say so when evidence is thin.</li><li><strong>Small steps.</strong> We recommend the least effort that produces real change.</li><li><strong>Honest funding.</strong> The site is funded by advertising, voluntary reader support and clearly labelled sponsorship.</li></ul>
<h2>Who is behind it</h2><p>The site is operated by a small independent publishing team working with freelance contributors. It is not part of, or affiliated with, any magazine, media company, supplement brand or coaching programme. To reach us, use the <a href="{{R}}contact.html">contact page</a>.</p>''')

    legal("editorial-policy.html", "Editorial policy", "How Best.Life content is written, reviewed, corrected and funded.", f'''
<h2>How we write</h2><p>Guides are written in plain language by the editorial team and contributors. We rely on consensus guidance from recognised public-health, medical and research bodies, on peer-reviewed research, and on long-standing professional practice. We avoid sensational claims and do not promise outcomes.</p>
<h2>Review and updates</h2><p>Each guide shows the date it was last reviewed. Health and money content is checked against current mainstream guidance, and pages are revised when that guidance changes.</p>
<h2>Corrections</h2><p>If you believe something is wrong or out of date, tell us through the <a href="{{R}}contact.html">contact page</a>. We correct confirmed errors promptly.</p>
<h2>Advertising and independence</h2><p>The site displays advertising, including ads served by Google AdSense. Advertisers do not choose, review or influence editorial content. Sponsored content, when it exists, is labelled as such. We do not publish paid reviews or testimonials.</p>
<h2>Third-party material</h2><p>Videos are embedded with YouTube's standard player from their owners' channels. The research feed shows headlines with attribution and links to the publisher; we do not copy article text. Quotations are from public-domain sources or are brief and attributed.</p>
<h2>Not professional advice</h2><p>Everything here is general education. See the <a href="{{R}}disclaimer.html">disclaimer</a>.</p>''')

    legal("privacy.html", "Privacy & cookie policy", "What information Best.Life collects, how cookies and advertising work, and the choices you have.", f'''
<h2>Summary</h2><ul><li>The tools on this site run in your browser. What you enter into them is not sent to us.</li><li>We receive personal details only when you choose to submit a form.</li><li>We show ads through Google AdSense, which uses cookies.</li></ul>
<h2>Information you give us</h2><p>When you submit a form (newsletter signup, contact, pledge, contest registration, job application or emailed Life Score), we receive the details you enter — typically your name, email address and message. Forms are delivered to our inbox by a third-party form-relay service (FormSubmit), which processes the submission on our behalf. We use this information only to respond, to send what you asked for, to run the contest you entered, or to process your pledge. We do not sell personal information.</p>
<h2>Information stored on your device</h2><p>Tool data — Life Score history, habits, journal entries, timer counts, theme and cookie choice — is kept in your browser's local storage. It stays on your device and you can erase it at any time by clearing site data in your browser.</p>
<h2>Cookies and advertising</h2><p>Third-party vendors, including Google, use cookies to serve ads based on your prior visits to this and other websites. Google's use of advertising cookies enables it and its partners to serve ads to you based on your visits to this site and/or other sites on the Internet. You may opt out of personalised advertising by visiting <a href="https://www.google.com/settings/ads" target="_blank" rel="noopener">Google Ads Settings</a>, or opt out of some third-party vendors' use of cookies at <a href="https://www.aboutads.info/choices/" target="_blank" rel="noopener">aboutads.info</a>. More about how Google uses information from sites that use its services: <a href="https://policies.google.com/technologies/partner-sites" target="_blank" rel="noopener">policies.google.com/technologies/partner-sites</a>.</p>
<p>Where required by law (for example in the EEA, the UK and Switzerland), consent for advertising cookies is requested through a consent message before personalised ads are shown.</p>
<h2>Embedded content</h2><p>Videos load from YouTube's privacy-enhanced domain only after you press play; YouTube may then set cookies under its own policy. Fonts are loaded from Google Fonts.</p>
<h2>Hosting and logs</h2><p>The site is served by a static hosting provider that may log technical data such as IP address and browser type for security and operations.</p>
<h2>Children</h2><p>This site is intended for adults and is not directed to children under 16. We do not knowingly collect personal information from children.</p>
<h2>Your rights</h2><p>Depending on where you live, you may have rights to access, correct, delete or restrict use of your personal information, and to withdraw consent. To make a request, use the <a href="{{R}}contact.html">contact page</a>. To stop emails, reply “stop” to any message.</p>
<h2>Changes</h2><p>We will update this page when our practices change and revise the date below.</p>''')

    legal("terms.html", "Terms of use", "The terms that apply when you use Best.Life.", f'''
<p>By using this website you agree to these terms. If you do not agree, please do not use the site.</p>
<h2>Use of the site</h2><p>You may use the tools and read the content for personal, non-commercial purposes. You may not scrape, republish or sell the content, interfere with the site's operation, or use it unlawfully.</p>
<h2>No professional advice</h2><p>Content and tool results are general information only and are not medical, psychological, nutritional, financial, legal or other professional advice. See the <a href="{{R}}disclaimer.html">disclaimer</a>.</p>
<h2>Intellectual property</h2><p>Text, design, code and graphics created for this site are owned by the site's operator. Third-party videos, headlines, names and marks belong to their owners. If you believe material here infringes your rights, send details through the <a href="{{R}}contact.html">contact page</a> and we will review and, where appropriate, remove it promptly.</p>
<h2>Submissions</h2><p>If you send us feedback, reflections or contest entries, you confirm they are your own and grant us permission to use them to operate the site. We will not publish personal stories with your name without asking first.</p>
<h2>Donations and contests</h2><p>Donations are voluntary and non-refundable except where required by law. Contests are governed by the rules published on the <a href="{{R}}challenges.html">challenges page</a> for each round.</p>
<h2>Advertising and links</h2><p>The site displays third-party advertising and links to other websites. We are not responsible for third-party content, products or practices.</p>
<h2>Disclaimer of warranties; limitation of liability</h2><p>The site is provided “as is” without warranties of any kind. To the fullest extent permitted by law, the operator is not liable for any loss or damage arising from use of the site or reliance on its content.</p>
<h2>Changes</h2><p>We may update these terms. Continued use after changes means you accept the revised terms.</p>''')

    legal("disclaimer.html", "Disclaimer, trademark & copyright disclosure", "Important notices about advice, trademarks and copyright on Best.Life.", f'''
<h2>General information only</h2><p>Best.Life provides general educational information and self-reflection tools. Nothing on this website is medical, psychological, nutritional, financial, tax, legal or other professional advice, and nothing here creates a professional–client relationship. Always seek the advice of a qualified professional about your own circumstances. Never disregard professional advice or delay seeking it because of something you read here. If you think you may have a medical or mental-health emergency, call your local emergency number immediately.</p>
<h2>Tools and results</h2><p>The Life Score and other tools produce estimates and reflections based on what you enter. They are not diagnostic, are not validated clinical instruments, and should not be used to make health or financial decisions on their own.</p>
<h2>Trademark disclosure</h2><p>“Best.Life” is the internet domain name at which this website is published. It is used here as the site's address and in its ordinary descriptive sense. This website is an independent publication. It is <strong>not</strong> affiliated with, associated with, authorised by, endorsed by, sponsored by or in any way officially connected to any person, company, publication, product, programme or service that uses the words “best” and “life”, alone or in combination or as a single word, in its name or branding — including any magazine or online publication, media or lifestyle brand, supplement or nutrition product, insurer, healthcare organisation, coaching programme or slogan.</p>
<p>All product names, logos, brands, channel names and other trademarks or registered trademarks mentioned or shown on this site are the property of their respective owners and are used for identification only. Their use does not imply endorsement. We do not claim any rights in third-party marks and we take care not to present this site in a way that could be confused with any other brand. If you are a rights holder with a concern, contact us through the <a href="{{R}}contact.html">contact page</a> and we will respond promptly.</p>
<h2>Copyright disclosure</h2><ul><li>Articles, tool text, code, layout and graphics on this site are original works © {TODAY[:4]} the site operator, all rights reserved, unless stated otherwise.</li><li>Videos are embedded using YouTube's player from the uploaders' own channels and remain the property of their creators. We do not host or copy video files.</li><li>Research-feed headlines are short factual titles shown with attribution and a link to the publisher; article text is not reproduced.</li><li>Quotations are from public-domain sources or are brief and attributed.</li><li>Fonts are used under their open-source licences.</li></ul>
<p>To request removal or correction of any material, use the <a href="{{R}}contact.html">contact page</a> and include the page address and the basis of your request.</p>
<h2>Advertising disclosure</h2><p>This site is funded in part by advertising, including Google AdSense, and by voluntary reader support and labelled sponsorship. Advertisers and sponsors do not control editorial content.</p>''')

    page("404.html", "Page not found", "That page does not exist.", '<section class="center"><div class="wrap"><h1>404</h1><p class="lede">That page has moved or never existed.</p><p><a class="btn btn-primary" href="index.html">Go to the homepage</a></p></div></section>', index=False,
         head_extra="<script>document.write('<base href=\"'+(location.hostname.indexOf('github.io')>-1?'/best-life/':'/')+'\">')</script>")

# ------------------------------------------------------------------ META FILES
def build_meta():
    urls = "".join(f"<url><loc>{BASE}{'' if p == 'index.html' else p}</loc><lastmod>{TODAY}</lastmod></url>" for p, *_ in PAGES)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n")
    write("ads.txt", f"google.com, {ADS.replace('ca-', '')}, DIRECT, f08c47fec0942fa0\n")
    write(".nojekyll", "")
    write("data/search.json", json.dumps([{"u": p, "t": t, "d": d, "k": k} for p, t, d, k in PAGES if p not in ("search.html",)], ensure_ascii=False))
    write("manifest.webmanifest", json.dumps({"name": SITE, "short_name": SITE, "start_url": "./index.html", "display": "standalone", "background_color": "#FBF7F0", "theme_color": "#1F5C4A", "icons": [{"src": "assets/img/favicon.svg", "sizes": "any", "type": "image/svg+xml"}]}))
    write("assets/img/favicon.svg", LOGO.replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ').replace(' aria-hidden="true"', ""))
    items = "".join(f"<item><title>{e(x['title'])}</title><link>{BASE}guides/{x['slug']}.html</link><guid>{BASE}guides/{x['slug']}.html</guid><description>{e(x['desc'])}</description></item>" for x in PILLARS + ARTICLES)
    write("feed.xml", f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>{SITE} guides</title><link>{BASE}</link><description>Guides for a better life</description>{items}</channel></rss>\n')

if __name__ == "__main__":
    build_tools(); build_guides(); build_core(); build_meta()
    print(f"Built {len(PAGES)} indexable pages")
