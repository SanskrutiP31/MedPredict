import os
BASE = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(BASE, 'static', 'script.js')

JS2 = """
// ── COLLECT FORM DATA
function collectFormData() {
  const symptoms = Array.from(
    document.querySelectorAll('input[name="symptom"]:checked')
  ).map(cb => cb.value);
  const medHistory = Array.from(
    document.querySelectorAll('input[name="medHistory"]:checked')
  ).map(cb => cb.value);
  const famHistory = Array.from(
    document.querySelectorAll('input[name="famHistory"]:checked')
  ).map(cb => cb.value);
  return {
    name:           document.getElementById('patientName').value || 'Patient',
    age:            parseInt(document.getElementById('age').value) || 30,
    gender:         document.getElementById('gender').value,
    height:         parseFloat(document.getElementById('height').value) || 170,
    weight:         parseFloat(document.getElementById('weight').value) || 70,
    temperature:    parseFloat(document.getElementById('temperature').value) || 37.0,
    heart_rate:     parseInt(document.getElementById('heartRate').value) || 75,
    oxygen_sat:     parseInt(document.getElementById('oxygenSat').value) || 98,
    blood_pressure: document.getElementById('bloodPressure').value || '120/80',
    smoking:        document.getElementById('smoking').value,
    alcohol:        document.getElementById('alcohol').value,
    exercise:       document.getElementById('exercise').value,
    sleep:          parseInt(document.getElementById('sleep').value) || 7,
    medical_history: medHistory,
    family_history:  famHistory,
    symptoms:        symptoms
  };
}

// ── FORM SUBMIT
document.getElementById('diagnosisForm').addEventListener('submit', async function (e) {
  e.preventDefault();
  const data = collectFormData();
  const errEl = document.getElementById('errorMsg');
  errEl.classList.add('hidden');

  if (data.symptoms.length === 0) {
    errEl.textContent = 'Please select at least one symptom in Step 3 before running the diagnosis.';
    errEl.classList.remove('hidden');
    goStep(3);
    return;
  }

  const btn = document.getElementById('predictBtn');
  document.getElementById('btnText').classList.add('hidden');
  document.getElementById('btnLoader').classList.remove('hidden');
  btn.disabled = true;
  document.getElementById('resultsSection').classList.add('hidden');

  try {
    const res = await fetch('/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    const result = await res.json();
    if (!res.ok || result.error) throw new Error(result.error || 'Prediction failed');
    renderResults(result);
  } catch (err) {
    errEl.textContent = 'Error: ' + err.message;
    errEl.classList.remove('hidden');
  } finally {
    document.getElementById('btnText').classList.remove('hidden');
    document.getElementById('btnLoader').classList.add('hidden');
    btn.disabled = false;
  }
});

// ── RESET
function resetForm() {
  document.getElementById('resultsSection').classList.add('hidden');
  document.getElementById('diagnosisForm').reset();
  document.querySelectorAll('.gender-btn').forEach((b,i) => b.classList.toggle('active', i===0));
  document.getElementById('gender').value = 'male';
  ['smokingGroup','alcoholGroup','exerciseGroup'].forEach(g => {
    const btns = document.getElementById(g).querySelectorAll('.tog');
    btns.forEach((b,i) => b.classList.toggle('active', i===0));
  });
  document.getElementById('smoking').value = 'none';
  document.getElementById('alcohol').value = 'none';
  document.getElementById('exercise').value = 'daily';
  document.getElementById('selNum').textContent = '0';
  if (diseaseChart) { diseaseChart.destroy(); diseaseChart = null; }
  goStep(1);
}
"""

with open(p, 'a', encoding='utf-8') as f:
    f.write(JS2)
print(f"JS part 2: {os.path.getsize(p)} bytes")
