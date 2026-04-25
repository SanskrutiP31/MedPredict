import os
BASE = os.path.dirname(os.path.abspath(__file__))

JS = """\
'use strict';

let diseaseChart = null;

// ── STEP NAVIGATION
function goStep(n) {
  document.querySelectorAll('.step-panel').forEach(p => p.classList.remove('active'));
  document.getElementById('step' + n).classList.add('active');
  document.querySelectorAll('.step-dot').forEach(d => {
    const s = parseInt(d.dataset.step);
    d.classList.toggle('active', s === n);
    d.classList.toggle('done', s < n);
  });
  document.querySelectorAll('.step-label').forEach(l => {
    l.classList.toggle('active', parseInt(l.dataset.step) === n);
  });
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ── BMI
function calcBMI() {
  const h = parseFloat(document.getElementById('height').value) || 170;
  const w = parseFloat(document.getElementById('weight').value) || 70;
  const bmi = w / ((h / 100) ** 2);
  document.getElementById('bmiVal').textContent = bmi.toFixed(1);
  const tag = document.getElementById('bmiTag');
  if (bmi < 18.5)      { tag.textContent = 'Underweight'; tag.className = 'bmi-tag warn'; }
  else if (bmi < 25)   { tag.textContent = 'Normal';      tag.className = 'bmi-tag'; }
  else if (bmi < 30)   { tag.textContent = 'Overweight';  tag.className = 'bmi-tag warn'; }
  else                 { tag.textContent = 'Obese';        tag.className = 'bmi-tag danger'; }
}

// ── GENDER TOGGLE
document.querySelectorAll('.gender-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.gender-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById('gender').value = btn.dataset.val;
  });
});

// ── TOGGLE GROUPS
function initToggleGroup(groupId, hiddenId) {
  document.getElementById(groupId).querySelectorAll('.tog').forEach(btn => {
    btn.addEventListener('click', () => {
      document.getElementById(groupId).querySelectorAll('.tog').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      document.getElementById(hiddenId).value = btn.dataset.val;
    });
  });
}
initToggleGroup('smokingGroup', 'smoking');
initToggleGroup('alcoholGroup', 'alcohol');
initToggleGroup('exerciseGroup', 'exercise');

// ── VITAL INDICATORS
const VITAL_CFG = {
  temp: { min: 35, max: 42, low: 36.1, high: 37.2 },
  hr:   { min: 30, max: 200, low: 60, high: 100 },
  o2:   { min: 50, max: 100, low: 95, high: 100 },
};

function updateVital(key, val) {
  val = parseFloat(val);
  const cfg = VITAL_CFG[key];
  if (!cfg) return;
  const pct = Math.min(100, Math.max(0, ((val - cfg.min) / (cfg.max - cfg.min)) * 100));
  const fill  = document.getElementById('vfill-' + key);
  const badge = document.getElementById('vstatus-' + key);
  const card  = document.getElementById('vcard-' + key);
  let status = 'Normal', color = 'var(--success)', cls = '';
  if (key === 'o2') {
    if (val < 90)      { status = 'Critical'; color = 'var(--danger)';  cls = 'abnormal'; }
    else if (val < 95) { status = 'Low';      color = 'var(--warning)'; cls = 'warning'; }
  } else if (key === 'temp') {
    if (val >= 39.5)      { status = 'High Fever'; color = 'var(--danger)';  cls = 'abnormal'; }
    else if (val >= 38.5) { status = 'Fever';      color = 'var(--warning)'; cls = 'warning'; }
    else if (val >= 37.3) { status = 'Elevated';   color = 'var(--warning)'; cls = 'warning'; }
    else if (val < 36.1)  { status = 'Low';        color = 'var(--warning)'; cls = 'warning'; }
  } else if (key === 'hr') {
    if (val > 130 || val < 40)    { status = 'Critical'; color = 'var(--danger)';  cls = 'abnormal'; }
    else if (val > 100 || val < 60) { status = 'Abnormal'; color = 'var(--warning)'; cls = 'warning'; }
  }
  if (fill)  { fill.style.width = pct + '%'; fill.style.background = color; }
  if (badge) { badge.textContent = status; badge.className = 'vital-status-badge' + (cls ? ' ' + cls : ''); }
  if (card)  { card.className = 'vital-card' + (cls ? ' ' + cls : ''); }
}
updateVital('temp', 37.0);
updateVital('hr', 75);
updateVital('o2', 98);

// ── SYMPTOM SEARCH
document.getElementById('symptomSearch').addEventListener('input', function () {
  const q = this.value.toLowerCase().trim();
  document.querySelectorAll('.pill').forEach(p => {
    const t = p.dataset.sym.replace(/_/g, ' ');
    p.classList.toggle('hidden', q !== '' && !t.includes(q));
  });
});

// ── CATEGORY FILTER
document.getElementById('catBar').querySelectorAll('.cat-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.getElementById('catBar').querySelectorAll('.cat-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const cat = btn.dataset.cat;
    document.querySelectorAll('.pill').forEach(p => {
      p.classList.toggle('hidden', cat !== 'all' && p.dataset.cat !== cat);
    });
  });
});

// ── SELECTED COUNT
document.getElementById('symptomPills').addEventListener('change', () => {
  const n = document.querySelectorAll('input[name="symptom"]:checked').length;
  document.getElementById('selNum').textContent = n;
});
"""

with open(os.path.join(BASE, 'static', 'script.js'), 'w', encoding='utf-8') as f:
    f.write(JS)
print(f"JS part 1: {os.path.getsize(os.path.join(BASE,'static','script.js'))} bytes")
