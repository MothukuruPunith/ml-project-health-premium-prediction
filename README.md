# 🏥 Health Insurance Premium Prediction – ML Project

A complete machine learning project that predicts **health insurance premium amounts** using demographic, lifestyle, and medical attributes.

---

## 📁 Project Structure

```txt
ml-project-health-premium-prediction/
│
├── data/                          # Dataset(s)
│   └── health_insurance.csv       # Sample dataset
│
├── notebooks/                     # EDA & modeling notebooks
│   ├── 01_data_cleaning.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_feature_engineering.ipynb
│   └── 04_model_training.ipynb
│
├── models/                        # Trained ML models
│   └── premium_model.pkl
│
├── src/                           # Python scripts
│   ├── preprocess.py
│   ├── train.py
│   └── predict.py
│
├── requirements.txt
└── README.md
```

---

## 🚀 Features

- End-to-end machine learning pipeline  
- Cleans data, encodes categories, scales numerical fields  
- Performs EDA (distributions, correlations, patterns)  
- Trains multiple ML models (Linear Regression, Random Forest, XGBoost)  
- Predicts annual **health insurance premium** for new input  
- Saves trained model to `models/`  
- Includes a simple prediction script  

---

## 📊 ML Pipeline

### 🔍 Preprocessing
- Handle missing values  
- Encode categorical variables  
- Remove outliers  
- Scale numeric fields  
- Train-test split  

### 📈 EDA
- Distribution plots  
- Heatmaps  
- Insights into premium-driving factors  

### 🤖 Model Training
- Linear Regression  
- Random Forest Regressor  
- XGBoost Regressor  

### 🧪 Model Evaluation
- MAE  
- MSE / RMSE  
- R² Score  

### 🔮 Prediction System
`predict.py` loads `premium_model.pkl` and predicts premium for new input.

---

## 🛠️ Technologies

- Python  
- Pandas, NumPy  
- Scikit-learn  
- Matplotlib, Seaborn  
- XGBoost  
- Joblib / Pickle  

---

## 📦 Installation

### 1️⃣ Clone Repo
```bash
git clone https://github.com/MothukuruPunith/ml-project-health-premium-prediction.git
cd ml-project-health-premium-prediction
```

### 2️⃣ Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Train the Model
```bash
python src/train.py
```

Model will be saved to:
```
models/premium_model.pkl
```

### 5️⃣ Run Prediction Script
```bash
python src/predict.py
```

---

## 🔍 Example Output

```
Predicted Health Insurance Premium: ₹32,450 per year
```

---

## 📄 requirements.txt (major libs)

```txt
pandas
numpy
scikit-learn
xgboost
matplotlib
seaborn
joblib
```

---

## 👨‍💼 Author
**Punith Mothukuru**  
Machine Learning & GenAI Enthusiast  
SRM Institute of Science and Technology  

---

## 📌 Note
This project is intended for demonstration and educational use only.
