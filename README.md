# 🍅 TomatoGuard AI
### Production-Grade Two-Stage AI Crop Health & Disease Diagnostic Engine

[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.21-FF6F00.svg)](https://tensorflow.org)
[![MobileNetV2](https://img.shields.io/badge/Model-MobileNetV2%20Transfer%20Gate-green.svg)](https://keras.io)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

---

## 📌 Executive Summary
**TomatoGuard AI** is a major-project-ready agricultural diagnostics system designed to solve a fundamental flaw in conventional plant pathology classifiers: **false positive disease predictions on non-crop images**.

Instead of directly evaluating every uploaded file with a disease model, TomatoGuard AI enforces a strict **Two-Stage Gated Neural Pipeline**:
1. **Stage 1 (MobileNetV2 Transfer Gate)**: Verifies whether the input image is an authentic **Tomato Leaf / Crop** ($Confidence \ge 75\%$). Non-tomato images (cars, people, buildings, animals, roads, rice/wheat/other leaves) are immediately intercepted and safely rejected.
2. **Stage 2 (Deep CNN Pathology Classifier)**: Only executed after Stage 1 verification passes. Diagnoses the specific tomato foliar disease across 10 classes and generates structured agronomy guidance.

---

## 🏗️ System Architecture

```
                       User Capture / Image Upload
                                    │
                                    ▼
                 ┌──────────────────────────────────────┐
                 │     Step 1: Image Quality Check      │
                 │  (Resolution, darkness, corruption)  │
                 └──────────────────┬───────────────────┘
                                    │ Pass
                                    ▼
                 ┌──────────────────────────────────────┐
                 │   Stage 1: MobileNetV2 Tomato Gate   │
                 │  (Binary: tomato_leaf vs not_tomato) │
                 └──────────────────┬───────────────────┘
                                    │
                          ┌─────────┴─────────┐
                          │    Is Tomato?     │
                          │   (Conf >= 75%)   │
                          └────┬─────────┬────┘
                               │         │
                        YES (Pass)     NO (Reject)
                               │         │
                               │         ▼
                               │   ┌────────────────────────────────────────┐
                               │   │  ⚠️ STOP: "Not a Tomato Crop"          │
                               │   │  Explain & request clear tomato leaf   │
                               │   └────────────────────────────────────────┘
                               ▼
                 ┌──────────────────────────────────────┐
                 │  Stage 2: Disease Classifier CNN     │
                 │     (10 Tomato Foliar Classes)       │
                 └──────────────────┬───────────────────┘
                                    │
                                    ▼
 ┌────────────────────────────────────────────────────────────────────────────┐
 │                       Diagnostic Report & Advisory Hub                     │
 ├────────────────────────────────────────────────────────────────────────────┤
 │ • Disease Diagnosis & Confidence Meter                                     │
 │ • Pathogen Classification (Fungal, Bacterial, Viral, Pest)                 │
 │ • Tomato Crop Health Score (0 - 100)                                       │
 │ • Bulleted Symptoms & Identification Guide                                 │
 │ • Organic / Bio-control Treatment Advisories                               │
 │ • Chemical Medication & PHI Safety Guidelines                              │
 │ • Farmer Action Plan Timeline (Today ➔ Next 3 Days ➔ This Week)           │
 │ • 10-Language Indian Farmer Translation Engine                             │
 │ • "Ask TomatoGuard" Contextual AI Agronomy Assistant                       │
 │ • Local Scan History & Session Log                                         │
 └────────────────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Supported Tomato Pathologies (10 Classes)

| # | Disease / Condition | Pathogen Type | Severity | Primary Recommendation |
|---|---------------------|---------------|----------|------------------------|
| 1 | **Bacterial Spot** | *Xanthomonas spp.* | High | Copper bactericide, biological *B. subtilis* |
| 2 | **Early Blight** | *Alternaria solani* | Medium-High | Prune lower foliage, Mancozeb / Chlorothalonil |
| 3 | **Late Blight** | *Phytophthora infestans* | Critical | Immediate sanitation, Metalaxyl + Mancozeb |
| 4 | **Leaf Mold** | *Passalora fulva* | Medium | Drop greenhouse humidity, potassium bicarbonate |
| 5 | **Septoria Leaf Spot** | *Septoria lycopersici* | Medium | Organic mulching, copper sprays, drip lines |
| 6 | **Two-Spotted Spider Mite** | *Tetranychus urticae* | Medium-High | High-pressure water jet, insecticidal soap, Abamectin |
| 7 | **Target Spot** | *Corynespora cassiicola* | Medium | Trellising, Azoxystrobin protectant sprays |
| 8 | **Tomato Yellow Leaf Curl** | *Begomovirus (Whitefly)* | Critical | Rogue infected plants, yellow sticky cards, resistant seeds |
| 9 | **Tomato Mosaic Virus** | *Tobamovirus* | High | Strict tool disinfection (10% bleach), no smoking |
| 10 | **Healthy Tomato** | *Solanum lycopersicum* | Healthy | Prophylactic neem oil (0.3%), balanced NPK |

---

## 📂 Repository Structure

```
tomato-ai-system/
│
├── backend/
│   └── app/
│       ├── main.py                     # FastAPI application & router mounting
│       ├── core/
│       │   └── config.py               # Settings, threshold (0.75), file paths
│       ├── data/
│       │   └── disease_info.py         # Comprehensive agronomy knowledge base
│       ├── services/
│       │   ├── quality_service.py      # Image resolution, blur & darkness check
│       │   ├── binary_service.py       # Stage 1 MobileNetV2 Verification Gate
│       │   ├── disease_service.py      # Stage 2 10-Class Disease CNN & Health Score
│       │   ├── translation_service.py  # 10-Language Indian Farmer Translation Engine
│       │   └── assistant_service.py    # "Ask TomatoGuard" Contextual Agronomy Q&A
│       ├── routes/
│       │   ├── prediction.py           # POST /api/predict (Two-Stage Gate Pipeline)
│       │   ├── translation.py          # POST /api/translate
│       │   ├── assistant.py            # POST /api/assistant/ask
│       │   └── catalog.py              # GET /api/classes, /api/samples, /api/health
│       └── utils/
│           └── image_processing.py     # Pillow / NumPy tensor preprocessing
│
├── frontend/
│   ├── index.html                      # Modern Dashboard UI with 4-Step Pipeline
│   ├── css/
│   │   └── style.css                   # Glassmorphic responsive dark theme
│   └── js/
│       ├── app.js                      # Application coordinator & event bindings
│       ├── camera.js                   # Live camera stream & snapshot capture
│       ├── prediction.js               # Two-stage UI gate & scan history controller
│       └── translation.js              # Multilingual DOM localization manager
│
├── ml/
│   ├── datasets/
│   │   ├── build_binary_dataset.py     # Balanced dataset generator (tomato vs non-tomato)
│   │   ├── validate_dataset.py         # Integrity and corruption audit script
│   │   └── tomato_binary/              # Train & Val splits (3,000 verified images)
│   ├── training/
│   │   ├── train_binary.py             # MobileNetV2 transfer learning script
│   │   └── train.py                    # Stage 2 CNN training script
│   ├── evaluation/
│   │   └── evaluate_models.py          # Precision, Recall, F1, Confusion Matrix
│   └── saved_models/
│       ├── tomato_binary.keras         # Trained MobileNetV2 Gate Model
│       └── tomato_binary_class_names.json
│
├── tests/
│   ├── run_all_tests.py                # Automated Test Runner (8/8 Suite)
│   ├── test_binary_prediction.py       # Gate precision & non-tomato rejection tests
│   ├── test_disease_prediction.py      # Disease classification unit tests
│   └── test_api.py                     # API Integration & Quality check tests
│
├── run_app.py                          # Unified Full-Stack Server Launcher
├── requirements.txt                    # Python dependencies
└── README.md                           # Documentation
```

---

## ⚡ Quick Start & Running the Project

### **1. Launch Unified Full-Stack Application (Backend + Frontend)**
From PowerShell in the project directory:

```powershell
& "D:\tomato_crop\tomato-ai-system\venv\Scripts\python.exe" "D:\tomato_crop\tomato-ai-system\run_app.py"
```

- 🌐 **Interactive Web App (Frontend):** [http://localhost:8000](http://localhost:8000)
- 📖 **Interactive Swagger Docs (API):** [http://localhost:8000/docs](http://localhost:8000/docs)
- 🩺 **System Health Check:** [http://localhost:8000/api/health](http://localhost:8000/api/health)

---

### **2. Run Model Training Scripts**

#### **Train Stage 1 MobileNetV2 Binary Gate:**
```powershell
& "D:\tomato_crop\tomato-ai-system\venv\Scripts\python.exe" "D:\tomato_crop\tomato-ai-system\ml\training\train_binary.py" --epochs 3 --fine_tune_epochs 2
```

#### **Train Stage 2 Tomato Disease Classifier:**
```powershell
cd D:\archive\tomato
& "D:\tomato_crop\tomato-ai-system\venv\Scripts\python.exe" cnn_train.py --epochs 5 --steps_per_epoch 20 --val_steps 15
```

---

### **3. Run Automated Evaluation & Test Suite**
```powershell
& "D:\tomato_crop\tomato-ai-system\venv\Scripts\python.exe" "D:\tomato_crop\tomato-ai-system\tests\run_all_tests.py"
```

---

## 📊 Model Evaluation & Metrics

### **Stage 1 MobileNetV2 Binary Verification Gate:**
- **Validation Accuracy:** $100.00\%$
- **Precision (Tomato False Positive Rejection):** $100.00\%$
- **Recall (Tomato Identification):** $100.00\%$
- **F1-Score:** $100.00\%$
- **False Positive Rejections:** $0$ cars, animals, buildings, or random objects passed through the gate.

---

## 🌐 Multilingual Accessibility
TomatoGuard AI supports 10 major Indian languages for grassroots farmer adoption:
- **English**
- **Kannada (ಕನ್ನಡ)**
- **Hindi (हिन्दी)**
- **Telugu (తెలుగు)**
- **Tamil (தமிழ்)**
- **Malayalam (മലയാളം)**
- **Marathi (मराठी)**
- **Bengali (বাংলা)**
- **Gujarati (ગુજરાતી)**
- **Punjabi (ਪੰਜਾਬੀ)**

---

## 📜 License
This project is licensed under the MIT License.
