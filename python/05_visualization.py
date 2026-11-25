import os
import pandas as pd
import matplotlib.pyplot as plt


# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INPUT_FILE = os.path.join(
    BASE_DIR,
    "data",
    "cleaned",
    "municipal_budget_cleaned.csv"
)

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "reports",
    "charts"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

df = pd.read_csv(INPUT_FILE)

df["BUDGET FISCAL YEAR"] = pd.to_numeric(
    df["BUDGET FISCAL YEAR"],
    errors="coerce"
)

df["TOTAL EXPENDITURES"] = pd.to_numeric(
    df["TOTAL EXPENDITURES"],
    errors="coerce"
)

df["TOTAL BUDGET"] = pd.to_numeric(
    df["TOTAL BUDGET"],
    errors="coerce"
)

df["DEPARTMENT NAME"] = df["DEPARTMENT NAME"].astype(str).str.strip()
df["FUND NAME"] = df["FUND NAME"].astype(str).str.strip()


# ---------------------------------------------------------
# PRIMARY ANALYSIS PERIOD
# FY2012-FY2026
# FY2027 excluded because of incomplete coverage
# ---------------------------------------------------------

analysis_df = df[
    (df["BUDGET FISCAL YEAR"] >= 2012) &
    (df["BUDGET FISCAL YEAR"] <= 2026)
].copy()


# ---------------------------------------------------------
# 1. TOTAL MUNICIPAL EXPENDITURE BY FISCAL YEAR
# ---------------------------------------------------------

yearly_expenditure = (
    analysis_df
    .groupby("BUDGET FISCAL YEAR")["TOTAL EXPENDITURES"]
    .sum()
    .sort_index()
)

plt.figure(figsize=(12, 7))

plt.plot(
    yearly_expenditure.index,
    yearly_expenditure.values,
    marker="o",
    linewidth=2
)

plt.title("Total Municipal Expenditure by Fiscal Year")
plt.xlabel("Fiscal Year")
plt.ylabel("Total Expenditure")

plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "expenditure_by_year.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ---------------------------------------------------------
# 2. TOP 15 DEPARTMENTS BY TOTAL EXPENDITURE
# ---------------------------------------------------------

department_expenditure = (
    analysis_df
    .groupby("DEPARTMENT NAME")["TOTAL EXPENDITURES"]
    .sum()
    .sort_values(ascending=False)
)

top_departments = department_expenditure.head(15).sort_values()

plt.figure(figsize=(13, 8))

plt.barh(
    top_departments.index,
    top_departments.values
)

plt.title("Top 15 Departments by Total Expenditure")
plt.xlabel("Total Expenditure")
plt.ylabel("Department")

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "top_departments_expenditure.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ---------------------------------------------------------
# 3. TOP 15 DEPARTMENTS EXCLUDING WATER AND POWER
# ---------------------------------------------------------

department_without_wp = department_expenditure.drop(
    labels=["WATER AND POWER"],
    errors="ignore"
)

top_departments_without_wp = (
    department_without_wp
    .head(15)
    .sort_values()
)

plt.figure(figsize=(13, 8))

plt.barh(
    top_departments_without_wp.index,
    top_departments_without_wp.values
)

plt.title(
    "Top 15 Departments by Expenditure "
    "(Excluding Water and Power)"
)

plt.xlabel("Total Expenditure")
plt.ylabel("Department")

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "top_departments_excluding_water_power.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ---------------------------------------------------------
# 4. WATER AND POWER EXPENDITURE BY YEAR
# ---------------------------------------------------------

water_power = analysis_df[
    analysis_df["DEPARTMENT NAME"] == "WATER AND POWER"
]

water_power_yearly = (
    water_power
    .groupby("BUDGET FISCAL YEAR")["TOTAL EXPENDITURES"]
    .sum()
    .sort_index()
)

plt.figure(figsize=(12, 7))

plt.plot(
    water_power_yearly.index,
    water_power_yearly.values,
    marker="o",
    linewidth=2
)

plt.title("Water and Power Expenditure by Fiscal Year")
plt.xlabel("Fiscal Year")
plt.ylabel("Total Expenditure")

plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "water_power_expenditure.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ---------------------------------------------------------
# 5. TOP 15 FUNDS BY TOTAL EXPENDITURE
# ---------------------------------------------------------

fund_expenditure = (
    analysis_df
    .groupby("FUND NAME")["TOTAL EXPENDITURES"]
    .sum()
    .sort_values(ascending=False)
)

top_funds = fund_expenditure.head(15).sort_values()

plt.figure(figsize=(13, 8))

plt.barh(
    top_funds.index,
    top_funds.values
)

plt.title("Top 15 Funds by Total Expenditure")
plt.xlabel("Total Expenditure")
plt.ylabel("Fund")

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "top_funds_expenditure.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ---------------------------------------------------------
# 6. TOP 15 DEPARTMENTS: BUDGET VS EXPENDITURE
# ---------------------------------------------------------

department_budget = (
    analysis_df
    .groupby("DEPARTMENT NAME")
    .agg(
        TOTAL_BUDGET=("TOTAL BUDGET", "sum"),
        TOTAL_EXPENDITURES=("TOTAL EXPENDITURES", "sum")
    )
)

# Exclude departments with no reported budget
budget_reported = department_budget[
    department_budget["TOTAL_BUDGET"] > 0
].copy()

top_budget_departments = (
    budget_reported
    .sort_values(
        "TOTAL_EXPENDITURES",
        ascending=False
    )
    .head(15)
    .sort_values("TOTAL_EXPENDITURES")
)

plt.figure(figsize=(14, 9))

positions = range(len(top_budget_departments))

plt.barh(
    list(positions),
    top_budget_departments["TOTAL_BUDGET"],
    label="Total Budget"
)

plt.barh(
    list(positions),
    top_budget_departments["TOTAL_EXPENDITURES"],
    label="Total Expenditures"
)

plt.yticks(
    list(positions),
    top_budget_departments.index
)

plt.title("Top 15 Departments: Budget vs Expenditure")
plt.xlabel("Amount")
plt.ylabel("Department")
plt.legend()

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "budget_vs_expenditure.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ---------------------------------------------------------
# 7. TOP 15 DEPARTMENTS BY BUDGET UTILIZATION
# ---------------------------------------------------------

department_performance = (
    analysis_df
    .groupby("DEPARTMENT NAME")
    .agg(
        TOTAL_BUDGET=("TOTAL BUDGET", "sum"),
        TOTAL_EXPENDITURES=("TOTAL EXPENDITURES", "sum")
    )
)

# Only departments with a reported budget
department_performance = department_performance[
    department_performance["TOTAL_BUDGET"] > 0
].copy()

department_performance["UTILIZATION %"] = (
    department_performance["TOTAL_EXPENDITURES"]
    / department_performance["TOTAL_BUDGET"]
) * 100

# Exclude over-budget departments from this chart.
# Utilization above 100% is handled separately in EDA.
within_budget = department_performance[
    department_performance["UTILIZATION %"] <= 100
]

top_utilization = (
    within_budget
    .sort_values(
        "UTILIZATION %",
        ascending=False
    )
    .head(15)
    .sort_values("UTILIZATION %")
)

plt.figure(figsize=(13, 8))

plt.barh(
    top_utilization.index,
    top_utilization["UTILIZATION %"]
)

plt.title(
    "Top 15 Departments by Budget Utilization"
)

plt.xlabel("Budget Utilization (%)")
plt.ylabel("Department")

plt.xlim(0, 100)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "department_utilization.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ---------------------------------------------------------
# COMPLETION MESSAGE
# ---------------------------------------------------------

print("\n--- VISUALIZATION COMPLETE ---")

print(f"Analysis period: FY2012-FY2026")
print(f"Charts saved to: {OUTPUT_DIR}")

print("\nGenerated charts:")

for filename in sorted(os.listdir(OUTPUT_DIR)):
    if filename.endswith(".png"):
        print(f"- {filename}")