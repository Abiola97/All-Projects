-- Identify customers with at least one funded savings plan and one funded investment plan
SELECT 
    u.id AS owner_id,
    CONCAT(u.first_name, ' ', u.last_name) AS name,
    savings.savings_count,
    investments.investment_count,
    ROUND(deposits.total_deposits / 100.0, 2) AS total_deposits
FROM cowrywise_data_analyst_assessment_db.users_customuser u

-- Count savings plans
JOIN (
    SELECT owner_id, COUNT(*) AS savings_count
    FROM cowrywise_data_analyst_assessment_db.plans_plan
    WHERE is_regular_savings = 1
    GROUP BY owner_id
) AS savings ON u.id = savings.owner_id

-- Count investment plans
JOIN (
    SELECT owner_id, COUNT(*) AS investment_count
    FROM cowrywise_data_analyst_assessment_db.plans_plan
    WHERE is_a_fund = 1
    GROUP BY owner_id
) AS investments ON u.id = investments.owner_id

-- Sum deposits
JOIN (
    SELECT owner_id, SUM(confirmed_amount) AS total_deposits
    FROM cowrywise_data_analyst_assessment_db.savings_savingsaccount
    GROUP BY owner_id
) AS deposits ON u.id = deposits.owner_id

ORDER BY total_deposits DESC;

