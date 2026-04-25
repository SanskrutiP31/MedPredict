"""MedPredict - Flask Backend"""
import os, sys, io, re, subprocess
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
sys.path.insert(0, os.path.dirname(__file__))
from db import save_record, get_records, get_analytics, MONGO_AVAILABLE

# ── PROLOG SETUP ────────────────────────────────────────────
PROLOG_AVAILABLE = False
_prolog = None
PROLOG_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "prolog_engine"))

# Try swipl with full path fallback
SWIPL_CMD = "swipl"
for _p in ["swipl", r"C:\Program Files\swipl\bin\swipl.exe", r"C:\Program Files (x86)\swipl\bin\swipl.exe"]:
    try:
        r = subprocess.run([_p, "--version"], capture_output=True, timeout=5)
        if r.returncode == 0:
            SWIPL_CMD = _p
            break
    except Exception:
        continue

try:
    import os as _os
    _os.environ["PATH"] = r"C:\Program Files\swipl\bin;" + _os.environ.get("PATH","")
    from pyswip import Prolog
    _prolog = Prolog()
    for pl in ["knowledge_base.pl","diagnosis_engine.pl","risk_analysis.pl",
               "explanation_engine.pl","medicine.pl"]:
        _prolog.consult(os.path.join(PROLOG_DIR, pl).replace("\\", "/"))
    PROLOG_AVAILABLE = True
except Exception as _pe:
    print(f"[Prolog] Not available: {_pe}")

app = Flask(__name__,
    template_folder=os.path.join(os.path.dirname(__file__), "..", "templates"),
    static_folder=os.path.join(os.path.dirname(__file__), "..", "static"))

# ── KNOWLEDGE BASE ──────────────────────────────────────────
SEVERITY = {"none": 0, "mild": 1, "moderate": 2, "severe": 3}

DISEASE_WEIGHTS = {
    "flu":            {"fever":9,"cough":8,"body_aches":9,"fatigue":8,"headache":7,"chills":8,"sore_throat":6,"runny_nose":7,"sneezing":6,"loss_of_appetite":5},
    "covid19":        {"fever":8,"cough":9,"fatigue":8,"loss_of_taste":10,"loss_of_smell":10,"shortness_of_breath":9,"body_aches":7,"headache":6,"chills":7,"sore_throat":6},
    "dengue":         {"fever":10,"headache":9,"eye_pain":8,"joint_pain":9,"muscle_pain":9,"rash":8,"bleeding_gums":7,"nausea":6,"vomiting":6,"fatigue":7},
    "malaria":        {"fever":10,"chills":10,"headache":8,"nausea":7,"vomiting":7,"muscle_pain":7,"fatigue":8,"abdominal_pain":6,"diarrhea":5},
    "pneumonia":      {"fever":9,"cough":10,"shortness_of_breath":10,"chest_pain":9,"fatigue":8,"chills":7,"productive_cough":9,"confusion":6,"nausea":5},
    "asthma":         {"wheezing":10,"shortness_of_breath":10,"cough":8,"chest_pain":7,"fatigue":6},
    "bronchitis":     {"cough":10,"productive_cough":9,"fatigue":7,"shortness_of_breath":7,"chest_pain":6,"fever":5,"sore_throat":5,"wheezing":6},
    "tuberculosis":   {"cough":10,"blood_in_sputum":10,"night_sweats":9,"weight_loss":9,"fever":8,"fatigue":8,"chest_pain":7,"loss_of_appetite":7,"productive_cough":8},
    "diabetes":       {"frequent_urination":10,"excessive_thirst":10,"blurred_vision":8,"fatigue":7,"slow_healing":9,"numbness":7,"tingling":7,"weight_loss":6,"dry_skin":6},
    "hypertension":   {"headache":8,"dizziness":7,"chest_pain":7,"shortness_of_breath":6,"palpitations":7,"blurred_vision":6,"nausea":5},
    "heart_disease":  {"chest_pain":10,"shortness_of_breath":9,"palpitations":9,"irregular_heartbeat":10,"fatigue":8,"dizziness":7,"swelling":7,"nausea":5},
    "gastroenteritis":{"nausea":9,"vomiting":9,"diarrhea":10,"abdominal_pain":9,"fever":6,"fatigue":6,"loss_of_appetite":7,"bloating":6},
    "food_poisoning": {"nausea":10,"vomiting":10,"diarrhea":9,"abdominal_pain":9,"fever":7,"fatigue":6,"chills":5},
    "migraine":       {"headache":10,"nausea":8,"vomiting":7,"photophobia":9,"dizziness":7,"blurred_vision":6,"fatigue":5},
    "allergy":        {"sneezing":9,"runny_nose":9,"watery_eyes":9,"itchy_eyes":9,"rash":7,"skin_redness":7,"cough":6,"wheezing":6,"swelling":5},
    "skin_infection": {"rash":10,"skin_redness":10,"swelling":8,"fever":6},
    "dehydration":    {"dizziness":9,"fatigue":8,"excessive_thirst":10,"dark_urine":9,"dry_skin":7,"headache":6,"confusion":7,"constipation":5},
    "hepatitis":      {"jaundice":10,"dark_urine":9,"clay_colored_stool":9,"fatigue":8,"abdominal_pain":8,"nausea":7,"vomiting":6,"fever":6,"loss_of_appetite":7},
    "typhoid":        {"fever":10,"headache":8,"abdominal_pain":8,"constipation":7,"diarrhea":6,"fatigue":7,"loss_of_appetite":7,"rash":6,"night_sweats":6},
    "anemia":         {"fatigue":10,"pale_skin":10,"shortness_of_breath":8,"dizziness":8,"headache":6,"cold_intolerance":7,"hair_loss":6,"palpitations":7,"chest_pain":5},
}

DISEASE_DESCRIPTIONS = {
    "flu":"Influenza - viral respiratory illness with fever, cough, and body aches",
    "covid19":"COVID-19 - coronavirus infection affecting the respiratory system",
    "dengue":"Dengue fever - mosquito-borne viral disease with high fever and rash",
    "malaria":"Malaria - parasitic disease transmitted by mosquitoes causing cyclic fever",
    "pneumonia":"Pneumonia - lung infection causing inflammation and breathing difficulty",
    "asthma":"Asthma - chronic respiratory condition causing airway inflammation",
    "bronchitis":"Bronchitis - inflammation of bronchial tubes causing persistent cough",
    "tuberculosis":"Tuberculosis - bacterial lung infection with chronic cough and weight loss",
    "diabetes":"Diabetes - metabolic disorder affecting blood sugar regulation",
    "hypertension":"Hypertension - high blood pressure affecting cardiovascular system",
    "heart_disease":"Heart Disease - conditions affecting heart function and blood flow",
    "gastroenteritis":"Gastroenteritis - stomach and intestinal inflammation",
    "food_poisoning":"Food Poisoning - illness from contaminated food",
    "migraine":"Migraine - severe recurring headaches with neurological symptoms",
    "allergy":"Allergy - immune response to environmental or food triggers",
    "skin_infection":"Skin Infection - bacterial or fungal infection of skin tissue",
    "dehydration":"Dehydration - insufficient fluid levels affecting body function",
    "hepatitis":"Hepatitis - liver inflammation usually caused by viral infection",
    "typhoid":"Typhoid - bacterial infection causing sustained fever and GI symptoms",
    "anemia":"Anemia - low red blood cell count causing fatigue and weakness",
}

SERIOUS_DISEASES = {"pneumonia","tuberculosis","heart_disease","hepatitis","dengue",
                    "malaria","typhoid","covid19","diabetes","hypertension"}

# ── PYTHON FALLBACK ENGINE ──────────────────────────────────

def python_diagnose(symptom_severities: dict):
    """symptom_severities: {symptom: severity_int 0-3}"""
    scores = {}
    for disease, weights in DISEASE_WEIGHTS.items():
        raw = sum(weights.get(s, 0) * sev for s, sev in symptom_severities.items() if sev > 0)
        mx = sum(weights.values()) * 3  # max if all severe
        scores[disease] = (raw / mx * 100) if mx > 0 else 0
    scored = [(d, s) for d, s in scores.items() if s > 0]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored

def python_risk_score(data):
    score = 0
    age = data.get("age", 30); temp = data.get("temperature", 37.0)
    hr = data.get("heart_rate", 75); o2 = data.get("oxygen_sat", 98)
    smoking = data.get("smoking", "none"); alcohol = data.get("alcohol", "none")
    med = data.get("medical_history", []); fam = data.get("family_history", [])
    syms = list(data.get("symptom_severities", {}).keys())
    h = data.get("height", 170); w = data.get("weight", 70)
    score += [0,0,5,10,15,20,25,30][min(int(age//10), 7)]
    if temp < 37.5: score += 0
    elif temp < 38.5: score += 10
    elif temp < 39.5: score += 20
    else: score += 30
    if 60 <= hr <= 100: score += 0
    elif 50 <= hr <= 110: score += 10
    elif 40 <= hr <= 130: score += 20
    else: score += 30
    if o2 >= 95: score += 0
    elif o2 >= 90: score += 15
    elif o2 >= 85: score += 25
    else: score += 35
    score += {"none":0,"former":5,"light":10,"heavy":20}.get(smoking, 0)
    score += {"none":0,"occasional":5,"moderate":10,"heavy":20}.get(alcohol, 0)
    cr = {"diabetes":15,"hypertension":15,"heart_disease":20,"asthma":10,"lung_disease":15}
    for c in med: score += cr.get(c, 5)
    fr = {"diabetes":8,"heart_disease":10,"hypertension":8,"cancer":10}
    for c in fam: score += fr.get(c, 3)
    sv = {"shortness_of_breath":15,"chest_pain":20,"confusion":15,"blood_in_sputum":15,"irregular_heartbeat":20}
    for s in syms: score += sv.get(s, 2)
    try:
        bmi = w / ((h/100)**2)
        if bmi < 18.5: score += 5
        elif bmi < 25: score += 0
        elif bmi < 30: score += 5
        elif bmi < 35: score += 10
        else: score += 15
    except Exception: pass
    return score

def risk_label(s):
    if s <= 30: return "Low"
    if s <= 60: return "Moderate"
    if s <= 90: return "High"
    return "Critical"

def health_score(rs):
    return max(0, min(100, round(100 - rs * 0.5)))

def python_medicines(disease):
    OTC = {
        "flu":["Paracetamol (500mg) for fever","Cetirizine for runny nose","Vitamin C supplements","Throat lozenges"],
        "allergy":["Cetirizine (10mg) antihistamine","Loratadine as alternative","Nasal saline spray","Hydrocortisone cream for rash"],
        "migraine":["Ibuprofen (400mg) for pain","Paracetamol (500-1000mg)","Rest in dark quiet room","Cold compress on forehead"],
        "gastroenteritis":["ORS to prevent dehydration","Loperamide for diarrhea","Domperidone for nausea","Probiotics"],
        "food_poisoning":["ORS - primary treatment","Domperidone for nausea","Avoid solid food 24h","Stay hydrated"],
        "dehydration":["ORS immediately","Electrolyte drinks","Increase water intake","Coconut water"],
        "bronchitis":["Guaifenesin cough syrup","Paracetamol if fever","Steam inhalation 2-3x daily","Honey ginger tea"],
        "asthma":["Use prescribed inhaler as directed","Avoid known triggers","Keep rescue inhaler accessible"],
        "skin_infection":["Topical antibiotic cream","Antifungal cream if needed","Keep area clean and dry"],
        "anemia":["Iron supplements with Vitamin C","Folic acid supplements","Iron-rich diet"],
    }
    if disease in SERIOUS_DISEASES:
        return ["Immediate doctor consultation recommended. Do not self-medicate."]
    return OTC.get(disease, ["Consult a healthcare professional for proper diagnosis"])

def python_home_care(disease):
    CARE = {
        "flu":["Rest completely 3-5 days","Drink warm fluids: soup, herbal tea","Steam inhalation for congestion","Gargle warm salt water"],
        "covid19":["Isolate immediately","Monitor oxygen saturation","Stay well hydrated","Seek emergency care if O2 < 94%"],
        "dengue":["Complete bed rest","Drink plenty of fluids","Monitor platelet count daily","Avoid aspirin/ibuprofen"],
        "malaria":["Seek immediate medical treatment","Rest and stay hydrated","Use mosquito nets","Complete full antimalarial course"],
        "pneumonia":["Seek immediate medical attention","Rest in semi-upright position","Stay well hydrated","Monitor oxygen levels"],
        "gastroenteritis":["BRAT diet: Banana, Rice, Applesauce, Toast","Stay hydrated with ORS","Avoid dairy and spicy foods","Wash hands frequently"],
        "food_poisoning":["Stop solid food temporarily","Sip ORS slowly","Rest completely","Seek help if vomiting > 24h"],
        "migraine":["Rest in dark quiet room","Cold/warm compress on head","Stay hydrated","Avoid screens and bright lights"],
        "dehydration":["Drink ORS immediately","Sip fluids slowly and frequently","Rest in cool environment","Monitor urine color"],
        "allergy":["Identify and avoid allergen triggers","Keep windows closed during pollen season","Use air purifier","Shower after outdoor exposure"],
        "asthma":["Avoid triggers: dust, smoke, cold air","Keep rescue inhaler accessible","Practice breathing exercises","Monitor peak flow"],
        "diabetes":["Monitor blood glucose regularly","Follow prescribed diet","Exercise as advised","Take medications as prescribed"],
        "hypertension":["Reduce sodium intake","Exercise 30 min daily","Manage stress","Avoid alcohol and smoking"],
    }
    return CARE.get(disease, ["Rest adequately and stay hydrated","Eat light nutritious meals","Monitor symptoms","Consult a doctor"])

def python_emergency_check(data, symptoms):
    o2 = data.get("oxygen_sat", 98)
    hr = data.get("heart_rate", 75)
    temp = data.get("temperature", 37.0)
    if o2 < 90: return True
    if hr > 140 or hr < 40: return True
    if temp >= 40.0: return True
    if "chest_pain" in symptoms: return True
    if "irregular_heartbeat" in symptoms: return True
    if "confusion" in symptoms and "fever" in symptoms: return True
    return False

def python_clinical_recommendations(disease, risk_level):
    CLINICAL = {
        "flu":["Rest at home and avoid contact with others","Take antipyretics for fever management","Seek medical care if symptoms worsen after 5 days","Annual flu vaccination recommended for prevention"],
        "covid19":["Isolate immediately for at least 5 days","Notify close contacts","Seek emergency care if O2 drops below 94%","Follow local health authority guidelines"],
        "dengue":["Hospitalization may be required for severe cases","Daily platelet count monitoring essential","IV fluids if oral intake is insufficient","Avoid NSAIDs — use only Paracetamol for pain"],
        "malaria":["Immediate antimalarial drug therapy required","Blood smear test to confirm parasite type","Follow complete prescribed treatment course","Repeat blood test after treatment to confirm clearance"],
        "pneumonia":["Chest X-ray and sputum culture recommended","Antibiotic therapy as prescribed by doctor","Hospitalization if O2 < 92% or high fever persists","Pulmonologist referral for recurrent cases"],
        "tuberculosis":["DOTS (Directly Observed Treatment) for 6 months","Sputum AFB test and chest X-ray required","Isolate patient until non-infectious","Contact tracing for family members"],
        "diabetes":["HbA1c test every 3 months","Regular ophthalmology and nephrology checkups","Strict dietary management with dietitian guidance","Foot care and wound monitoring daily"],
        "hypertension":["Regular BP monitoring twice daily","Cardiology consultation if BP > 160/100","ECG and kidney function tests annually","Medication compliance is critical — do not skip doses"],
        "heart_disease":["Cardiology referral immediately","ECG, Echo, and stress test required","Cardiac rehabilitation program recommended","Emergency plan for chest pain episodes"],
        "hepatitis":["Liver function tests (LFT) every month","Gastroenterology/hepatology referral","Avoid alcohol completely","Vaccination for Hepatitis A and B if not immune"],
        "asthma":["Pulmonologist consultation for long-term management","Spirometry test to assess lung function","Avoid known triggers and allergens","Carry rescue inhaler at all times"],
        "bronchitis":["Chest X-ray to rule out pneumonia","Avoid smoking and secondhand smoke","Pulmonary function test if recurrent","Antibiotics only if bacterial infection confirmed"],
        "migraine":["Neurology consultation for chronic migraines","Keep a migraine diary to identify triggers","Preventive medication if attacks > 4/month","MRI if new onset or unusual pattern"],
        "anemia":["Complete blood count (CBC) and iron studies","Identify and treat underlying cause","Hematology referral for severe cases","Dietary counseling for iron-rich foods"],
        "gastroenteritis":["Stool culture if symptoms persist > 3 days","IV rehydration if unable to tolerate oral fluids","Avoid anti-diarrheal drugs in bacterial infections","Food safety review to prevent recurrence"],
        "food_poisoning":["Report to health authority if outbreak suspected","Stool culture for pathogen identification","IV fluids if severe dehydration","Avoid solid food until vomiting stops"],
        "dehydration":["IV fluid replacement if severe","Electrolyte panel blood test","Identify and treat underlying cause","Monitor urine output and kidney function"],
        "allergy":["Allergy skin test or RAST blood test","Immunotherapy (allergy shots) for long-term relief","Carry epinephrine auto-injector if anaphylaxis risk","Allergist consultation for management plan"],
        "skin_infection":["Wound swab culture for antibiotic sensitivity","Oral antibiotics if spreading beyond local area","Dermatology referral if not improving in 48h","Diabetic patients need urgent medical review"],
        "typhoid":["Blood culture (Widal test) for confirmation","Antibiotic therapy as per sensitivity report","Hospitalization for severe or complicated cases","Typhoid vaccination for household contacts"],
        "malaria":["Immediate antimalarial drug therapy required","Blood smear test to confirm parasite type","Follow complete prescribed treatment course","Repeat blood test after treatment to confirm clearance"],
    }
    RISK_CLINICAL = {
        "Critical":["URGENT: Go to emergency room immediately","Do not drive — call emergency services","Bring list of current medications","Continuous vital sign monitoring required"],
        "High":["Schedule urgent appointment within 24 hours","Bring all previous medical records","Do not delay — condition may worsen rapidly","Consider calling your doctor now"],
        "Moderate":["Book appointment with GP within 2-3 days","Prepare symptom history for the doctor","Monitor vitals daily until appointment","Avoid strenuous activity"],
        "Low":["Routine checkup within 1-2 weeks","Maintain healthy diet and exercise","Monitor symptoms — seek care if worsening","Preventive health screening recommended"],
    }
    disease_recs = CLINICAL.get(disease, ["Consult a qualified healthcare professional","Get proper diagnostic tests done","Follow prescribed treatment plan","Schedule follow-up appointments as advised"])
    risk_recs = RISK_CLINICAL.get(risk_level, [])
    return disease_recs + risk_recs


    o2 = data.get("oxygen_sat", 98)
    hr = data.get("heart_rate", 75)
    temp = data.get("temperature", 37.0)
    if o2 < 90: return True
    if hr > 140 or hr < 40: return True
    if temp >= 40.0: return True
    if "chest_pain" in symptoms: return True
    if "irregular_heartbeat" in symptoms: return True
    if "confusion" in symptoms and "fever" in symptoms: return True
    return False

def build_explanations(disease, symptom_severities, data):
    exps = []
    weights = DISEASE_WEIGHTS.get(disease, {})
    sev_labels = {1:"mild",2:"moderate",3:"severe"}
    matched = sorted(
        [(s, weights[s], sev) for s, sev in symptom_severities.items()
         if s in weights and weights[s] >= 7 and sev > 0],
        key=lambda x: x[1]*x[2], reverse=True
    )
    for sym, w, sev in matched[:5]:
        label = sev_labels.get(sev, "")
        exps.append(f"{sym.replace('_',' ').title()} ({label} severity) strongly matches {disease.replace('_',' ').title()}")
    temp = data.get("temperature", 37.0); o2 = data.get("oxygen_sat", 98)
    age = data.get("age", 30); smoking = data.get("smoking", "none")
    med = data.get("medical_history", [])
    if temp >= 38.5 and "fever" in weights: exps.append("High body temperature supports this diagnosis")
    if o2 < 95 and disease in ("pneumonia","covid19","asthma","heart_disease"): exps.append("Oxygen saturation below normal range")
    if age > 50 and disease in ("heart_disease","diabetes","hypertension","pneumonia"): exps.append("Age above 50 increases risk for this condition")
    if smoking in ("heavy","light") and disease in ("bronchitis","tuberculosis","pneumonia","asthma"): exps.append("Smoking history increases respiratory disease risk")
    if "diabetes" in med and disease == "heart_disease": exps.append("Diabetes history increases cardiovascular risk")
    return exps or ["Symptom pattern matches disease profile"]

def build_risk_explanations(rs, data):
    exps = []
    age = data.get("age", 30); temp = data.get("temperature", 37.0)
    hr = data.get("heart_rate", 75); o2 = data.get("oxygen_sat", 98)
    smoking = data.get("smoking", "none"); alcohol = data.get("alcohol", "none")
    med = data.get("medical_history", [])
    if rs > 90: exps.append("CRITICAL: Multiple severe risk factors present")
    elif rs > 60: exps.append("HIGH RISK: Significant risk factors detected")
    if age > 65: exps.append("Age above 65 is a significant risk factor")
    elif age > 50: exps.append("Age above 50 increases health risk")
    if temp >= 39.0: exps.append("High fever (39°C+) indicates serious infection")
    if hr > 110 or hr < 50: exps.append("Abnormal heart rate detected")
    if o2 < 95: exps.append("Low oxygen saturation is a critical warning sign")
    if smoking in ("heavy","light"): exps.append("Smoking increases risk of multiple diseases")
    if alcohol in ("heavy","moderate"): exps.append("Alcohol consumption contributes to health risks")
    if med: exps.append("Pre-existing medical conditions increase overall risk")
    return exps or ["Risk assessment based on provided data"]

# ── PROLOG WRAPPERS ─────────────────────────────────────────

def _pl_query(q, maxresult=1):
    try:
        return list(_prolog.query(q, maxresult=maxresult))
    except Exception:
        return []

def prolog_diagnose(symptom_severities):
    # Build weighted symptom list for Prolog: multiply base weight by severity
    sym_list = "[" + ",".join(s for s, v in symptom_severities.items() if v > 0) + "]"
    res = _pl_query(f"top_diagnoses({sym_list},3,Top),normalize_scores(Top,Norm)")
    if not res:
        return []
    out = []
    for item in res[0].get("Norm", []):
        try:
            out.append((str(item.args[0]), float(item.args[1])))
        except Exception:
            pass
    return out

def prolog_risk(data, symptoms):
    age = int(data.get("age", 30)); temp = float(data.get("temperature", 37.0))
    hr = int(data.get("heart_rate", 75)); o2 = int(data.get("oxygen_sat", 98))
    smoking = data.get("smoking", "none"); alcohol = data.get("alcohol", "none")
    med = "[" + ",".join(data.get("medical_history", [])) + "]"
    fam = "[" + ",".join(data.get("family_history", [])) + "]"
    syms = "[" + ",".join(symptoms) + "]"
    h = float(data.get("height", 170)); w = float(data.get("weight", 70))
    try: bmi = round(w / ((h/100)**2), 1)
    except: bmi = 22.0
    exercise = data.get("exercise", "daily")
    pd = f"patient({age},{temp},{hr},{o2},{smoking},{alcohol},{med},{fam},{syms},{bmi},{exercise})"
    res = _pl_query(f"calculate_risk_score({pd},RS),risk_level(RS,RL),health_score(RS,HS)")
    if res:
        try:
            return int(res[0]["RS"]), str(res[0]["RL"]), int(res[0]["HS"])
        except Exception:
            pass
    rs = min(python_risk_score(data), 200)
    return rs, risk_label(rs), health_score(rs)

def prolog_medicines(disease):
    res = _pl_query(f"otc_medicines({disease},Meds)")
    if res:
        try: return [str(m) for m in res[0].get("Meds", [])]
        except: pass
    return python_medicines(disease)

def prolog_home_care(disease):
    res = _pl_query(f"home_care({disease},Care)")
    if res:
        try: return [str(c) for c in res[0].get("Care", [])]
        except: pass
    return python_home_care(disease)

def prolog_emergency(data, symptoms):
    o2 = int(data.get("oxygen_sat", 98))
    hr = int(data.get("heart_rate", 75))
    temp = float(data.get("temperature", 37.0))
    syms = "[" + ",".join(symptoms) + "]"
    res = _pl_query(f"emergency_check(vitals({o2},{hr},{temp}),{syms},R)")
    if res:
        try: return str(res[0].get("R","false")) == "true"
        except: pass
    return python_emergency_check(data, symptoms)

def prolog_explain(disease, symptom_severities, data):
    symptoms = [s for s, v in symptom_severities.items() if v > 0]
    age = int(data.get("age", 30)); temp = float(data.get("temperature", 37.0))
    hr = int(data.get("heart_rate", 75)); o2 = int(data.get("oxygen_sat", 98))
    smoking = data.get("smoking", "none"); alcohol = data.get("alcohol", "none")
    med = "[" + ",".join(data.get("medical_history", [])) + "]"
    fam = "[" + ",".join(data.get("family_history", [])) + "]"
    syms = "[" + ",".join(symptoms) + "]"
    h = float(data.get("height", 170)); w = float(data.get("weight", 70))
    try: bmi = round(w / ((h/100)**2), 1)
    except: bmi = 22.0
    exercise = data.get("exercise", "daily")
    pd = f"patient({age},{temp},{hr},{o2},{smoking},{alcohol},{med},{fam},{syms},{bmi},{exercise})"
    res = _pl_query(f"explain_diagnosis({disease},{syms},{pd},Exps)")
    if res:
        try: return [str(e) for e in res[0].get("Exps", [])]
        except: pass
    return build_explanations(disease, symptom_severities, data)

# ── MAIN RUNNER ─────────────────────────────────────────────

def run_diagnosis(symptom_severities: dict, data: dict):
    symptoms = [s for s, v in symptom_severities.items() if v > 0]
    if not symptoms:
        return None

    if PROLOG_AVAILABLE:
        scored = prolog_diagnose(symptom_severities) or python_diagnose(symptom_severities)
    else:
        scored = python_diagnose(symptom_severities)

    if not scored:
        return None

    top3 = scored[:3]
    total = sum(s for _, s in top3)
    norm = [(d, round(s/total*100) if total > 0 else 0) for d, s in top3]
    primary = norm[0][0]

    if PROLOG_AVAILABLE:
        rs, rl, hs = prolog_risk(data, symptoms)
        exps = prolog_explain(primary, symptom_severities, data)
        risk_exps = build_risk_explanations(rs, data)
        medicines = prolog_medicines(primary)
        home_care = prolog_home_care(primary)
        is_emergency = prolog_emergency(data, symptoms)
        clinical_recs = python_clinical_recommendations(primary, rl)
    else:
        rs = min(python_risk_score(data), 200)
        rl = risk_label(rs); hs = health_score(rs)
        exps = build_explanations(primary, symptom_severities, data)
        risk_exps = build_risk_explanations(rs, data)
        medicines = python_medicines(primary)
        home_care = python_home_care(primary)
        is_emergency = python_emergency_check(data, symptoms)
        clinical_recs = python_clinical_recommendations(primary, rl)

    return {
        "engine": "SWI-Prolog" if PROLOG_AVAILABLE else "Python Inference Engine",
        "top_diseases": [{"name":d.replace("_"," ").title(),"key":d,"probability":p,
            "description":DISEASE_DESCRIPTIONS.get(d,""),
            "matched_symptoms":[s for s in symptoms if s in DISEASE_WEIGHTS.get(d,{})]}
            for d,p in norm],
        "primary_disease": {"name":primary.replace("_"," ").title(),"key":primary,
            "description":DISEASE_DESCRIPTIONS.get(primary,""),"confidence":norm[0][1],
            "matched_symptoms":[s for s in symptoms if s in DISEASE_WEIGHTS.get(primary,{})]},
        "risk": {"score":rs,"level":rl,"explanations":risk_exps},
        "health_score": hs,
        "explanations": exps,
        "medicines": medicines,
        "home_care": home_care,
        "recommendations": clinical_recs,
        "is_emergency": is_emergency,
        "is_serious": primary in SERIOUS_DISEASES,
        "symptoms_analyzed": symptoms,
        "symptom_severities": symptom_severities,
    }

# ── PDF REPORT ──────────────────────────────────────────────

def generate_pdf(data, result):
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.units import cm

        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=A4, topMargin=2*cm, bottomMargin=2*cm,
                                leftMargin=2*cm, rightMargin=2*cm)
        styles = getSampleStyleSheet()
        story = []

        title_style = ParagraphStyle("title", parent=styles["Title"],
                                     fontSize=22, textColor=colors.HexColor("#1e3a8a"), spaceAfter=6)
        h2 = ParagraphStyle("h2", parent=styles["Heading2"],
                             fontSize=13, textColor=colors.HexColor("#2563eb"), spaceBefore=14, spaceAfter=4)
        normal = styles["Normal"]

        story.append(Paragraph("MedPredict — Medical Report", title_style))
        story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", normal))
        story.append(Spacer(1, 0.4*cm))

        # Patient info
        story.append(Paragraph("Patient Information", h2))
        pinfo = [
            ["Name", data.get("name","—"), "Age", str(data.get("age","—"))],
            ["Gender", data.get("gender","—"), "Blood Group", data.get("blood_group","—")],
            ["Height", f"{data.get('height','—')} cm", "Weight", f"{data.get('weight','—')} kg"],
        ]
        t = Table(pinfo, colWidths=[3.5*cm,5*cm,3.5*cm,5*cm])
        t.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#f0f4ff")),
            ("GRID",(0,0),(-1,-1),0.5,colors.HexColor("#c7d2fe")),
            ("FONTNAME",(0,0),(0,-1),"Helvetica-Bold"),
            ("FONTNAME",(2,0),(2,-1),"Helvetica-Bold"),
            ("PADDING",(0,0),(-1,-1),6),
        ]))
        story.append(t); story.append(Spacer(1,0.3*cm))

        # Vitals
        story.append(Paragraph("Vital Signs", h2))
        vitals = [["Temperature","Heart Rate","Oxygen Sat","Blood Pressure"],
                  [f"{data.get('temperature','—')}°C", f"{data.get('heart_rate','—')} bpm",
                   f"{data.get('oxygen_sat','—')}%", data.get("blood_pressure","—")]]
        tv = Table(vitals, colWidths=[4.25*cm]*4)
        tv.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#1e3a8a")),
            ("TEXTCOLOR",(0,0),(-1,0),colors.white),
            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
            ("BACKGROUND",(0,1),(-1,-1),colors.HexColor("#eff6ff")),
            ("GRID",(0,0),(-1,-1),0.5,colors.HexColor("#bfdbfe")),
            ("ALIGN",(0,0),(-1,-1),"CENTER"),
            ("PADDING",(0,0),(-1,-1),7),
        ]))
        story.append(tv); story.append(Spacer(1,0.3*cm))

        # Diagnosis
        story.append(Paragraph("Diagnosis Results", h2))
        primary = result["primary_disease"]
        risk = result["risk"]
        diag_data = [
            ["Primary Diagnosis", primary["name"]],
            ["Confidence", f"{primary['confidence']}%"],
            ["Risk Level", risk["level"]],
            ["Risk Score", str(risk["score"])],
            ["Health Score", f"{result['health_score']}/100"],
        ]
        td = Table(diag_data, colWidths=[5*cm,12*cm])
        td.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(0,-1),colors.HexColor("#dbeafe")),
            ("FONTNAME",(0,0),(0,-1),"Helvetica-Bold"),
            ("GRID",(0,0),(-1,-1),0.5,colors.HexColor("#93c5fd")),
            ("PADDING",(0,0),(-1,-1),7),
        ]))
        story.append(td); story.append(Spacer(1,0.3*cm))

        # Top 3
        story.append(Paragraph("Top 3 Predictions", h2))
        for i, d in enumerate(result["top_diseases"], 1):
            story.append(Paragraph(f"{i}. {d['name']} — {d['probability']}%", normal))

        # Explanations
        story.append(Paragraph("Why This Prediction?", h2))
        for e in result.get("explanations", []):
            story.append(Paragraph(f"• {e}", normal))

        # Medicines
        story.append(Paragraph("Medicine Suggestions", h2))
        for m in result.get("medicines", []):
            story.append(Paragraph(f"• {m}", normal))

        # Home care
        story.append(Paragraph("Home Care Tips", h2))
        for c in result.get("home_care", []):
            story.append(Paragraph(f"• {c}", normal))

        if result.get("is_emergency"):
            story.append(Spacer(1,0.4*cm))
            story.append(Paragraph("⚠ EMERGENCY ALERT", ParagraphStyle("em",parent=styles["Normal"],
                fontSize=14,textColor=colors.red,fontName="Helvetica-Bold")))
            story.append(Paragraph("Seek immediate emergency medical attention.", normal))

        story.append(Spacer(1,0.5*cm))
        story.append(Paragraph("Disclaimer: This report is AI-generated for educational purposes only. Always consult a qualified healthcare professional.", 
                                ParagraphStyle("disc",parent=styles["Normal"],fontSize=8,textColor=colors.grey)))

        doc.build(story)
        buf.seek(0)
        return buf
    except Exception as e:
        return None

# ── ROUTES ──────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Build symptom_severities dict from incoming data
        # Accepts either: {"symptom_severities": {"fever": 2, ...}} or legacy {"symptoms": [...]}
        if "symptom_severities" in data:
            raw_sev = data["symptom_severities"]
            symptom_severities = {k.strip().lower().replace(" ","_"): int(v)
                                  for k, v in raw_sev.items() if int(v) > 0}
        else:
            syms = [s.strip().lower().replace(" ","_") for s in data.get("symptoms", []) if s.strip()]
            symptom_severities = {s: 2 for s in syms}  # default moderate

        if not symptom_severities:
            return jsonify({"error": "Please provide at least one symptom"}), 400

        data["symptom_severities"] = symptom_severities
        result = run_diagnosis(symptom_severities, data)
        if not result:
            return jsonify({"error": "No matching diseases found"}), 400

        # Save to MongoDB
        record = {
            "name": data.get("name", "Unknown"),
            "age": data.get("age"), "gender": data.get("gender"),
            "height": data.get("height"), "weight": data.get("weight"),
            "blood_group": data.get("blood_group"),
            "temperature": data.get("temperature"), "heart_rate": data.get("heart_rate"),
            "oxygen_sat": data.get("oxygen_sat"), "blood_pressure": data.get("blood_pressure"),
            "symptoms": list(symptom_severities.keys()),
            "symptom_severities": symptom_severities,
            "medical_history": data.get("medical_history", []),
            "family_history": data.get("family_history", []),
            "smoking": data.get("smoking"), "alcohol": data.get("alcohol"),
            "exercise": data.get("exercise"), "sleep": data.get("sleep"),
            "primary_diagnosis": result["primary_disease"]["key"],
            "confidence": result["primary_disease"]["confidence"],
            "risk_level": result["risk"]["level"],
            "risk_score": result["risk"]["score"],
            "health_score": result["health_score"],
            "is_emergency": result["is_emergency"],
            "engine": result["engine"],
        }
        mongo_id = save_record(record)
        result["record_id"] = mongo_id
        result["patient_data"] = data
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/records", methods=["GET"])
def records():
    search = request.args.get("search", "")
    return jsonify(get_records(search=search))

@app.route("/analytics", methods=["GET"])
def analytics():
    return jsonify(get_analytics())

@app.route("/download_pdf", methods=["POST"])
def download_pdf():
    try:
        payload = request.get_json()
        data = payload.get("patient_data", {})
        result = payload.get("result", {})
        buf = generate_pdf(data, result)
        if not buf:
            return jsonify({"error": "PDF generation failed"}), 500
        name = data.get("name", "patient").replace(" ", "_")
        filename = f"MedPredict_{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        return send_file(buf, mimetype="application/pdf",
                         as_attachment=True, download_name=filename)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health")
def health_check():
    return jsonify({
        "status": "ok",
        "engine": "SWI-Prolog" if PROLOG_AVAILABLE else "Python fallback",
        "database": "MongoDB" if MONGO_AVAILABLE else "unavailable"
    })

if __name__ == "__main__":
    print("=" * 50)
    print("  MedPredict - AI Medical Expert System")
    print(f"  Engine : {'SWI-Prolog' if PROLOG_AVAILABLE else 'Python Inference Engine'}")
    print(f"  DB     : {'MongoDB' if MONGO_AVAILABLE else 'Unavailable'}")
    print("  URL    : http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, host="0.0.0.0", port=5000)
