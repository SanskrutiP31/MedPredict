'use strict';

let diseaseChart = null;
let _lastResult = null;
let _lastData = null;

// ── SYMPTOM DATA ─────────────────────────────────────────────
const SYMPTOMS = [
  {key:"fever",label:"Fever",cat:"general"},
  {key:"cough",label:"Cough",cat:"respiratory"},
  {key:"fatigue",label:"Fatigue",cat:"general"},
  {key:"shortness_of_breath",label:"Shortness of Breath",cat:"respiratory"},
  {key:"chest_pain",label:"Chest Pain",cat:"cardiovascular"},
  {key:"headache",label:"Headache",cat:"neurological"},
  {key:"body_aches",label:"Body Aches",cat:"general"},
  {key:"sore_throat",label:"Sore Throat",cat:"respiratory"},
  {key:"runny_nose",label:"Runny Nose",cat:"respiratory"},
  {key:"nausea",label:"Nausea",cat:"digestive"},
  {key:"vomiting",label:"Vomiting",cat:"digestive"},
  {key:"diarrhea",label:"Diarrhea",cat:"digestive"},
  {key:"abdominal_pain",label:"Abdominal Pain",cat:"digestive"},
  {key:"loss_of_appetite",label:"Loss of Appetite",cat:"general"},
  {key:"weight_loss",label:"Weight Loss",cat:"general"},
  {key:"night_sweats",label:"Night Sweats",cat:"general"},
  {key:"chills",label:"Chills",cat:"general"},
  {key:"rash",label:"Rash",cat:"skin"},
  {key:"joint_pain",label:"Joint Pain",cat:"general"},
  {key:"muscle_pain",label:"Muscle Pain",cat:"general"},
  {key:"dizziness",label:"Dizziness",cat:"neurological"},
  {key:"confusion",label:"Confusion",cat:"neurological"},
  {key:"loss_of_taste",label:"Loss of Taste",cat:"neurological"},
  {key:"loss_of_smell",label:"Loss of Smell",cat:"neurological"},
  {key:"sneezing",label:"Sneezing",cat:"respiratory"},
  {key:"watery_eyes",label:"Watery Eyes",cat:"general"},
  {key:"itchy_eyes",label:"Itchy Eyes",cat:"general"},
  {key:"skin_redness",label:"Skin Redness",cat:"skin"},
  {key:"swelling",label:"Swelling",cat:"general"},
  {key:"bleeding_gums",label:"Bleeding Gums",cat:"general"},
  {key:"eye_pain",label:"Eye Pain",cat:"neurological"},
  {key:"back_pain",label:"Back Pain",cat:"general"},
  {key:"frequent_urination",label:"Frequent Urination",cat:"general"},
  {key:"excessive_thirst",label:"Excessive Thirst",cat:"general"},
  {key:"blurred_vision",label:"Blurred Vision",cat:"neurological"},
  {key:"slow_healing",label:"Slow Healing",cat:"skin"},
  {key:"numbness",label:"Numbness",cat:"neurological"},
  {key:"tingling",label:"Tingling",cat:"neurological"},
  {key:"palpitations",label:"Palpitations",cat:"cardiovascular"},
  {key:"irregular_heartbeat",label:"Irregular Heartbeat",cat:"cardiovascular"},
  {key:"wheezing",label:"Wheezing",cat:"respiratory"},
  {key:"productive_cough",label:"Productive Cough",cat:"respiratory"},
  {key:"blood_in_sputum",label:"Blood in Sputum",cat:"respiratory"},
  {key:"pale_skin",label:"Pale Skin",cat:"skin"},
  {key:"jaundice",label:"Jaundice",cat:"skin"},
  {key:"dark_urine",label:"Dark Urine",cat:"digestive"},
  {key:"clay_colored_stool",label:"Clay Colored Stool",cat:"digestive"},
  {key:"bloating",label:"Bloating",cat:"digestive"},
  {key:"constipation",label:"Constipation",cat:"digestive"},
  {key:"photophobia",label:"Photophobia",cat:"neurological"},
  {key:"dry_skin",label:"Dry Skin",cat:"skin"},
  {key:"hair_loss",label:"Hair Loss",cat:"skin"},
  {key:"cold_intolerance",label:"Cold Intolerance",cat:"general"},
  {key:"swollen_lymph_nodes",label:"Swollen Lymph Nodes",cat:"general"},
  {key:"hoarseness",label:"Hoarseness",cat:"respiratory"},
];

const SEV_LABELS = ["None","Mild","Moderate","Severe"];
const SEV_COLORS = ["#94a3b8","#22c55e","#f59e0b","#ef4444"];

// ── BUILD SYMPTOM LIST ────────────────────────────────────────
function buildSymptomList() {
  const container = document.getElementById('symptomsList');
  container.innerHTML = '';
  SYMPTOMS.forEach(sym => {
    const row = document.createElement('div');
    row.className = 'sym-row';
    row.dataset.cat = sym.cat;
    row.dataset.key = sym.key;
    row.innerHTML = `
      <div class="sym-name">${sym.label}</div>
      <div class="sev-btns">
        ${SEV_LABELS.map((l,i) => `<button type="button" class="sev-btn${i===0?' active':''}" data-val="${i}" style="${i===0?'border-color:'+SEV_COLORS[i]+';color:'+SEV_COLORS[i]:''}">${l}</button>`).join('')}
      </div>`;
    row.querySelectorAll('.sev-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        row.querySelectorAll('.sev-btn').forEach(b => {
          b.classList.remove('active');
          b.style.borderColor = ''; b.style.color = ''; b.style.background = '';
        });
        btn.classList.add('active');
        const v = parseInt(btn.dataset.val);
        btn.style.borderColor = SEV_COLORS[v];
        btn.style.color = v === 0 ? SEV_COLORS[v] : '#fff';
        btn.style.background = v === 0 ? '' : SEV_COLORS[v];
        updateSelCount();
      });
    });
    container.appendChild(row);
  });
}

function updateSelCount() {
  const n = document.querySelectorAll('.sym-row .sev-btn.active[data-val]:not([data-val="0"])').length;
  document.getElementById('selNum').textContent = n;
}

function getSymptomSeverities() {
  const result = {};
  document.querySelectorAll('.sym-row').forEach(row => {
    const active = row.querySelector('.sev-btn.active');
    if (active) {
      const v = parseInt(active.dataset.val);
      if (v > 0) result[row.dataset.key] = v;
    }
  });
  return result;
}

// ── STEP NAVIGATION ───────────────────────────────────────────
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

// ── GENDER TOGGLE ─────────────────────────────────────────────
document.querySelectorAll('.gender-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.gender-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById('gender').value = btn.dataset.val;
  });
});

// ── TOGGLE GROUPS ─────────────────────────────────────────────
function initToggleGroup(groupId, hiddenId) {
  document.getElementById(groupId).querySelectorAll('.tog').forEach(btn => {
    btn.addEventListener('click', () => {
      document.getElementById(groupId).querySelectorAll('.tog').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      document.getElementById(hiddenId).value = btn.dataset.val;
    });
  });
}
initToggleGroup('smokingGroup','smoking');
initToggleGroup('alcoholGroup','alcohol');
initToggleGroup('exerciseGroup','exercise');

// ── VITAL INDICATORS ──────────────────────────────────────────
const VITAL_CFG = {
  temp:{min:35,max:42,low:36.1,high:37.2},
  hr:{min:30,max:200,low:60,high:100},
  o2:{min:50,max:100,low:95,high:100},
};
function updateVital(key, val) {
  val = parseFloat(val);
  const cfg = VITAL_CFG[key]; if (!cfg) return;
  const pct = Math.min(100,Math.max(0,((val-cfg.min)/(cfg.max-cfg.min))*100));
  const fill=document.getElementById('vfill-'+key);
  const badge=document.getElementById('vstatus-'+key);
  const card=document.getElementById('vcard-'+key);
  let status='Normal',color='var(--success)',cls='';
  if(key==='o2'){if(val<90){status='Critical';color='var(--danger)';cls='abnormal';}else if(val<95){status='Low';color='var(--warning)';cls='warning';}}
  else if(key==='temp'){if(val>=39.5){status='High Fever';color='var(--danger)';cls='abnormal';}else if(val>=38.5){status='Fever';color='var(--warning)';cls='warning';}else if(val>=37.3){status='Elevated';color='var(--warning)';cls='warning';}else if(val<36.1){status='Low';color='var(--warning)';cls='warning';}}
  else if(key==='hr'){if(val>130||val<40){status='Critical';color='var(--danger)';cls='abnormal';}else if(val>100||val<60){status='Abnormal';color='var(--warning)';cls='warning';}}
  if(fill){fill.style.width=pct+'%';fill.style.background=color;}
  if(badge){badge.textContent=status;badge.className='vital-status-badge'+(cls?' '+cls:'');}
  if(card){card.className='vital-card'+(cls?' '+cls:'');}
}
updateVital('temp',37.0); updateVital('hr',75); updateVital('o2',98);

// ── SYMPTOM SEARCH & FILTER ───────────────────────────────────
document.getElementById('symptomSearch').addEventListener('input', function() {
  const q = this.value.toLowerCase().trim();
  document.querySelectorAll('.sym-row').forEach(r => {
    const t = r.dataset.key.replace(/_/g,' ');
    r.classList.toggle('hidden', q !== '' && !t.includes(q));
  });
});
document.getElementById('catBar').querySelectorAll('.cat-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.getElementById('catBar').querySelectorAll('.cat-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const cat = btn.dataset.cat;
    document.querySelectorAll('.sym-row').forEach(r => {
      r.classList.toggle('hidden', cat !== 'all' && r.dataset.cat !== cat);
    });
  });
});

// ── COLLECT FORM DATA ─────────────────────────────────────────
function collectFormData() {
  return {
    name: document.getElementById('patientName').value.trim(),
    age: parseInt(document.getElementById('age').value)||30,
    gender: document.getElementById('gender').value,
    height: parseFloat(document.getElementById('height').value)||170,
    weight: parseFloat(document.getElementById('weight').value)||70,
    blood_group: document.getElementById('bloodGroup').value,
    temperature: parseFloat(document.getElementById('temperature').value)||37.0,
    heart_rate: parseInt(document.getElementById('heartRate').value)||75,
    oxygen_sat: parseInt(document.getElementById('oxygenSat').value)||98,
    blood_pressure: document.getElementById('bloodPressure').value||'120/80',
    smoking: document.getElementById('smoking').value,
    alcohol: document.getElementById('alcohol').value,
    exercise: document.getElementById('exercise').value,
    sleep: parseInt(document.getElementById('sleep').value)||7,
    medical_history: Array.from(document.querySelectorAll('input[name="medHistory"]:checked')).map(c=>c.value),
    family_history: Array.from(document.querySelectorAll('input[name="famHistory"]:checked')).map(c=>c.value),
    symptom_severities: getSymptomSeverities(),
  };
}

// ── FORM SUBMIT ───────────────────────────────────────────────
document.getElementById('diagnosisForm').addEventListener('submit', async function(e) {
  e.preventDefault();
  const data = collectFormData();
  const errEl = document.getElementById('errorMsg');
  errEl.classList.add('hidden');

  if (!data.name) { errEl.textContent='Please enter the patient name.'; errEl.classList.remove('hidden'); goStep(1); return; }
  if (!data.age||data.age<1) { errEl.textContent='Please enter a valid age.'; errEl.classList.remove('hidden'); goStep(1); return; }
  if (Object.keys(data.symptom_severities).length === 0) {
    errEl.textContent='Please select at least one symptom with severity in Step 3.';
    errEl.classList.remove('hidden'); goStep(3); return;
  }

  const btn = document.getElementById('predictBtn');
  document.getElementById('btnText').classList.add('hidden');
  document.getElementById('btnLoader').classList.remove('hidden');
  btn.disabled = true;
  document.getElementById('resultsSection').classList.add('hidden');

  try {
    const res = await fetch('/predict', {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify(data)
    });
    const result = await res.json();
    if (!res.ok || result.error) throw new Error(result.error||'Prediction failed');
    _lastResult = result;
    _lastData = data;
    renderResults(result);
  } catch(err) {
    errEl.textContent = 'Error: ' + err.message;
    errEl.classList.remove('hidden');
  } finally {
    document.getElementById('btnText').classList.remove('hidden');
    document.getElementById('btnLoader').classList.add('hidden');
    btn.disabled = false;
  }
});

// ── RESET ─────────────────────────────────────────────────────
function resetForm() {
  document.getElementById('resultsSection').classList.add('hidden');
  document.getElementById('diagnosisForm').reset();
  document.querySelectorAll('.gender-btn').forEach((b,i)=>b.classList.toggle('active',i===0));
  document.getElementById('gender').value='male';
  ['smokingGroup','alcoholGroup','exerciseGroup'].forEach(g=>{
    const btns=document.getElementById(g).querySelectorAll('.tog');
    btns.forEach((b,i)=>b.classList.toggle('active',i===0));
  });
  document.getElementById('smoking').value='none';
  document.getElementById('alcohol').value='none';
  document.getElementById('exercise').value='daily';
  document.getElementById('selNum').textContent='0';
  // Reset all severity buttons to None
  document.querySelectorAll('.sym-row').forEach(row=>{
    row.querySelectorAll('.sev-btn').forEach((b,i)=>{
      b.classList.toggle('active',i===0);
      b.style.borderColor=''; b.style.color=''; b.style.background='';
    });
  });
  if(diseaseChart){diseaseChart.destroy();diseaseChart=null;}
  goStep(1);
}

// ── RENDER RESULTS ────────────────────────────────────────────
function renderResults(data) {
  // Emergency alert
  const emAlert = document.getElementById('emergencyAlert');
  if (data.is_emergency) {
    emAlert.classList.remove('hidden');
  } else {
    emAlert.classList.add('hidden');
  }

  const primary = data.primary_disease;
  document.getElementById('primaryDiseaseName').textContent = primary.name;
  document.getElementById('primaryDiseaseDesc').textContent = primary.description;
  document.getElementById('confidenceValue').textContent = primary.confidence + '%';
  setTimeout(()=>{ document.getElementById('confidenceBar').style.width = primary.confidence+'%'; },100);

  renderRisk(data.risk);
  renderHealthScore(data.health_score);
  renderChart(data.top_diseases);
  renderExpList('explanationList', data.explanations);
  renderTopDiseases(data.top_diseases);
  renderCareList('medicineList', data.medicines || []);
  renderCareList('homeCareList', data.home_care || []);

  const medDisc = document.getElementById('medDisclaimer');
  if (data.is_serious) {
    medDisc.textContent = '⚠ Serious condition detected. Do not self-medicate. Consult a doctor immediately.';
    medDisc.style.color = 'var(--danger)';
  } else {
    medDisc.textContent = 'These are general OTC suggestions only. Always consult a pharmacist or doctor.';
    medDisc.style.color = 'var(--muted)';
  }

  // Recommendations
  const recEl = document.getElementById('recommendationList');
  recEl.innerHTML = '';
  (data.recommendations || []).forEach((item,i)=>{
    const d = document.createElement('div');
    d.className='rec-item'; d.textContent=item;
    d.style.animationDelay=(i*0.07)+'s';
    recEl.appendChild(d);
  });

  const sec = document.getElementById('resultsSection');
  sec.classList.remove('hidden');
  setTimeout(()=>sec.scrollIntoView({behavior:'smooth',block:'start'}),100);
}

function renderRisk(risk) {
  const COLORS={Low:'#10b981',Moderate:'#f59e0b',High:'#ef4444',Critical:'#7c3aed'};
  const pct = Math.min((risk.score/150)*100,100);
  const color = COLORS[risk.level]||'#ef4444';
  const arc = document.getElementById('riskArc');
  arc.style.stroke = color;
  setTimeout(()=>{arc.style.strokeDashoffset=314-(pct/100)*314;arc.style.transition='stroke-dashoffset 1s ease';},100);
  document.getElementById('riskPct').textContent = Math.round(pct)+'%';
  document.getElementById('riskLvlText').textContent = risk.level;
  document.getElementById('riskLvlText').style.color = color;
  const exps = document.getElementById('riskExplanations');
  exps.innerHTML='';
  (risk.explanations||[]).slice(0,4).forEach(e=>{
    const d=document.createElement('div'); d.className='risk-exp-item'; d.textContent=e; exps.appendChild(d);
  });
}

function renderHealthScore(score) {
  const arc = document.getElementById('healthArc');
  setTimeout(()=>{arc.style.strokeDashoffset=314-(score/100)*314;arc.style.transition='stroke-dashoffset 1s ease';},200);
  document.getElementById('healthScoreVal').textContent=score;
  const label=document.getElementById('healthScoreLabel');
  let text='Good Health',color='#10b981';
  if(score<25){text='Critical';color='#7c3aed';}
  else if(score<50){text='Poor Health';color='#ef4444';}
  else if(score<75){text='Fair Health';color='#f59e0b';}
  label.textContent=text; label.style.color=color; arc.style.stroke=color;
}

function renderChart(diseases) {
  const ctx=document.getElementById('diseaseChart').getContext('2d');
  if(diseaseChart) diseaseChart.destroy();
  diseaseChart=new Chart(ctx,{
    type:'bar',
    data:{labels:diseases.map(d=>d.name),
      datasets:[{label:'Probability (%)',data:diseases.map(d=>d.probability),
        backgroundColor:['rgba(37,99,235,0.8)','rgba(124,58,237,0.8)','rgba(8,145,178,0.8)'],
        borderColor:['#2563eb','#7c3aed','#0891b2'],borderWidth:2,borderRadius:8,borderSkipped:false}]},
    options:{responsive:true,maintainAspectRatio:false,
      plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>' '+c.parsed.y+'% probability'}}},
      scales:{y:{beginAtZero:true,max:100,ticks:{callback:v=>v+'%',color:'#64748b'},grid:{color:'rgba(148,163,184,0.12)'}},
        x:{ticks:{color:'#64748b',font:{weight:'600'}},grid:{display:false}}},
      animation:{duration:900,easing:'easeOutQuart'}}
  });
}

function renderExpList(id, items) {
  const el=document.getElementById(id); el.innerHTML='';
  (items||[]).forEach((item,i)=>{
    const li=document.createElement('li'); li.textContent=item; li.style.animationDelay=(i*0.07)+'s'; el.appendChild(li);
  });
}

function renderCareList(id, items) {
  const el=document.getElementById(id); el.innerHTML='';
  (items||[]).forEach((item,i)=>{
    const d=document.createElement('div'); d.className='care-item'; d.textContent=item;
    d.style.animationDelay=(i*0.07)+'s'; el.appendChild(d);
  });
}

function renderTopDiseases(diseases) {
  const grid=document.getElementById('topDiseasesGrid'); grid.innerHTML='';
  const ranks=['#1 Prediction','#2 Prediction','#3 Prediction'];
  const bars=['bar-1','bar-2','bar-3'];
  diseases.forEach((d,i)=>{
    const tags=(d.matched_symptoms||[]).slice(0,4).map(s=>`<span class="sym-tag">${s.replace(/_/g,' ')}</span>`).join('');
    const card=document.createElement('div'); card.className='disease-card';
    card.innerHTML=`<div class="dc-rank">${ranks[i]||'#'+(i+1)}</div>
      <div class="dc-name">${d.name}</div><div class="dc-desc">${d.description}</div>
      <div class="dc-prob">${d.probability}%</div>
      <div class="dc-bar-wrap"><div class="dc-bar ${bars[i]||'bar-1'}" style="width:0" data-w="${d.probability}"></div></div>
      <div class="dc-tags">${tags}</div>`;
    grid.appendChild(card);
  });
  setTimeout(()=>{ document.querySelectorAll('.dc-bar').forEach(b=>{b.style.width=b.dataset.w+'%';}); },150);
}

// ── PDF DOWNLOAD ──────────────────────────────────────────────
async function downloadPDF() {
  if (!_lastResult || !_lastData) return;
  const btn = document.getElementById('btnPdf');
  btn.textContent = 'Generating...'; btn.disabled = true;
  try {
    const res = await fetch('/download_pdf', {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({patient_data: _lastData, result: _lastResult})
    });
    if (!res.ok) throw new Error('PDF failed');
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href=url; a.download=`MedPredict_Report.pdf`; a.click();
    URL.revokeObjectURL(url);
  } catch(e) {
    alert('PDF generation failed. Make sure reportlab is installed.');
  } finally {
    btn.innerHTML='<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg> Download PDF';
    btn.disabled = false;
  }
}

// ── INIT ──────────────────────────────────────────────────────
buildSymptomList();
