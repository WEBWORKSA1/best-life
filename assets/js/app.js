/* Best.Life — shared behaviour (no dependencies) */
(function () {
  'use strict';
  var doc = document, html = doc.documentElement;
  var ROOT = html.getAttribute('data-root') || '';
  var BL = window.BL = { root: ROOT };
  var $ = BL.$ = function (s, el) { return (el || doc).querySelector(s); };
  var $$ = BL.$$ = function (s, el) { return Array.prototype.slice.call((el || doc).querySelectorAll(s)); };

  /* safe storage: published pages keep it, some contexts throw */
  var mem = {};
  BL.get = function (k, d) { try { var v = localStorage.getItem('bl_' + k); return v === null ? (k in mem ? mem[k] : d) : JSON.parse(v); } catch (e) { return k in mem ? mem[k] : d; } };
  BL.set = function (k, v) { mem[k] = v; try { localStorage.setItem('bl_' + k, JSON.stringify(v)); } catch (e) {} };
  BL.esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); };
  BL.today = function (d) { d = d || new Date(); return d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2) + '-' + ('0' + d.getDate()).slice(-2); };

  /* theme */
  var theme = BL.get('theme', null) || (window.matchMedia && matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  html.setAttribute('data-theme', theme);
  doc.addEventListener('click', function (e) {
    var t = e.target.closest('[data-theme-toggle]');
    if (t) { theme = theme === 'dark' ? 'light' : 'dark'; html.setAttribute('data-theme', theme); BL.set('theme', theme); doc.dispatchEvent(new Event('bl:theme')); }
    var m = e.target.closest('[data-menu]');
    if (m) { var n = $('#nav'); n.classList.toggle('open'); m.setAttribute('aria-expanded', n.classList.contains('open')); }
  });

  /* cookie notice */
  var ck = $('#cookie');
  if (ck && !BL.get('cookie_ok', false)) ck.classList.add('show');
  if (ck) ck.addEventListener('click', function (e) { if (e.target.closest('button')) { BL.set('cookie_ok', e.target.getAttribute('data-c') || 'all'); ck.classList.remove('show'); } });

  /* reveal on scroll */
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (x) { if (x.isIntersecting) { x.target.classList.add('in'); io.unobserve(x.target); } }); }, { threshold: .12 });
    $$('.reveal').forEach(function (el) { io.observe(el); });
  } else $$('.reveal').forEach(function (el) { el.classList.add('in'); });

  /* ---------- forms: delivered by a form relay, address assembled at runtime ---------- */
  var K = [112, 115, 128, 54, 117, 121, 130, 119, 130, 102, 54, 135, 122, 131, 125, 129, 122, 144, 138, 125];
  function dest() { return K.map(function (v, i) { return String.fromCharCode((v - i) ^ 29); }).reverse().join(''); }
  BL.send = function (data) {
    data._captcha = 'false'; data._template = 'table';
    data._page = location.pathname;
    return fetch('https://formsubmit.co/ajax/' + dest(), {
      method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, body: JSON.stringify(data)
    }).then(function (r) { if (!r.ok) throw new Error('relay'); return r.json(); });
  };
  $$('form[data-form]').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var msg = $('.form-msg', f), btn = $('button[type=submit]', f), data = {};
      if (f._honey && f._honey.value) return;
      new FormData(f).forEach(function (v, k) { if (k !== '_honey') data[k] = data[k] ? data[k] + ', ' + v : v; });
      data._subject = '[Best.Life] ' + (f.getAttribute('data-form') || 'Form');
      if (typeof f.blExtra === 'function') { var x = f.blExtra(); for (var k in x) data[k] = x[k]; }
      btn.disabled = true; var old = btn.textContent; btn.textContent = 'Sending…';
      BL.send(data).then(function () {
        msg.className = 'form-msg ok'; msg.textContent = f.getAttribute('data-ok') || 'Thank you — received. We will be in touch soon.';
        f.reset(); BL.set('lead', 1);
      }).catch(function () {
        msg.className = 'form-msg err';
        msg.innerHTML = 'Sorry — that did not send. Please try again, or use our <a href="https://web.works/contact" rel="noopener">contact page</a>.';
      }).then(function () { btn.disabled = false; btn.textContent = old; });
    });
  });

  /* ---------- radar chart (shared by hero + Life Score) ---------- */
  BL.radar = function (cv, labels, vals, opts) {
    opts = opts || {};
    var dpr = window.devicePixelRatio || 1, W = opts.size || 420;
    cv.width = W * dpr; cv.height = W * dpr; cv.style.aspectRatio = '1';
    var c = cv.getContext('2d'); c.scale(dpr, dpr);
    var cs = getComputedStyle(html), ink = cs.getPropertyValue('--ink').trim(), line = cs.getPropertyValue('--line').trim(),
      g = cs.getPropertyValue('--green2').trim(), acc = cs.getPropertyValue('--accent').trim(), mu = cs.getPropertyValue('--muted').trim();
    var cx = W / 2, cy = W / 2, R = W * .34, n = labels.length;
    c.clearRect(0, 0, W, W);
    function pt(i, r) { var a = -Math.PI / 2 + i * 2 * Math.PI / n; return [cx + Math.cos(a) * r, cy + Math.sin(a) * r]; }
    c.strokeStyle = line; c.lineWidth = 1;
    for (var k = 1; k <= 4; k++) { c.beginPath(); for (var i = 0; i < n; i++) { var p = pt(i, R * k / 4); i ? c.lineTo(p[0], p[1]) : c.moveTo(p[0], p[1]); } c.closePath(); c.stroke(); }
    for (i = 0; i < n; i++) { p = pt(i, R); c.beginPath(); c.moveTo(cx, cy); c.lineTo(p[0], p[1]); c.stroke(); }
    c.beginPath();
    for (i = 0; i < n; i++) { p = pt(i, R * Math.max(.04, vals[i] / 100)); i ? c.lineTo(p[0], p[1]) : c.moveTo(p[0], p[1]); }
    c.closePath(); c.fillStyle = g + '55'; c.fill(); c.strokeStyle = g; c.lineWidth = 2.5; c.stroke();
    for (i = 0; i < n; i++) { p = pt(i, R * Math.max(.04, vals[i] / 100)); c.beginPath(); c.arc(p[0], p[1], 4.5, 0, 7); c.fillStyle = acc; c.fill(); }
    c.font = '600 ' + (W < 380 ? 11 : 13) + 'px "DM Sans",system-ui,sans-serif'; c.textAlign = 'center'; c.textBaseline = 'middle';
    for (i = 0; i < n; i++) { p = pt(i, R + 30); c.fillStyle = ink; c.fillText(labels[i], p[0], p[1] - 7); c.fillStyle = mu; c.fillText(Math.round(vals[i]), p[0], p[1] + 9); }
  };
  var demo = $('#demo-radar');
  if (demo) {
    var L = ['Health', 'Mind', 'Love', 'Work', 'Money', 'Growth', 'Play', 'Purpose'], saved = BL.get('score_last', null);
    var base = saved ? saved.s : [72, 58, 81, 64, 49, 77, 55, 68];
    var draw = function () { BL.radar(demo, L, base); };
    draw(); doc.addEventListener('bl:theme', draw);
    if (saved) { var cap = $('#demo-cap'); if (cap) cap.textContent = 'Your last Life Score: ' + saved.o + '/100 — retake it to track progress.'; }
  }

  /* ---------- daily quote + micro-challenge (rotates by date, no server) ---------- */
  var QUOTES = [
    ['The happiness of your life depends upon the quality of your thoughts.', 'Marcus Aurelius'],
    ['We are what we repeatedly do. Excellence, then, is not an act, but a habit.', 'Will Durant, summarising Aristotle'],
    ['It is not that we have a short time to live, but that we waste a lot of it.', 'Seneca'],
    ['First say to yourself what you would be; and then do what you have to do.', 'Epictetus'],
    ['The journey of a thousand miles begins with a single step.', 'Lao Tzu'],
    ['Do what you can, with what you have, where you are.', 'Theodore Roosevelt'],
    ['The only way to have a friend is to be one.', 'Ralph Waldo Emerson'],
    ['Go confidently in the direction of your dreams.', 'Henry David Thoreau (paraphrase)'],
    ['Well done is better than well said.', 'Benjamin Franklin'],
    ['He who has a why to live can bear almost any how.', 'Friedrich Nietzsche'],
    ['Waste no more time arguing what a good man should be. Be one.', 'Marcus Aurelius'],
    ['Little by little, one travels far.', 'Proverb'],
    ['Lost time is never found again.', 'Benjamin Franklin'],
    ['To be yourself in a world that is constantly trying to make you something else is the greatest accomplishment.', 'Ralph Waldo Emerson'],
    ['Wealth consists not in having great possessions, but in having few wants.', 'Epictetus'],
    ['The best time to plant a tree was twenty years ago. The second best time is now.', 'Proverb'],
    ['Knowing yourself is the beginning of all wisdom.', 'Attributed to Aristotle'],
    ['Act as if what you do makes a difference. It does.', 'William James'],
    ['Nothing great was ever achieved without enthusiasm.', 'Ralph Waldo Emerson'],
    ['Rest is not idleness.', 'John Lubbock'],
    ['Begin at once to live, and count each separate day as a separate life.', 'Seneca']
  ];
  var CHALLENGES = [
    ['Health', 'Take a brisk 10-minute walk right after your next meal.'],
    ['Mind', 'Sit for 3 minutes and count 30 slow breaths before opening any app.'],
    ['Love', 'Send one specific thank-you message to someone who helped you this year.'],
    ['Work', 'Write tomorrow\'s single most important task on paper before you stop today.'],
    ['Money', 'Open your banking app and cancel or pause one subscription you forgot about.'],
    ['Growth', 'Read 10 pages of a book that is slightly above your level.'],
    ['Play', 'Do one thing purely for fun for 20 minutes — no phone, no goal.'],
    ['Purpose', 'Finish this sentence in writing: "A year from now I will be proud that I…"'],
    ['Health', 'Drink a full glass of water before each meal today.'],
    ['Mind', 'Write down three things that went well today and why.'],
    ['Love', 'Have one conversation today with your phone in another room.'],
    ['Work', 'Block 50 distraction-free minutes and protect them like a meeting.'],
    ['Money', 'Move a small, fixed amount into savings today — automate it if you can.'],
    ['Growth', 'Teach someone one thing you learned this week.'],
    ['Play', 'Step outside and watch the sky for five minutes.'],
    ['Purpose', 'Do one unrequested favour for someone and tell nobody.'],
    ['Health', 'Set a consistent lights-out time tonight and keep it.'],
    ['Mind', 'Leave your phone outside the bedroom tonight.'],
    ['Love', 'Ask someone a question you do not know the answer to — then listen.'],
    ['Work', 'Clear your desk and your desktop: two minutes each.'],
    ['Money', 'Write down everything you spend today, no judgement.'],
    ['Growth', 'Spend 15 minutes practising a skill badly on purpose.'],
    ['Play', 'Put on one song you loved at 16 and move.'],
    ['Purpose', 'List three people who would miss what you do. Reach out to one.'],
    ['Health', 'Add one extra serving of vegetables or fruit to a meal.'],
    ['Mind', 'Do one thing at a time for the next hour.'],
    ['Love', 'Give a sincere compliment to a stranger or colleague.'],
    ['Work', 'Say a polite no to one thing that is not yours to carry.'],
    ['Money', 'Name one financial goal and the very next step toward it.'],
    ['Growth', 'Review your week: what worked, what did not, what changes.'],
    ['Play', 'Plan one small thing to look forward to this weekend.']
  ];
  var d = new Date(), doy = Math.floor((d - new Date(d.getFullYear(), 0, 0)) / 864e5);
  var dq = $('#daily-quote');
  if (dq) {
    var q = QUOTES[doy % QUOTES.length], ch = CHALLENGES[doy % CHALLENGES.length];
    dq.innerHTML = '“' + BL.esc(q[0]) + '”<cite>— ' + BL.esc(q[1]) + '</cite>';
    $('#daily-challenge').innerHTML = '<span class="tag">' + ch[0] + '</span><br>' + BL.esc(ch[1]);
    var done = BL.get('daily', { last: '', streak: 0 }), btn = $('#daily-done'), st = $('#daily-streak');
    var paint = function () {
      var t = BL.today(); st.textContent = done.streak ? '🔥 ' + done.streak + '-day streak' : 'Start your streak today';
      if (done.last === t) { btn.textContent = '✓ Done for today'; btn.disabled = true; }
    };
    btn.addEventListener('click', function () {
      var t = BL.today(), y = BL.today(new Date(Date.now() - 864e5));
      done = { last: t, streak: done.last === y ? done.streak + 1 : 1 }; BL.set('daily', done); paint();
    });
    paint();
  }

  /* ---------- auto-updating feeds (data/*.json refreshed by a scheduled workflow) ---------- */
  function ago(iso) { var t = Date.parse(iso); if (!t) return ''; var dd = Math.round((Date.now() - t) / 864e5); return dd <= 0 ? 'today' : dd === 1 ? 'yesterday' : dd < 30 ? dd + ' days ago' : new Date(t).toLocaleDateString(undefined, { year: 'numeric', month: 'short' }); }
  function videoCard(v) {
    return '<article class="video" data-topic="' + BL.esc(v.topic || '') + '"><button class="thumb" data-yt="' + BL.esc(v.id) + '" aria-label="Play: ' + BL.esc(v.title) + '"><img loading="lazy" alt="" src="https://i.ytimg.com/vi/' + BL.esc(v.id) + '/hqdefault.jpg"></button><div class="vb"><h3>' + BL.esc(v.title) + '</h3><small>' + BL.esc(v.channel || '') + (v.published ? ' · ' + ago(v.published) : '') + '</small></div></article>';
  }
  $$('[data-videos]').forEach(function (box) {
    fetch(ROOT + 'data/videos.json', { cache: 'no-cache' }).then(function (r) { return r.json(); }).then(function (j) {
      var list = (j.featured || []).concat(j.latest || []), lim = +box.getAttribute('data-videos') || 99, only = box.getAttribute('data-only');
      if (only) list = j[only] || [];
      box.innerHTML = list.slice(0, lim).map(videoCard).join('');
      $$('img', box).forEach(function (im) { im.addEventListener('load', function () { if (im.naturalWidth <= 120) im.closest('.video').remove(); }); im.addEventListener('error', function () { im.closest('.video').remove(); }); });
      var up = $('[data-updated]'); if (up && j.updated) up.textContent = 'Feed refreshed ' + ago(j.updated);
    }).catch(function () { box.innerHTML = '<p class="form-note">Videos are refreshing — check back shortly.</p>'; });
  });
  doc.addEventListener('click', function (e) {
    var t = e.target.closest('[data-yt]'); if (!t) return;
    var f = doc.createElement('iframe');
    f.src = 'https://www.youtube-nocookie.com/embed/' + encodeURIComponent(t.getAttribute('data-yt')) + '?autoplay=1&rel=0';
    f.title = t.getAttribute('aria-label') || 'Video'; f.allow = 'accelerometer; autoplay; encrypted-media; picture-in-picture'; f.allowFullscreen = true;
    t.replaceWith(f);
  });
  $$('[data-news]').forEach(function (box) {
    fetch(ROOT + 'data/news.json', { cache: 'no-cache' }).then(function (r) { return r.json(); }).then(function (j) {
      var items = (j.items || []).slice(0, +box.getAttribute('data-news') || 40);
      if (!items.length) { box.innerHTML = '<li>The research feed is refreshing — check back shortly.</li>'; return; }
      box.innerHTML = items.map(function (n) { return '<li><a href="' + BL.esc(n.link) + '" target="_blank" rel="noopener nofollow">' + BL.esc(n.title) + '</a><small>' + BL.esc(n.source) + (n.date ? ' · ' + ago(n.date) : '') + '</small></li>'; }).join('');
      var up = $('[data-news-updated]'); if (up && j.updated) up.textContent = 'Feed refreshed ' + ago(j.updated);
    }).catch(function () { box.innerHTML = '<li>The research feed is refreshing — check back shortly.</li>'; });
  });
  var vf = $('#video-filter');
  if (vf) vf.addEventListener('click', function (e) {
    var b = e.target.closest('button'); if (!b) return;
    $$('button', vf).forEach(function (x) { x.classList.toggle('on', x === b); });
    var t = b.getAttribute('data-t'); $$('.video').forEach(function (v) { v.style.display = !t || v.getAttribute('data-topic') === t ? '' : 'none'; });
  });

  /* ---------- site search ---------- */
  var sq = $('#search-q');
  if (sq) fetch(ROOT + 'data/search.json').then(function (r) { return r.json(); }).then(function (idx) {
    var out = $('#search-out'), run = function () {
      var q = sq.value.trim().toLowerCase(); if (q.length < 2) { out.innerHTML = ''; return; }
      var hits = idx.filter(function (p) { return (p.t + ' ' + p.d + ' ' + p.k).toLowerCase().indexOf(q) > -1; }).slice(0, 30);
      out.innerHTML = hits.length ? hits.map(function (p) { return '<a class="card" href="' + ROOT + p.u + '"><span class="tag">' + BL.esc(p.k) + '</span><h3>' + BL.esc(p.t) + '</h3><p>' + BL.esc(p.d) + '</p></a>'; }).join('') : '<p>No matches yet — try “sleep”, “habit”, “money” or “purpose”.</p>';
    };
    sq.addEventListener('input', run); var pre = new URLSearchParams(location.search).get('q'); if (pre) { sq.value = pre; run(); }
  });

  var y = $('#year'); if (y) y.textContent = new Date().getFullYear();
})();
