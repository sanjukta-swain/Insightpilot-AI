import pandas as pd

def clean_data(df):
    """
    Cleans the uploaded dataset.
    """

    original_rows = len(df)

    # Remove duplicate rows
    duplicates_removed = df.duplicated().sum()
    df = df.drop_duplicates()

    # Count missing values before cleaning
    missing_before = df.isnull().sum().sum()

    # Fill missing values
    for column in df.columns:

     if pd.api.types.is_numeric_dtype(df[column]):
        df[column] = df[column].fillna(df[column].mean())

    else:
        mode = df[column].mode()

        if not mode.empty:
            df[column] = df[column].fillna(mode[0])
    # Count missing values after cleaning
    missing_after = df.isnull().sum().sum()

    summary = {
        "Original Rows": original_rows,
        "Rows After Cleaning": len(df),
        "Duplicates Removed": duplicates_removed,
        "Missing Values Before": missing_before,
        "Missing Values After": missing_after
    }
    
    return df, summary