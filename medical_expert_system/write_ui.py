"""Writes the full UI files for the Medical AI Expert System."""
import os

BASE = os.path.dirname(os.path.abspath(__file__))

# ── HTML ─────────────────────────────────────────────────────
HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1.0"/>
  <title>MedAI Diagnostics</title>
  <link rel="stylesheet" href="/static/style.css"/>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet"/>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>

<header class="header">
  <div class="header-inner">
    <div class="header-logo">
      <div class="logo-mark">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none">
          <rect x="10" y="3" width="4" height="18" rx="2" fill="white"/>
          <rect x="3" y="10" width="18" height="4" rx="2" fill="white"/>
        </svg>
      </div>
      <div>
        <h1 class="header-title">MedAI Diagnostics</h1>
        <p class="header-subtitle">AI-Powered Disease Prediction &amp; Risk Assessment</p>
      </div>
    </div>
    <div class="step-indicator" id="stepIndicator">
      <div class="step-dot active" data-step="1"><span>1</span></div>
      <div class="step-line"></div>
      <div class="step-dot" data-step="2"><span>2</span></div>
      <div class="step-line"></div>
      <div class="step-dot" data-step="3"><span>3</span></div>
      <div class="step-line"></div>
      <div class="step-dot" data-step="4"><span>4</span></div>
    </div>
  </div>
</header>

<main class="main">

  <div class="step-labels">
    <span class="step-label active" data-step="1">Patient Profile</span>
    <span class="step-label" data-step="2">Vital Signs</span>
    <span class="step-label" data-step="3">Symptoms</span>
    <span class="step-label" data-step="4">History &amp; Lifestyle</span>
  </div>

  <form id="diagnosisForm">

    <!-- STEP 1: PATIENT PROFILE -->
    <div class="step-panel active" id="step1">
      <div class="step-hero">
        <div class="step-hero-icon">👤</div>
        <h2 class="step-hero-title">Patient Profile</h2>
        <p class="step-hero-sub">Enter basic patient information to begin the assessment</p>
      </div>
      <div class="profile-grid">
        <div class="profile-avatar-card">
          <div class="avatar-circle">
            <svg width="52" height="52" viewBox="0 0 24 24" fill="none">
              <circle cx="12" cy="8" r="4" fill="#2563eb" opacity="0.8"/>
              <path d="M4 20c0-4 3.6-7 8-7s8 3 8 7" fill="#2563eb" opacity="0.4"/>
            </svg>
          </div>
          <div class="field-full">
            <label class="field-label">Full Name</label>
            <input class="field-input" type="text" id="patientName" placeholder="Enter patient name"/>
          </div>
          <div class="field-full">
            <label class="field-label">Gender</label>
            <div class="gender-toggle">
              <button type="button" class="gender-btn active" data-val="male">&#9794; Male</button>
              <button type="button" class="gender-btn" data-val="female">&#9792; Female</button>
              <button type="button" class="gender-btn" data-val="other">Other</button>
            </div>
            <input type="hidden" id="gender" value="male"/>
          </div>
        </div>
        <div class="profile-fields-card">
          <div class="fields-2col">
            <div class="field-group">
              <label class="field-label">Age <span class="req">*</span></label>
              <div class="field-unit-wrap">
                <input class="field-input" type="number" id="age" value="35" min="1" max="120" required/>
                <span class="field-unit">yrs</span>
              </div>
            </div>
            <div class="field-group">
              <label class="field-label">Height</label>
              <div class="field-unit-wrap">
                <input class="field-input" type="number" id="height" value="170" min="50" max="250" oninput="calcBMI()"/>
                <span class="field-unit">cm</span>
              </div>
            </div>
            <div class="field-group">
              <label class="field-label">Weight</label>
              <div class="field-unit-wrap">
                <input class="field-input" type="number" id="weight" value="70" min="10" max="300" oninput="calcBMI()"/>
                <span class="field-unit">kg</span>
              </div>
            </div>
            <div class="field-group">
              <label class="field-label">BMI</label>
              <div class="bmi-display">
                <span id="bmiVal">24.2</span>
                <span class="bmi-tag" id="bmiTag">Normal</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="step-nav">
        <div></div>
        <button type="button" class="btn-next" onclick="goStep(2)">Next: Vital Signs <span class="btn-arrow">&#8594;</span></button>
      </div>
    </div>

    <!-- STEP 2: VITALS -->
    <div class="step-panel" id="step2">
      <div class="step-hero">
        <div class="step-hero-icon">&#128152;</div>
        <h2 class="step-hero-title">Vital Signs</h2>
        <p class="step-hero-sub">Enter current measurements — status indicators update in real time</p>
      </div>
      <div class="vitals-grid">
        <div class="vital-card" id="vcard-temp">
          <div class="vital-top">
            <span class="vital-emoji">&#127777;&#65039;</span>
            <div class="vital-meta">
              <div class="vital-name">Body Temperature</div>
              <div class="vital-range">Normal: 36.1 – 37.2&#176;C</div>
            </div>
            <div class="vital-status-badge" id="vstatus-temp">Normal</div>
          </div>
          <div class="vital-input-row">
            <input class="vital-input" type="number" id="temperature" value="37.0" step="0.1" min="35" max="42" oninput="updateVital('temp',this.value)"/>
            <span class="vital-unit">&#176;C</span>
          </div>
          <div class="vital-track"><div class="vital-fill" id="vfill-temp"></div></div>
        </div>
        <div class="vital-card" id="vcard-hr">
          <div class="vital-top">
            <span class="vital-emoji">&#10084;&#65039;</span>
            <div class="vital-meta">
              <div class="vital-name">Heart Rate</div>
              <div class="vital-range">Normal: 60 – 100 bpm</div>
            </div>
            <div class="vital-status-badge" id="vstatus-hr">Normal</div>
          </div>
          <div class="vital-input-row">
            <input class="vital-input" type="number" id="heartRate" value="75" min="30" max="200" oninput="updateVital('hr',this.value)"/>
            <span class="vital-unit">bpm</span>
          </div>
          <div class="vital-track"><div class="vital-fill" id="vfill-hr"></div></div>
        </div>
        <div class="vital-card" id="vcard-o2">
          <div class="vital-top">
            <span class="vital-emoji">&#129754;</span>
            <div class="vital-meta">
              <div class="vital-name">Oxygen Saturation</div>
              <div class="vital-range">Normal: 95 – 100%</div>
            </div>
            <div class="vital-status-badge" id="vstatus-o2">Normal</div>
          </div>
          <div class="vital-input-row">
            <input class="vital-input" type="number" id="oxygenSat" value="98" min="50" max="100" oninput="updateVital('o2',this.value)"/>
            <span class="vital-unit">%</span>
          </div>
          <div class="vital-track"><div class="vital-fill" id="vfill-o2"></div></div>
        </div>
        <div class="vital-card" id="vcard-bp">
          <div class="vital-top">
            <span class="vital-emoji">&#129978;</span>
            <div class="vital-meta">
              <div class="vital-name">Blood Pressure</div>
              <div class="vital-range">Normal: 90/60 – 120/80</div>
            </div>
            <div class="vital-status-badge" id="vstatus-bp">Normal</div>
          </div>
          <div class="vital-input-row">
            <input class="vital-input" type="text" id="bloodPressure" value="120/80" placeholder="120/80"/>
            <span class="vital-unit">mmHg</span>
          </div>
          <div class="vital-track"><div class="vital-fill" id="vfill-bp" style="width:55%;background:var(--success)"></div></div>
        </div>
      </div>
      <div class="step-nav">
        <button type="button" class="btn-back" onclick="goStep(1)"><span class="btn-arrow">&#8592;</span> Back</button>
        <button type="button" class="btn-next" onclick="goStep(3)">Next: Symptoms <span class="btn-arrow">&#8594;</span></button>
      </div>
    </div>

    <!-- STEP 3: SYMPTOMS -->
    <div class="step-panel" id="step3">
      <div class="step-hero">
        <div class="step-hero-icon">&#129514;</div>
        <h2 class="step-hero-title">Symptom Selector</h2>
        <p class="step-hero-sub">Tap to select all symptoms the patient is currently experiencing</p>
      </div>
      <div class="symptom-toolbar">
        <div class="sym-search-wrap">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="2.5"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
          <input type="text" id="symptomSearch" class="sym-search" placeholder="Search symptoms..."/>
        </div>
        <div class="cat-bar" id="catBar">
          <button type="button" class="cat-btn active" data-cat="all">All</button>
          <button type="button" class="cat-btn" data-cat="general">&#9889; General</button>
          <button type="button" class="cat-btn" data-cat="respiratory">&#129754; Respiratory</button>
          <button type="button" class="cat-btn" data-cat="digestive">Digestive</button>
          <button type="button" class="cat-btn" data-cat="neurological">&#129504; Neuro</button>
          <button type="button" class="cat-btn" data-cat="cardiovascular">&#10084; Cardio</button>
          <button type="button" class="cat-btn" data-cat="skin">&#129657; Skin</button>
        </div>
      </div>
      <div class="sel-count" id="selectedCount"><span id="selNum">0</span> symptoms selected</div>
      <div class="pills-grid" id="symptomPills">
"""

# Inject symptoms
SYMPTOMS = [
    ('fever','general'),('cough','respiratory'),('fatigue','general'),
    ('shortness_of_breath','respiratory'),('chest_pain','cardiovascular'),
    ('headache','neurological'),('body_aches','general'),('sore_throat','respiratory'),
    ('runny_nose','respiratory'),('nausea','digestive'),('vomiting','digestive'),
    ('diarrhea','digestive'),('abdominal_pain','digestive'),('loss_of_appetite','digestive'),
    ('weight_loss','general'),('night_sweats','general'),('chills','general'),
    ('rash','skin'),('joint_pain','general'),('muscle_pain','general'),
    ('dizziness','neurological'),('confusion','neurological'),('loss_of_taste','neurological'),
    ('loss_of_smell','neurological'),('sneezing','respiratory'),('watery_eyes','general'),
    ('itchy_eyes','general'),('skin_redness','skin'),('swelling','general'),
    ('bleeding_gums','general'),('eye_pain','neurological'),('back_pain','general'),
    ('neck_stiffness','neurological'),('frequent_urination','general'),
    ('excessive_thirst','general'),('blurred_vision','neurological'),
    ('slow_healing','skin'),('numbness','neurological'),('tingling','neurological'),
    ('palpitations','cardiovascular'),('irregular_heartbeat','cardiovascular'),
    ('swollen_lymph_nodes','general'),('difficulty_swallowing','respiratory'),
    ('hoarseness','respiratory'),('wheezing','respiratory'),('productive_cough','respiratory'),
    ('blood_in_sputum','respiratory'),('pale_skin','skin'),('jaundice','skin'),
    ('dark_urine','digestive'),('clay_colored_stool','digestive'),('bloating','digestive'),
    ('heartburn','digestive'),('constipation','digestive'),('eye_redness','general'),
    ('photophobia','neurological'),('stiff_joints','general'),('dry_skin','skin'),
    ('hair_loss','skin'),('cold_intolerance','general'),
]

for sym, cat in SYMPTOMS:
    label = sym.replace('_', ' ').title()
    HTML += f'        <label class="pill" data-cat="{cat}" data-sym="{sym}"><input type="checkbox" name="symptom" value="{sym}"/><span>{label}</span></label>\n'

HTML += r"""      </div>
      <div class="step-nav">
        <button type="button" class="btn-back" onclick="goStep(2)"><span class="btn-arrow">&#8592;</span> Back</button>
        <button type="button" class="btn-next" onclick="goStep(4)">Next: History <span class="btn-arrow">&#8594;</span></button>
      </div>
    </div>

    <!-- STEP 4: HISTORY & LIFESTYLE -->
    <div class="step-panel" id="step4">
      <div class="step-hero">
        <div class="step-hero-icon">&#128203;</div>
        <h2 class="step-hero-title">History &amp; Lifestyle</h2>
        <p class="step-hero-sub">Medical background and lifestyle factors refine the risk assessment</p>
      </div>
      <div class="history-grid">
        <div class="hcard">
          <div class="hcard-title">&#127973; Medical History</div>
          <div class="pill-toggles">
            <label class="pill-toggle"><input type="checkbox" name="medHistory" value="diabetes"/><span>Diabetes</span></label>
            <label class="pill-toggle"><input type="checkbox" name="medHistory" value="hypertension"/><span>Hypertension</span></label>
            <label class="pill-toggle"><input type="checkbox" name="medHistory" value="asthma"/><span>Asthma</span></label>
            <label class="pill-toggle"><input type="checkbox" name="medHistory" value="heart_disease"/><span>Heart Disease</span></label>
            <label class="pill-toggle"><input type="checkbox" name="medHistory" value="lung_disease"/><span>Lung Disease</span></label>
            <label class="pill-toggle"><input type="checkbox" name="medHistory" value="kidney_disease"/><span>Kidney Disease</span></label>
            <label class="pill-toggle"><input type="checkbox" name="medHistory" value="liver_disease"/><span>Liver Disease</span></label>
            <label class="pill-toggle"><input type="checkbox" name="medHistory" value="cancer"/><span>Cancer</span></label>
          </div>
        </div>
        <div class="hcard">
          <div class="hcard-title">&#128106; Family History</div>
          <div class="pill-toggles">
            <label class="pill-toggle"><input type="checkbox" name="famHistory" value="diabetes"/><span>Diabetes</span></label>
            <label class="pill-toggle"><input type="checkbox" name="famHistory" value="heart_disease"/><span>Heart Disease</span></label>
            <label class="pill-toggle"><input type="checkbox" name="famHistory" value="hypertension"/><span>Hypertension</span></label>
            <label class="pill-toggle"><input type="checkbox" name="famHistory" value="cancer"/><span>Cancer</span></label>
            <label class="pill-toggle"><input type="checkbox" name="famHistory" value="stroke"/><span>Stroke</span></label>
          </div>
        </div>
        <div class="hcard">
          <div class="hcard-title">&#128684; Smoking</div>
          <div class="toggle-row" id="smokingGroup">
            <button type="button" class="tog active" data-val="none">None</button>
            <button type="button" class="tog" data-val="former">Former</button>
            <button type="button" class="tog" data-val="light">Light</button>
            <button type="button" class="tog" data-val="heavy">Heavy</button>
          </div>
          <input type="hidden" id="smoking" value="none"/>
        </div>
        <div class="hcard">
          <div class="hcard-title">&#127863; Alcohol</div>
          <div class="toggle-row" id="alcoholGroup">
            <button type="button" class="tog active" data-val="none">None</button>
            <button type="button" class="tog" data-val="occasional">Occasional</button>
            <button type="button" class="tog" data-val="moderate">Moderate</button>
            <button type="button" class="tog" data-val="heavy">Heavy</button>
          </div>
          <input type="hidden" id="alcohol" value="none"/>
        </div>
        <div class="hcard">
          <div class="hcard-title">&#127939; Exercise</div>
          <div class="toggle-row" id="exerciseGroup">
            <button type="button" class="tog active" data-val="daily">Daily</button>
            <button type="button" class="tog" data-val="weekly">Weekly</button>
            <button type="button" class="tog" data-val="rarely">Rarely</button>
            <button type="button" class="tog" data-val="never">Never</button>
          </div>
          <input type="hidden" id="exercise" value="daily"/>
        </div>
        <div class="hcard">
          <div class="hcard-title">&#128564; Sleep Duration</div>
          <input type="range" id="sleepRange" min="1" max="12" value="7" class="sleep-slider" oninput="document.getElementById('sleepVal').textContent=this.value;document.getElementById('sleep').value=this.value"/>
          <div class="sleep-display"><span id="sleepVal">7</span> hrs / night</div>
          <input type="hidden" id="sleep" value="7"/>
        </div>
      </div>

      <div class="predict-section">
        <button type="submit" class="btn-predict" id="predictBtn">
          <span id="btnText">&#128300; Run AI Diagnosis</span>
          <span id="btnLoader" class="hidden"><span class="spinner"></span> Analyzing...</span>
        </button>
        <p class="predict-note">Powered by Prolog inference engine + weighted symptom analysis</p>
      </div>
      <div class="step-nav" style="margin-top:1rem">
        <button type="button" class="btn-back" onclick="goStep(3)"><span class="btn-arrow">&#8592;</span> Back</button>
        <div></div>
      </div>
    </div>

  </form>

  <div id="errorMsg" class="error-msg hidden"></div>

  <!-- RESULTS -->
  <div id="resultsSection" class="hidden">
    <div class="results-banner">
      <div class="results-banner-left">
        <div class="results-icon">&#129516;</div>
        <div>
          <h2 class="results-title">Diagnosis Complete</h2>
          <p class="results-sub">AI analysis finished — review your results below</p>
        </div>
      </div>
      <div class="results-banner-right">
        <span class="engine-pill" id="engineBadge"></span>
        <button class="btn-new" onclick="resetForm()">+ New Assessment</button>
      </div>
    </div>

    <div class="results-grid-3">
      <div class="rcard primary-rcard">
        <div class="rcard-label">Primary Diagnosis</div>
        <div class="primary-disease" id="primaryDiseaseName"></div>
        <div class="primary-desc" id="primaryDiseaseDesc"></div>
        <div class="conf-row"><span class="conf-label">Confidence</span><span class="conf-val" id="confidenceValue"></span></div>
        <div class="conf-track"><div class="conf-fill" id="confidenceBar"></div></div>
      </div>
      <div class="rcard risk-rcard">
        <div class="rcard-label">Risk Level</div>
        <div class="risk-ring-wrap">
          <svg class="ring-svg" viewBox="0 0 120 120">
            <circle cx="60" cy="60" r="50" fill="none" stroke="#e2e8f0" stroke-width="10"/>
            <circle cx="60" cy="60" r="50" fill="none" stroke-width="10" stroke-linecap="round"
              stroke-dasharray="314" stroke-dashoffset="314" id="riskArc" transform="rotate(-90 60 60)"/>
          </svg>
          <div class="ring-inner"><div class="ring-pct" id="riskPct">0%</div><div class="ring-label" id="riskLvlText">—</div></div>
        </div>
        <div class="risk-exps" id="riskExplanations"></div>
      </div>
      <div class="rcard health-rcard">
        <div class="rcard-label">Health Score</div>
        <div class="risk-ring-wrap">
          <svg class="ring-svg" viewBox="0 0 120 120">
            <circle cx="60" cy="60" r="50" fill="none" stroke="#e2e8f0" stroke-width="10"/>
            <circle cx="60" cy="60" r="50" fill="none" stroke="#10b981" stroke-width="10"
              stroke-linecap="round" stroke-dasharray="314" stroke-dashoffset="314"
              id="healthArc" transform="rotate(-90 60 60)"/>
          </svg>
          <div class="ring-inner"><div class="ring-pct" id="healthScoreVal">--</div><div class="ring-label">/100</div></div>
        </div>
        <div class="health-status" id="healthScoreLabel"></div>
      </div>
    </div>

    <div class="results-grid-2">
      <div class="rcard">
        <div class="rcard-header"><span class="rcard-icon">&#128202;</span><span class="rcard-title">Disease Probability</span></div>
        <div class="chart-wrap"><canvas id="diseaseChart"></canvas></div>
      </div>
      <div class="rcard">
        <div class="rcard-header"><span class="rcard-icon">&#129504;</span><span class="rcard-title">Why This Prediction?</span></div>
        <ul class="exp-list" id="explanationList"></ul>
      </div>
    </div>

    <div class="rcard">
      <div class="rcard-header"><span class="rcard-icon">&#127942;</span><span class="rcard-title">Top Disease Predictions</span></div>
      <div class="top-grid" id="topDiseasesGrid"></div>
    </div>

    <div class="rcard">
      <div class="rcard-header"><span class="rcard-icon">&#128138;</span><span class="rcard-title">Clinical Recommendations</span></div>
      <div class="rec-grid" id="recommendationList"></div>
      <p class="disclaimer">&#9888;&#65039; This AI system is for educational purposes only. Always consult a qualified healthcare professional.</p>
    </div>
  </div>

</main>

<footer class="footer">
  <span>MedAI Diagnostics &mdash; Prolog Inference Engine + Python Flask</span>
  <span class="footer-sep">|</span>
  <span>For research &amp; educational use only</span>
</footer>

<script src="/static/script.js"></script>
</body>
</html>
"""

with open(os.path.join(BASE, 'templates', 'index.html'), 'w', encoding='utf-8') as f:
    f.write(HTML)
print(f"HTML: {os.path.getsize(os.path.join(BASE,'templates','index.html'))} bytes")
