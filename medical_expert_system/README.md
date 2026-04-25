# Medical AI Expert System

AI-powered disease prediction and risk assessment using Prolog inference engine + Python Flask.

## Stack
- **Backend**: Python Flask
- **Inference Engine**: SWI-Prolog via pyswip (falls back to Python engine if unavailable)
- **Frontend**: HTML5, CSS3, JavaScript, Chart.js

## Setup

### 1. Install SWI-Prolog (optional but recommended)
- Windows: https://www.swi-prolog.org/download/stable
- Ubuntu: `sudo apt install swi-prolog`
- macOS: `brew install swi-prolog`

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the application
```bash
cd medical_expert_system
python backend/app.py
```

Open http://localhost:5000 in your browser.

## Notes
- If SWI-Prolog / pyswip is not installed, the system automatically uses the Python fallback engine with identical logic.
- The system is for educational/research purposes only — not a substitute for professional medical advice.

## Project Structure
```
medical_expert_system/
├── prolog_engine/
│   ├── knowledge_base.pl       # 20 diseases, 60 symptoms, weights
│   ├── diagnosis_engine.pl     # Scoring and ranking logic
│   ├── risk_analysis.pl        # Multi-factor risk calculation
│   └── explanation_engine.pl   # Explainable AI reasoning
├── backend/
│   └── app.py                  # Flask API + Python fallback engine
├── templates/
│   └── index.html              # Full dashboard UI
├── static/
│   ├── style.css               # Glassmorphism medical UI
│   └── script.js               # Frontend logic + Chart.js
└── requirements.txt
```
