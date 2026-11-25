
USE municipal_budget_analysis;

-- QUERY 1: Overall budget utilization
SELECT
    ROUND(SUM(total_budget), 2) AS total_budget,
    ROUND(SUM(total_expenditures), 2) AS total_expenditure,
    ROUND(
        SUM(total_expenditures) / NULLIF(SUM(total_budget), 0) * 100,
        2
    ) AS budget_utilization_percentage
FROM municipal_budget;

-- QUERY 2: Budget utilization by financial year
SELECT
    fiscal_year,
    ROUND(SUM(total_budget), 2) AS total_budget,
    ROUND(SUM(total_expenditures), 2) AS total_expenditure,
    ROUND(
        SUM(total_expenditures) / NULLIF(SUM(total_budget), 0) * 100,
        2
    ) AS budget_utilization_percentage
FROM municipal_budget
WHERE fiscal_year BETWEEN 2012 AND 2026
GROUP BY fiscal_year
ORDER BY fiscal_year;

-- QUERY 3: Department-wise budget utilization
SELECT
    department_name,
    ROUND(SUM(total_budget), 2) AS total_budget,
    ROUND(SUM(total_expenditures), 2) AS total_expenditure,
    ROUND(
        SUM(total_expenditures) / NULLIF(SUM(total_budget), 0) * 100,
        2
    ) AS budget_utilization_percentage
FROM municipal_budget
WHERE fiscal_year BETWEEN 2012 AND 2026
GROUP BY department_name
HAVING SUM(total_budget) > 0
ORDER BY budget_utilization_percentage DESC;
