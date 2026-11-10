import pandas as pd
import numpy as np
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = PROJECT_ROOT / "data"
INPUT_FILE = DATA_ROOT / "AI_Usage_and_Impact_on_Students_and_Professionals.csv"
OUTPUT_FILE = DATA_ROOT / "AI_Usage_and_Impact_on_Students_and_Professionals_cleaned.csv"


def clean_dataset(dataframe):
	"""Standardize text and missing values, remove empty records, and impute gaps."""
	cleaned = dataframe.copy()

	# Trim headers and text cells, and treat common textual null markers as missing.
	cleaned.columns = cleaned.columns.astype(str).str.strip()
	text_columns = cleaned.select_dtypes(include=["object", "string"]).columns
	for column in text_columns:
		cleaned[column] = cleaned[column].str.strip()
	cleaned.replace(
		to_replace=r"(?i)^\s*(?:na|n/a|null|none|nan)\s*$",
		value=np.nan,
		regex=True,
		inplace=True,
	)
	for column in ("Monthly_Income", "Monthly_AI_Cost"):
		if column in cleaned.columns:
			cleaned[column] = pd.to_numeric(
				cleaned[column]
				.astype("string")
				.str.replace("$", "", regex=False)
				.str.replace(",", "", regex=False)
				.str.strip(),
				errors="coerce",
			).astype("float64")

	for column in cleaned.select_dtypes(include=["object", "string"]).columns:
		values = cleaned[column].astype("string")
		has_unit_suffix = values.str.contains(
			r"\s*(?:hrs?|yrs?)\s*$", case=False, na=False, regex=True
		)
		if has_unit_suffix.any():
			cleaned[column] = pd.to_numeric(
				values.str.replace(
					r"\s*(?:hrs?|yrs?)\s*$", "", case=False, regex=True
				),
				errors="coerce",
			).astype("float64")

	if "AI_Tool" in cleaned.columns:
		cleaned["AI_Tool"] = cleaned["AI_Tool"].str.casefold().str.replace(
			r"\s+", " ", regex=True
		)

	cleaned.replace([np.inf, -np.inf], np.nan, inplace=True)
	cleaned.dropna(axis=0, how="all", inplace=True)
	cleaned.dropna(axis=1, how="all", inplace=True)
	cleaned.drop_duplicates(inplace=True)

	# Use the median for numeric fields and the most frequent value for others.
	for column in cleaned.select_dtypes(include=[np.number]).columns:
		median = cleaned[column].median()
		if pd.notna(median):
			cleaned[column] = cleaned[column].fillna(median)

	for column in cleaned.columns:
		if column not in cleaned.select_dtypes(include=[np.number]).columns:
			modes = cleaned[column].mode(dropna=True)
			fill_value = modes.iloc[0] if not modes.empty else "Unknown"
			cleaned[column] = cleaned[column].fillna(fill_value)

	return cleaned.reset_index(drop=True)


if __name__ == "__main__":
	df = pd.read_csv(INPUT_FILE)
	cleaned_df = clean_dataset(df)
	cleaned_df.to_csv(OUTPUT_FILE, index=False)
	print(f"Cleaned dataset saved to {OUTPUT_FILE}")