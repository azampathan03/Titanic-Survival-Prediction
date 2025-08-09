Titanic Survival Prediction
The sinking of the **RMS Titanic** in 1912 remains one of the most tragic maritime disasters in history. With **1,502 lives lost** out of **2,224 passengers and crew**, the event has been widely studied, including in data science and machine learning. Predicting survival on the Titanic is a classic classification problem used to teach predictive modeling.

Overview
<img width="960" height="540" alt="titanic app" src="https://github.com/user-attachments/assets/1524d1e3-82b6-48ab-b72e-6cd2dd6d7058" />

## **1. Understanding the Dataset**

The Titanic dataset contains information about passengers, including:

- **PassengerId** – Unique identifier
- **Survived** – 0 (No), 1 (Yes) *(Target Variable)*
- **Pclass** – Ticket class (1st, 2nd, 3rd)
- **Name** – Passenger name
- **Sex** – Male or Female
- **Age** – Age in years
- **SibSp** – Number of siblings/spouses aboard
- **Parch** – Number of parents/children aboard
- **Ticket** – Ticket number
- **Fare** – Passenger fare
- **Cabin** – Cabin number
- **Embarked** – Port of embarkation (C = Cherbourg, Q = Queenstown, S = Southampton)


---

## **2. Key Factors Affecting Survival**

### **A. Socio-Economic Status (Pclass)**

- **1st class passengers** had a higher survival rate (**~63%**) due to proximity to lifeboats.
- **3rd class passengers** had the lowest survival rate (**~24%**).

### **B. Gender (Sex)**

- **Female passengers** had a **~74%** survival rate due to the "women and children first" protocol.
- **Male passengers** had only a **~19%** survival rate.

### **C. Age (Age)**

- **Children (<10 years)** had a higher chance of survival.
- **Elderly passengers** had lower survival rates.

### **D. Family Size (SibSp & Parch)**

- Passengers with **1-2 family members** had better survival odds.
- Large families (>3) struggled to evacuate together.

---

## **3. Machine Learning Approach**

### **A. Data Preprocessing**

- **Handling missing values** (e.g., filling missing **`Age`** with median).
- **Converting categorical data** (e.g., **`Sex`** and **`Embarked`** into numerical values).
- **Feature engineering** (e.g., extracting titles from **`Name`**, grouping **`Age`** into bins).

### **B. Model Selection**

Common algorithms used:

1. **Logistic Regression** (Baseline model)
2. **Random Forest** (Handles non-linear relationships well)
3. **Gradient Boosting (XGBoost)** (High accuracy)
4. **Support Vector Machines (SVM)** (Works well with structured data)

### **C. Model Evaluation**

Metrics used:

- **Accuracy** (Overall correctness)
- **Precision & Recall** (Minimizing false positives/negatives)
- **F1-Score** (Balanced measure)
- **ROC-AUC** (Performance across thresholds)

---

## **4. Example Prediction (Random Forest)**

A trained model might predict survival based on input features:

| **Feature** | **Passenger 1 (Survived)** | **Passenger 2 (Did Not Survive)** |
| --- | --- | --- |
| **Pclass** | 1 (Upper) | 3 (Lower) |
| **Sex** | Female | Male |
| **Age** | 28 | 45 |
| **Fare** | £50 | £8 |
| **Embarked** | C (Cherbourg) | S (Southampton) |
| **Prediction** | ✅ **Survived (95%)** | ❌ **Died (87%)** |

---

---

## **5. Conclusion**

- **Women, children, and upper-class passengers** had the best survival odds.
- **Machine learning models** can predict survival with **~80% accuracy** using the right features.
- **Feature engineering** (e.g., family size, title extraction) improves predictions.

This analysis helps us understand historical biases in survival and serves as a foundation for classification problems in data science.
