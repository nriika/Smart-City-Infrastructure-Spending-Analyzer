import pandas as pd
import numpy as np

df = pd.read_csv("data/cleaned/municipal_budget_cleaned.csv")

print("Cleaned Dataset loaded.")
print("Original Shape:",df.shape)

#Budget Variance
df["BUDGET VARIANCE"] = (df["TOTAL BUDGET"]-df["TOTAL EXPENDITURES"])

#Budget Utilization %
df["BUDGET UTILIZATION %"] = np.where(
  df["TOTAL BUDGET"] > 0,
  (df["TOTAL EXPENDITURES"]/df["TOTAL BUDGET"]) * 100,
  np.nan
)

print("\nRecords with zero total budget:")
print((df["TOTAL BUDGET"] == 0).sum())

print("\nRecords with unavailable budget utilization:")
print(df["BUDGET UTILIZATION %"].isna().sum())

#Over Budget Flag
df["BUDGET STATUS"] = np.select(
    [
        (df["TOTAL BUDGET"] <= 0) & (df["TOTAL EXPENDITURES"] <= 0),
        (df["TOTAL BUDGET"] <= 0) & (df["TOTAL EXPENDITURES"] > 0),
        (df["TOTAL BUDGET"] > 0) & (df["TOTAL EXPENDITURES"] > df["TOTAL BUDGET"])
    ],
    [
        "No Budget Allocated",
        "Expenditure Without Budget",
        "Over Budget"
    ],
    default="Under Budget"
)

#Remaining Budget
df["REMAINING BUDGET"] = (df["TOTAL BUDGET"] - df["TOTAL EXPENDITURES"])

#Total Committed
df["TOTAL COMMITTED"] = (
    df["ENCUMBRANCE AMOUNT"]
    + df["PRE-ENCUMBRANCE AMOUNT"]
)

#Calculated Budget
df["CALCULATED BUDGET"] = (
    df["ADOPTED BUDGET AMOUNT"]
    + df["BUDGET CHANGE AMOUNT"]
    + df["BUDGET TRANSFER IN AMOUNT"]
    - df["BUDGET TRANSFER OUT AMOUNT"]
)

#Display The New Features
new_columns = [
  "BUDGET VARIANCE",
  "BUDGET UTILIZATION %",
  "BUDGET STATUS",
  "REMAINING BUDGET",
  "TOTAL COMMITTED",
  "CALCULATED BUDGET"
]

print("\nNew Columns Created.")
print(df[new_columns].head(10))

#Over-Budget Analysis
print("\nBudget Status Distribution:")
print(df["BUDGET STATUS"].value_counts())

#Utilization Statistics
print("\nBudget Utilization Statistics:")
print(df["BUDGET UTILIZATION %"].describe())

#Budget Calculation Validation
df["BUDGET DIFFERENCE CHECK"] = (
  df["TOTAL BUDGET"] - df["CALCULATED BUDGET"]
)

print("\nBudget Calculation Check:")
print(df["BUDGET DIFFERENCE CHECK"].describe())

print("\nRecords where calculated budget differs from total budget:",
      (df["BUDGET DIFFERENCE CHECK"].abs() > 0.01).sum()
)


# Investigate budget calculation differences

difference_records = df[
    df["BUDGET DIFFERENCE CHECK"].abs() > 0.01
].copy()

print("\nNumber of meaningful budget differences:")
print(len(difference_records))

print("\nLargest budget calculation differences:")

print(
    difference_records[
        [
            "BUDGET FISCAL YEAR",
            "DEPARTMENT NAME",
            "FUND NAME",
            "ACCOUNT NAME",
            "TOTAL BUDGET",
            "ADOPTED BUDGET AMOUNT",
            "BUDGET CHANGE AMOUNT",
            "BUDGET TRANSFER IN AMOUNT",
            "BUDGET TRANSFER OUT AMOUNT",
            "CALCULATED BUDGET",
            "BUDGET DIFFERENCE CHECK"
        ]
    ]
    .sort_values(
        "BUDGET DIFFERENCE CHECK",
        key=lambda x: x.abs(),
        ascending=False
    )
    .head(10)
)

#Save The Processed Dataset
output_path = "data/processed/municipal_budget_feature_engineered.csv"
df.to_csv(output_path, index = False)

print("\nFeature-engineered dataset saved to:")
print(output_path)