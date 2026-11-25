
USE municipal_budget_analysis;

-- QUERY 1: Total expenditure by department
SELECT
    department_name,
    COUNT(*) AS number_of_records,
    ROUND(SUM(total_expenditures), 2) AS total_expenditure
FROM municipal_budget
GROUP BY department_name
ORDER BY total_expenditure DESC;

-- QUERY 2: Top 10 departments by expenditure
SELECT
    department_name,
    ROUND(SUM(total_expenditures), 2) AS total_expenditure
FROM municipal_budget
GROUP BY department_name
ORDER BY total_expenditure DESC
LIMIT 10;

-- QUERY 3: Department-wise expenditure for FY2012–FY2026
SELECT
    department_name,
    ROUND(SUM(total_expenditures), 2) AS total_expenditure
FROM municipal_budget
WHERE fiscal_year BETWEEN 2012 AND 2026
GROUP BY department_name
ORDER BY total_expenditure DESC
LIMIT 10;
