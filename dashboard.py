from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st


DATA_PATH = (
    Path(__file__).resolve().parent
    / "data"
    / "AI_Usage_and_Impact_on_Students_and_Professionals.csv"
)

NUMERIC_COLUMNS = [
    "Age",
    "Monthly_Income",
    "Monthly_AI_Cost",
    "AI_Usage_Hours_Per_Day",
    "Productivity_Score",
    "Accuracy_Rating",
    "Satisfaction_Score",
    "Time_Saved_Hours_Per_Week",
    "Work_or_Study_Hours_Per_Day",
]

CATEGORY_COLUMNS = [
    "Country",
    "User_Type",
    "AI_Tool",
    "AI_Purpose",
    "Would_Recommend",
]

REQUIRED_COLUMNS = {
    "User_ID",
    "Country",
    "User_Type",
    "AI_Tool",
    "AI_Purpose",
    "AI_Usage_Hours_Per_Day",
    "Productivity_Score",
    "Satisfaction_Score",
    "Time_Saved_Hours_Per_Week",
    "Would_Recommend",
}

TOOL_ALIASES = {
    "chat gpt": "ChatGPT",
    "claude": "Claude",
    "copilot": "Microsoft Copilot",
    "microsoft copilot": "Microsoft Copilot",
    "gemini": "Google Gemini",
    "google gemini": "Google Gemini",
}

CHART_COLORS = ["#4F7CAC", "#67A88A", "#E0A458", "#8B79B8", "#D7796B"]


@st.cache_data
def load_data() -> pd.DataFrame:
    if not DATA_PATH.is_file():
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

    data = pd.read_csv(DATA_PATH)
    missing_columns = REQUIRED_COLUMNS.difference(data.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Dataset is missing required columns: {missing}")

    for column in NUMERIC_COLUMNS:
        if column in data.columns:
            values = data[column].astype("string").str.replace(",", "", regex=False)
            numbers = values.str.extract(r"([-+]?\d*\.?\d+)")[0]
            data[column] = pd.to_numeric(numbers, errors="coerce")

    for column in CATEGORY_COLUMNS:
        data[column] = data[column].astype("string").str.strip()
        data[column] = data[column].replace("", pd.NA).fillna("Not specified")

    normalized_tools = data["AI_Tool"].str.casefold()
    data["AI_Tool"] = normalized_tools.map(TOOL_ALIASES).fillna(data["AI_Tool"])
    return data


def format_hours(value: float) -> str:
    return f"{value:.1f} hrs" if pd.notna(value) else "—"


st.set_page_config(
    page_title="AI Usage Dashboard",
    page_icon="✳",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    html, body, [class*="css"] { font-family: sans-serif; }
    .stApp { background: #f7f8fa; color: #202733; }
    [data-testid="stHeader"] { background: rgba(247, 248, 250, 0.9); }
    [data-testid="stSidebar"] {
        background: #e9eef4; border-right: 1px solid #d5dde7; color: #202733;
    }
    [data-testid="stMetric"] {
        background: #e9eef4; border: 1px solid #d5dde7; border-radius: 12px;
        padding: 18px 20px;
    }
    [data-testid="stMetricLabel"] { color: #536174; }
    [data-testid="stMetricValue"] { color: #202733; }
    h1 { letter-spacing: -0.04em; font-weight: 600 !important; }
    h2, h3 { letter-spacing: -0.02em; }
    .eyebrow {
        color: #4F7CAC; text-transform: uppercase; letter-spacing: .12em;
        font-size: .75rem; font-weight: 700; margin-bottom: .35rem;
    }
    .subtle { color: #707987; }
    </style>
    """,
    unsafe_allow_html=True,
)

try:
    df = load_data()
except (FileNotFoundError, ValueError, pd.errors.ParserError) as error:
    st.error(f"Could not load the dashboard dataset: {error}")
    st.stop()

st.sidebar.markdown("## Explore the data")
st.sidebar.caption("Filters update every metric and chart.")

filter_columns = [
    ("User type", "User_Type"),
    ("Country", "Country"),
    ("AI tool", "AI_Tool"),
]
selections: dict[str, list[str]] = {}
for label, column in filter_columns:
    options = sorted(df[column].unique().tolist())
    selections[column] = st.sidebar.multiselect(
        label,
        options,
        default=options,
        help=f"Choose one or more {label.lower()} values.",
    )

filtered = df.copy()
for column, selected in selections.items():
    filtered = filtered[filtered[column].isin(selected)]

st.markdown('<div class="eyebrow">AI usage · survey overview</div>', unsafe_allow_html=True)
st.title("How people use AI")
st.markdown(
    '<p class="subtle">A snapshot of AI adoption, productivity, and sentiment '
    "among students and professionals.</p>",
    unsafe_allow_html=True,
)

if filtered.empty:
    st.info("No responses match these filters. Select at least one value in each filter.")
    st.stop()

respondents = filtered["User_ID"].nunique()
avg_usage = filtered["AI_Usage_Hours_Per_Day"].mean()
avg_time_saved = filtered["Time_Saved_Hours_Per_Week"].mean()
avg_satisfaction = filtered["Satisfaction_Score"].mean()

metric_columns = st.columns(4)
metric_columns[0].metric("Respondents", f"{respondents:,}")
metric_columns[1].metric("Daily AI use", format_hours(avg_usage))
metric_columns[2].metric("Time saved / week", format_hours(avg_time_saved))
metric_columns[3].metric(
    "Satisfaction",
    f"{avg_satisfaction:.1f} / 10" if pd.notna(avg_satisfaction) else "—",
)

st.markdown("")
left_chart, right_chart = st.columns(2, gap="large")

with left_chart:
    st.subheader("Most-used AI tools")
    tool_counts = (
        filtered.loc[filtered["AI_Tool"] != "Not specified", "AI_Tool"]
        .value_counts()
        .rename_axis("AI tool")
        .reset_index(name="Responses")
    )
    if tool_counts.empty:
        st.caption("No tool responses are available for this selection.")
    else:
        tool_chart = px.bar(
            tool_counts.sort_values("Responses"),
            x="Responses",
            y="AI tool",
            orientation="h",
            color_discrete_sequence=CHART_COLORS,
        )
        tool_chart.update_layout(
            height=390,
            margin=dict(l=4, r=10, t=10, b=10),
            showlegend=False,
            xaxis_title="Responses",
            yaxis_title=None,
            plot_bgcolor="#f7f8fa",
            paper_bgcolor="#e9eef4",
            font_color="#202733",
        )
        tool_chart.update_xaxes(
            showgrid=True, gridcolor="#dfe5ec", zeroline=False,
            tickfont_color="#202733", title_font_color="#202733",
        )
        tool_chart.update_yaxes(showgrid=False, tickfont_color="#202733")
        st.plotly_chart(tool_chart, use_container_width=True)

with right_chart:
    st.subheader("Why people use AI")
    purpose_counts = (
        filtered.loc[filtered["AI_Purpose"] != "Not specified", "AI_Purpose"]
        .value_counts()
        .rename_axis("Purpose")
        .reset_index(name="Responses")
    )
    if purpose_counts.empty:
        st.caption("No purpose responses are available for this selection.")
    else:
        purpose_chart = px.bar(
            purpose_counts.sort_values("Responses"),
            x="Responses",
            y="Purpose",
            orientation="h",
            color_discrete_sequence=[CHART_COLORS[1]],
        )
        purpose_chart.update_layout(
            height=390,
            margin=dict(l=4, r=10, t=10, b=10),
            showlegend=False,
            xaxis_title="Responses",
            yaxis_title=None,
            plot_bgcolor="#f7f8fa",
            paper_bgcolor="#e9eef4",
            font_color="#202733",
        )
        purpose_chart.update_xaxes(
            showgrid=True, gridcolor="#dfe5ec", zeroline=False,
            tickfont_color="#202733", title_font_color="#202733",
        )
        purpose_chart.update_yaxes(showgrid=False, tickfont_color="#202733")
        st.plotly_chart(purpose_chart, use_container_width=True)

st.markdown("")
lower_left, lower_right = st.columns(2, gap="large")

with lower_left:
    st.subheader("AI use and time saved")
    scatter_data = filtered.dropna(
        subset=["AI_Usage_Hours_Per_Day", "Time_Saved_Hours_Per_Week"]
    )
    if scatter_data.empty:
        st.caption("Not enough complete responses to show this relationship.")
    else:
        scatter_chart = px.scatter(
            scatter_data,
            x="AI_Usage_Hours_Per_Day",
            y="Time_Saved_Hours_Per_Week",
            color="User_Type",
            hover_data=["AI_Tool", "AI_Purpose"],
            color_discrete_sequence=CHART_COLORS,
            labels={
                "AI_Usage_Hours_Per_Day": "AI use (hours / day)",
                "Time_Saved_Hours_Per_Week": "Time saved (hours / week)",
                "User_Type": "User type",
            },
        )
        scatter_chart.update_traces(marker=dict(size=9, opacity=0.72))
        scatter_chart.update_layout(
            height=350,
            margin=dict(l=4, r=10, t=10, b=10),
            plot_bgcolor="#f7f8fa",
            paper_bgcolor="#e9eef4",
            font_color="#202733",
            legend_title_text="",
        )
        scatter_chart.update_xaxes(
            showgrid=True, gridcolor="#dfe5ec", rangemode="tozero",
            tickfont_color="#202733", title_font_color="#202733",
        )
        scatter_chart.update_yaxes(
            showgrid=True, gridcolor="#dfe5ec", rangemode="tozero",
            tickfont_color="#202733", title_font_color="#202733",
        )
        st.plotly_chart(scatter_chart, use_container_width=True)

with lower_right:
    st.subheader("Satisfaction by AI tool")
    satisfaction = (
        filtered.loc[
            (filtered["AI_Tool"] != "Not specified")
            & filtered["Satisfaction_Score"].notna()
        ]
        .groupby("AI_Tool", as_index=False)["Satisfaction_Score"]
        .mean()
        .sort_values("Satisfaction_Score")
    )
    if satisfaction.empty:
        st.caption("No satisfaction scores are available for this selection.")
    else:
        satisfaction_chart = px.bar(
            satisfaction,
            x="Satisfaction_Score",
            y="AI_Tool",
            orientation="h",
            color_discrete_sequence=[CHART_COLORS[3]],
            labels={"Satisfaction_Score": "Average score (out of 10)", "AI_Tool": "AI tool"},
        )
        satisfaction_chart.update_layout(
            height=350,
            margin=dict(l=4, r=10, t=10, b=10),
            showlegend=False,
            xaxis_range=[0, 10],
            yaxis_title=None,
            plot_bgcolor="#f7f8fa",
            paper_bgcolor="#e9eef4",
            font_color="#202733",
        )
        satisfaction_chart.update_xaxes(
            showgrid=True, gridcolor="#dfe5ec", zeroline=False,
            tickfont_color="#202733", title_font_color="#202733",
        )
        satisfaction_chart.update_yaxes(showgrid=False, tickfont_color="#202733")
        st.plotly_chart(satisfaction_chart, use_container_width=True)

with st.expander("View filtered responses"):
    st.caption(f"{len(filtered):,} responses · {len(df):,} total")
    st.dataframe(filtered, use_container_width=True, hide_index=True)
    st.download_button(
        "Download filtered data",
        data=filtered.to_csv(index=False).encode("utf-8"),
        file_name="ai_usage_filtered.csv",
        mime="text/csv",
    )
