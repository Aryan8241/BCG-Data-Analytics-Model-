Python 3.12.1 (tags/v3.12.1:2305ca5, Dec  7 2023, 22:03:25) [MSC v.1937 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> import pandas as pd
... import numpy as np
... 
... def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
...     """Remove irrelevant or redundant columns."""
...     # Drop columns with only 1 unique value
...     nunique = df.nunique()
...     to_drop = nunique[nunique == 1].index
...     df = df.drop(columns=to_drop)
... 
...     # Drop duplicate columns (if any)
...     df = df.loc[:, ~df.columns.duplicated()]
... 
...     return df
... 
... 
... def expand_date_features(df: pd.DataFrame, date_columns: list) -> pd.DataFrame:
...     """Expand datetime columns into year, month, day, etc."""
...     for col in date_columns:
...         df[col] = pd.to_datetime(df[col], errors="coerce")
...         df[f"{col}_year"] = df[col].dt.year
...         df[f"{col}_month"] = df[col].dt.month
...         df[f"{col}_day"] = df[col].dt.day
...         df[f"{col}_dayofweek"] = df[col].dt.dayofweek
...         df[f"{col}_is_weekend"] = (df[col].dt.dayofweek >= 5).astype(int)
...     return df
... 
... 
... def combine_features(df: pd.DataFrame) -> pd.DataFrame:
...     """Example of combining features to create better predictors."""
...     if {"tenure", "monthly_charges"}.issubset(df.columns):
...         df["total_spent"] = df["tenure"] * df["monthly_charges"]
... 
...     if {"num_calls", "num_messages"}.issubset(df.columns):
...         df["total_interactions"] = df["num_calls"] + df["num_messages"]
... 
...     return df
... 
... 
... def join_datasets(df1: pd.DataFrame, df2: pd.DataFrame, on: str) -> pd.DataFrame:
...     """Join two datasets on a common key."""
...     return pd.merge(df1, df2, on=on, how="left")
... 
... 
... def feature_engineering_pipeline(df: pd.DataFrame, date_columns: list = None) -> pd.DataFrame:
...     df = clean_columns(df)
...     if date_columns:
...         df = expand_date_features(df, date_columns)
    df = combine_features(df)
    return df


if __name__ == "__main__":
    # Example usage (replace with your actual dataset paths)
    df = pd.read_csv("customer_data.csv")
    df = feature_engineering_pipeline(df, date_columns=["signup_date", "last_active_date"])

    # Save engineered dataset
    df.to_csv("customer_data_engineered.csv", index=False)
