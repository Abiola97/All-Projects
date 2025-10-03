-- Categorize customers based on average transactions per month
WITH txn_summary AS (
    SELECT 
        s.owner_id,
        COUNT(*) AS txn_count,
        TIMESTAMPDIFF(MONTH, MIN(s.transaction_date), MAX(s.transaction_date)) + 1 AS active_months
    FROM cowrywise_data_analyst_assessment_db.savings_savingsaccount s
    GROUP BY s.owner_id
),
categorized AS (
    SELECT 
        CASE 
            WHEN txn_count / active_months >= 10 THEN 'High Frequency'
            WHEN txn_count / active_months BETWEEN 3 AND 9 THEN 'Medium Frequency'
            ELSE 'Low Frequency'
        END AS frequency_category,
        COUNT(*) AS customer_count,
        ROUND(AVG(txn_count / active_months), 2) AS avg_transactions_per_month
    FROM txn_summary
    GROUP BY frequency_category
)
SELECT * FROM categorized;