/* Best.Life — interactive tools. Everything runs in the browser; nothing is uploaded. */
(function () {
  'use strict';
  var BL = window.BL, $ = BL.$, $$ = BL.$$, esc = BL.esc;
  var T = {};
  function fmtTime(d) { return d.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' }); }
  function money(n) { return n.toLocaleString(undefined, { maximumFractionDigits: 0 }); }
  function num(id, d) { var v = parseFloat($('#' + id).value); return isNaN(v) ? d : v; }

  /* ============ LIFE SCORE ============ */
  T.score = function (el) {
    var AREAS = [
      { k: 'Health', i: '🌿', g: 'guides/health.html', q: ['I wake up most days with enough energy for what I need to do.', 'I move my body on purpose at least three times a week.', 'What I eat and drink most days supports how I want to feel.'],
        a: ['Fix your sleep window first: same wake time for 14 days.', 'Add a 10-minute walk after your largest meal.', 'Book the check-up you have been postponing.'] },
      { k: 'Mind', i: '🧠', g: 'guides/mind.html', q: ['I can calm myself down when I am stressed.', 'I rarely feel overwhelmed for days at a time.', 'I spend time each week without a screen in front of me.'],
        a: ['Practise 5 minutes of slow breathing daily (try the Breathing Timer).', 'Write three good things each night for two weeks.', 'Create one phone-free hour every day.'] },
      { k: 'Love', i: '💛', g: 'guides/relationships.html', q: ['I have at least one person I can call at 3 a.m.', 'I spend unhurried time with people I care about every week.', 'I feel heard and respected in my closest relationships.'],
        a: ['Schedule one recurring weekly call or meal with someone who matters.', 'Send two specific appreciation messages this week.', 'Have one device-free conversation per day.'] },
      { k: 'Work', i: '🛠️', g: 'guides/career.html', q: ['My work uses skills I enjoy using.', 'I know what progress looks like for me in the next 12 months.', 'I can usually stop working without guilt at the end of the day.'],
        a: ['Define one 90-day skill goal and block 3 hours a week for it.', 'Protect one 50-minute deep-work block every morning.', 'Ask one person ahead of you for 20 minutes of advice.'] },
      { k: 'Money', i: '💰', g: 'guides/money.html', q: ['I spend less than I earn in a typical month.', 'I could cover an unexpected expense without panic.', 'I know roughly where my money goes.'],
        a: ['Track every expense for 30 days — awareness comes first.', 'Automate a small transfer to savings on payday.', 'List every subscription and cancel the bottom third.'] },
      { k: 'Growth', i: '📚', g: 'guides/growth.html', q: ['I am learning something new right now.', 'I regularly do things slightly outside my comfort zone.', 'I reflect on what is and is not working in my life.'],
        a: ['Read 10 pages a day — one book a month follows.', 'Run a weekly 15-minute review: keep, stop, start.', 'Pick one skill and practise it 20 minutes a day for 30 days.'] },
      { k: 'Play', i: '🎈', g: 'guides/play.html', q: ['I do something purely for enjoyment every week.', 'I laugh often.', 'I have a hobby or interest that absorbs me.'],
        a: ['Put one fun, non-productive activity in your calendar this week.', 'Revive one hobby you dropped — 30 minutes is enough.', 'Plan a small adventure within 20 km of home.'] },
      { k: 'Purpose', i: '🧭', g: 'guides/purpose.html', q: ['I know what matters most to me.', 'My daily actions mostly line up with my values.', 'I feel I contribute to something beyond myself.'],
        a: ['Write your top five values and rank them.', 'Give two hours this month to a cause or a person who needs it.', 'Write a one-paragraph description of a great ordinary day five years from now.'] }
    ];
    var total = 24, form = $('#score-form', el), res = $('#score-result', el), prog = $('#score-prog', el), cnt = $('#score-count', el), h = '';
    AREAS.forEach(function (A, ai) {
      h += '<fieldset style="border:0;padding:0;margin:0 0 26px"><legend><h3>' + A.i + ' ' + A.k + '</h3></legend>';
      A.q.forEach(function (q, qi) {
        var n = 'q' + ai + '_' + qi; h += '<div class="q"><p id="' + n + 'l">' + q + '</p><div class="scale" role="radiogroup" aria-labelledby="' + n + 'l">';
        for (var v = 1; v <= 5; v++) h += '<label><input type="radio" name="' + n + '" value="' + v + '"><span>' + v + '</span></label>';
        h += '</div><div class="scale-legend"><span>Not true</span><span>Very true</span></div></div>';
      });
      h += '</fieldset>';
    });
    $('#score-qs', el).innerHTML = h;
    form.addEventListener('change', function () { var n = $$('input:checked', form).length; prog.style.width = (n / total * 100) + '%'; cnt.textContent = n + ' of ' + total + ' answered'; });

    function shape(s) {
      var mx = Math.max.apply(0, s), mn = Math.min.apply(0, s), avg = s.reduce(function (a, b) { return a + b; }, 0) / s.length, spread = mx - mn;
      if (avg >= 75 && spread < 25) return ['The Full Circle', 'High and even. Your job now is maintenance and depth — protect what works and stretch one area on purpose.'];
      if (spread < 20) return avg >= 50 ? ['The Steady Wheel', 'Balanced with room to rise. Small upgrades anywhere lift everything — start with whichever area excites you most.'] : ['The Reset', 'Evenly low is not failure, it is a clean starting line. Pick one keystone area — usually Health — and let momentum spread.'];
      if (spread >= 45) return ['The Spike', 'One or two areas are carrying you while another is being starved. The fastest win is not more strength — it is patching the gap.'];
      return ['The Climber', 'Clear strengths, clear gaps. You already know how to build an area up — point that same skill at your lowest score.'];
    }
    function render(s, o, when) {
      var order = s.map(function (v, i) { return [v, i]; }).sort(function (a, b) { return a[0] - b[0]; }), low = order.slice(0, 2), sh = shape(s), hist = BL.get('score_hist', []);
      var bars = AREAS.map(function (A, i) { return '<div class="bar' + (i === low[0][1] || i === low[1][1] ? ' low' : '') + '"><span>' + A.i + ' ' + A.k + '</span><div><i style="width:' + s[i] + '%"></i></div><b>' + s[i] + '</b></div>'; }).join('');
      var plan = low.map(function (l) { var A = AREAS[l[1]]; return '<div class="card"><span class="tag">Focus area · ' + l[0] + '/100</span><h3>' + A.i + ' ' + A.k + '</h3><ol>' + A.a.map(function (x) { return '<li>' + x + '</li>'; }).join('') + '</ol><a href="' + BL.root + A.g + '">Read the ' + A.k + ' guide →</a></div>'; }).join('');
      var trend = hist.length > 1 ? '<p class="form-note">Previous score: ' + hist[hist.length - 2].o + '/100 on ' + hist[hist.length - 2].d + ' → change of ' + (o - hist[hist.length - 2].o >= 0 ? '+' : '') + (o - hist[hist.length - 2].o) + '.</p>' : '';
      res.innerHTML = '<div class="tool"><div class="grid g2" style="align-items:center"><div><span class="eyebrow">Your Life Score' + (when ? ' · ' + when : '') + '</span><div class="big" style="font-size:4rem">' + o + '<small style="font-size:1.4rem;color:var(--muted)">/100</small></div><h2 style="margin-top:8px">' + sh[0] + '</h2><p>' + sh[1] + '</p>' + trend + '<div class="no-print" style="display:flex;gap:10px;flex-wrap:wrap"><button class="btn btn-ghost btn-sm" id="sc-share">Copy share link</button><button class="btn btn-ghost btn-sm" onclick="print()">Print / save PDF</button><button class="btn btn-ghost btn-sm" id="sc-again">Retake</button></div></div><canvas id="sc-radar" aria-label="Radar chart of your eight life areas"></canvas></div><div style="margin-top:22px">' + bars + '</div></div><h2 style="margin-top:40px">Your 30-day plan</h2><p class="lede">Do not fix everything. Work only on your two lowest areas for 30 days, then retake the score.</p><div class="grid g2">' + plan + '</div>';
      var cv = $('#sc-radar'), lab = AREAS.map(function (A) { return A.k; }), draw = function () { BL.radar(cv, lab, s); };
      draw(); document.addEventListener('bl:theme', draw);
      $('#sc-share').onclick = function () { var u = location.origin + location.pathname + '#s=' + s.join('-'); (navigator.clipboard ? navigator.clipboard.writeText(u) : Promise.reject()).then(function () { $('#sc-share').textContent = 'Link copied ✓'; }, function () { prompt('Copy this link', u); }); };
      $('#sc-again').onclick = function () { res.innerHTML = ''; form.style.display = ''; form.reset(); prog.style.width = 0; form.scrollIntoView(); };
      var lf = $('#score-lead'); if (lf) { lf.style.display = ''; lf.blExtra = function () { var x = { life_score: o + '/100', life_shape: sh[0] }; AREAS.forEach(function (A, i) { x['score_' + A.k] = s[i]; }); x._autoresponse = 'Your Best.Life Life Score: ' + o + '/100 (' + sh[0] + '). ' + AREAS.map(function (A, i) { return A.k + ' ' + s[i]; }).join(', ') + '. Focus for the next 30 days: ' + AREAS[low[0][1]].k + ' and ' + AREAS[low[1][1]].k + '. Retake any time at best.life/life-score.html'; return x; }; }
      form.style.display = 'none'; res.scrollIntoView({ behavior: 'smooth' });
    }
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if ($$('input:checked', form).length < total) { var first = AREAS.map(function (A, ai) { return [0, 1, 2].map(function (qi) { return 'q' + ai + '_' + qi; }); }).reduce(function (a, b) { return a.concat(b); }).filter(function (n) { return !$('input[name=' + n + ']:checked', form); })[0]; $('input[name=' + first + ']', form).closest('.q').scrollIntoView({ behavior: 'smooth', block: 'center' }); cnt.textContent = 'Please answer all 24 — ' + $$('input:checked', form).length + ' done'; return; }
      var s = AREAS.map(function (A, ai) { var t = 0; for (var qi = 0; qi < 3; qi++) t += +$('input[name=q' + ai + '_' + qi + ']:checked', form).value; return Math.round((t - 3) / 12 * 100); });
      var o = Math.round(s.reduce(function (a, b) { return a + b; }, 0) / 8), hist = BL.get('score_hist', []);
      hist.push({ d: BL.today(), o: o, s: s }); BL.set('score_hist', hist.slice(-24)); BL.set('score_last', { o: o, s: s });
      render(s, o);
    });
    var m = location.hash.match(/s=([\d-]+)/);
    if (m) { var s = m[1].split('-').map(Number); if (s.length === 8 && s.every(function (v) { return v >= 0 && v <= 100; })) render(s, Math.round(s.reduce(function (a, b) { return a + b; }, 0) / 8), 'shared result'); }
  };

  /* ============ SLEEP ============ */
  T.sleep = function (el) {
    var mode = 'wake';
    function run() {
      var t = $('#sl-time').value || '07:00', lat = num('sl-lat', 15), p = t.split(':'), base = new Date(); base.setHours(+p[0], +p[1], 0, 0);
      var chips = [6, 5, 4, 3].map(function (c) {
        var mins = c * 90 + lat, d = new Date(base.getTime() + (mode === 'wake' ? -mins : mins) * 6e4);
        return '<div class="chip' + (c === 5 || c === 6 ? ' best' : '') + '">' + fmtTime(d) + '<small>' + c + ' cycles · ' + (c * 1.5) + ' h asleep</small></div>';
      });
      $('#sl-out').innerHTML = '<strong>' + (mode === 'wake' ? 'To wake at ' + fmtTime(base) + ', get into bed around:' : 'If you get into bed at ' + fmtTime(base) + ', set an alarm for:') + '</strong><div class="chips">' + chips.join('') + '</div><p class="form-note" style="margin-top:12px">Highlighted options give most adults the 7–9 hours commonly recommended. Includes ' + lat + ' minutes to fall asleep.</p>';
    }
    $$('.seg button', el).forEach(function (b) { b.onclick = function () { mode = b.getAttribute('data-m'); $$('.seg button', el).forEach(function (x) { x.classList.toggle('on', x === b); }); $('#sl-label').textContent = mode === 'wake' ? 'I need to wake up at' : 'I plan to go to bed at'; run(); }; });
    el.addEventListener('input', run); run();
  };

  /* ============ HABIT TRACKER ============ */
  T.habits = function (el) {
    var st = BL.get('habits', { list: [], log: {} });
    function days(n) { var a = []; for (var i = n - 1; i >= 0; i--) a.push(new Date(Date.now() - i * 864e5)); return a; }
    function streak(id) { var n = 0, d = new Date(); if (!(st.log[id] || {})[BL.today(d)]) d = new Date(d - 864e5); while ((st.log[id] || {})[BL.today(d)]) { n++; d = new Date(d - 864e5); } return n; }
    function draw() {
      var ds = days(7), out = $('#hb-out');
      if (!st.list.length) { out.innerHTML = '<p>No habits yet. Add your first one above — keep it so small you cannot say no.</p>'; return; }
      var h = '<div class="tablewrap"><table class="habit-grid"><thead><tr><th>Habit</th>' + ds.map(function (d) { return '<th>' + d.toLocaleDateString([], { weekday: 'short' }) + '<br><small>' + d.getDate() + '</small></th>'; }).join('') + '<th>Streak</th><th>30d</th><th></th></tr></thead><tbody>';
      st.list.forEach(function (hb) {
        var log = st.log[hb.id] || {}, c30 = days(30).filter(function (d) { return log[BL.today(d)]; }).length;
        h += '<tr><td><strong>' + esc(hb.name) + '</strong></td>' + ds.map(function (d) { var k = BL.today(d); return '<td><button class="tick' + (log[k] ? ' on' : '') + '" data-h="' + hb.id + '" data-d="' + k + '" aria-label="' + esc(hb.name) + ' on ' + k + '" aria-pressed="' + !!log[k] + '">' + (log[k] ? '✓' : '') + '</button></td>'; }).join('') + '<td>🔥 ' + streak(hb.id) + '</td><td>' + Math.round(c30 / 30 * 100) + '%</td><td><button class="del" data-del="' + hb.id + '" aria-label="Delete ' + esc(hb.name) + '">✕</button></td></tr>';
      });
      out.innerHTML = h + '</tbody></table></div>';
    }
    $('#hb-add').addEventListener('submit', function (e) { e.preventDefault(); var v = $('#hb-name').value.trim(); if (!v) return; st.list.push({ id: 'h' + Date.now(), name: v.slice(0, 60) }); BL.set('habits', st); $('#hb-name').value = ''; draw(); });
    el.addEventListener('click', function (e) {
      var t = e.target.closest('.tick'), d = e.target.closest('[data-del]');
      if (t) { var id = t.getAttribute('data-h'), k = t.getAttribute('data-d'); st.log[id] = st.log[id] || {}; if (st.log[id][k]) delete st.log[id][k]; else st.log[id][k] = 1; BL.set('habits', st); draw(); }
      if (d) { var x = d.getAttribute('data-del'); st.list = st.list.filter(function (h) { return h.id !== x; }); delete st.log[x]; BL.set('habits', st); draw(); }
      if (e.target.id === 'hb-export') { var a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([JSON.stringify(st, null, 2)], { type: 'application/json' })); a.download = 'best-life-habits.json'; a.click(); }
    });
    draw();
  };

  /* ============ LIFE IN WEEKS ============ */
  T.weeks = function (el) {
    function run() {
      var dob = $('#wk-dob').value, exp = Math.min(110, Math.max(40, num('wk-exp', 85))); if (!dob) return;
      var b = new Date(dob), now = new Date(); if (isNaN(b) || b > now) return;
      var lived = Math.floor((now - b) / (7 * 864e5)), tot = Math.round(exp * 52.18), left = Math.max(0, tot - lived), pct = Math.min(100, lived / tot * 100);
      var age = (now - b) / (365.25 * 864e5);
      $('#wk-stats').innerHTML = [['Weeks lived', lived.toLocaleString()], ['Weeks ahead', left.toLocaleString()], ['Of the journey', pct.toFixed(1) + '%'], ['Summers ahead', Math.max(0, Math.round(exp - age))], ['Weekends ahead', left.toLocaleString()]].map(function (s) { return '<div class="stat"><b>' + s[1] + '</b><span>' + s[0] + '</span></div>'; }).join('');
      var cv = $('#wk-cv'), cols = 52, rows = exp, cell = 9, gap = 2, pad = 26, dpr = window.devicePixelRatio || 1, W = pad + cols * (cell + gap), H = pad + rows * (cell + gap);
      cv.width = W * dpr; cv.height = H * dpr; cv.style.width = '100%'; cv.style.maxWidth = W + 'px';
      var c = cv.getContext('2d'); c.scale(dpr, dpr); var cs = getComputedStyle(document.documentElement);
      c.fillStyle = cs.getPropertyValue('--card'); c.fillRect(0, 0, W, H);
      c.font = '10px sans-serif'; c.fillStyle = cs.getPropertyValue('--muted');
      for (var r = 0; r < rows; r++) { if (r % 5 === 0) c.fillText(r, 2, pad + r * (cell + gap) + 8); for (var k = 0; k < cols; k++) { var i = r * 52 + k; c.fillStyle = i < lived ? cs.getPropertyValue('--green2') : i === lived ? cs.getPropertyValue('--accent') : cs.getPropertyValue('--line'); c.fillRect(pad + k * (cell + gap), pad + r * (cell + gap), cell, cell); } }
      $('#wk-dl').style.display = '';
    }
    el.addEventListener('input', run); document.addEventListener('bl:theme', run);
    $('#wk-dl').onclick = function () { var a = document.createElement('a'); a.href = $('#wk-cv').toDataURL('image/png'); a.download = 'my-life-in-weeks.png'; a.click(); };
  };

  /* ============ COMPOUND GROWTH ============ */
  T.compound = function (el) {
    function run() {
      var P = num('cg-start', 0), M = num('cg-month', 0), r = num('cg-rate', 0) / 100, Y = Math.min(60, Math.max(1, num('cg-years', 10))), inf = num('cg-inf', 0) / 100;
      var bal = P, paid = P, rows = [], pts = [[0, P, P]];
      for (var y = 1; y <= Y; y++) { for (var m = 0; m < 12; m++) { bal = bal * (1 + r / 12) + M; paid += M; } rows.push([y, paid, bal]); pts.push([y, paid, bal]); }
      var real = bal / Math.pow(1 + inf, Y);
      $('#cg-stats').innerHTML = [['Final balance', money(bal)], ['You put in', money(paid)], ['Growth earned', money(bal - paid)], ['In today\'s money', money(real)]].map(function (s) { return '<div class="stat"><b>' + s[1] + '</b><span>' + s[0] + '</span></div>'; }).join('');
      var cv = $('#cg-cv'), dpr = window.devicePixelRatio || 1, W = 640, H = 300; cv.width = W * dpr; cv.height = H * dpr; cv.style.width = '100%';
      var c = cv.getContext('2d'); c.scale(dpr, dpr); c.clearRect(0, 0, W, H); var cs = getComputedStyle(document.documentElement), mx = bal || 1, px = function (y) { return 44 + y / Y * (W - 60); }, py = function (v) { return H - 30 - v / mx * (H - 50); };
      [[2, cs.getPropertyValue('--green2')], [1, cs.getPropertyValue('--gold')]].forEach(function (s) { c.beginPath(); c.moveTo(px(0), py(0)); pts.forEach(function (p) { c.lineTo(px(p[0]), py(p[s[0]])); }); c.lineTo(px(Y), py(0)); c.closePath(); c.fillStyle = s[1].trim() + (s[0] === 2 ? '66' : 'AA'); c.fill(); });
      c.fillStyle = cs.getPropertyValue('--muted'); c.font = '12px sans-serif'; c.fillText('Year 0', 44, H - 10); c.fillText('Year ' + Y, W - 60, H - 10); c.fillText(money(mx), 4, 16);
      $('#cg-table').innerHTML = '<tr><th>Year</th><th>Contributed</th><th>Balance</th></tr>' + rows.filter(function (x, i) { return Y <= 15 || (i + 1) % 5 === 0 || i === rows.length - 1; }).map(function (x) { return '<tr><td>' + x[0] + '</td><td>' + money(x[1]) + '</td><td>' + money(x[2]) + '</td></tr>'; }).join('');
    }
    el.addEventListener('input', run); document.addEventListener('bl:theme', run); run();
  };

  /* ============ DAILY ENERGY + WATER ============ */
  T.energy = function (el) {
    function run() {
      var sex = $('#en-sex').value, age = num('en-age', 30), unit = $('#en-unit').value, w = num('en-w', 70), h = num('en-h', 170), act = +$('#en-act').value;
      if (unit === 'imperial') { w = w * 0.4536; h = h * 2.54; }
      $('#en-wl').textContent = unit === 'imperial' ? 'Weight (lb)' : 'Weight (kg)'; $('#en-hl').textContent = unit === 'imperial' ? 'Height (in)' : 'Height (cm)';
      if (age < 18 || !(w > 0) || !(h > 0)) { $('#en-out').innerHTML = '<p>This estimator is designed for adults aged 18 and over.</p>'; return; }
      var bmr = 10 * w + 6.25 * h - 5 * age + (sex === 'm' ? 5 : -161), tdee = bmr * act, water = w * 0.033;
      $('#en-out').innerHTML = '<div class="stats">' + [['Resting energy / day', Math.round(bmr) + ' kcal'], ['Estimated maintenance', Math.round(tdee / 10) * 10 + ' kcal'], ['Water guide', water.toFixed(1) + ' L']].map(function (s) { return '<div class="stat"><b>' + s[1] + '</b><span>' + s[0] + '</span></div>'; }).join('') + '</div><p class="form-note" style="margin-top:12px">Mifflin–St Jeor estimate; real needs vary by ±10% or more. This is a maintenance estimate for general education — not a diet target and not medical advice.</p>';
    }
    el.addEventListener('input', run); run();
  };

  /* ============ BREATHING ============ */
  T.breath = function (el) {
    var P = { box: [['Inhale', 4, 1.9], ['Hold', 4, 1.9], ['Exhale', 4, 1], ['Hold', 4, 1]], '478': [['Inhale', 4, 1.9], ['Hold', 7, 1.9], ['Exhale', 8, 1]], calm: [['Inhale', 5, 1.9], ['Exhale', 5, 1]] };
    var cur = 'box', tm = null, orb = $('#br-orb'), rounds = 0;
    function stop() { clearTimeout(tm); tm = null; orb.style.transform = 'scale(1)'; orb.textContent = 'Ready'; $('#br-go').textContent = 'Start'; }
    function step(i) { var s = P[cur][i]; orb.style.transitionDuration = s[1] + 's'; orb.style.transform = 'scale(' + s[2] + ')'; orb.textContent = s[0]; if (i === 0) { rounds++; $('#br-count').textContent = 'Round ' + rounds; } tm = setTimeout(function () { step((i + 1) % P[cur].length); }, s[1] * 1000); }
    $('#br-go').onclick = function () { if (tm) { stop(); return; } rounds = 0; this.textContent = 'Stop'; step(0); };
    $$('.seg button', el).forEach(function (b) { b.onclick = function () { cur = b.getAttribute('data-p'); $$('.seg button', el).forEach(function (x) { x.classList.toggle('on', x === b); }); stop(); }; });
  };

  /* ============ FOCUS TIMER ============ */
  T.focus = function (el) {
    var left = 25 * 60, run = null, mode = 'focus', log = BL.get('focus', {}), out = $('#fc-time');
    function show() { out.textContent = ('0' + Math.floor(left / 60)).slice(-2) + ':' + ('0' + left % 60).slice(-2); document.title = (run ? out.textContent + ' · ' : '') + 'Focus Timer — Best.Life'; $('#fc-today').textContent = (log[BL.today()] || 0) + ' focus sessions today'; }
    function set() { left = (mode === 'focus' ? num('fc-f', 25) : num('fc-b', 5)) * 60; $('#fc-mode').textContent = mode === 'focus' ? 'Focus' : 'Break'; show(); }
    function tick() { left--; if (left <= 0) { clearInterval(run); run = null; if (mode === 'focus') { log[BL.today()] = (log[BL.today()] || 0) + 1; BL.set('focus', log); } try { var a = new (window.AudioContext || window.webkitAudioContext)(), o = a.createOscillator(), g = a.createGain(); o.connect(g); g.connect(a.destination); o.frequency.value = 660; g.gain.setValueAtTime(.2, a.currentTime); g.gain.exponentialRampToValueAtTime(.001, a.currentTime + 1.2); o.start(); o.stop(a.currentTime + 1.2); } catch (e) {} mode = mode === 'focus' ? 'break' : 'focus'; set(); $('#fc-go').textContent = 'Start'; } show(); }
    $('#fc-go').onclick = function () { if (run) { clearInterval(run); run = null; this.textContent = 'Resume'; } else { run = setInterval(tick, 1000); this.textContent = 'Pause'; } show(); };
    $('#fc-reset').onclick = function () { clearInterval(run); run = null; mode = 'focus'; set(); $('#fc-go').textContent = 'Start'; };
    $('#fc-f').oninput = $('#fc-b').oninput = function () { if (!run) set(); };
    set();
  };

  /* ============ GRATITUDE JOURNAL ============ */
  T.gratitude = function (el) {
    var list = BL.get('gratitude', []);
    function draw() { $('#gr-out').innerHTML = list.length ? list.slice().reverse().map(function (g, i) { return '<div class="card" style="margin-bottom:12px"><small class="form-note">' + esc(g.d) + '</small><p style="color:var(--ink);white-space:pre-wrap">' + esc(g.t) + '</p><button class="del" data-i="' + (list.length - 1 - i) + '" aria-label="Delete entry">✕ remove</button></div>'; }).join('') : '<p>Your entries will appear here. They are stored only in this browser.</p>'; $('#gr-n').textContent = list.length + ' entries'; }
    $('#gr-form').addEventListener('submit', function (e) { e.preventDefault(); var v = $('#gr-text').value.trim(); if (!v) return; list.push({ d: new Date().toLocaleDateString(undefined, { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }), t: v.slice(0, 2000) }); BL.set('gratitude', list); $('#gr-text').value = ''; draw(); });
    el.addEventListener('click', function (e) { var d = e.target.closest('[data-i]'); if (d) { list.splice(+d.getAttribute('data-i'), 1); BL.set('gratitude', list); draw(); } if (e.target.id === 'gr-export') { var a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([list.map(function (g) { return g.d + '\n' + g.t; }).join('\n\n')], { type: 'text/plain' })); a.download = 'gratitude-journal.txt'; a.click(); } });
    var PR = ['What made you smile today?', 'Who helped you recently, and how?', 'What is something ordinary you would miss if it vanished?', 'What did your body let you do today?', 'What problem do you no longer have?', 'Which small comfort did you enjoy today?', 'What are you looking forward to?'];
    $('#gr-prompt').textContent = PR[new Date().getDay()];
    draw();
  };

  /* ============ GOAL BUILDER ============ */
  T.goal = function (el) {
    $('#gl-form').addEventListener('submit', function (e) {
      e.preventDefault();
      var what = $('#gl-what').value.trim(), meas = $('#gl-meas').value.trim(), why = $('#gl-why').value.trim(), wks = Math.min(52, Math.max(1, num('gl-weeks', 12))), small = $('#gl-small').value.trim(), block = $('#gl-block').value.trim();
      if (!what) return; var end = new Date(Date.now() + wks * 7 * 864e5), ms = [];
      [0.25, 0.5, 0.75, 1].forEach(function (f) { var w = Math.max(1, Math.round(wks * f)); ms.push('<li><strong>Week ' + w + ':</strong> ' + Math.round(f * 100) + '% of the way' + (meas ? ' — check: ' + esc(meas) : '') + '</li>'); });
      $('#gl-out').innerHTML = '<div class="card"><span class="tag">Your goal statement</span><blockquote style="font-family:var(--display);font-size:1.3rem;margin:8px 0 16px">By <strong>' + end.toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' }) + '</strong>, I will <strong>' + esc(what) + '</strong>' + (meas ? ', measured by <strong>' + esc(meas) + '</strong>' : '') + (why ? ', because <strong>' + esc(why) + '</strong>' : '') + '.</blockquote><h3>Checkpoints</h3><ul>' + ms.join('') + '</ul>' + (small ? '<h3>Daily minimum</h3><p style="color:var(--ink)">Even on the worst day: ' + esc(small) + '</p>' : '') + (block ? '<h3>If–then plan</h3><p style="color:var(--ink)">If ' + esc(block) + ' happens, then I will do my daily minimum anyway and restart tomorrow.</p>' : '') + '<button class="btn btn-ghost btn-sm no-print" onclick="print()">Print this plan</button></div>';
      $('#gl-out').scrollIntoView({ behavior: 'smooth' });
    });
  };

  $$('[data-tool]').forEach(function (el) { var f = T[el.getAttribute('data-tool')]; if (f) f(el); });
})();
