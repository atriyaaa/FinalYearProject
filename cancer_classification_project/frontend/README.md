# 🧬 CancerXAI Frontend – React Web Application

This is the **React-based frontend** of the Cancer Subtype Predictor. It allows users to upload gene expression data and receive cancer subtype predictions with clean, aesthetic UI, built using Material UI and custom styles.

---

## 🌟 Features

- 🔼 Upload `.csv` gene expression files
- ⚙️ Sends data to backend for prediction (`/api/predict/`)
- 🧬 Displays predicted **subtype** and **cancer type**
- 📥 Supports download of results as CSV
- 🌈 Minimalist UI with frosted-glass card styling
- 📱 Fully responsive design

---

## 🛠 Tech Stack

- **React** (v19)
- **Material UI (MUI)**
- **Axios**
- **React Router DOM**
- **Custom CSS** (Glassmorphism-inspired design)

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/cancer-xai-app.git
cd cancer-xai-app/frontend




Install dependencies
npm install

Start the app
npm start


⚠️ Notes

Ensure the Django backend is running on http://127.0.0.1:8000.
If backend is hosted elsewhere, update the API URL in Upload.js (axios.post(...)).
The backend must return:
predictions: array of results
download_url: for CSV download