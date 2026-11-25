USE municipal_budget_analysis;

-- VIEW 1: Annual Expenditure Trends

CREATE OR REPLACE VIEW vw_annual_expenditure AS

SELECT
    fiscal_year,

    COUNT(*) AS total_records,

    COUNT(DISTINCT department_name)
        AS department_count,

    ROUND(SUM(total_budget), 2)
        AS total_budget,

    ROUND(SUM(total_expenditures), 2)
        AS total_expenditure,

    ROUND(
        SUM(total_expenditures) - SUM(total_budget), 2
    ) AS budget_expenditure_difference

FROM municipal_budget

WHERE fiscal_year BETWEEN 2012 AND 2026

GROUP BY fiscal_year;


CREATE OR REPLACE VIEW vw_department_expenditure AS
SELECT
    department_name,
    COUNT(*) AS total_records,
    COUNT(DISTINCT fiscal_year) AS years_covered,
    ROUND(SUM(total_budget), 2) AS total_budget,
    ROUND(SUM(total_expenditures), 2) AS total_expenditure,
    ROUND(
        SUM(total_expenditures) - SUM(total_budget), 2
    ) AS budget_expenditure_difference
FROM municipal_budget
WHERE fiscal_year BETWEEN 2012 AND 2026
GROUP BY department_name;



CREATE OR REPLACE VIEW vw_fund_expenditure AS
SELECT
    fund_name,
    COUNT(*) AS total_records,
    COUNT(DISTINCT fiscal_year) AS years_covered,
    COUNT(DISTINCT department_name) AS department_count,
    ROUND(SUM(total_budget), 2) AS total_budget,
    ROUND(SUM(total_expenditures), 2) AS total_expenditure
FROM municipal_budget
WHERE fiscal_year BETWEEN 2012 AND 2026
GROUP BY fund_name;


CREATE OR REPLACE VIEW vw_department_budget_utilization AS
SELECT
    department_name,
    COUNT(*) AS total_records,
    ROUND(SUM(total_budget), 2) AS total_budget,
    ROUND(SUM(total_expenditures), 2) AS total_expenditure,
    ROUND(
        SUM(total_expenditures) /
        NULLIF(SUM(total_budget), 0) * 100,
        2
    ) AS budget_utilization_percentage,
    CASE
        WHEN SUM(total_budget) = 0
             AND SUM(total_expenditures) > 0
            THEN 'Expenditure Without Recorded Budget'
        WHEN SUM(total_budget) = 0
             AND SUM(total_expenditures) = 0
            THEN 'No Budget or Expenditure'
        WHEN SUM(total_expenditures) > SUM(total_budget)
            THEN 'Expenditure Above Budget'
        ELSE 'Expenditure Within Budget'
    END AS budget_status
FROM municipal_budget
WHERE fiscal_year BETWEEN 2012 AND 2026
GROUP BY department_name;


CREATE OR REPLACE VIEW vw_annual_department_expenditure AS
SELECT
    fiscal_year,
    department_name,
    COUNT(*) AS total_records,
    ROUND(SUM(total_budget), 2) AS total_budget,
    ROUND(SUM(total_expenditures), 2) AS total_expenditure
FROM municipal_budget
WHERE fiscal_year BETWEEN 2012 AND 2026
GROUP BY
    fiscal_year,
    department_name;



CREATE OR REPLACE VIEW vw_annual_fund_expenditure AS
SELECT
    fiscal_year,
    fund_name,
    COUNT(*) AS total_records,
    ROUND(SUM(total_budget), 2) AS total_budget,
    ROUND(SUM(total_expenditures), 2) AS total_expenditure
FROM municipal_budget
WHERE fiscal_year BETWEEN 2012 AND 2026
GROUP BY
    fiscal_year,
    fund_name;


CREATE OR REPLACE VIEW vw_annual_budget_variance AS
SELECT
    fiscal_year,
    department_name,
    ROUND(SUM(total_budget), 2) AS total_budget,
    ROUND(SUM(total_expenditures), 2) AS total_expenditure,
    ROUND(
        SUM(total_budget) - SUM(total_expenditures), 2
    ) AS budget_variance,
    CASE
        WHEN SUM(total_budget) = 0
             AND SUM(total_expenditures) > 0
            THEN 'No Recorded Budget'
        WHEN SUM(total_budget) = 0
             AND SUM(total_expenditures) = 0
            THEN 'No Budget or Expenditure'
        WHEN SUM(total_budget) < SUM(total_expenditures)
            THEN 'Negative Variance'
        ELSE 'Positive Variance'
    END AS variance_status
FROM municipal_budget
WHERE fiscal_year BETWEEN 2012 AND 2026
GROUP BY
    fiscal_year,
    department_name;
