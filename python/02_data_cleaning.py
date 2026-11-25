import pandas as pd
import numpy as np

df = pd.read_csv("data/raw/City_Budget_and_Expenditures_20260813.csv")

print("Raw Dataset Loaded.")
print("Original Shape:",df.shape)

#create clean dataframe
df_clean = df.copy()

#Convert financial columns to numeric
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

for column in money_columns:
  df_clean[column] = (
    df_clean[column]
    .astype("string")
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False)
    .str.strip()
    .astype(float)

  )

#Clean text columns
text_columns = [
    "DEPARTMENT NAME",
    "FUND NAME",
    "ACCOUNT NAME",
    "ACCOUNT GROUP NAME"
]

for column in text_columns:
  df_clean[column] = (
    df_clean[column]
    .astype("string")
    .str.strip()
  )

#Validations
print("\nFinancial Column Data Types:")
print(df_clean[money_columns].dtypes)

print("\nMissing values after financial conversions:")
for column in money_columns:
  print(column, df_clean[column].isna().sum())

print("\nDuplicate rows after cleaning:")
print(df_clean.duplicated().sum())

print("\nClean Dataset Shape:")
print(df_clean.shape)

#Save the cleaned dataset
output_path = "data/cleaned/municipal_budget_cleaned.csv"
df_clean.to_csv(output_path, index = False)

print("\nCleaned Dataset saved to:")
print(output_path)