import pandas as pd

OUTPUT_FILE = "data/processed/finance_clean.csv"


def clean_bank_data_from_excel(excel_path):
    """
    Clean bank statement where transaction table
    starts at row 19 (0-based index 18)
    """

    # =========================
    # Read Excel
    # =========================
    df = pd.read_excel(
        excel_path,
        skiprows=18,
        engine="openpyxl"
    )

    # Defensive rename
    df.columns = [
        "Txn Date",
        "Value Date",
        "Description",
        "Ref No",
        "Branch Code",
        "Debit",
        "Credit",
        "Balance"
    ]

    # Drop non-transaction rows
    df = df.dropna(subset=["Txn Date"])

    # =========================
    # Date parsing
    # =========================
    df["date"] = pd.to_datetime(
        df["Txn Date"],
        format="%d-%b-%y",
        errors="coerce"
    )
    df = df.dropna(subset=["date"])

    # =========================
    # Numeric cleanup
    # =========================
    for col in ["Debit", "Credit", "Balance"]:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", "", regex=False)
            .replace("nan", "0")
        )
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # =========================
    # Amount & type
    # =========================
    df["amount"] = df["Credit"] - df["Debit"]
    df["type"] = df["amount"].apply(
        lambda x: "income" if x > 0 else "expense"
    )
    df["amount"] = df["amount"].abs()

    # =========================
    # CATEGORY LOGIC (IMPORTANT)
    # =========================
    def categorize(desc, txn_type):
        d = str(desc).lower()

        # ---------- INCOME ----------
        if txn_type == "income":
            if "easebuzz" in d:
                return "Payment Gateway Settlement"
            if "amazon" in d:
                return "Marketplace Settlement"
            if "gokwik" in d:
                return "Online Sales"
            if "internal ac" in d:
                return "Internal Transfer / Capital"
            return "Other Income"

        # ---------- EXPENSE ----------
        else:
            if "facebook" in d or "ads" in d or "bulk posting" in d:
                return "Advertising & Marketing"

            if "blue dart" in d or "delhivery" in d:
                return "Logistics & Shipping"

            if "salary payment" in d:
                return "Salary / Payroll"

            if any(v in d for v in [
                "rainbow marketing",
                "krishna packaging",
                "trend max"
            ]):
                return "Vendor / Raw Material"

            if "adobe" in d or "apple" in d:
                return "Software / Subscriptions"

            if any(p in d for p in [
                "aashutosh",
                "dineshkumar",
                "ganatra"
            ]):
                return "Owner / Partner Transfer"

            if "insufficient" in d or "decline charge" in d:
                return "Bank Charges"

            return "Other Expense"

    df["category"] = df.apply(
        lambda x: categorize(x["Description"], x["type"]),
        axis=1
    )

    # =========================
    # SOURCE
    # =========================
    def source(desc):
        d = str(desc).lower()
        if "neft" in d:
            return "NEFT"
        if "imps" in d:
            return "IMPS"
        if "pos" in d or "debit card" in d:
            return "CARD"
        return "OTHER"

    df["source"] = df["Description"].apply(source)

    # =========================
    # Final output
    # =========================
    final_df = df[
        ["date", "type", "category", "amount", "source", "Description", "Balance"]
    ]

    final_df.columns = [
        "date",
        "type",
        "category",
        "amount",
        "source",
        "description",
        "balance"
    ]

    #final_df.to_csv(OUTPUT_FILE, index=False) //temp comented

    return final_df
