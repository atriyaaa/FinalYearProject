# 🧬 CancerXAI – Multi-Cancer Subtype Classification with Explainable AI

CancerXAI is an **interactive full-stack web application** that predicts cancer subtypes from gene expression data and provides **explainable AI** outputs using SHAP. Built with a Django REST API backend and a modern React.js frontend.

---

## 📌 Project Overview

This system allows researchers, clinicians, and bioinformaticians to:

- Upload patient **gene expression profiles**
- Automatically **classify cancer subtypes** using trained ML models
- View predictions along with **SHAP-based visual explanations**
- Download batch prediction results as **CSV**

---
# 🧬 CancerXAI – Multi-Cancer Subtype Classification with Explainable AI

CancerXAI is a full-stack web application that predicts cancer subtypes using gene expression data and explains the results using SHAP-based visualizations. The system is built with a Django backend for ML inference and a React frontend for user interaction.

---

## 📌 Features

- ✅ Upload patient `.csv` gene expression files
- ✅ Predict subtypes across multiple cancer types (breast, lung, prostate, kidney, colorectal)
- ✅ Interactive and visually pleasing result display
- ✅ SHAP visualizations (for selected samples)
- ✅ CSV download support for predictions

---

## 🏗️ Tech Stack

| Layer     | Technology        |
|-----------|-------------------|
| Backend   | Python, Django REST Framework |
| ML Engine | scikit-learn, SHAP, PCA       |
| Frontend  | React.js, Material UI, CSS    |
| Deployment Ready | Docker, AWS/GCP Ready |

---

## 📁 Project Structure


📦 cancer_classification_project/
│
├── 📁 backend/ (Django REST API)
│ ├── src/
│ ├── models/
│ ├── api/
│ ├── datasets/
│ └── ...
│
├── 📁 frontend/ (React UI)
│ ├── src/
│ ├── public/
│ ├── App.js
│ ├── Upload.js
│ ├── Results.js
│ └── ...



---


---

## 🚀 Setup Instructions

### ✅ Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver

Runs on: http://127.0.0.1:8000/api/predict/

### ✅ Frontend
cd frontend
npm install
npm start

Opens at: http://localhost:3000



📤 Upload Format

A CSV file with gene expression values, one row per sample.
Header must contain Ensembl IDs as columns (e.g., ENSG00000...).

ENSG00000000003,ENSG00000000005,...,ENSG99999999999
12.4,0.00,...,7.4
15.9,0.05,...,6.7

📥 Output Format (API)

{
  "predictions": [
    { "sample": 1, "subtype": "BRCA_LumA", "cancer_type": "Breast" },
    { "sample": 2, "subtype": "LUAD", "cancer_type": "Lung" }
  ],
  "download_url": "/media/predictions_YYYY-MM-DD.csv"
}
🧠 ML Pipeline

Preprocessing:
Mean imputation
Standard scaling
PCA (n=50 components)
Models:
Random Forest (selected best)
SVM, MLP (also evaluated)
Subtype labels: encoded using LabelEncoder
SHAP used for feature importance per sample
🎨 UI Highlights

Material UI components
Custom frosted glass card designs
Color-coded cancer type chips
Responsive layout with animation effects


📥 Future Work

 Add SHAP waterfall for individual sample
 Authentication for clinicians
 Docker container support
 Deploy to AWS or Render
👨‍💻 Author

Atriya Sivakumar - as05140@surrey.ac.uk
University of Surrey (Final Year BSc(Hons) Computer Science)
