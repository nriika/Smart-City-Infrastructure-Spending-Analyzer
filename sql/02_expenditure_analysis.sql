
USE municipal_budget_analysis;

-- QUERY 1: Overall financial summary
SELECT
    COUNT(*) AS total_records,
    MIN(fiscal_year) AS earliest_fiscal_year,
    MAX(fiscal_year) AS latest_fiscal_year,
    ROUND(SUM(adopted_budget_amount), 2) AS total_adopted_budget,
    ROUND(SUM(total_budget), 2) AS total_final_budget,
    ROUND(SUM(total_expenditures), 2) AS total_expenditure
FROM municipal_budget;

-- QUERY 2: Expenditure by financial year
SELECT
    fiscal_year,
    ROUND(SUM(total_expenditures), 2) AS annual_expenditure
FROM municipal_budget
GROUP BY fiscal_year
ORDER BY fiscal_year;

-- QUERY 3: Budget versus expenditure by financial year
SELECT
    fiscal_year,
    ROUND(SUM(total_budget), 2) AS total_budget,
    ROUND(SUM(total_expenditures), 2) AS total_expenditure,
    ROUND(SUM(total_budget) - SUM(total_expenditures), 2) AS budget_variance
FROM municipal_budget
GROUP BY fiscal_year
ORDER BY fiscal_year;

-- QUERY 4: Highest expenditure financial years
SELECT
    fiscal_year,
    ROUND(SUM(total_expenditures), 2) AS annual_expenditure
FROM municipal_budget
GROUP BY fiscal_year
ORDER BY annual_expenditure DESC
LIMIT 10;
