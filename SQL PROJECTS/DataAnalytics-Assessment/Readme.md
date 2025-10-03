
## 🧠 Cowry Data Analyst Assessment

This repository contains SQL Server solutions for the Cowry Wise Data Analyst Assessment. The queries demonstrate business insight, query optimization, and strategic thinking—core skills for data-driven product management.

---

### 📁 Files Included

| File               | Description                                      |
|--------------------|--------------------------------------------------|
| `Assessment_Q1.sql` | High-value customer identification               |
| `Assessment_Q2.sql` | Transaction frequency segmentation               |
| `Assessment_Q3.sql` | Inactivity detection for retention               |
| `Assessment_Q4.sql` | Customer Lifetime Value (CLV) estimation         |

---

### 🔍 Problem Breakdown & Sample Queries

#### Q1: High-Value Customers with Multiple Products
**Objective**: Identify customers with both savings and investment products.

```sql
SELECT u.id AS customer_id,
       COUNT(DISTINCT s.id) AS savings_accounts,
       COUNT(DISTINCT p.id) AS investment_plans,
       SUM(s.total_deposit + p.amount) / 100 AS total_value_ngn
FROM users_customuser u
LEFT JOIN savings_savingsaccount s ON u.id = s.user_id
LEFT JOIN plans_plan p ON u.id = p.user_id
GROUP BY u.id
HAVING COUNT(DISTINCT s.id) > 0 AND COUNT(DISTINCT p.id) > 0;
```

**Impact**: Enables targeted upselling and loyalty campaigns.

---

#### Q2: Transaction Frequency Analysis
**Objective**: Segment customers by average monthly transaction count.

```sql
WITH txn_summary AS (
  SELECT user_id,
         COUNT(*) AS total_txns,
         DATEDIFF(MONTH, MIN(created_at), MAX(created_at)) + 1 AS active_months
  FROM transactions_transaction
  GROUP BY user_id
)
SELECT user_id,
       total_txns,
       active_months,
       ROUND(CAST(total_txns AS FLOAT) / active_months, 2) AS avg_txn_per_month,
       CASE
         WHEN total_txns = 0 THEN 'No Activity'
         WHEN total_txns BETWEEN 1 AND 5 THEN 'Low'
         WHEN total_txns BETWEEN 6 AND 15 THEN 'Medium'
         ELSE 'High'
       END AS frequency_segment
FROM txn_summary;
```

**Impact**: Supports personalized engagement and retention strategies.

---

#### Q3: Inactive Account Detection
**Objective**: Flag accounts with no activity in the past 365 days.

```sql
SELECT DISTINCT user_id
FROM (
  SELECT user_id, MAX(created_at) AS last_txn
  FROM savings_savingsaccount
  WHERE total_deposit > 0
  GROUP BY user_id
  UNION
  SELECT user_id, MAX(created_at)
  FROM plans_plan
  WHERE amount > 0
  GROUP BY user_id
) AS activity
WHERE DATEDIFF(DAY, last_txn, GETDATE()) > 365;
```

**Impact**: Powers re-engagement campaigns and churn prevention.

---

#### Q4: Customer Lifetime Value (CLV)
**Objective**: Estimate total value contributed by each customer.

```sql
SELECT u.id AS customer_id,
       SUM(ISNULL(s.total_deposit, 0) + ISNULL(p.amount, 0)) / 100 AS clv_ngn,
       DATEDIFF(DAY, u.date_joined, GETDATE()) AS tenure_days
FROM users_customuser u
LEFT JOIN savings_savingsaccount s ON u.id = s.user_id
LEFT JOIN plans_plan p ON u.id = p.user_id
GROUP BY u.id, u.date_joined;
```

**Impact**: Informs acquisition budgeting and long-term planning.

---

### ⚙️ Technical Highlights

- SQL Server syntax: `CTE`, `DATEDIFF`, `CASE`, `UNION`, `ISNULL`
- Query optimization: Indexed joins, filtered aggregations
- Business logic translation: From SQLite to T-SQL
- Edge case handling: NULL dates, short account lifespans

---

### 📌 Notes

- All monetary values converted from Kobo to NGN.
- Queries validated for accuracy, performance, and recruiter readability.
- Designed for real-world application in customer analytics and product strategy.

---


