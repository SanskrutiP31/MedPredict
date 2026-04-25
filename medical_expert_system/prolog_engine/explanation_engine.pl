% ============================================================
% MEDICAL EXPERT SYSTEM - Explanation Engine
% explanation_engine.pl
% ============================================================

:- module(explanation_engine, [
    explain_diagnosis/4,
    explain_risk/3,
    generate_recommendations/3
]).

:- use_module(knowledge_base).
:- use_module(risk_analysis).

% ============================================================
% EXPLAIN DIAGNOSIS
% explain_diagnosis(+Disease, +Symptoms, +PatientData, -Explanations)
% ============================================================
explain_diagnosis(Disease, Symptoms, PatientData, Explanations) :-
    PatientData = patient(Age, Temp, _HR, OxygenSat,
                          Smoking, _Alcohol, MedHistory, _FamHistory,
                          _Syms, _BMI, _Exercise),
    findall(Exp,
        explain_symptom_match(Disease, Symptoms, Exp),
        SymExps),
    findall(Exp,
        explain_vital_factor(Disease, Temp, OxygenSat, Exp),
        VitalExps),
    findall(Exp,
        explain_age_factor(Disease, Age, Exp),
        AgeExps),
    findall(Exp,
        explain_history_factor(Disease, MedHistory, Exp),
        HistExps),
    findall(Exp,
        explain_lifestyle_factor(Disease, Smoking, Exp),
        LifeExps),
    append([SymExps, VitalExps, AgeExps, HistExps, LifeExps], AllExps),
    (AllExps = [] ->
        Explanations = ['Symptoms match disease profile']
    ;
        Explanations = AllExps
    ).

% ============================================================
% SYMPTOM MATCH EXPLANATIONS
% ============================================================
explain_symptom_match(Disease, Symptoms, Explanation) :-
    member(Symptom, Symptoms),
    disease_weight(Disease, Symptom, Weight),
    Weight >= 7,
    symptom_explanation(Symptom, Explanation).

symptom_explanation(fever, 'Fever detected - key indicator').
symptom_explanation(cough, 'Persistent cough present').
symptom_explanation(shortness_of_breath, 'Shortness of breath reported').
symptom_explanation(chest_pain, 'Chest pain - significant warning sign').
symptom_explanation(fatigue, 'Fatigue and weakness noted').
symptom_explanation(loss_of_taste, 'Loss of taste - distinctive marker').
symptom_explanation(loss_of_smell, 'Loss of smell - distinctive marker').
symptom_explanation(blood_in_sputum, 'Blood in sputum - serious symptom').
symptom_explanation(night_sweats, 'Night sweats reported').
symptom_explanation(weight_loss, 'Unexplained weight loss').
symptom_explanation(frequent_urination, 'Frequent urination pattern').
symptom_explanation(excessive_thirst, 'Excessive thirst reported').
symptom_explanation(jaundice, 'Jaundice (yellowing) detected').
symptom_explanation(wheezing, 'Wheezing during breathing').
symptom_explanation(rash, 'Skin rash present').
symptom_explanation(joint_pain, 'Joint pain reported').
symptom_explanation(muscle_pain, 'Muscle pain and aches').
symptom_explanation(chills, 'Chills and shivering').
symptom_explanation(headache, 'Headache present').
symptom_explanation(nausea, 'Nausea reported').
symptom_explanation(vomiting, 'Vomiting episodes').
symptom_explanation(diarrhea, 'Diarrhea present').
symptom_explanation(abdominal_pain, 'Abdominal pain noted').
symptom_explanation(dizziness, 'Dizziness reported').
symptom_explanation(confusion, 'Confusion or disorientation').
symptom_explanation(palpitations, 'Heart palpitations detected').
symptom_explanation(irregular_heartbeat, 'Irregular heartbeat - critical sign').
symptom_explanation(pale_skin, 'Pale skin coloration').
symptom_explanation(photophobia, 'Light sensitivity present').
symptom_explanation(productive_cough, 'Productive cough with mucus').
symptom_explanation(Symptom, Explanation) :-
    atom_string(Symptom, S),
    string_concat('Symptom present: ', S, Explanation).

% ============================================================
% VITAL SIGN EXPLANATIONS
% ============================================================
explain_vital_factor(Disease, Temp, _O2, Explanation) :-
    Temp >= 38.5,
    disease_weight(Disease, fever, W), W >= 7,
    Explanation = 'High body temperature (fever) supports diagnosis'.

explain_vital_factor(Disease, _Temp, OxygenSat, Explanation) :-
    OxygenSat < 95,
    (Disease = pneumonia ; Disease = covid19 ; Disease = asthma),
    Explanation = 'Oxygen saturation below normal range'.

explain_vital_factor(Disease, _Temp, OxygenSat, Explanation) :-
    OxygenSat < 90,
    Explanation = 'Critically low oxygen saturation detected'.

% ============================================================
% AGE FACTOR EXPLANATIONS
% ============================================================
explain_age_factor(Disease, Age, Explanation) :-
    Age > 50,
    (Disease = heart_disease ; Disease = diabetes ; Disease = hypertension ; Disease = pneumonia),
    Explanation = 'Age above 50 increases risk for this condition'.

explain_age_factor(Disease, Age, Explanation) :-
    Age > 65,
    Explanation = 'Advanced age (65+) is a significant risk factor'.

% ============================================================
% MEDICAL HISTORY EXPLANATIONS
% ============================================================
explain_history_factor(Disease, MedHistory, Explanation) :-
    member(Condition, MedHistory),
    history_disease_link(Condition, Disease, Explanation).

history_disease_link(diabetes, heart_disease, 'Diabetes history increases cardiovascular risk').
history_disease_link(diabetes, hypertension, 'Diabetes often co-occurs with hypertension').
history_disease_link(hypertension, heart_disease, 'Hypertension is a major heart disease risk factor').
history_disease_link(asthma, pneumonia, 'Asthma history increases pneumonia susceptibility').
history_disease_link(asthma, bronchitis, 'Asthma history linked to bronchitis risk').
history_disease_link(lung_disease, tuberculosis, 'Lung disease history increases TB risk').
history_disease_link(lung_disease, pneumonia, 'Pre-existing lung disease increases pneumonia risk').
history_disease_link(Cond, Disease, Explanation) :-
    atom_string(Cond, CS),
    atom_string(Disease, DS),
    string_concat('Medical history of ', CS, P1),
    string_concat(P1, ' noted for ', P2),
    string_concat(P2, DS, Explanation).

% ============================================================
% LIFESTYLE FACTOR EXPLANATIONS
% ============================================================
explain_lifestyle_factor(Disease, Smoking, Explanation) :-
    (Smoking = heavy ; Smoking = light),
    (Disease = bronchitis ; Disease = tuberculosis ; Disease = pneumonia ; Disease = asthma),
    Explanation = 'Smoking history significantly increases respiratory disease risk'.

explain_lifestyle_factor(Disease, Smoking, Explanation) :-
    Smoking = heavy,
    Disease = heart_disease,
    Explanation = 'Heavy smoking is a major cardiovascular risk factor'.

% ============================================================
% EXPLAIN RISK LEVEL
% explain_risk(+RiskScore, +PatientData, -RiskExplanations)
% ============================================================
explain_risk(RiskScore, PatientData, RiskExplanations) :-
    PatientData = patient(Age, Temp, HeartRate, OxygenSat,
                          Smoking, Alcohol, MedHistory, _FamHistory,
                          _Syms, _BMI, _Exercise),
    findall(Exp, risk_explanation(RiskScore, Age, Temp, HeartRate,
                                   OxygenSat, Smoking, Alcohol,
                                   MedHistory, Exp), RiskExplanations).

risk_explanation(Score, _, _, _, _, _, _, _, Exp) :-
    Score > 90,
    Exp = 'CRITICAL: Multiple severe risk factors present - immediate medical attention required'.

risk_explanation(Score, _, _, _, _, _, _, _, Exp) :-
    Score > 60,
    Exp = 'HIGH RISK: Significant risk factors detected - medical consultation recommended'.

risk_explanation(_, Age, _, _, _, _, _, _, Exp) :-
    Age > 65,
    Exp = 'Age above 65 is a significant risk factor'.

risk_explanation(_, _, Temp, _, _, _, _, _, Exp) :-
    Temp >= 39.0,
    Exp = 'High fever (39°C+) indicates serious infection'.

risk_explanation(_, _, _, HeartRate, _, _, _, _, Exp) :-
    (HeartRate > 110 ; HeartRate < 50),
    Exp = 'Abnormal heart rate detected'.

risk_explanation(_, _, _, _, OxygenSat, _, _, _, Exp) :-
    OxygenSat < 95,
    Exp = 'Low oxygen saturation is a critical warning sign'.

risk_explanation(_, _, _, _, _, Smoking, _, _, Exp) :-
    (Smoking = heavy ; Smoking = light),
    Exp = 'Smoking increases risk of multiple diseases'.

risk_explanation(_, _, _, _, _, _, Alcohol, _, Exp) :-
    (Alcohol = heavy ; Alcohol = moderate),
    Exp = 'Alcohol consumption contributes to health risks'.

risk_explanation(_, _, _, _, _, _, _, MedHistory, Exp) :-
    MedHistory \= [],
    length(MedHistory, L), L > 0,
    Exp = 'Pre-existing medical conditions increase overall risk'.

% ============================================================
% GENERATE HEALTH RECOMMENDATIONS
% ============================================================
generate_recommendations(Disease, RiskLevel, Recommendations) :-
    findall(R, disease_recommendation(Disease, R), DiseaseRecs),
    findall(R, risk_recommendation(RiskLevel, R), RiskRecs),
    append(DiseaseRecs, RiskRecs, AllRecs),
    (AllRecs = [] ->
        Recommendations = ['Consult a healthcare professional for proper diagnosis']
    ;
        Recommendations = AllRecs
    ).

disease_recommendation(pneumonia, 'Seek immediate medical attention').
disease_recommendation(pneumonia, 'Monitor oxygen levels closely').
disease_recommendation(covid19, 'Isolate and contact health authorities').
disease_recommendation(covid19, 'Monitor oxygen saturation regularly').
disease_recommendation(heart_disease, 'Seek emergency care if chest pain worsens').
disease_recommendation(heart_disease, 'Avoid strenuous physical activity').
disease_recommendation(diabetes, 'Monitor blood glucose levels').
disease_recommendation(diabetes, 'Follow prescribed medication regimen').
disease_recommendation(tuberculosis, 'Isolate and seek specialist care').
disease_recommendation(tuberculosis, 'Complete full antibiotic course').
disease_recommendation(_, 'Stay hydrated and rest adequately').
disease_recommendation(_, 'Monitor symptoms and seek care if worsening').

risk_recommendation('Critical', 'URGENT: Seek emergency medical care immediately').
risk_recommendation('High', 'Schedule urgent medical appointment within 24 hours').
risk_recommendation('Moderate', 'Consult a doctor within the next few days').
risk_recommendation('Low', 'Monitor symptoms and maintain healthy lifestyle').
