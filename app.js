'use strict';
/* CAT Quant Practice: one question at a time, options shuffled on every attempt. */
const $ = id => document.getElementById(id);
const LETTERS = 'ABCD';
let DATA = null, block = null, order = [], idx = 0, picks = [];

const store = {
  get(k, d) { try { const v = localStorage.getItem('cqp.' + k); return v == null ? d : JSON.parse(v); } catch (e) { return d; } },
  set(k, v) { try { localStorage.setItem('cqp.' + k, JSON.stringify(v)); } catch (e) { /* private mode: scores just aren't kept */ } },
};

function shuffle(a) { const b = a.slice(); for (let i = b.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [b[i], b[j]] = [b[j], b[i]]; } return b; }
function screen(id) { ['home', 'quiz', 'results'].forEach(s => { $(s).hidden = s !== id; }); window.scrollTo(0, 0); }

function renderHome() {
  $('blocks').innerHTML = DATA.blocks.map((b, i) => {
    const best = store.get('best.' + b.id, null);
    return `<button class="block" type="button" data-b="${b.id}">
      <span class="num">Block ${i + 1} · ${b.questions.length} questions</span>
      <h2>${b.name}</h2><p>${b.blurb}</p>
      ${best != null ? `<span class="best">Best: ${best}/${b.questions.length}</span>` : ''}</button>`;
  }).join('');
  $('blocks').querySelectorAll('[data-b]').forEach(el => el.onclick = () => { location.hash = el.dataset.b; });
  screen('home');
}

function start(id) {
  block = DATA.blocks.find(b => b.id === id);
  if (!block) { renderHome(); return; }
  // each question gets a fresh option order; `order[i]` maps display position → original option index
  order = block.questions.map(q => shuffle([0, 1, 2, 3]));
  idx = 0; picks = [];
  screen('quiz');
  show();
}

function show() {
  const q = block.questions[idx], ord = order[idx];
  $('qCount').textContent = `${block.name} · ${idx + 1} of ${block.questions.length}`;
  $('qBar').style.width = (100 * idx / block.questions.length) + '%';
  $('qTopic').textContent = q.topic; $('qLevel').textContent = q.level;
  $('qText').innerHTML = q.text;
  $('opts').innerHTML = ord.map((o, i) => `<button class="opt" type="button" data-i="${o}"><span class="l">${LETTERS[i]}</span><span>${q.options[o]}</span></button>`).join('');
  $('opts').querySelectorAll('.opt').forEach(b => b.onclick = () => answer(+b.dataset.i));
  $('feedback').hidden = true; $('nextBtn').hidden = true;
  $('opts').querySelector('.opt').focus({ preventScroll: true });
}

function answer(choice) {
  const q = block.questions[idx], ord = order[idx];
  picks[idx] = choice;
  $('opts').querySelectorAll('.opt').forEach(b => {
    const i = +b.dataset.i; b.disabled = true;
    if (i === q.answer) b.classList.add('right');
    else if (i === choice) b.classList.add('wrong');
    else b.classList.add('dim');
  });
  const ok = choice === q.answer;
  const letter = LETTERS[ord.indexOf(q.answer)];
  $('verdict').className = 'verdict ' + (ok ? 'good' : 'bad');
  $('verdict').innerHTML = ok ? '✓ Correct' : `✗ Not quite. The answer is ${letter}: ${q.options[q.answer]}`;
  $('solution').innerHTML = q.solution.map(s => `<li>${s}</li>`).join('');
  $('explanation').innerHTML = q.explanation;
  $('feedback').hidden = false;
  $('nextBtn').hidden = false;
  $('nextBtn').textContent = idx === block.questions.length - 1 ? 'See my score' : 'Next question';
  $('nextBtn').focus({ preventScroll: true });
  $('qBar').style.width = (100 * (idx + 1) / block.questions.length) + '%';
}

function next() {
  if (idx < block.questions.length - 1) { idx++; show(); window.scrollTo({ top: 0, behavior: 'smooth' }); }
  else results();
}

function results() {
  const n = block.questions.length;
  const score = block.questions.reduce((s, q, i) => s + (picks[i] === q.answer ? 1 : 0), 0);
  const best = store.get('best.' + block.id, null);
  if (best == null || score > best) store.set('best.' + block.id, score);
  $('rBlock').textContent = `Block ${DATA.blocks.indexOf(block) + 1} · ${block.name}`;
  $('rScore').textContent = score; $('rOf').textContent = `/ ${n} correct`;
  $('rMsg').textContent = score === n ? 'Full marks. Try another block, or come back to this one in a few days to make sure it sticks.'
    : score >= n - 1 ? 'Nearly there. Read the explanation for the one you missed, then try the block again.'
    : 'Read the explanations below for the ones you missed, then try the block again. The options come in a new order each time.';
  $('review').innerHTML = block.questions.map((q, i) => {
    const ok = picks[i] === q.answer;
    return `<details class="${ok ? 'ok' : 'no'}"><summary><span class="m">${ok ? '✓' : '✗'}</span><span>${q.text}</span></summary>
      <div class="body"><p><b>Answer:</b> ${q.options[q.answer]}${ok ? '' : ` · <b>You chose:</b> ${q.options[picks[i]]}`}</p>
      <ol>${q.solution.map(s => `<li>${s}</li>`).join('')}</ol><p class="explain">${q.explanation}</p></div></details>`;
  }).join('');
  screen('results');
}

function route() {
  const id = location.hash.replace('#', '');
  if (id && DATA.blocks.some(b => b.id === id)) start(id); else renderHome();
}

$('nextBtn').onclick = next;
$('quitBtn').onclick = () => { location.hash = ''; };
$('homeBtn').onclick = () => { location.hash = ''; };
$('retryBtn').onclick = () => start(block.id);
window.addEventListener('hashchange', route);

fetch('questions.json').then(r => r.json()).then(d => { DATA = d; route(); })
  .catch(() => { $('blocks').innerHTML = '<p class="lede">The questions could not be loaded. Refresh the page to try again.</p>'; });
