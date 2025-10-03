-- Estimate CLV based on tenure and transaction volume
WITH txn AS (
    SELECT 
        s.owner_id,
        COUNT(*) AS total_transactions,
        ROUND(AVG(s.confirmed_amount * 0.001) / 100.0, 2) AS avg_profit_per_transaction
    FROM cowrywise_data_analyst_assessment_db.savings_savingsaccount s
    GROUP BY s.owner_id
),
tenure AS (
    SELECT 
        u.id AS customer_id,
        CONCAT(u.first_name, ' ', u.last_name) AS name,
        TIMESTAMPDIFF(MONTH, u.date_joined, CURRENT_DATE) AS tenure_months
    FROM cowrywise_data_analyst_assessment_db.users_customuser u
)
SELECT 
    t.customer_id,
    t.name,
    t.tenure_months,
    tx.total_transactions,
    ROUND((tx.total_transactions / t.tenure_months) * 12 * tx.avg_profit_per_transaction, 2) AS estimated_clv
FROM tenure t
JOIN txn tx ON t.customer_id = tx.owner_id
WHERE t.tenure_months > 0
ORDER BY estimated_clv DESC;