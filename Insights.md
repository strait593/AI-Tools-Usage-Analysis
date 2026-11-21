# Insights

## Executive summary

The dashboard describes **288 unique survey respondents** across 19 fields. The overall picture is positive: respondents report using AI **2.9 hours per day**, saving **5.8 hours per week**, and rating satisfaction at **6.1/10** and productivity at **5.2/10**. **60.8%** say they would recommend their AI tool.

The clearest relationship in the data is between AI usage and reported outcomes. Daily usage has a strong positive association with weekly time saved (**r = 0.74**) and a moderate-to-strong association with productivity (**r = 0.64**). These are descriptive survey relationships, not proof that AI caused the reported gains.

## Most important findings

### 1. Adoption is concentrated in a few tools

- **ChatGPT** is the leading tool: 129 of 288 respondents (**44.8%**) after standardizing the `chat gpt` and `chatgpt` variants.
- **Gemini** follows with 39 respondents (**13.5%**), then **Microsoft Copilot** with 33 (**11.5%**) and **Claude** with 31 (**10.8%**).
- Together, these four tools account for more than four fifths of the cleaned sample.

The dashboard should use normalized tool names; otherwise variants in the raw data split the ChatGPT and Gemini totals unnecessarily.

### 2. Coding is the dominant use case

- Coding: 78 respondents (**27.1%**)
- Writing: 49 (**17.0%**)
- Studying: 40 (**13.9%**)
- Research: 38 (**13.2%**)

Coding is the largest use case, but its average reported results are below several other purposes: **4.90 productivity**, **5.89 satisfaction**, and **5.47 hours saved per week**. Writing respondents report higher time savings (**6.94 hours**) and satisfaction (**6.29**), while office-work respondents have the highest productivity (**5.95**) in a small group of 11.

### 3. Usage is strongly associated with time saved and productivity

The simple linear relationships are:

- Daily usage to weekly time saved: **r = 0.74**, **R-squared = 0.55**
- Daily usage to productivity: **r = 0.64**, **R-squared = 0.40**
- Daily usage to satisfaction: **r = 0.42**, **R-squared = 0.18**

The time-saved model implies approximately **1.23 additional hours saved per week for each additional hour of daily AI use**. This should be presented as an observed association because the survey may include recall bias and self-selection.

AI usage is not strongly associated with accuracy (**r = 0.05**) or work/study hours (**r = -0.03**). More use does not appear to correspond with higher accuracy in this cross-section.

### 4. Students and professionals report broadly similar outcomes

- **52.4%** of respondents are students; **47.6%** are professionals.
- Students report slightly more daily use (**3.0 vs 2.9 hours**) and time saved (**6.0 vs 5.5 hours**).
- Professionals report slightly higher productivity (**5.27 vs 5.18**) and accuracy (**3.47 vs 3.37**).
- Recommendation rates are close: **61.6%** of students and **59.9%** of professionals.

The notebook's student-versus-professional efficiency test found no statistically meaningful difference in time saved per AI-use hour (**p = 0.508** for the t-test and **p = 0.585** for Mann-Whitney U). The practical differences are small, so user type does not appear to be a primary segmentation variable.

## Tool-level patterns

After name normalization:

| Tool | Respondents | Avg. satisfaction | Avg. productivity | Avg. time saved/week | Would recommend |
|---|---:|---:|---:|---:|---:|
| ChatGPT | 129 | 6.26 | 5.29 | 5.87 | 61.2% |
| Gemini | 39 | 5.69 | 5.06 | 5.38 | 66.7% |
| Microsoft Copilot | 33 | 6.30 | 5.48 | 6.53 | 57.6% |
| Claude | 31 | 6.10 | 5.27 | 5.57 | 61.3% |
| Perplexity AI | 23 | 5.83 | 4.69 | 5.61 | 56.5% |
| Grammarly | 14 | 6.29 | 5.11 | 5.49 | 64.3% |
| Meta AI | 10 | 6.10 | 5.15 | 4.79 | 40.0% |
| DeepSeek | 9 | 6.11 | 5.53 | 6.21 | 66.7% |

**Microsoft Copilot** has the strongest average productivity and time savings among tools with meaningful sample sizes, although ChatGPT is far better represented in the sample. **Grammarly** has the highest accuracy rating (**3.86**), but the result is based on only 14 respondents. Tool comparisons should therefore emphasize uncertainty and avoid ranking very small samples.

## Recommendations

1. **Feature use intensity and time saved first.** They show the clearest positive relationship and are likely to be the most useful headline measures.
2. **Segment by purpose, not only tool or user type.** Writing and office work appear especially productive, while coding is the most common use case and has more room for measurable improvement.
3. **Improve the coding experience.** It represents over a quarter of the sample but has lower satisfaction and productivity than office work and customer support.
4. **Do not over-interpret tool superiority.** Tool counts and outcomes are uneven, and tool choice may reflect differences in user type, purpose, and experience.
5. **Validate the survey with longitudinal data.** Repeated usage and outcome measurements would better establish whether increased AI use precedes gains.

## Data quality and limitations

- The raw file contains 300 records, while cleaning reduces it to **288 rows** after removing 12 duplicate records and imputing missing values.
- The raw file has 204 missing cell values across text and numeric fields. Numeric gaps are median-imputed and categorical gaps are mode-imputed.
- Tool, country, gender, and education labels contain capitalization and spelling variants. The dashboard already normalizes several aliases, but the underlying cleaned data could also be standardized more systematically.
- The data contains possible self-report outliers, including ages above 52, daily AI use above 7.75 hours, and monthly income above the IQR upper bound. These records should be reviewed rather than silently removed.
- `Monthly_AI_Cost` and accuracy show little association with reported benefits in this sample.
- The sample is cross-sectional and is not representative by design. The findings describe the 288 survey respondents and cannot be generalized to all users.
