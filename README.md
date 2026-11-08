# AI Usage Dashboard

A minimal Streamlit dashboard for the survey dataset in `data/`.

# The Dataset
Dataset used for analysis -> https://www.kaggle.com/datasets/eishatuzzuhra/ai-usage-and-impact-on-students-and-professionals

It is a survey about the AI usage both in professional use as well as among students.
## Run locally

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

Use the sidebar to filter by user type, country, and AI tool. Metrics and charts
update together, and the response table can be downloaded after filtering.
# AI-Tools-analysis