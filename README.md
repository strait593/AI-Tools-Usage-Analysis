# AI Tools Usage Analysis

A Streamlit dashboard for exploring survey responses about AI tool use by students
and professionals.

## Run locally

```bash
python -m pip install -r requirements.txt
streamlit run dashboard.py
```

The dashboard loads the cleaned CSV from `data/` when available. If it is missing,
the raw survey CSV is cleaned before use. Use the sidebar filters to explore
respondents by user type, country, AI tool, purpose, and gender. The Responses tab
lets you download the filtered responses or the summary by tool.