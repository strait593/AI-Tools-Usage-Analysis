# Intro to the anylsis on topic "AI Tool usage."

### Key quesitons to be answered and the insights to be drown
---
| Question | Analysis tehchnique |
| ---------|---------------------| 
| Is more AI use asosciated with greater utility? | Simple correlation check (also a hypothesis test for means of both groups) |
| Do students and professionals repoart different outcomes? | Whitney U test would be a good tool to use since it checks whether the data fits the assumption. I will compare usage, time saved, productivity, satisfaction scores and cost|
| Outcomes among different AI tools (I will focus on coding since it is the field where AI Tools are used the most) | Kruskal - Wallis test across different groups|

### Folder structure of the project

```text
neural-nets-usage-analysis/
├── data/
│   ├── AI_Usage_and_Impact_on_Students_and_Professionals.csv
│   |── AI_Usage_and_Impact_on_Students_and_Professionals_clean.csv
│   │
├── notebooks/
│   ├── 01_data_cleaning.ipynb
│   ├── 02_exploratory_analysis.ipynb
│   ├── 03_statistical_tests.ipynb
│   └── 04_visualizations.ipynb
├── src/
│   ├── __init__.py
│   ├── data_cleaning.py
│   ├── analysis.py
│   ├── statistics.py
│   └── plotting.py
├── reports/
│   ├── figures/
│   └── final_report.md
└── INTRO.md
├── README.md
├── requirements.txt
├── .gitignore
```
