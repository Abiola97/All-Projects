# 🏦 Bank Marketing Campaign Analysis (Decision Tree)

A machine learning project to predict whether customers will subscribe to a bank’s term deposit during a marketing campaign. Built using the **Bank Marketing Dataset (UCI Repository)** and a **Decision Tree Classifier**, this project demonstrates the end-to-end pipeline of preprocessing, training, evaluation, and visualization.

---

## 📦 Features

* ✅ Data import and preprocessing of demographic, financial, and campaign variables
* 🔠 Label encoding of categorical features (job, marital, education, etc.)
* 📊 Train-validation split with stratification for class balance
* 🌳 Decision Tree Classifier with visualized tree structure
* 📈 Evaluation using Accuracy, Precision, Recall, F1-score, and Confusion Matrix
* 💾 Model persistence with `joblib` for future predictions

---

## 📂 Dataset Overview

* **Source**: [UCI Machine Learning Repository – Bank Marketing](https://archive.ics.uci.edu/ml/datasets/bank+marketing)
* **Rows**: ~45,000 records across train/test
* **Target Variable**: `y` → `yes` (subscribed) or `no` (not subscribed)
* **Key Features**:

  * Demographics: `age`, `job`, `marital`, `education`
  * Finance: `balance`, `housing`, `loan`
  * Campaign: `duration`, `pdays`, `previous`, `poutcome`

---

## ⚙️ Methodology

1. **Data Loading**
   Imported dataset from Excel files (`bank-full`, `bank`).

2. **Splitting**

   * Train (80%) and Validation (20%) on `bank-full`.
   * Separate Test dataset (`bank`).

3. **Preprocessing**

   * Encoded categorical variables using `LabelEncoder`.
   * Checked distributions and missing values.

4. **Model Training**

   * Applied **DecisionTreeClassifier** (`scikit-learn`).
   * Tuned max depth & splitting criteria.

5. **Evaluation**

   * Accuracy Score
   * Classification Report (Precision, Recall, F1-score)
   * Confusion Matrix (visualized with Seaborn)

---

## 📊 Results

### Validation Set

* **Accuracy**: ~0.88
* Precision/Recall balanced for majority class (`no`), weaker for minority class (`yes`).

### Test Set

* **Accuracy**: ~0.86
* **Classification Report** (simplified view):

  * `yes` → Precision: 0.67, Recall: 0.45, F1-score: 0.54
  * `no` → Precision: 0.90, Recall: 0.96, F1-score: 0.93

### Confusion Matrix (Test Set)

```
         Predicted
        Yes   No
Actual
Yes      532  642
No       380 8486
```

📌 **Interpretation**:

* Model performs well in identifying customers who will **not** purchase (`no`).
* False negatives remain a challenge (customers predicted as `no` but actually `yes`).
* Features like **call duration, previous outcome, and balance** were most influential.

---

## 🚀 Next Steps

* Try **Random Forest** or **Gradient Boosting** for better generalization.
* Apply **SMOTE or class weighting** to handle imbalance in `yes/no` outcomes.
* Integrate explainability (SHAP/LIME) for feature-level insights.

---

## 📈 Dashboard/Visualization

* Decision tree visualization using `sklearn.tree.plot_tree()`
* Confusion Matrix heatmap using **Seaborn**
* Accuracy/Performance metrics exported for reporting

---

## 👤 Author

Built by Abiola Ajao
🎓 Master’s in Collective Intelligence @ UM6P
💼 Data Analyst → Product Manager
📍 Morocco & Nigeria
🔗 [LinkedIn](https://www.linkedin.com/in/abiola-ajao/) | 📧 [ajaoabiola0812@gmail.com](mailto:ajaoabiola0812@gmail.com)

---

