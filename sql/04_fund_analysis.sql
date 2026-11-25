
USE municipal_budget_analysis;

-- QUERY 1: Total expenditure by fund
SELECT
    fund_name,
    COUNT(*) AS number_of_records,
    ROUND(SUM(total_expenditures), 2) AS total_expenditure
FROM municipal_budget
GROUP BY fund_name
ORDER BY total_expenditure DESC;

-- QUERY 2: Top 10 funds by expenditure
SELECT
    fund_name,
    ROUND(SUM(total_expenditures), 2) AS total_expenditure
FROM municipal_budget
GROUP BY fund_name
ORDER BY total_expenditure DESC
LIMIT 10;

-- QUERY 3: Top 10 funds by expenditure (FY2012–FY2026)
SELECT
    fund_name,
    ROUND(SUM(total_expenditures), 2) AS total_expenditure
FROM municipal_budget
WHERE fiscal_year BETWEEN 2012 AND 2026
GROUP BY fund_name
ORDER BY total_expenditure DESC
LIMIT 10;
