import pandas as pd
import tempfile
import os
from src.data_cleaning import clean_bank_data


def process_uploaded_excel(uploaded_file):
    """
    Save uploaded Excel,
    convert rows to raw text-like file,
    run existing bank cleaning logic,
    return cleaned DataFrame
    """

    # Save uploaded Excel temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
        tmp.write(uploaded_file.read())
        excel_path = tmp.name

    # Read Excel WITHOUT pandas auto-parsing
    df_excel = pd.read_excel(
        excel_path,
        header=None,
        dtype=str,
        engine="openpyxl"
    )

    # Convert each row into a single text line
    temp_txt = excel_path.replace(".xlsx", ".txt")
    with open(temp_txt, "w", encoding="utf-8") as f:
        for _, row in df_excel.iterrows():
            line = " ".join([str(x) if x != "nan" else "" for x in row.tolist()])
            f.write(line + "\n")

    # Run your stable cleaning logic on text
    clean_bank_data(raw_file=temp_txt)

    # Load cleaned result
    clean_df = pd.read_csv(
        "data/processed/finance_clean.csv",
        parse_dates=["date"]
    )

    return clean_df
