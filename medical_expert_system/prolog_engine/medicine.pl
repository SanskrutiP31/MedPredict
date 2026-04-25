% ============================================================
% MEDICAL EXPERT SYSTEM - Medicine & Home Care Rules
% medicine.pl
% ============================================================

:- module(medicine, [
    otc_medicines/2,
    home_care/2,
    is_serious_disease/1,
    emergency_check/3
]).

% ============================================================
% SERIOUS DISEASES - no OTC medicine, doctor only
% ============================================================
is_serious_disease(pneumonia).
is_serious_disease(tuberculosis).
is_serious_disease(heart_disease).
is_serious_disease(hepatitis).
is_serious_disease(dengue).
is_serious_disease(malaria).
is_serious_disease(typhoid).
is_serious_disease(covid19).
is_serious_disease(diabetes).
is_serious_disease(hypertension).

% ============================================================
% OTC MEDICINE SUGGESTIONS (minor diseases only)
% otc_medicines(+Disease, -Medicines)
% ============================================================
otc_medicines(Disease, ['Immediate doctor consultation recommended. Do not self-medicate.']) :-
    is_serious_disease(Disease), !.

otc_medicines(flu, [
    'Paracetamol (500mg) for fever and body aches',
    'Cetirizine for runny nose and sneezing',
    'Vitamin C supplements to boost immunity',
    'Throat lozenges for sore throat'
]).

otc_medicines(allergy, [
    'Cetirizine (10mg) antihistamine for allergic symptoms',
    'Loratadine as alternative antihistamine',
    'Nasal saline spray for congestion',
    'Hydrocortisone cream for skin rash'
]).

otc_medicines(migraine, [
    'Ibuprofen (400mg) for pain relief',
    'Paracetamol (500-1000mg) for headache',
    'Rest in a dark quiet room',
    'Cold compress on forehead'
]).

otc_medicines(gastroenteritis, [
    'ORS (Oral Rehydration Salts) to prevent dehydration',
    'Loperamide for diarrhea control',
    'Domperidone for nausea and vomiting',
    'Probiotics to restore gut flora'
]).

otc_medicines(food_poisoning, [
    'ORS (Oral Rehydration Salts) - primary treatment',
    'Activated charcoal if taken within 1 hour',
    'Domperidone for nausea',
    'Avoid solid food for 24 hours'
]).

otc_medicines(dehydration, [
    'ORS (Oral Rehydration Salts) immediately',
    'Electrolyte drinks (sports drinks)',
    'Increase water intake significantly',
    'Coconut water as natural electrolyte'
]).

otc_medicines(bronchitis, [
    'Guaifenesin cough expectorant syrup',
    'Paracetamol for fever if present',
    'Steam inhalation 2-3 times daily',
    'Honey and ginger tea for throat relief'
]).

otc_medicines(asthma, [
    'Use prescribed inhaler (Salbutamol) as directed',
    'Avoid known triggers',
    'Consult doctor if symptoms worsen',
    'Keep rescue inhaler accessible at all times'
]).

otc_medicines(skin_infection, [
    'Topical antibiotic cream (Mupirocin)',
    'Antifungal cream if fungal infection suspected',
    'Keep area clean and dry',
    'Consult doctor if spreading or worsening'
]).

otc_medicines(anemia, [
    'Iron supplements (Ferrous Sulfate) with Vitamin C',
    'Folic acid supplements',
    'Iron-rich diet (spinach, lentils, red meat)',
    'Consult doctor for blood test confirmation'
]).

otc_medicines(_, [
    'Consult a healthcare professional for proper diagnosis',
    'Do not self-medicate without medical advice'
]).

% ============================================================
% HOME CARE SUGGESTIONS
% home_care(+Disease, -CareTips)
% ============================================================
home_care(flu, [
    'Rest completely for 3-5 days',
    'Drink warm fluids: soup, herbal tea, warm water',
    'Steam inhalation to relieve congestion',
    'Gargle with warm salt water for sore throat',
    'Maintain good hygiene to prevent spreading'
]).

home_care(covid19, [
    'Isolate immediately from others',
    'Monitor oxygen saturation with pulse oximeter',
    'Stay well hydrated with warm fluids',
    'Rest and avoid physical exertion',
    'Seek emergency care if O2 drops below 94%'
]).

home_care(dengue, [
    'Complete bed rest is essential',
    'Drink plenty of fluids and coconut water',
    'Monitor platelet count daily',
    'Avoid aspirin and ibuprofen',
    'Use mosquito nets and repellent'
]).

home_care(malaria, [
    'Seek immediate medical treatment',
    'Rest and stay hydrated',
    'Use mosquito nets while sleeping',
    'Complete the full course of antimalarial drugs',
    'Monitor temperature regularly'
]).

home_care(pneumonia, [
    'Seek immediate medical attention',
    'Rest in semi-upright position to ease breathing',
    'Stay well hydrated',
    'Monitor oxygen levels closely',
    'Avoid smoking and secondhand smoke'
]).

home_care(gastroenteritis, [
    'Stay hydrated with ORS and clear fluids',
    'Follow BRAT diet: Banana, Rice, Applesauce, Toast',
    'Avoid dairy, fatty and spicy foods',
    'Rest and avoid strenuous activity',
    'Wash hands frequently to prevent spreading'
]).

home_care(food_poisoning, [
    'Stop eating solid food temporarily',
    'Sip ORS or clear fluids slowly',
    'Rest completely',
    'Gradually reintroduce bland foods after 24 hours',
    'Seek medical help if vomiting persists over 24 hours'
]).

home_care(migraine, [
    'Rest in a dark, quiet room',
    'Apply cold or warm compress to head/neck',
    'Stay hydrated',
    'Avoid screen time and bright lights',
    'Identify and avoid personal triggers'
]).

home_care(dehydration, [
    'Drink ORS immediately',
    'Sip fluids slowly and frequently',
    'Avoid caffeine and alcohol',
    'Rest in a cool environment',
    'Monitor urine color - aim for pale yellow'
]).

home_care(allergy, [
    'Identify and avoid allergen triggers',
    'Keep windows closed during high pollen season',
    'Use air purifier indoors',
    'Shower after outdoor exposure',
    'Wear mask in dusty environments'
]).

home_care(asthma, [
    'Avoid known triggers (dust, smoke, cold air)',
    'Keep rescue inhaler accessible',
    'Practice breathing exercises',
    'Maintain clean indoor air quality',
    'Monitor peak flow regularly'
]).

home_care(diabetes, [
    'Monitor blood glucose levels regularly',
    'Follow prescribed diet plan strictly',
    'Exercise regularly as advised by doctor',
    'Take medications as prescribed',
    'Check feet daily for wounds or sores'
]).

home_care(hypertension, [
    'Reduce sodium (salt) intake significantly',
    'Exercise regularly - 30 min daily walking',
    'Manage stress through meditation or yoga',
    'Avoid alcohol and smoking',
    'Monitor blood pressure daily'
]).

home_care(_, [
    'Rest adequately and stay hydrated',
    'Eat light nutritious meals',
    'Monitor symptoms and seek care if worsening',
    'Maintain good personal hygiene',
    'Consult a doctor for proper diagnosis'
]).

% ============================================================
% EMERGENCY CHECK
% emergency_check(+Vitals, +Symptoms, -IsEmergency)
% Vitals = vitals(OxygenSat, HeartRate, Temperature)
% ============================================================
emergency_check(vitals(O2, _HR, _Temp), _Symptoms, true) :-
    O2 < 90, !.

emergency_check(vitals(_O2, HR, _Temp), _Symptoms, true) :-
    (HR > 140 ; HR < 40), !.

emergency_check(vitals(_O2, _HR, Temp), _Symptoms, true) :-
    Temp >= 40.0, !.

emergency_check(vitals(_O2, _HR, _Temp), Symptoms, true) :-
    member(chest_pain, Symptoms), !.

emergency_check(vitals(_O2, _HR, _Temp), Symptoms, true) :-
    member(shortness_of_breath, Symptoms),
    member(chest_pain, Symptoms), !.

emergency_check(vitals(_O2, _HR, _Temp), Symptoms, true) :-
    member(irregular_heartbeat, Symptoms), !.

emergency_check(vitals(_O2, _HR, _Temp), Symptoms, true) :-
    member(confusion, Symptoms),
    member(fever, Symptoms), !.

emergency_check(_, _, false).
