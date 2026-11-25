
USE municipal_budget_analysis;

-- QUERY 1: Compare budget components
SELECT
    fiscal_year,
    ROUND(SUM(adopted_budget_amount), 2) AS adopted_budget,
    ROUND(SUM(budget_change_amount), 2) AS budget_changes,
    ROUND(SUM(budget_transfer_in_amount), 2) AS transfers_in,
    ROUND(SUM(budget_transfer_out_amount), 2) AS transfers_out,
    ROUND(SUM(total_budget), 2) AS total_budget,
    ROUND(SUM(total_expenditures), 2) AS total_expenditure
FROM municipal_budget
WHERE fiscal_year BETWEEN 2012 AND 2026
GROUP BY fiscal_year
ORDER BY fiscal_year;

-- QUERY 2: Overall budget composition
SELECT
    ROUND(SUM(adopted_budget_amount), 2) AS adopted_budget,
    ROUND(SUM(budget_change_amount), 2) AS budget_changes,
    ROUND(SUM(budget_transfer_in_amount), 2) AS transfers_in,
    ROUND(SUM(budget_transfer_out_amount), 2) AS transfers_out,
    ROUND(SUM(total_budget), 2) AS total_budget,
    ROUND(SUM(total_expenditures), 2) AS total_expenditure
FROM municipal_budget;

-- QUERY 3: Verify total budget calculation

SELECT
    fiscal_year,

    ROUND(SUM(adopted_budget_amount), 2)
        AS adopted_budget,

    ROUND(SUM(budget_change_amount), 2)
        AS budget_changes,

    ROUND(SUM(budget_transfer_in_amount), 2)
        AS transfers_in,

    ROUND(SUM(budget_transfer_out_amount), 2)
        AS transfers_out,

    ROUND(
        SUM(
            adopted_budget_amount
            + budget_change_amount
            + budget_transfer_in_amount
            - budget_transfer_out_amount
        ), 2
    ) AS calculated_budget,

    ROUND(SUM(total_budget), 2)
        AS recorded_total_budget,

    ROUND(
        SUM(total_budget) -
        SUM(
            adopted_budget_amount
            + budget_change_amount
            + budget_transfer_in_amount
            - budget_transfer_out_amount
        ), 2
    ) AS difference

FROM municipal_budget
WHERE fiscal_year BETWEEN 2012 AND 2026
GROUP BY fiscal_year
ORDER BY fiscal_year;

-- QUERY 4: Departments where expenditure exceeds total budget
-- FY2012 to FY2026

SELECT
    department_name,

    COUNT(*) AS record_count,

    ROUND(SUM(total_budget), 2)
        AS total_budget,

    ROUND(SUM(total_expenditures), 2)
        AS total_expenditure,

    ROUND(
        SUM(total_expenditures) - SUM(total_budget), 2
    ) AS expenditure_above_budget,

    ROUND(
        SUM(total_expenditures) /
        NULLIF(SUM(total_budget), 0) * 100, 2
    ) AS utilization_percentage

FROM municipal_budget

WHERE fiscal_year BETWEEN 2012 AND 2026

GROUP BY department_name

HAVING SUM(total_expenditures) > SUM(total_budget)

ORDER BY expenditure_above_budget DESC;

-- QUERY 5: Annual budget and expenditure
-- for departments with zero recorded budgets

SELECT
    fiscal_year,
    department_name,

    COUNT(*) AS record_count,

    ROUND(SUM(adopted_budget_amount), 2)
        AS adopted_budget,

    ROUND(SUM(total_budget), 2)
        AS total_budget,

    ROUND(SUM(total_expenditures), 2)
        AS total_expenditure

FROM municipal_budget

WHERE fiscal_year BETWEEN 2012 AND 2026

AND department_name IN (
    'WATER AND POWER',
    'AIRPORTS',
    'HARBOR'
)

GROUP BY
    fiscal_year,
    department_name

ORDER BY
    fiscal_year,
    department_name;


-- QUERY 6: Fund-wise expenditure for the three departments

SELECT
    department_name,
    fund_name,

    COUNT(*) AS record_count,

    ROUND(SUM(adopted_budget_amount), 2)
        AS adopted_budget,

    ROUND(SUM(budget_change_amount), 2)
        AS budget_changes,

    ROUND(SUM(budget_transfer_in_amount), 2)
        AS transfers_in,

    ROUND(SUM(budget_transfer_out_amount), 2)
        AS transfers_out,

    ROUND(SUM(total_budget), 2)
        AS total_budget,

    ROUND(SUM(total_expenditures), 2)
        AS total_expenditure

FROM municipal_budget

WHERE fiscal_year BETWEEN 2012 AND 2026

AND department_name IN (
    'WATER AND POWER',
    'AIRPORTS',
    'HARBOR'
)

GROUP BY
    department_name,
    fund_name

HAVING SUM(total_expenditures) > 0

ORDER BY
    department_name,
    total_expenditure DESC;

-- QUERY 7: Examine expenditure components
-- for Water and Power, Airports and Harbor

SELECT
    department_name,

    ROUND(SUM(total_expenditures), 2)
        AS total_expenditure,

    ROUND(SUM(actual_expense), 2)
        AS actual_expense,

    ROUND(SUM(encumbrance_amount), 2)
        AS encumbrance,

    ROUND(SUM(pre_encumbrance_amount), 2)
        AS pre_encumbrance,

    ROUND(SUM(budget_uncommitted_amount), 2)
        AS budget_uncommitted

FROM municipal_budget

WHERE fiscal_year BETWEEN 2012 AND 2026

AND department_name IN (
    'WATER AND POWER',
    'AIRPORTS',
    'HARBOR'
)

GROUP BY department_name

ORDER BY total_expenditure DESC;

-- QUERY 8: Check budget and expenditure components
-- at individual fund level

SELECT
    department_name,
    fund_name,

    COUNT(*) AS record_count,

    ROUND(SUM(total_budget), 2)
        AS total_budget,

    ROUND(SUM(total_expenditures), 2)
        AS total_expenditure,

    ROUND(SUM(actual_expense), 2)
        AS actual_expense,

    ROUND(SUM(budget_uncommitted_amount), 2)
        AS budget_uncommitted

FROM municipal_budget

WHERE fiscal_year BETWEEN 2012 AND 2026

AND department_name IN (
    'WATER AND POWER',
    'AIRPORTS',
    'HARBOR'
)

GROUP BY
    department_name,
    fund_name

HAVING SUM(total_expenditures) > 0

ORDER BY
    department_name,
    total_expenditure DESC;