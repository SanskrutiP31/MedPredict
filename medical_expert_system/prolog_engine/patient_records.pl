% ============================================================
% MEDICAL EXPERT SYSTEM - Patient Records
% patient_records.pl
%
% Each record is stored as a fact:
% patient_record(
%   ID,           % unique integer
%   Name,         % atom
%   Age,          % integer
%   Gender,       % atom
%   Height,       % number (cm)
%   Weight,       % number (kg)
%   BloodGroup,   % atom
%   Temperature,  % float (Celsius)
%   HeartRate,    % integer (bpm)
%   OxygenSat,    % integer (%)
%   BloodPressure,% atom e.g. '120/80'
%   Symptoms,     % list of atoms
%   MedHistory,   % list of atoms
%   FamHistory,   % list of atoms
%   Smoking,      % atom
%   Alcohol,      % atom
%   Exercise,     % atom
%   Sleep,        % integer (hours)
%   PrimaryDx,    % atom  - primary diagnosis key
%   RiskLevel,    % atom  - Low/Moderate/High/Critical
%   RiskScore,    % integer
%   HealthScore,  % integer
%   Timestamp     % atom  - ISO datetime string
% ).
% ============================================================

:- module(patient_records, [patient_record/28]).

patient_record(1,'abc',35,'female',170,70,'unknown',37,75,98,'120/80',['fever','cough','headache','body_aches','muscle_pain'],[],[],'none','none','daily',7,'flu','Low',20,90,'2026-03-16T19:57:13').
