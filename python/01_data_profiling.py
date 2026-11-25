import pandas as pd
import numpy as np

#Load the raw dataset
df = pd.read_csv("data/raw/City_Budget_and_Expenditures_20260813.csv")

print("Dataset loaded successfully!")

print("\nDataset Shape:")
print(df.shape)

print("\nFirst 5 rows:")
print(df.head())

print("\nColumn Names:")
for column in df.columns:
  print(column)

print("\nData Types:")
print(df.dtypes)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

print("\nNumber of Unique Departments:")
print(df["DEPARTMENT NAME"].nunique())

print("\nDepartments:")
print(df["DEPARTMENT NAME"].unique())

print("\nFiscal Years:")
print(df["BUDGET FISCAL YEAR"].unique())

print("\nNumber of Unique Funds:")
print(df["FUND NAME"].nunique())

print("\nTOP 10 Funds:")
print(df["FUND NAME"].value_counts().head(10))

print("\nAccount Groups:")
print(df["ACCOUNT NAME"].value_counts().head(20))

print("\nAccount Group Name:")
print(df["ACCOUNT GROUP NAME"].value_counts().head(20))

money_columns = [
    "ADOPTED BUDGET AMOUNT",
    "BUDGET CHANGE AMOUNT",
    "BUDGET TRANSFER IN AMOUNT",
    "BUDGET TRANSFER OUT AMOUNT",
    "TOTAL BUDGET",
    "TOTAL EXPENDITURES",
    "ACTUAL EXPENSE",
    "ENCUMBRANCE AMOUNT",
    "PRE-ENCUMBRANCE AMOUNT",
    "BUDGET UNCOMMITTED AMOUNT"
]

print("\nSample Values From Finanical Columns:")
for column in money_columns:
  print(f"\n{column}:")
  print(df[column].head(5).tolist())


print("\nTesting financial columns for numeric conversion:")

for column in money_columns:
    temp = (
        df[column]
        .astype("string")
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )

    converted = pd.to_numeric(temp, errors="coerce")

    invalid = converted.isna() & df[column].notna()

    print(f"{column}: {invalid.sum()} non-numeric values")


print("\nNegative values in financial columns:")

for column in money_columns:
    temp = (
        df[column]
        .astype("string")
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )

    converted = pd.to_numeric(temp, errors="coerce")

    print(f"{column}: {(converted < 0).sum()} negative values")


print("\nZero values in financial columns:")

for column in money_columns:
    temp = (
        df[column]
        .astype("string")
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )

    converted = pd.to_numeric(temp, errors="coerce")

    print(f"{column}: {(converted == 0).sum()} zero values")


print("\nRecords By Fiscal Years:")
print(df["BUDGET FISCAL YEAR"].value_counts().sort_index())

print("\nTOP 20 Departments by Number of Records:")
print(df["DEPARTMENT NAME"].value_counts().head(20))

account_group_missing = df["ACCOUNT GROUP NAME"].isna().sum()
account_group_total = len(df)

print("\nAccount Group Missing:")
print(account_group_missing)

print("\nAccount GrouP Missing Percentage:")
print(round((account_group_missing/account_group_total)*100,2),"%")

print("\nUnique Account Codes:")
print(df["ACCOUNT"].nunique())

print("\nUnique Account Names:")
print(df["ACCOUNT NAME"].nunique())




