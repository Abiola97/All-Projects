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

   ```python
   import pandas as pd
   df_full = pd.read_excel("Bank Marketing Dataset combined.xlsx", sheet_name="bank-full")
   df_test = pd.read_excel("Bank Marketing Dataset combined.xlsx", sheet_name="bank")
   ```

2. **Splitting**

   ```python
   from sklearn.model_selection import train_test_split
   train_df, val_df = train_test_split(df_full, test_size=0.2, stratify=df_full['y'], random_state=42)
   ```

3. **Preprocessing**

   ```python
   from sklearn.preprocessing import LabelEncoder
   le = LabelEncoder()
   for col in train_df.select_dtypes(include="object").columns:
       train_df[col] = le.fit_transform(train_df[col])
       val_df[col] = le.transform(val_df[col])
       df_test[col] = le.transform(df_test[col])
   ```

4. **Model Training**

   ```python
   from sklearn.tree import DecisionTreeClassifier
   clf = DecisionTreeClassifier(max_depth=6, random_state=42)
   clf.fit(train_df.drop("y", axis=1), train_df["y"])
   ```

5. **Evaluation**

   ```python
   from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
   y_test = df_test["y"]
   X_test = df_test.drop("y", axis=1)
   y_pred = clf.predict(X_test)

   print("Test Accuracy:", accuracy_score(y_test, y_pred))
   print("\nClassification Report:\n", classification_report(y_test, y_pred))
   print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
   ```

---

## 📊 Results

### Test Set Performance

* **Accuracy**: **0.9757** (~98%)

**Classification Report:**

```
               precision    recall  f1-score   support

          no       0.99      0.98      0.99      4000
         yes       0.88      0.92      0.90       521

    accuracy                           0.98      4521
   macro avg       0.93      0.95      0.94      4521
weighted avg       0.98      0.98      0.98      4521
```

**Confusion Matrix:**

```
         Predicted
        No   Yes
Actual
No      3933   67
Yes       43  478
```

### Business-Level Insights

* 🎯 **Detected Actual Buyers (True Positives): 478**
* ❌ **Missed Buyers (False Negatives): 43**
* ⚠️ **Incorrectly Predicted Buyers (False Positives): 67**
* ✅ **Correctly Predicted Non-buyers (True Negatives): 3,933**

📌 **Interpretation**:

* Model achieves **98% accuracy**, with strong recall for buyers (`yes` = 0.92).
* Few buyers are missed (43), meaning campaign effectiveness is preserved.
* High precision for `no` means marketing resources are not wasted on unlikely customers.
* Features like **call duration, previous outcome, and balance** had the highest influence.

---

## 🚀 Next Steps

* Try **Random Forest** or **Gradient Boosting** for better generalization.
* Apply **SMOTE or class weighting** to improve recall on minority class (`yes`).
* Integrate explainability (SHAP/LIME) for feature-level insights.

---

## 👤 Author

Built by Abiola Ajao
🎓 Master’s in Collective Intelligence @ UM6P
💼 Data Analyst → Product Manager
📍 Morocco & Nigeria
🔗 [LinkedIn](https://www.linkedin.com/in/abiola-ajao/) | 📧 [ajaoabiola0812@gmail.com](mailto:ajaoabiola0812@gmail.com)

---
