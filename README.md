CARDIOVOICE 
Everything is invented. Voice and clinical rows belong to the same IMAGINARY person. It proves nothing about heart failure.
Do not train or test a model on it, do not quote accuracy, do not show it as patient data.

RUN:  pip install numpy scipy pandas openpyxl matplotlib
      python cardiovoice_pipeline_v2.py       (makes audio/, features_merged.csv, differences csv, charts/, all_patients_charts.png)
      python make_excel.py                    (makes the Excel guide)

SIX PEOPLE, SIX STORIES
 DEMO_001 stable control | DEMO_002 weight only | DEMO_003 full episode
 DEMO_004 voice only     | DEMO_005 cold (confounder) | DEMO_006 phone change + noisy + clipped recordings
A flag is only a 'review suggested' message for a clinician. Never 'safe', never 'critical'.

REAL DATA LATER: keep the table layout, missing-data rules, quality gate, per-phone baseline and flag code.
Replace the simple estimators with Parselmouth/librosa (same settings every time). Thresholds are examples; the doctor
and statistician set them BEFORE looking at outcomes. Real patient data only after ethics approval and written consent.
