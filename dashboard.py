from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from scripts.data_cleaning import DATA_ROOT, clean_dataset

st.set_page_config(
    page_title="AI Tools Usage Analysis",
    page_icon="📊",
    layout="wide",
)

st.markdown(
    """
    <style>
        :root {
            --bg: #f5f7fb;
            --text: #172033;
            --muted: #6b7280;
            --border: #e5e7eb;
        }

        .stApp {
            background: var(--bg);
            color: var(--text);
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        div[data-testid="stSidebar"] {
            background: #eff4f9;
            border-right: 1px solid var(--border);
        }

        .section-subtitle {
            color: var(--muted);
            font-size: 0.9rem;
            margin-bottom: 0.75rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

CLEANED_FILE = DATA_ROOT / "AI_Usage_and_Impact_on_Students_and_Professionals_cleaned.csv"
RAW_FILE = DATA_ROOT / "AI_Usage_and_Impact_on_Students_and_Professionals.csv"
DATA_FILE = CLEANED_FILE if CLEANED_FILE.is_file() else RAW_FILE

if not DATA_FILE.is_file():
    st.error(f"Survey data file not found: {DATA_FILE}")
    st.stop()


@st.cache_data(show_spinner="Loading survey responses...")
def load_responses(file_path: str) -> pd.DataFrame:
    data = pd.read_csv(file_path)
    if Path(file_path).name == RAW_FILE.name:
        data = clean_dataset(data)
    return data


responses = load_responses(str(DATA_FILE))
required_columns = {
    "User_ID",
    "User_Type",
    "Country",
    "Gender",
    "AI_Tool",
    "AI_Purpose",
    "Satisfaction_Score",
    "Time_Saved_Hours_Per_Week",
    "AI_Usage_Hours_Per_Day",
    "Productivity_Score",
    "Accuracy_Rating",
    "Would_Recommend",
}
missing_columns = sorted(required_columns.difference(responses.columns))
if missing_columns:
    st.error(f"The survey file is missing required columns: {', '.join(missing_columns)}")
    st.stop()


def normalize_category(
    values: pd.Series, aliases: dict[str, str] | None = None
) -> pd.Series:
    cleaned = values.astype("string").str.strip()
    display_values = cleaned.str.title()
    if aliases:
        display_values = cleaned.str.casefold().map(aliases).fillna(display_values)
    return display_values


responses["User_Type"] = normalize_category(responses["User_Type"])
responses["Country"] = normalize_category(responses["Country"])
responses["Gender"] = normalize_category(
    responses["Gender"],
    {"m": "Male", "f": "Female", "non binary": "Non-binary"},
)
responses["AI_Tool"] = normalize_category(
    responses["AI_Tool"],
    {
        "chat gpt": "ChatGPT",
        "chatgpt": "ChatGPT",
        "google gemini": "Gemini",
        "gemini": "Gemini",
        "microsoft copilot": "Microsoft Copilot",
        "copilot": "Microsoft Copilot",
        "perplexity ai": "Perplexity AI",
        "meta ai": "Meta AI",
        "deepseek": "DeepSeek",
    },
)
responses["AI_Purpose"] = normalize_category(responses["AI_Purpose"])
responses["Would_Recommend"] = normalize_category(responses["Would_Recommend"])

st.title("AI Tools Usage Analysis")
st.markdown(
    f"<div class='section-subtitle'>Explore {len(responses):,} survey responses "
    "on AI tool adoption, experience, and reported outcomes.</div>",
    unsafe_allow_html=True,
)
st.caption(
    f"Source: {DATA_FILE.name}. This is survey data, so charts compare respondents "
    "rather than showing changes over time."
)

with st.sidebar:
    st.header("Filters")
    user_types = st.multiselect(
        "User type",
        sorted(responses["User_Type"].dropna().unique()),
        default=sorted(responses["User_Type"].dropna().unique()),
    )
    countries = st.multiselect(
        "Country",
        sorted(responses["Country"].dropna().unique()),
        default=sorted(responses["Country"].dropna().unique()),
    )
    tools = st.multiselect(
        "AI tool",
        sorted(responses["AI_Tool"].dropna().unique()),
        default=sorted(responses["AI_Tool"].dropna().unique()),
    )
    purposes = st.multiselect(
        "Purpose",
        sorted(responses["AI_Purpose"].dropna().unique()),
        default=sorted(responses["AI_Purpose"].dropna().unique()),
    )
    genders = st.multiselect(
        "Gender",
        sorted(responses["Gender"].dropna().unique()),
        default=sorted(responses["Gender"].dropna().unique()),
    )

filtered = responses[
    responses["User_Type"].isin(user_types)
    & responses["Country"].isin(countries)
    & responses["AI_Tool"].isin(tools)
    & responses["AI_Purpose"].isin(purposes)
    & responses["Gender"].isin(genders)
].copy()

if filtered.empty:
    st.warning("No responses match these filters. Select at least one value in each filter.")
    st.stop()

with st.sidebar:
    st.divider()
    st.caption(f"Showing {filtered['User_ID'].nunique():,} of {responses['User_ID'].nunique():,} respondents")

respondent_count = filtered["User_ID"].nunique()
average_satisfaction = filtered["Satisfaction_Score"].mean()
average_time_saved = filtered["Time_Saved_Hours_Per_Week"].mean()
recommend_rate = filtered["Would_Recommend"].eq("Yes").mean()
average_usage = filtered["AI_Usage_Hours_Per_Day"].mean()

overview_tab, tools_tab, outcomes_tab, responses_tab = st.tabs(
    ["Overview", "Tools & purposes", "Outcomes", "Responses"]
)

with overview_tab:
    kpi_columns = st.columns(4)
    kpi_columns[0].metric("Survey responses", f"{respondent_count:,}")
    kpi_columns[1].metric("Avg. satisfaction", f"{average_satisfaction:.1f} / 10")
    kpi_columns[2].metric("Avg. time saved", f"{average_time_saved:.1f} hrs / week")
    kpi_columns[3].metric("Would recommend", f"{recommend_rate:.0%}")
    st.caption(f"Average reported AI use: {average_usage:.1f} hours per day.")

    tool_counts = (
        filtered.groupby("AI_Tool")["User_ID"]
        .nunique()
        .sort_values()
        .rename("Respondents")
        .reset_index()
    )
    user_type_counts = (
        filtered.groupby("User_Type")["User_ID"]
        .nunique()
        .rename("Respondents")
        .reset_index()
    )

    chart_columns = st.columns(2)
    with chart_columns[0]:
        tool_chart = px.bar(
            tool_counts,
            x="Respondents",
            y="AI_Tool",
            orientation="h",
            text="Respondents",
            title="Most-used AI tools",
            color_discrete_sequence=["#426b94"],
        )
        tool_chart.update_traces(textposition="outside")
        st.plotly_chart(tool_chart, width="stretch")
    with chart_columns[1]:
        user_chart = px.pie(
            user_type_counts,
            names="User_Type",
            values="Respondents",
            hole=0.58,
            title="Respondents by user type",
            color_discrete_sequence=["#426b94", "#9ab5d0"],
        )
        st.plotly_chart(user_chart, width="stretch")

    top_tool = tool_counts.iloc[-1]
    top_purpose = filtered["AI_Purpose"].value_counts().idxmax()
    st.subheader("At a glance")
    insight_columns = st.columns(3)
    insight_columns[0].info(
        f"**{top_tool['AI_Tool']}** is the most-used tool in this selection "
        f"({int(top_tool['Respondents']):,} respondents)."
    )
    insight_columns[1].info(f"**{top_purpose}** is the most common reported purpose.")
    insight_columns[2].info(
        f"Respondents report an average of **{average_time_saved:.1f} hours saved per week**."
    )

with tools_tab:
    st.subheader("Tool and purpose breakdown")
    tool_counts = (
        filtered["AI_Tool"]
        .value_counts()
        .rename_axis("AI tool")
        .rename("Respondents")
        .reset_index()
    )
    purpose_counts = (
        filtered["AI_Purpose"]
        .value_counts()
        .rename_axis("Purpose")
        .rename("Respondents")
        .reset_index()
    )
    chart_columns = st.columns(2)
    with chart_columns[0]:
        st.plotly_chart(
            px.bar(
                tool_counts.sort_values("Respondents"),
                x="Respondents",
                y="AI tool",
                orientation="h",
                title="Responses by AI tool",
                color_discrete_sequence=["#426b94"],
            ),
            width="stretch",
        )
    with chart_columns[1]:
        st.plotly_chart(
            px.bar(
                purpose_counts.sort_values("Respondents"),
                x="Respondents",
                y="Purpose",
                orientation="h",
                title="Responses by purpose",
                color_discrete_sequence=["#7b9aba"],
            ),
            width="stretch",
        )

    tool_summary = (
        filtered.groupby("AI_Tool", as_index=False)
        .agg(
            Respondents=("User_ID", "nunique"),
            Satisfaction=("Satisfaction_Score", "mean"),
            Productivity=("Productivity_Score", "mean"),
            Accuracy=("Accuracy_Rating", "mean"),
            Time_saved_hours_per_week=("Time_Saved_Hours_Per_Week", "mean"),
        )
        .sort_values("Respondents", ascending=False)
        .round(1)
    )
    st.dataframe(tool_summary, hide_index=True, width="stretch")

with outcomes_tab:
    st.subheader("Reported outcomes")
    outcome_columns = st.columns(2)
    with outcome_columns[0]:
        st.plotly_chart(
            px.scatter(
                filtered,
                x="AI_Usage_Hours_Per_Day",
                y="Time_Saved_Hours_Per_Week",
                color="User_Type",
                hover_data=["AI_Tool", "AI_Purpose", "Productivity_Score"],
                labels={
                    "AI_Usage_Hours_Per_Day": "AI use (hours per day)",
                    "Time_Saved_Hours_Per_Week": "Time saved (hours per week)",
                    "User_Type": "User type",
                },
                title="AI use and reported time saved",
                color_discrete_sequence=["#426b94", "#91abc5"],
            ),
            width="stretch",
        )
    with outcome_columns[1]:
        recommendation_counts = (
            filtered["Would_Recommend"]
            .value_counts()
            .rename_axis("Response")
            .rename("Respondents")
            .reset_index()
        )
        st.plotly_chart(
            px.pie(
                recommendation_counts,
                names="Response",
                values="Respondents",
                hole=0.58,
                title="Would respondents recommend AI tools?",
                color_discrete_sequence=["#426b94", "#9ab5d0", "#d9e2ec"],
            ),
            width="stretch",
        )

    satisfaction_counts = (
        filtered["Satisfaction_Score"]
        .value_counts()
        .sort_index()
        .rename_axis("Satisfaction score")
        .rename("Respondents")
        .reset_index()
    )
    st.plotly_chart(
        px.bar(
            satisfaction_counts,
            x="Satisfaction score",
            y="Respondents",
            title="Satisfaction score distribution",
            color_discrete_sequence=["#56836f"],
        ),
        width="stretch",
    )
    st.caption("These are descriptive survey results; they do not establish cause and effect.")

with responses_tab:
    st.subheader("Filtered survey responses")
    st.download_button(
        "Download filtered responses",
        data=filtered.to_csv(index=False).encode("utf-8"),
        file_name="ai_usage_survey_filtered.csv",
        mime="text/csv",
    )
    st.dataframe(filtered, hide_index=True, width="stretch")

    st.download_button(
        "Download summary by AI tool",
        data=tool_summary.to_csv(index=False).encode("utf-8"),
        file_name="ai_usage_tool_summary.csv",
        mime="text/csv",
    )
