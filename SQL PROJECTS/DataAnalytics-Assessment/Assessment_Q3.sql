-- Flag active savings and investment plans with no inflow in the last 365 days
WITH last_txn AS (
    SELECT 
        s.plan_id,
        s.owner_id,
        MAX(s.transaction_date) AS last_transaction_date
    FROM cowrywise_data_analyst_assessment_db.savings_savingsaccount s
    GROUP BY s.plan_id, s.owner_id
),
plan_type AS (
    SELECT 
        p.id AS plan_id,
        CASE 
            WHEN p.is_regular_savings = 1 THEN 'Savings'
            WHEN p.is_a_fund = 1 THEN 'Investment'
            ELSE 'Other'
        END AS type
    FROM cowrywise_data_analyst_assessment_db.plans_plan p
    WHERE p.is_archived = 0 AND p.is_deleted = 0
),
inactivity AS (
    SELECT 
        l.plan_id,
        l.owner_id,
        pt.type,
        l.last_transaction_date,
        DATEDIFF(CURRENT_DATE, l.last_transaction_date) AS inactivity_days
    FROM last_txn l
    JOIN plan_type pt ON l.plan_id = pt.plan_id
    WHERE l.last_transaction_date < CURRENT_DATE - INTERVAL 365 DAY
)
SELECT * FROM inactivity
ORDER BY inactivity_days DESC;