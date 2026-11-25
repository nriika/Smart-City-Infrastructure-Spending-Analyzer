import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load feature-engineered dataset
df = pd.read_csv(
    "data/processed/municipal_budget_feature_engineered.csv"
)

print("Feature-engineered dataset loaded.")
print("Dataset shape:", df.shape)

print("\n---Dataset Overview---")

print("\nNumber Of Records:", len(df))

print("\nFiscal Year Range:",
      df["BUDGET FISCAL YEAR"].min(),
      "to",df["BUDGET FISCAL YEAR"].max()
)

print(
    "Number of departments:",
    df["DEPARTMENT NAME"].nunique()
)

print(
    "Number of funds:",
    df["FUND NAME"].nunique()
)

print(
    "Number of account codes:",
    df["ACCOUNT"].nunique()
)

print(
    "Number of account names:",
    df["ACCOUNT NAME"].nunique()
)

#Expenditure by Fiscal Year
yearly_expenditure = (
    df.groupby("BUDGET FISCAL YEAR")["TOTAL EXPENDITURES"]
    .sum()
    .reset_index()
)

print("\n--- EXPENDITURE BY FISCAL YEAR ---")
print(yearly_expenditure)

plt.figure(figsize=(12,6))
plt.plot(
  yearly_expenditure["BUDGET FISCAL YEAR"],
  yearly_expenditure["TOTAL EXPENDITURES"],
  marker = "o"
)

plt.title("Total Municipal Expenditure by Fiscal Year")
plt.xlabel("Fiscal Year")
plt.ylabel("Total Expenditure")

plt.tight_layout()
plt.show()

#Departments Expenditure
department_expenditure = (
    df.groupby("DEPARTMENT NAME")["TOTAL EXPENDITURES"]
    .sum()
    .sort_values(ascending=False)
)

print("\n--- TOP 15 DEPARTMENTS BY EXPENDITURE ---")
print(department_expenditure.head(15))

top_departments = department_expenditure.head(15).sort_values()

plt.figure(figsize=(10, 7))

plt.barh(
    top_departments.index,
    top_departments.values
)

plt.title("Top 15 Departments by Total Expenditure")
plt.xlabel("Total Expenditure")
plt.ylabel("Department")

plt.tight_layout()
plt.show()


# Water And Power Expenditure By Year

water_power = df[
    df["DEPARTMENT NAME"] == "WATER AND POWER"
]

water_power_yearly = (
    water_power
    .groupby("BUDGET FISCAL YEAR")["TOTAL EXPENDITURES"]
    .sum()
    .reset_index()
)

print("\n--- WATER AND POWER EXPENDITURE BY YEAR ---")
print(water_power_yearly)

plt.figure(figsize=(12, 6))

plt.plot(
    water_power_yearly["BUDGET FISCAL YEAR"],
    water_power_yearly["TOTAL EXPENDITURES"],
    marker="o"
)

plt.title("Water and Power Expenditure by Fiscal Year")
plt.xlabel("Fiscal Year")
plt.ylabel("Total Expenditure")

plt.tight_layout()
plt.show()

#Expenditure Excluding Water & Power

df_without_water_power = df[
    df["DEPARTMENT NAME"] != "WATER AND POWER"
]

department_expenditure_without_wp = (
    df_without_water_power
    .groupby("DEPARTMENT NAME")["TOTAL EXPENDITURES"]
    .sum()
    .sort_values(ascending=False)
)

print("\n--- TOP 15 DEPARTMENTS BY EXPENDITURE EXCLUDING WATER AND POWER ---")
print(department_expenditure_without_wp.head(15))

top_departments_without_wp = (
    department_expenditure_without_wp
    .head(15)
    .sort_values()
)

plt.figure(figsize=(10, 7))

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
plt.show()

# DEPARTMENT BUDGET VS EXPENDITURE

department_financials = (
    df.groupby("DEPARTMENT NAME")[
        [
            "TOTAL BUDGET",
            "TOTAL EXPENDITURES"
        ]
    ]
    .sum()
    .sort_values(
        "TOTAL EXPENDITURES",
        ascending=False
    )
)

print("\n--- TOP 15 DEPARTMENTS: BUDGET VS EXPENDITURE ---")
print(department_financials.head(15))

# =========================================
# DEPARTMENT UTILIZATION
# ONLY DEPARTMENTS WITH REPORTED BUDGET
# =========================================

department_utilization = (
    df[df["TOTAL BUDGET"] > 0]
    .groupby("DEPARTMENT NAME")
    .agg(
        TOTAL_BUDGET=("TOTAL BUDGET", "sum"),
        TOTAL_EXPENDITURES=("TOTAL EXPENDITURES", "sum")
    )
)

department_utilization["UTILIZATION %"] = (
    department_utilization["TOTAL_EXPENDITURES"]
    / department_utilization["TOTAL_BUDGET"]
) * 100

department_utilization = (
    department_utilization
    .sort_values("UTILIZATION %", ascending=False)
)

print("\n--- DEPARTMENT UTILIZATION ---")
print(department_utilization.head(15))

# =========================================
# EXPENDITURE WITHOUT REPORTED BUDGET
# =========================================

no_budget_expenditure = df[
    df["BUDGET STATUS"] == "Expenditure Without Budget"
]

print("\n--- EXPENDITURE WITHOUT REPORTED BUDGET ---")

print(
    "Number of records:",
    len(no_budget_expenditure)
)

print(
    "Total expenditure:",
    no_budget_expenditure["TOTAL EXPENDITURES"].sum()
)

no_budget_by_department = (
    no_budget_expenditure
    .groupby("DEPARTMENT NAME")["TOTAL EXPENDITURES"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTop departments by expenditure without reported budget:")
print(no_budget_by_department.head(15))

# =========================================
# DEPARTMENTS WITH ZERO REPORTED BUDGET
# =========================================

zero_budget_departments = (
    df.groupby("DEPARTMENT NAME")
    .agg(
        TOTAL_BUDGET=("TOTAL BUDGET", "sum"),
        TOTAL_EXPENDITURES=("TOTAL EXPENDITURES", "sum")
    )
)

zero_budget_departments = (
    zero_budget_departments[
        (zero_budget_departments["TOTAL_BUDGET"] == 0)
        & (zero_budget_departments["TOTAL_EXPENDITURES"] > 0)
    ]
    .sort_values(
        "TOTAL_EXPENDITURES",
        ascending=False
    )
)

print("\n--- DEPARTMENTS WITH EXPENDITURE BUT ZERO REPORTED BUDGET ---")
print(zero_budget_departments)

fund_expenditure = (
    df.groupby("FUND NAME")["TOTAL EXPENDITURES"]
    .sum()
    .sort_values(ascending=False)
)

print("\n--- TOP 15 FUNDS BY EXPENDITURE ---")
print(fund_expenditure.head(15))

# =========================================
# TOP FUNDS BY EXPENDITURE
# =========================================

top_funds = (
    fund_expenditure
    .head(15)
    .sort_values()
)

plt.figure(figsize=(10, 7))

plt.barh(
    top_funds.index,
    top_funds.values
)

plt.title("Top 15 Funds by Total Expenditure")
plt.xlabel("Total Expenditure")
plt.ylabel("Fund")

plt.tight_layout()
plt.show()

# =========================================
# EXPENDITURE CONCENTRATION
# =========================================

total_expenditure = df["TOTAL EXPENDITURES"].sum()

top_5_department_expenditure = (
    department_expenditure
    .head(5)
    .sum()
)

top_5_percentage = (
    top_5_department_expenditure
    / total_expenditure
) * 100

print("\n--- EXPENDITURE CONCENTRATION ---")

print(
    "Total expenditure:",
    total_expenditure
)

print(
    "Top 5 department expenditure:",
    top_5_department_expenditure
)

print(
    "Top 5 departments share of total expenditure:",
    top_5_percentage,
    "%"
)

top_5_fund_expenditure = (
    fund_expenditure
    .head(5)
    .sum()
)

top_5_fund_percentage = (
    top_5_fund_expenditure
    / total_expenditure
) * 100

print(
    "\nTop 5 funds share of total expenditure:",
    top_5_fund_percentage,
    "%"
)

# =========================================
# YEAR-OVER-YEAR EXPENDITURE GROWTH
# =========================================

yearly_expenditure["YOY CHANGE"] = (
    yearly_expenditure["TOTAL EXPENDITURES"]
    .diff()
)

yearly_expenditure["YOY GROWTH %"] = (
    yearly_expenditure["TOTAL EXPENDITURES"]
    .pct_change() * 100
)

print("\n--- YEAR-OVER-YEAR EXPENDITURE CHANGE ---")

print(
    yearly_expenditure[
        [
            "BUDGET FISCAL YEAR",
            "TOTAL EXPENDITURES",
            "YOY CHANGE",
            "YOY GROWTH %"
        ]
    ]
)

largest_increases = (
    yearly_expenditure
    .sort_values(
        "YOY CHANGE",
        ascending=False
    )
    .head(10)
)

print("\n--- LARGEST YEAR-OVER-YEAR INCREASES ---")
print(largest_increases)

largest_decreases = (
    yearly_expenditure
    .sort_values(
        "YOY CHANGE",
        ascending=True
    )
    .head(10)
)

print("\n--- LARGEST YEAR-OVER-YEAR DECREASES ---")
print(largest_decreases)

# =========================================
# INVESTIGATE 2010-2012 STRUCTURAL BREAK
# DEPARTMENT LEVEL
# =========================================

break_period = df[
    df["BUDGET FISCAL YEAR"].between(2009, 2013)
]

break_department = (
    break_period
    .groupby(
        ["BUDGET FISCAL YEAR", "DEPARTMENT NAME"]
    )["TOTAL EXPENDITURES"]
    .sum()
    .reset_index()
)

print("\n--- DEPARTMENT EXPENDITURE: 2009-2013 ---")

print(
    break_department
    .sort_values(
        ["BUDGET FISCAL YEAR", "TOTAL EXPENDITURES"],
        ascending=[True, False]
    )
)

print("\n--- TOP 10 DEPARTMENTS FOR EACH YEAR: 2009-2013 ---")

for year in range(2009, 2014):

    yearly_departments = (
        break_period[
            break_period["BUDGET FISCAL YEAR"] == year
        ]
        .groupby("DEPARTMENT NAME")["TOTAL EXPENDITURES"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    print(f"\nFiscal Year {year}")
    print(yearly_departments)

# =========================================
# TOP FUNDS DURING 2010-2012
# =========================================

break_funds = (
    break_period
    .groupby(
        ["BUDGET FISCAL YEAR", "FUND NAME"]
    )["TOTAL EXPENDITURES"]
    .sum()
    .reset_index()
)

print("\n--- TOP FUNDS: 2010-2012 ---")

for year in range(2010, 2013):

    yearly_funds = (
        break_period[
            break_period["BUDGET FISCAL YEAR"] == year
        ]
        .groupby("FUND NAME")["TOTAL EXPENDITURES"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    print(f"\nFiscal Year {year}")
    print(yearly_funds)

# =========================================
# WATER & POWER CONTRIBUTION
# =========================================

water_power_break = (
    break_period[
        break_period["DEPARTMENT NAME"] == "WATER AND POWER"
    ]
    .groupby("BUDGET FISCAL YEAR")["TOTAL EXPENDITURES"]
    .sum()
)

total_break_yearly = (
    break_period
    .groupby("BUDGET FISCAL YEAR")["TOTAL EXPENDITURES"]
    .sum()
)

water_power_share = (
    water_power_break
    / total_break_yearly
) * 100

print("\n--- WATER & POWER SHARE OF TOTAL EXPENDITURE ---")

print(
    pd.DataFrame({
        "TOTAL EXPENDITURES": total_break_yearly,
        "WATER AND POWER EXPENDITURES": water_power_break,
        "WATER AND POWER SHARE %": water_power_share
    })
)

# =========================================
# DEPARTMENT COVERAGE OVER TIME
# =========================================

print("\n--- DEPARTMENT COVERAGE OVER TIME ---")

coverage_departments = [
    "WATER AND POWER",
    "AIRPORTS",
    "HARBOR",
    "NON-DEPARTMENTAL - GENERAL",
    "NON-DEPARTMENTAL - APPROPRIATIONS TO SPECIAL PURPOSE FUND"
]

for department in coverage_departments:

    department_records = (
        df[
            df["DEPARTMENT NAME"] == department
        ]
        .groupby("BUDGET FISCAL YEAR")
        .size()
    )

    print(f"\n{department}")
    print(department_records)

# =========================================
# RECORD COVERAGE BY YEAR
# =========================================

print("\n--- RECORD COUNT BY FISCAL YEAR ---")

records_by_year = (
    df
    .groupby("BUDGET FISCAL YEAR")
    .size()
)

print(records_by_year)

# =========================================
# NUMBER OF DEPARTMENTS BY YEAR
# =========================================

print("\n--- NUMBER OF DEPARTMENTS REPRESENTED BY YEAR ---")

departments_by_year = (
    df
    .groupby("BUDGET FISCAL YEAR")["DEPARTMENT NAME"]
    .nunique()
)

print(departments_by_year)

# =========================================
# NEW DEPARTMENTS APPEARING IN 2012
# =========================================

print("\n--- NEW DEPARTMENTS APPEARING IN 2012 ---")

departments_2011 = set(
    df.loc[
        df["BUDGET FISCAL YEAR"] == 2011,
        "DEPARTMENT NAME"
    ].dropna()
)

departments_2012 = set(
    df.loc[
        df["BUDGET FISCAL YEAR"] == 2012,
        "DEPARTMENT NAME"
    ].dropna()
)

new_departments_2012 = sorted(
    departments_2012 - departments_2011
)

print("Departments represented in 2011:", len(departments_2011))
print("Departments represented in 2012:", len(departments_2012))

print("\nDepartments appearing in 2012 but not 2011:")
for department in new_departments_2012:
    print(department)

print("\nNumber of newly represented departments:")
print(len(new_departments_2012))

# =========================================
# EXPENDITURE FROM NEWLY REPRESENTED
# DEPARTMENTS IN 2012
# =========================================

print("\n--- EXPENDITURE FROM NEWLY REPRESENTED DEPARTMENTS ---")

new_department_expenditure = (
    df[
        (df["BUDGET FISCAL YEAR"] == 2012) &
        (df["DEPARTMENT NAME"].isin(new_departments_2012))
    ]
    .groupby("DEPARTMENT NAME")["TOTAL EXPENDITURES"]
    .sum()
    .sort_values(ascending=False)
)

print(new_department_expenditure)

print("\nTotal expenditure from newly represented departments:")

print(
    new_department_expenditure.sum()
)

# =========================================
# CONTRIBUTION OF NEW DEPARTMENTS
# =========================================

expenditure_2011 = (
    df.loc[
        df["BUDGET FISCAL YEAR"] == 2011,
        "TOTAL EXPENDITURES"
    ].sum()
)

expenditure_2012 = (
    df.loc[
        df["BUDGET FISCAL YEAR"] == 2012,
        "TOTAL EXPENDITURES"
    ].sum()
)

yoy_increase = expenditure_2012 - expenditure_2011

new_department_expenditure_total = (
    new_department_expenditure.sum()
)

contribution_percentage = (
    new_department_expenditure_total /
    yoy_increase
) * 100

print("\n--- 2012 EXPENDITURE INCREASE ANALYSIS ---")

print("2011 expenditure:", expenditure_2011)
print("2012 expenditure:", expenditure_2012)
print("Increase:", yoy_increase)

print(
    "Expenditure from newly represented departments:",
    new_department_expenditure_total
)

print(
    "Share of 2011-2012 increase:",
    contribution_percentage,
    "%"
)

# =========================================
# 2027 COVERAGE CHECK
# =========================================

print("\n--- 2027 COVERAGE CHECK ---")

years_to_check = [2025, 2026, 2027]

for year in years_to_check:

    year_data = df[
        df["BUDGET FISCAL YEAR"] == year
    ]

    print(f"\nFiscal Year {year}")

    print("Number of records:", len(year_data))

    print(
        "Number of departments:",
        year_data["DEPARTMENT NAME"].nunique()
    )

    print(
        "Number of funds:",
        year_data["FUND NAME"].nunique()
    )

    print(
        "Total expenditure:",
        year_data["TOTAL EXPENDITURES"].sum()
    )

# =========================================
# DEPARTMENT COVERAGE CHANGE: 2026 vs 2027
# =========================================

departments_2026 = set(
    df.loc[
        df["BUDGET FISCAL YEAR"] == 2026,
        "DEPARTMENT NAME"
    ].dropna()
)

departments_2027 = set(
    df.loc[
        df["BUDGET FISCAL YEAR"] == 2027,
        "DEPARTMENT NAME"
    ].dropna()
)

missing_in_2027 = sorted(
    departments_2026 - departments_2027
)

print("\n--- DEPARTMENTS IN 2026 BUT NOT 2027 ---")

for department in missing_in_2027:
    print(department)

print(
    "\nNumber of departments present in 2026 but absent in 2027:",
    len(missing_in_2027)
)

# =========================================
# 2026 VS 2027 DEPARTMENT EXPENDITURE
# =========================================

comparison = (
    df[
        df["BUDGET FISCAL YEAR"].isin([2026, 2027])
    ]
    .groupby(
        ["DEPARTMENT NAME", "BUDGET FISCAL YEAR"]
    )["TOTAL EXPENDITURES"]
    .sum()
    .unstack(fill_value=0)
)

comparison["CHANGE"] = (
    comparison.get(2027, 0)
    - comparison.get(2026, 0)
)

print("\n--- LARGEST DEPARTMENT EXPENDITURE DECLINES: 2026 VS 2027 ---")

print(
    comparison
    .sort_values("CHANGE")
    .head(15)
)

# =========================================
# PRIMARY ANALYSIS PERIOD
# =========================================

analysis_df = df[
    (df["BUDGET FISCAL YEAR"] >= 2012) &
    (df["BUDGET FISCAL YEAR"] <= 2026)
].copy()

print("\n--- PRIMARY ANALYSIS PERIOD ---")

print("Analysis period: FY2012-FY2026")

print("Number of records:", len(analysis_df))

print(
    "Fiscal years:",
    analysis_df["BUDGET FISCAL YEAR"].min(),
    "to",
    analysis_df["BUDGET FISCAL YEAR"].max()
)

print(
    "Departments:",
    analysis_df["DEPARTMENT NAME"].nunique()
)

print(
    "Funds:",
    analysis_df["FUND NAME"].nunique()
)


# =========================================
# DEPARTMENT BUDGET PERFORMANCE
# =========================================

department_analysis = (
    analysis_df
    .groupby("DEPARTMENT NAME")
    .agg(
        TOTAL_BUDGET=("TOTAL BUDGET", "sum"),
        TOTAL_EXPENDITURES=("TOTAL EXPENDITURES", "sum"),
        TOTAL_COMMITTED=("TOTAL COMMITTED", "sum"),
        RECORD_COUNT=("DEPARTMENT NAME", "size")
    )
)

department_analysis["REMAINING_BUDGET"] = (
    department_analysis["TOTAL_BUDGET"]
    - department_analysis["TOTAL_EXPENDITURES"]
)

department_analysis["UTILIZATION %"] = np.where(
    department_analysis["TOTAL_BUDGET"] > 0,
    (
        department_analysis["TOTAL_EXPENDITURES"]
        / department_analysis["TOTAL_BUDGET"]
    ) * 100,
    np.nan
)

print("\n--- DEPARTMENT BUDGET PERFORMANCE ---")

print(
    department_analysis
    .sort_values(
        "TOTAL_EXPENDITURES",
        ascending=False
    )
    .head(20)
)

# =========================================
# DEPARTMENTS WITH LARGEST REMAINING BUDGET
# =========================================

print("\n--- DEPARTMENTS WITH LARGEST REMAINING BUDGET ---")

print(
    department_analysis[
        department_analysis["TOTAL_BUDGET"] > 0
    ]
    .sort_values(
        "REMAINING_BUDGET",
        ascending=False
    )
    .head(15)
)

# =========================================
# DEPARTMENTS WITH REPORTED BUDGET
# =========================================

reported_budget_departments = department_analysis[
    department_analysis["TOTAL_BUDGET"] > 0
].copy()

print("\n--- DEPARTMENTS WITH REPORTED BUDGET ---")

print(
    reported_budget_departments
    .sort_values(
        "UTILIZATION %",
        ascending=False
    )
    .head(15)
)

# =========================================
# LOWEST BUDGET UTILIZATION
# =========================================

print("\n--- LOWEST BUDGET UTILIZATION ---")

print(
    reported_budget_departments
    .sort_values(
        "UTILIZATION %",
        ascending=True
    )
    .head(15)
)

# =========================================
# OVER-BUDGET DEPARTMENTS
# =========================================

print("\n--- OVER-BUDGET DEPARTMENTS ---")

over_budget_departments = reported_budget_departments[
    reported_budget_departments["TOTAL_EXPENDITURES"]
    > reported_budget_departments["TOTAL_BUDGET"]
].copy()

print(
    over_budget_departments[
        [
            "TOTAL_BUDGET",
            "TOTAL_EXPENDITURES",
            "REMAINING_BUDGET",
            "UTILIZATION %"
        ]
    ]
    .sort_values(
        "UTILIZATION %",
        ascending=False
    )
)
