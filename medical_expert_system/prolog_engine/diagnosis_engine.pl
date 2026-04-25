% ============================================================
% MEDICAL EXPERT SYSTEM - Diagnosis Engine
% diagnosis_engine.pl
% ============================================================

:- module(diagnosis_engine, [
    diagnose/2,
    top_diagnoses/3,
    symptom_match_score/3,
    normalize_scores/2
]).

:- use_module(knowledge_base).


% ============================================================
% SYMPTOM MATCHING - Calculate match score for a disease
% symptom_match_score(+Disease, +Symptoms, -Score)
% ============================================================
symptom_match_score(Disease, Symptoms, Score) :-
    findall(W,
        (member(S, Symptoms), disease_weight(Disease, S, W)),
        Weights),
    sum_list(Weights, RawScore),
    findall(MaxW,
        disease_weight(Disease, _, MaxW),
        AllWeights),
    sum_list(AllWeights, MaxScore),
    (MaxScore > 0 ->
        Score is (RawScore / MaxScore) * 100
    ;
        Score is 0
    ).

% ============================================================
% DIAGNOSE - Get all disease scores for given symptoms
% diagnose(+Symptoms, -ScoredDiseases)
% ============================================================
diagnose(Symptoms, ScoredDiseases) :-
    findall(Score-Disease,
        (disease(Disease),
         symptom_match_score(Disease, Symptoms, Score),
         Score > 0),
        Pairs),
    sort(0, @>=, Pairs, SortedPairs),
    pairs_to_disease_scores(SortedPairs, ScoredDiseases).

pairs_to_disease_scores([], []).
pairs_to_disease_scores([S-D|Rest], [disease(D, S)|RestOut]) :-
    pairs_to_disease_scores(Rest, RestOut).

% ============================================================
% TOP N DIAGNOSES
% top_diagnoses(+Symptoms, +N, -TopDiseases)
% ============================================================
top_diagnoses(Symptoms, N, TopDiseases) :-
    diagnose(Symptoms, AllDiseases),
    length(AllDiseases, Len),
    Take is min(N, Len),
    length(TopDiseases, Take),
    append(TopDiseases, _, AllDiseases).

% ============================================================
% NORMALIZE SCORES to percentages summing to 100
% normalize_scores(+ScoredDiseases, -NormalizedDiseases)
% ============================================================
normalize_scores([], []).
normalize_scores(ScoredDiseases, NormalizedDiseases) :-
    ScoredDiseases \= [],
    findall(S, member(disease(_, S), ScoredDiseases), Scores),
    sum_list(Scores, Total),
    (Total > 0 ->
        maplist(normalize_disease(Total), ScoredDiseases, NormalizedDiseases)
    ;
        NormalizedDiseases = ScoredDiseases
    ).

normalize_disease(Total, disease(D, S), disease(D, NormScore)) :-
    NormScore is round((S / Total) * 100).

% ============================================================
% MATCHED SYMPTOMS for a disease
% matched_symptoms(+Disease, +Symptoms, -Matched)
% ============================================================
matched_symptoms(Disease, Symptoms, Matched) :-
    findall(S,
        (member(S, Symptoms), disease_symptom(Disease, S)),
        Matched).

% ============================================================
% CONFIDENCE LEVEL label
% ============================================================
confidence_label(Score, 'Very High') :- Score >= 70, !.
confidence_label(Score, 'High') :- Score >= 50, !.
confidence_label(Score, 'Moderate') :- Score >= 30, !.
confidence_label(Score, 'Low') :- Score >= 10, !.
confidence_label(_, 'Very Low').
