% ============================================================
% MEDICAL EXPERT SYSTEM - Knowledge Base
% knowledge_base.pl
% ============================================================

:- module(knowledge_base, [
    symptom/1,
    disease/1,
    disease_symptom/2,
    disease_weight/3,
    risk_factor/2,
    disease_description/2,
    disease_category/2
]).

% ============================================================
% SYMPTOMS (60 symptoms)
% ============================================================
symptom(fever).
symptom(cough).
symptom(fatigue).
symptom(shortness_of_breath).
symptom(chest_pain).
symptom(headache).
symptom(body_aches).
symptom(sore_throat).
symptom(runny_nose).
symptom(nausea).
symptom(vomiting).
symptom(diarrhea).
symptom(abdominal_pain).
symptom(loss_of_appetite).
symptom(weight_loss).
symptom(night_sweats).
symptom(chills).
symptom(rash).
symptom(joint_pain).
symptom(muscle_pain).
symptom(dizziness).
symptom(confusion).
symptom(loss_of_taste).
symptom(loss_of_smell).
symptom(sneezing).
symptom(watery_eyes).
symptom(itchy_eyes).
symptom(skin_redness).
symptom(swelling).
symptom(bleeding_gums).
symptom(eye_pain).
symptom(back_pain).
symptom(neck_stiffness).
symptom(frequent_urination).
symptom(excessive_thirst).
symptom(blurred_vision).
symptom(slow_healing).
symptom(numbness).
symptom(tingling).
symptom(palpitations).
symptom(irregular_heartbeat).
symptom(swollen_lymph_nodes).
symptom(difficulty_swallowing).
symptom(hoarseness).
symptom(wheezing).
symptom(productive_cough).
symptom(blood_in_sputum).
symptom(pale_skin).
symptom(jaundice).
symptom(dark_urine).
symptom(clay_colored_stool).
symptom(bloating).
symptom(heartburn).
symptom(constipation).
symptom(eye_redness).
symptom(photophobia).
symptom(stiff_joints).
symptom(dry_skin).
symptom(hair_loss).
symptom(cold_intolerance).

% ============================================================
% DISEASES (20 diseases)
% ============================================================
disease(flu).
disease(covid19).
disease(dengue).
disease(malaria).
disease(pneumonia).
disease(asthma).
disease(bronchitis).
disease(tuberculosis).
disease(diabetes).
disease(hypertension).
disease(heart_disease).
disease(gastroenteritis).
disease(food_poisoning).
disease(migraine).
disease(allergy).
disease(skin_infection).
disease(dehydration).
disease(hepatitis).
disease(typhoid).
disease(anemia).

% ============================================================
% DISEASE CATEGORIES
% ============================================================
disease_category(flu, infectious).
disease_category(covid19, infectious).
disease_category(dengue, infectious).
disease_category(malaria, infectious).
disease_category(pneumonia, respiratory).
disease_category(asthma, respiratory).
disease_category(bronchitis, respiratory).
disease_category(tuberculosis, respiratory).
disease_category(diabetes, metabolic).
disease_category(hypertension, cardiovascular).
disease_category(heart_disease, cardiovascular).
disease_category(gastroenteritis, gastrointestinal).
disease_category(food_poisoning, gastrointestinal).
disease_category(migraine, neurological).
disease_category(allergy, immunological).
disease_category(skin_infection, dermatological).
disease_category(dehydration, metabolic).
disease_category(hepatitis, gastrointestinal).
disease_category(typhoid, infectious).
disease_category(anemia, hematological).

% ============================================================
% DISEASE DESCRIPTIONS
% ============================================================
disease_description(flu, 'Influenza - viral respiratory illness with fever, cough, and body aches').
disease_description(covid19, 'COVID-19 - coronavirus infection affecting respiratory system').
disease_description(dengue, 'Dengue fever - mosquito-borne viral disease with high fever and rash').
disease_description(malaria, 'Malaria - parasitic disease transmitted by mosquitoes causing cyclic fever').
disease_description(pneumonia, 'Pneumonia - lung infection causing inflammation and breathing difficulty').
disease_description(asthma, 'Asthma - chronic respiratory condition causing airway inflammation').
disease_description(bronchitis, 'Bronchitis - inflammation of bronchial tubes causing cough').
disease_description(tuberculosis, 'Tuberculosis - bacterial lung infection with chronic cough and weight loss').
disease_description(diabetes, 'Diabetes - metabolic disorder affecting blood sugar regulation').
disease_description(hypertension, 'Hypertension - high blood pressure affecting cardiovascular system').
disease_description(heart_disease, 'Heart Disease - conditions affecting heart function and blood flow').
disease_description(gastroenteritis, 'Gastroenteritis - stomach and intestinal inflammation causing GI symptoms').
disease_description(food_poisoning, 'Food Poisoning - illness from contaminated food causing GI distress').
disease_description(migraine, 'Migraine - severe recurring headaches with neurological symptoms').
disease_description(allergy, 'Allergy - immune response to environmental or food triggers').
disease_description(skin_infection, 'Skin Infection - bacterial or fungal infection of skin tissue').
disease_description(dehydration, 'Dehydration - insufficient fluid levels affecting body function').
disease_description(hepatitis, 'Hepatitis - liver inflammation usually caused by viral infection').
disease_description(typhoid, 'Typhoid - bacterial infection causing sustained fever and GI symptoms').
disease_description(anemia, 'Anemia - low red blood cell count causing fatigue and weakness').

% ============================================================
% DISEASE-SYMPTOM ASSOCIATIONS WITH WEIGHTS
% disease_weight(Disease, Symptom, Weight 1-10)
% ============================================================

% FLU
disease_weight(flu, fever, 9).
disease_weight(flu, cough, 8).
disease_weight(flu, body_aches, 9).
disease_weight(flu, fatigue, 8).
disease_weight(flu, headache, 7).
disease_weight(flu, chills, 8).
disease_weight(flu, sore_throat, 6).
disease_weight(flu, runny_nose, 7).
disease_weight(flu, sneezing, 6).
disease_weight(flu, loss_of_appetite, 5).

% COVID-19
disease_weight(covid19, fever, 8).
disease_weight(covid19, cough, 9).
disease_weight(covid19, fatigue, 8).
disease_weight(covid19, loss_of_taste, 10).
disease_weight(covid19, loss_of_smell, 10).
disease_weight(covid19, shortness_of_breath, 9).
disease_weight(covid19, body_aches, 7).
disease_weight(covid19, headache, 6).
disease_weight(covid19, sore_throat, 6).
disease_weight(covid19, chills, 7).

% DENGUE
disease_weight(dengue, fever, 10).
disease_weight(dengue, severe_headache, 9).
disease_weight(dengue, eye_pain, 8).
disease_weight(dengue, joint_pain, 9).
disease_weight(dengue, muscle_pain, 9).
disease_weight(dengue, rash, 8).
disease_weight(dengue, bleeding_gums, 7).
disease_weight(dengue, nausea, 6).
disease_weight(dengue, vomiting, 6).
disease_weight(dengue, fatigue, 7).

% MALARIA
disease_weight(malaria, fever, 10).
disease_weight(malaria, chills, 10).
disease_weight(malaria, sweating, 9).
disease_weight(malaria, headache, 8).
disease_weight(malaria, nausea, 7).
disease_weight(malaria, vomiting, 7).
disease_weight(malaria, muscle_pain, 7).
disease_weight(malaria, fatigue, 8).
disease_weight(malaria, abdominal_pain, 6).
disease_weight(malaria, diarrhea, 5).

% PNEUMONIA
disease_weight(pneumonia, fever, 9).
disease_weight(pneumonia, cough, 10).
disease_weight(pneumonia, shortness_of_breath, 10).
disease_weight(pneumonia, chest_pain, 9).
disease_weight(pneumonia, fatigue, 8).
disease_weight(pneumonia, chills, 7).
disease_weight(pneumonia, productive_cough, 9).
disease_weight(pneumonia, confusion, 6).
disease_weight(pneumonia, nausea, 5).
disease_weight(pneumonia, loss_of_appetite, 6).

% ASTHMA
disease_weight(asthma, wheezing, 10).
disease_weight(asthma, shortness_of_breath, 10).
disease_weight(asthma, cough, 8).
disease_weight(asthma, chest_pain, 7).
disease_weight(asthma, fatigue, 6).

% BRONCHITIS
disease_weight(bronchitis, cough, 10).
disease_weight(bronchitis, productive_cough, 9).
disease_weight(bronchitis, fatigue, 7).
disease_weight(bronchitis, shortness_of_breath, 7).
disease_weight(bronchitis, chest_pain, 6).
disease_weight(bronchitis, fever, 5).
disease_weight(bronchitis, sore_throat, 5).
disease_weight(bronchitis, wheezing, 6).

% TUBERCULOSIS
disease_weight(tuberculosis, cough, 10).
disease_weight(tuberculosis, blood_in_sputum, 10).
disease_weight(tuberculosis, night_sweats, 9).
disease_weight(tuberculosis, weight_loss, 9).
disease_weight(tuberculosis, fever, 8).
disease_weight(tuberculosis, fatigue, 8).
disease_weight(tuberculosis, chest_pain, 7).
disease_weight(tuberculosis, loss_of_appetite, 7).
disease_weight(tuberculosis, productive_cough, 8).

% DIABETES
disease_weight(diabetes, frequent_urination, 10).
disease_weight(diabetes, excessive_thirst, 10).
disease_weight(diabetes, blurred_vision, 8).
disease_weight(diabetes, fatigue, 7).
disease_weight(diabetes, slow_healing, 9).
disease_weight(diabetes, numbness, 7).
disease_weight(diabetes, tingling, 7).
disease_weight(diabetes, weight_loss, 6).
disease_weight(diabetes, dry_skin, 6).

% HYPERTENSION
disease_weight(hypertension, headache, 8).
disease_weight(hypertension, dizziness, 7).
disease_weight(hypertension, chest_pain, 7).
disease_weight(hypertension, shortness_of_breath, 6).
disease_weight(hypertension, palpitations, 7).
disease_weight(hypertension, blurred_vision, 6).
disease_weight(hypertension, nausea, 5).

% HEART DISEASE
disease_weight(heart_disease, chest_pain, 10).
disease_weight(heart_disease, shortness_of_breath, 9).
disease_weight(heart_disease, palpitations, 9).
disease_weight(heart_disease, irregular_heartbeat, 10).
disease_weight(heart_disease, fatigue, 8).
disease_weight(heart_disease, dizziness, 7).
disease_weight(heart_disease, swelling, 7).
disease_weight(heart_disease, nausea, 5).

% GASTROENTERITIS
disease_weight(gastroenteritis, nausea, 9).
disease_weight(gastroenteritis, vomiting, 9).
disease_weight(gastroenteritis, diarrhea, 10).
disease_weight(gastroenteritis, abdominal_pain, 9).
disease_weight(gastroenteritis, fever, 6).
disease_weight(gastroenteritis, fatigue, 6).
disease_weight(gastroenteritis, loss_of_appetite, 7).
disease_weight(gastroenteritis, bloating, 6).

% FOOD POISONING
disease_weight(food_poisoning, nausea, 10).
disease_weight(food_poisoning, vomiting, 10).
disease_weight(food_poisoning, diarrhea, 9).
disease_weight(food_poisoning, abdominal_pain, 9).
disease_weight(food_poisoning, fever, 7).
disease_weight(food_poisoning, fatigue, 6).
disease_weight(food_poisoning, chills, 5).

% MIGRAINE
disease_weight(migraine, headache, 10).
disease_weight(migraine, nausea, 8).
disease_weight(migraine, vomiting, 7).
disease_weight(migraine, photophobia, 9).
disease_weight(migraine, dizziness, 7).
disease_weight(migraine, blurred_vision, 6).
disease_weight(migraine, fatigue, 5).

% ALLERGY
disease_weight(allergy, sneezing, 9).
disease_weight(allergy, runny_nose, 9).
disease_weight(allergy, watery_eyes, 9).
disease_weight(allergy, itchy_eyes, 9).
disease_weight(allergy, rash, 7).
disease_weight(allergy, skin_redness, 7).
disease_weight(allergy, cough, 6).
disease_weight(allergy, wheezing, 6).
disease_weight(allergy, swelling, 5).

% SKIN INFECTION
disease_weight(skin_infection, rash, 10).
disease_weight(skin_infection, skin_redness, 10).
disease_weight(skin_infection, swelling, 8).
disease_weight(skin_infection, fever, 6).
disease_weight(skin_infection, pain, 7).
disease_weight(skin_infection, itchy_eyes, 5).

% DEHYDRATION
disease_weight(dehydration, dizziness, 9).
disease_weight(dehydration, fatigue, 8).
disease_weight(dehydration, excessive_thirst, 10).
disease_weight(dehydration, dark_urine, 9).
disease_weight(dehydration, dry_skin, 7).
disease_weight(dehydration, headache, 6).
disease_weight(dehydration, confusion, 7).
disease_weight(dehydration, constipation, 5).

% HEPATITIS
disease_weight(hepatitis, jaundice, 10).
disease_weight(hepatitis, dark_urine, 9).
disease_weight(hepatitis, clay_colored_stool, 9).
disease_weight(hepatitis, fatigue, 8).
disease_weight(hepatitis, abdominal_pain, 8).
disease_weight(hepatitis, nausea, 7).
disease_weight(hepatitis, vomiting, 6).
disease_weight(hepatitis, fever, 6).
disease_weight(hepatitis, loss_of_appetite, 7).

% TYPHOID
disease_weight(typhoid, fever, 10).
disease_weight(typhoid, headache, 8).
disease_weight(typhoid, abdominal_pain, 8).
disease_weight(typhoid, constipation, 7).
disease_weight(typhoid, diarrhea, 6).
disease_weight(typhoid, fatigue, 7).
disease_weight(typhoid, loss_of_appetite, 7).
disease_weight(typhoid, rash, 6).
disease_weight(typhoid, night_sweats, 6).

% ANEMIA
disease_weight(anemia, fatigue, 10).
disease_weight(anemia, pale_skin, 10).
disease_weight(anemia, shortness_of_breath, 8).
disease_weight(anemia, dizziness, 8).
disease_weight(anemia, headache, 6).
disease_weight(anemia, cold_intolerance, 7).
disease_weight(anemia, hair_loss, 6).
disease_weight(anemia, palpitations, 7).
disease_weight(anemia, chest_pain, 5).

% ============================================================
% DISEASE-SYMPTOM RULES (for matching)
% ============================================================
disease_symptom(Disease, Symptom) :-
    disease_weight(Disease, Symptom, _).

% ============================================================
% RISK FACTORS
% ============================================================
risk_factor(smoking, respiratory_disease).
risk_factor(smoking, heart_disease).
risk_factor(smoking, cancer).
risk_factor(alcohol, liver_disease).
risk_factor(alcohol, heart_disease).
risk_factor(obesity, diabetes).
risk_factor(obesity, heart_disease).
risk_factor(obesity, hypertension).
risk_factor(sedentary, heart_disease).
risk_factor(sedentary, diabetes).
risk_factor(age_above_50, heart_disease).
risk_factor(age_above_50, diabetes).
risk_factor(age_above_50, hypertension).
risk_factor(family_history_diabetes, diabetes).
risk_factor(family_history_heart, heart_disease).
risk_factor(family_history_hypertension, hypertension).
