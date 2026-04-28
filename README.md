# MedPredict — AI-Powered Medical Expert System

An intelligent disease prediction and risk assessment system built with Prolog inference engine, Python Flask, and MongoDB.

---

## Features

- **Symptom Severity Scoring** — Rate each symptom as None / Mild / Moderate / Severe for accurate diagnosis
- **Top 3 Disease Predictions** — Shows top 3 diseases with confidence percentages and probability chart
- **Prolog Inference Engine** — Core reasoning runs inside SWI-Prolog for expert-level diagnosis
- **Risk Assessment** — Multi-factor risk scoring based on vitals, age, lifestyle, and medical history
- **Explainable AI** — Clear reasons shown for every prediction
- **Medicine Suggestions** — OTC medicine recommendations for minor diseases
- **Home Care Tips** — Practical self-care advice per disease
- **Clinical Recommendations** — Doctor-level advice, required tests, and referrals
- **Emergency Alert** — Automatic warning for critical vitals or dangerous symptoms
- **Patient History Dashboard** — Analytics with charts and searchable patient records
- **PDF Report Download** — Full medical report downloadable after each diagnosis
- **MongoDB Atlas** — All diagnoses stored in cloud database

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML, CSS, JavaScript, Chart.js |
| Backend | Python Flask |
| Inference Engine | SWI-Prolog + pyswip |
| Database | MongoDB Atlas |
| PDF Generation | ReportLab |

---

## Project Structure

```
medical_expert_system/
├── backend/
│   ├── app.py              # Flask backend + Prolog wrappers
│   └── db.py               # MongoDB integration
├── prolog_engine/
│   ├── knowledge_base.pl   # 20 diseases, 60 symptoms, weights
│   ├── diagnosis_engine.pl # Symptom scoring and ranking
│   ├── risk_analysis.pl    # Multi-factor risk calculation
│   ├── explanation_engine.pl # Explainable AI rules
│   └── medicine.pl         # Medicine, home care, emergency rules
├── templates/
│   ├── index.html          # Main diagnosis form
│   └── dashboard.html      # Analytics dashboard
├── static/
│   ├── style.css
│   └── script.js
├── .env                    # MongoDB URI (not pushed to GitHub)
└── requirements.txt
```

---

## Installation

**1. Clone the repository**
```bash
git clone https://github.com/SanskrutiP31/MedPredict.git
cd MedPredict
```

**2. Install Python dependencies**
```bash
pip install -r medical_expert_system/requirements.txt
```

**3. Install SWI-Prolog**

Download from https://www.swi-prolog.org/download/stable and add to system PATH.

**4. Configure MongoDB**

Create a `.env` file inside `medical_expert_system/`:
```
MONGO_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net/?appName=Cluster0
MONGO_DB=medpredict
```

**5. Run the app**
```bash
python medical_expert_system/backend/app.py
```

Open http://localhost:5000

---

## Usage

1. **Step 1** — Enter patient profile (name, age, gender, height, weight)
2. **Step 2** — Enter vital signs (temperature, heart rate, oxygen saturation, blood pressure)
3. **Step 3** — Select symptoms and rate severity (None / Mild / Moderate / Severe)
4. **Step 4** — Enter medical history and lifestyle factors
5. Click **Run Diagnosis** to get results
6. View dashboard at http://localhost:5000/dashboard

---

## Diseases Covered

Flu, COVID-19, Dengue, Malaria, Pneumonia, Asthma, Bronchitis, Tuberculosis, Diabetes, Hypertension, Heart Disease, Gastroenteritis, Food Poisoning, Migraine, Allergy, Skin Infection, Dehydration, Hepatitis, Typhoid, Anemia

---

## Disclaimer

This system is for educational and research purposes only. Always consult a qualified healthcare professional for medical advice.
