SELECT
    COUNT(*) AS total_records,
    SUM(adopted_budget_amount < 0) AS negative_budget_records,
    SUM(total_expenditures < 0) AS negative_expenditure_records
FROM municipal_budget;

SELECT
    COUNT(*) AS zero_budget_records
FROM municipal_budget
WHERE adopted_budget_amount = 0;

SELECT
    COUNT(*) AS over_budget_records
FROM municipal_budget
WHERE total_expenditures > adopted_budget_amount
AND adopted_budget_amount > 0;

SELECT
    ROUND(SUM(adopted_budget_amount), 2) AS total_adopted_budget,
    ROUND(SUM(total_expenditures), 2) AS total_expenditure
FROM municipal_budget;

SELECT
    COUNT(*) AS zero_budget_records,
    ROUND(SUM(total_expenditures), 2) AS expenditure_without_adopted_budget
FROM municipal_budget
WHERE adopted_budget_amount = 0
AND total_expenditures > 0;

SELECT
    department_name,
    COUNT(*) AS number_of_records,
    ROUND(SUM(total_expenditures), 2) AS total_expenditure
FROM municipal_budget
WHERE adopted_budget_amount = 0
AND total_expenditures > 0
GROUP BY department_name
ORDER BY total_expenditure DESC
LIMIT 10;

SELECT
    ROUND(SUM(adopted_budget_amount), 2) AS adopted_budget,
    ROUND(SUM(total_budget), 2) AS final_total_budget,
    ROUND(SUM(total_expenditures), 2) AS total_expenditure
FROM municipal_budget;