import os
BASE = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(BASE, 'static', 'script.js')

JS3 = """
// ── RENDER RESULTS
function renderResults(data) {
  document.getElementById('engineBadge').textContent = 'Engine: ' + data.engine;
  const primary = data.primary_disease;
  document.getElementById('primaryDiseaseName').textContent = primary.name;
  document.getElementById('primaryDiseaseDesc').textContent = primary.description;
  document.getElementById('confidenceValue').textContent = primary.confidence + '%';
  setTimeout(() => {
    document.getElementById('confidenceBar').style.width = primary.confidence + '%';
  }, 100);

  renderRisk(data.risk);
  renderHealthScore(data.health_score);
  renderChart(data.top_diseases);
  renderExpList('explanationList', data.explanations, 'exp-list');
  renderRecGrid(data.recommendations);
  renderTopDiseases(data.top_diseases);

  const sec = document.getElementById('resultsSection');
  sec.classList.remove('hidden');
  setTimeout(() => sec.scrollIntoView({ behavior: 'smooth', block: 'start' }), 100);
}

// ── RISK RING
function renderRisk(risk) {
  const COLORS = { Low: '#10b981', Moderate: '#f59e0b', High: '#ef4444', Critical: '#7c3aed' };
  const pct = Math.min((risk.score / 150) * 100, 100);
  const color = COLORS[risk.level] || '#ef4444';
  const arc = document.getElementById('riskArc');
  const offset = 314 - (pct / 100) * 314;
  arc.style.stroke = color;
  setTimeout(() => { arc.style.strokeDashoffset = offset; arc.style.transition = 'stroke-dashoffset 1s ease'; }, 100);
  document.getElementById('riskPct').textContent = Math.round(pct) + '%';
  document.getElementById('riskLvlText').textContent = risk.level;
  document.getElementById('riskLvlText').style.color = color;

  const exps = document.getElementById('riskExplanations');
  exps.innerHTML = '';
  (risk.explanations || []).slice(0, 4).forEach(e => {
    const d = document.createElement('div');
    d.className = 'risk-exp-item';
    d.textContent = e;
    exps.appendChild(d);
  });
}

// ── HEALTH RING
function renderHealthScore(score) {
  const arc = document.getElementById('healthArc');
  const offset = 314 - (score / 100) * 314;
  setTimeout(() => { arc.style.strokeDashoffset = offset; arc.style.transition = 'stroke-dashoffset 1s ease'; }, 200);
  document.getElementById('healthScoreVal').textContent = score;
  const label = document.getElementById('healthScoreLabel');
  let text = 'Good Health', color = '#10b981';
  if (score < 25)      { text = 'Critical';    color = '#7c3aed'; }
  else if (score < 50) { text = 'Poor Health'; color = '#ef4444'; }
  else if (score < 75) { text = 'Fair Health'; color = '#f59e0b'; }
  label.textContent = text;
  label.style.color = color;
  arc.style.stroke = color;
}

// ── CHART
function renderChart(diseases) {
  const ctx = document.getElementById('diseaseChart').getContext('2d');
  if (diseaseChart) diseaseChart.destroy();
  diseaseChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: diseases.map(d => d.name),
      datasets: [{
        label: 'Probability (%)',
        data: diseases.map(d => d.probability),
        backgroundColor: ['rgba(37,99,235,0.8)', 'rgba(124,58,237,0.8)', 'rgba(8,145,178,0.8)'],
        borderColor:     ['#2563eb', '#7c3aed', '#0891b2'],
        borderWidth: 2, borderRadius: 8, borderSkipped: false
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: { legend: { display: false }, tooltip: { callbacks: { label: c => ' ' + c.parsed.y + '% probability' } } },
      scales: {
        y: { beginAtZero: true, max: 100, ticks: { callback: v => v + '%', color: '#64748b' }, grid: { color: 'rgba(148,163,184,0.12)' } },
        x: { ticks: { color: '#64748b', font: { weight: '600' } }, grid: { display: false } }
      },
      animation: { duration: 900, easing: 'easeOutQuart' }
    }
  });
}

// ── EXPLANATION LIST
function renderExpList(id, items) {
  const el = document.getElementById(id);
  el.innerHTML = '';
  (items || []).forEach((item, i) => {
    const li = document.createElement('li');
    li.textContent = item;
    li.style.animationDelay = (i * 0.07) + 's';
    el.appendChild(li);
  });
}

// ── RECOMMENDATIONS GRID
function renderRecGrid(items) {
  const el = document.getElementById('recommendationList');
  el.innerHTML = '';
  (items || []).forEach((item, i) => {
    const d = document.createElement('div');
    d.className = 'rec-item';
    d.textContent = item;
    d.style.animationDelay = (i * 0.07) + 's';
    el.appendChild(d);
  });
}

// ── TOP DISEASES
function renderTopDiseases(diseases) {
  const grid = document.getElementById('topDiseasesGrid');
  grid.innerHTML = '';
  const ranks = ['#1 Prediction', '#2 Prediction', '#3 Prediction'];
  const bars  = ['bar-1', 'bar-2', 'bar-3'];
  diseases.forEach((d, i) => {
    const tags = (d.matched_symptoms || []).slice(0, 4)
      .map(s => '<span class="sym-tag">' + s.replace(/_/g, ' ') + '</span>').join('');
    const card = document.createElement('div');
    card.className = 'disease-card';
    card.innerHTML =
      '<div class="dc-rank">' + (ranks[i] || '#' + (i+1)) + '</div>' +
      '<div class="dc-name">' + d.name + '</div>' +
      '<div class="dc-desc">' + d.description + '</div>' +
      '<div class="dc-prob">' + d.probability + '%</div>' +
      '<div class="dc-bar-wrap"><div class="dc-bar ' + (bars[i]||'bar-1') + '" style="width:0" data-w="' + d.probability + '"></div></div>' +
      '<div class="dc-tags">' + tags + '</div>';
    grid.appendChild(card);
  });
  setTimeout(() => {
    document.querySelectorAll('.dc-bar').forEach(b => { b.style.width = b.dataset.w + '%'; });
  }, 150);
}
"""

with open(p, 'a', encoding='utf-8') as f:
    f.write(JS3)
print(f"JS final: {os.path.getsize(p)} bytes")
