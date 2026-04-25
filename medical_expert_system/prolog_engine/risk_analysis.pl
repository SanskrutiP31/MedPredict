% ============================================================
% MEDICAL EXPERT SYSTEM - Risk Analysis Engine
% risk_analysis.pl
% ============================================================

:- module(risk_analysis, [
    calculate_risk_score/2,
    risk_level/2,
    health_score/2
]).

% ============================================================
% CALCULATE RISK SCORE from patient data
% PatientData = patient(Age, Temp, HeartRate, OxygenSat,
%               Smoking, Alcohol, MedHistory, FamilyHistory,
%               Symptoms, BMI, ExerciseFreq)
% ============================================================
calculate_risk_score(PatientData, RiskScore) :-
    PatientData = patient(Age, Temp, HeartRate, OxygenSat,
                          Smoking, Alcohol, MedHistory, FamilyHistory,
                          Symptoms, BMI, _ExerciseFreq),
    age_risk(Age, AgeRisk),
    temp_risk(Temp, TempRisk),
    heart_rate_risk(HeartRate, HRRisk),
    oxygen_risk(OxygenSat, O2Risk),
    smoking_risk(Smoking, SmokingRisk),
    alcohol_risk(Alcohol, AlcoholRisk),
    history_risk(MedHistory, HistRisk),
    family_risk(FamilyHistory, FamRisk),
    symptom_severity_risk(Symptoms, SymRisk),
    bmi_risk(BMI, BMIRisk),
    RiskScore is AgeRisk + TempRisk + HRRisk + O2Risk +
                 SmokingRisk + AlcoholRisk + HistRisk +
                 FamRisk + SymRisk + BMIRisk.

% ============================================================
% AGE RISK
% ============================================================
age_risk(Age, 0)  :- Age < 18, !.
age_risk(Age, 5)  :- Age < 30, !.
age_risk(Age, 10) :- Age < 40, !.
age_risk(Age, 15) :- Age < 50, !.
age_risk(Age, 20) :- Age < 60, !.
age_risk(Age, 25) :- Age < 70, !.
age_risk(_, 30).

% ============================================================
% TEMPERATURE RISK (Celsius)
% ============================================================
temp_risk(Temp, 0)  :- Temp < 37.5, !.
temp_risk(Temp, 10) :- Temp < 38.5, !.
temp_risk(Temp, 20) :- Temp < 39.5, !.
temp_risk(_, 30).

% ============================================================
% HEART RATE RISK (bpm)
% ============================================================
heart_rate_risk(HR, 0)  :- HR >= 60, HR =< 100, !.
heart_rate_risk(HR, 10) :- HR >= 50, HR =< 110, !.
heart_rate_risk(HR, 20) :- HR >= 40, HR =< 130, !.
heart_rate_risk(_, 30).

% ============================================================
% OXYGEN SATURATION RISK (%)
% ============================================================
oxygen_risk(O2, 0)  :- O2 >= 95, !.
oxygen_risk(O2, 15) :- O2 >= 90, !.
oxygen_risk(O2, 25) :- O2 >= 85, !.
oxygen_risk(_, 35).

% ============================================================
% SMOKING RISK
% ============================================================
smoking_risk(none, 0)   :- !.
smoking_risk(former, 5) :- !.
smoking_risk(light, 10) :- !.
smoking_risk(heavy, 20) :- !.
smoking_risk(_, 0).

% ============================================================
% ALCOHOL RISK
% ============================================================
alcohol_risk(none, 0)      :- !.
alcohol_risk(occasional, 5):- !.
alcohol_risk(moderate, 10) :- !.
alcohol_risk(heavy, 20)    :- !.
alcohol_risk(_, 0).

% ============================================================
% MEDICAL HISTORY RISK
% ============================================================
history_risk(History, Risk) :-
    findall(R, (member(Cond, History), condition_risk(Cond, R)), Risks),
    (Risks = [] -> Risk = 0 ; sum_list(Risks, Risk)).

condition_risk(diabetes, 15).
condition_risk(hypertension, 15).
condition_risk(heart_disease, 20).
condition_risk(asthma, 10).
condition_risk(lung_disease, 15).
condition_risk(kidney_disease, 15).
condition_risk(liver_disease, 15).
condition_risk(cancer, 20).
condition_risk(_, 5).

% ============================================================
% FAMILY HISTORY RISK
% ============================================================
family_risk(FamilyHistory, Risk) :-
    findall(R, (member(Cond, FamilyHistory), family_condition_risk(Cond, R)), Risks),
    (Risks = [] -> Risk = 0 ; sum_list(Risks, Risk)).

family_condition_risk(diabetes, 8).
family_condition_risk(heart_disease, 10).
family_condition_risk(hypertension, 8).
family_condition_risk(cancer, 10).
family_condition_risk(_, 3).

% ============================================================
% SYMPTOM SEVERITY RISK
% ============================================================
symptom_severity_risk(Symptoms, Risk) :-
    findall(R, (member(S, Symptoms), severe_symptom_risk(S, R)), Risks),
    (Risks = [] -> Risk = 0 ; sum_list(Risks, Risk)).

severe_symptom_risk(shortness_of_breath, 15).
severe_symptom_risk(chest_pain, 20).
severe_symptom_risk(confusion, 15).
severe_symptom_risk(blood_in_sputum, 15).
severe_symptom_risk(irregular_heartbeat, 20).
severe_symptom_risk(loss_of_consciousness, 25).
severe_symptom_risk(severe_headache, 10).
severe_symptom_risk(_, 2).

% ============================================================
% BMI RISK
% ============================================================
bmi_risk(BMI, 0)  :- BMI >= 18.5, BMI < 25, !.
bmi_risk(BMI, 5)  :- BMI >= 25, BMI < 30, !.
bmi_risk(BMI, 10) :- BMI >= 30, BMI < 35, !.
bmi_risk(BMI, 15) :- BMI >= 35, !.
bmi_risk(_, 5).

% ============================================================
% RISK LEVEL from score
% ============================================================
risk_level(Score, 'Low')      :- Score =< 30, !.
risk_level(Score, 'Moderate') :- Score =< 60, !.
risk_level(Score, 'High')     :- Score =< 90, !.
risk_level(_, 'Critical').

% ============================================================
% HEALTH SCORE (inverse of risk, 0-100)
% ============================================================
health_score(RiskScore, HealthScore) :-
    RawHealth is 100 - (RiskScore * 0.5),
    HealthScore is max(0, min(100, round(RawHealth))).
