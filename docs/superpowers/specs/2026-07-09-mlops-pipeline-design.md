# MLOps Pipeline Design — Tabular Data End-to-End

**Date:** 2026-07-09  
**Scope:** First iteration MLOps pipeline with Git-triggered CI/CD  
**Timeline:** 8 hours  
**Goal:** Build a reproducible, automated training → evaluation → inference pipeline  

---

## 1. Overview

A GitHub Actions-driven MLOps pipeline that automatically trains, evaluates, and tests a machine learning model on every relevant code/data change. The pipeline produces a versioned model artifact (`model.pkl`) and metrics that can be iterated on.

**Core Loop:**
```
Code/Data Change → Git Push → GitHub Actions → Train → Evaluate → Test → Artifacts
```

---

## 2. Architecture

### 2.1 Repository Structure

```
ML-Ops/
├── data/
│   └── raw/                    # Public datasets (Iris loaded via sklearn)
├── src/
│   ├── train.py               # Training script
│   ├── evaluate.py            # Evaluation script
│   └── inference.py           # Inference script
├── tests/
│   ├── test_train.py          # Unit tests for training
│   └── test_inference.py      # Unit tests for inference
├── models/
│   └── model.pkl              # Trained model (gitignore)
├── results/
│   └── metrics.json           # Evaluation metrics
├── .github/workflows/
│   └── mlops-pipeline.yml      # GitHub Actions workflow
├── requirements.txt           # Python dependencies
└── README.md
```

### 2.2 Tech Stack

| Component | Technology | Reason |
|-----------|-----------|--------|
| **Data** | Iris (sklearn built-in) | Public, standard, fast |
| **ML Model** | Logistic Regression (scikit-learn) | Simple, fast, realistic |
| **Serialization** | joblib | Standard for sklearn models |
| **Testing** | pytest | Lightweight, integrates with CI |
| **CI/CD** | GitHub Actions | Native to GitHub, no extra infra |
| **Language** | Python 3.11 | Standard for ML |

---

## 3. Pipeline Workflow

### 3.1 Trigger Logic

**When does training run?**

```
On every push/PR:
├─ Check: Did train.py, evaluate.py, or data/ change?
├─ If YES → Run full pipeline (train + evaluate + test)
└─ If NO  → Skip training, run only unit tests (fast feedback)
```

**Implementation:** Use `git diff --name-only` in GitHub Actions to detect changes.

### 3.2 Workflow Jobs

**Job 0: Detect Changes**
- Output: `should_train=true/false` flag
- Checked by downstream jobs

**Job 1: Train** (conditional on `should_train=true`)
- Setup Python 3.11 + dependencies
- Run `python src/train.py`
  - Loads Iris dataset
  - Trains Logistic Regression (80/20 train/test split)
  - Saves model to `models/model.pkl` via joblib
- Upload artifact: `model.pkl`

**Job 2: Evaluate** (conditional on `should_train=true`)
- Download `model.pkl` from Job 1
- Run `python src/evaluate.py`
  - Loads model from `model.pkl`
  - Evaluates on test set
  - Computes: Accuracy, Precision, Recall, F1 per class
  - Saves to `results/metrics.json`
  - **Validation:** If accuracy < 0.70, fail workflow (prevents bad models)
- Upload artifact: `metrics.json`

**Job 3: Inference Test** (always runs)
- Download `model.pkl` (or use cached version if training skipped)
- Run `python src/inference.py`
  - Loads model
  - Makes predictions on sample data
  - Logs predictions to workflow output

**Job 4: Unit Tests** (always runs)
- Run `pytest tests/`
  - `test_train.py`: Verify training produces a valid model
  - `test_inference.py`: Verify inference works with saved model

---

## 4. Data & Model Strategy

### 4.1 Dataset

**Dataset:** Iris (150 samples, 4 features, 3 classes)
- Loaded directly in `train.py` via `sklearn.datasets.load_iris()`
- No CSV files needed, no storage overhead
- Train/Test Split: 80/20 (120 train, 30 test)

### 4.2 Model

**Model:** Logistic Regression (scikit-learn)
- Training time: <1 second
- Inference time: milliseconds
- Interpretable, suitable for first iteration
- **Metrics tracked:**
  - Accuracy (overall)
  - Precision, Recall, F1 per class
  - Confusion matrix (optional, for logs)

### 4.3 Model Serialization

- **Format:** joblib (`.pkl` file)
- **Location:** `models/model.pkl`
- **Versioning:** Each pipeline run produces a new `.pkl` (overwrites previous)
- **Archival:** GitHub Actions artifacts preserve old runs

---

## 5. Usage Pattern (Iteration Loop)

### 5.1 Local Development

**Before pushing:**
```bash
python src/train.py       # Train locally
python src/evaluate.py    # Evaluate
python src/inference.py   # Test inference
pytest tests/             # Run tests
```

### 5.2 Automated Pipeline

**After git push:**
1. GitHub detects changes → decides if training needed
2. Pipeline runs automatically
3. Model + metrics available as artifacts
4. Logs show accuracy, test predictions

### 5.3 Iteration

```
Iteration 1: Train with Iris, accuracy 0.95
↓ (Change train.py: better features)
Iteration 2: Re-train, accuracy 0.97 → new model.pkl
↓ (Add more data)
Iteration 3: Re-train with expanded data → newer model.pkl
```

**Each iteration overwrites `model.pkl`, but old versions are preserved in GitHub Actions artifact history.**

---

## 6. Inference Usage

### 6.1 Local Inference Script

```python
# inference.py
import joblib
import pandas as pd

model = joblib.load('models/model.pkl')
new_data = pd.DataFrame({...})  # Your data
predictions = model.predict(new_data)
```

### 6.2 Future: REST API (Iteration 2)

Once this pipeline works, wrap the model in Flask/FastAPI:
```python
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    prediction = model.predict(data)
    return {'prediction': prediction}
```

---

## 7. Testing & Validation

### 7.1 Unit Tests

- `test_train.py`
  - Verify training completes without error
  - Check that `model.pkl` is created
  - Verify model can make predictions

- `test_inference.py`
  - Verify saved model can be loaded
  - Check predictions on sample data

### 7.2 Integration Validation (in Workflow)

- **Accuracy Threshold:** If accuracy < 0.70 on test set, fail workflow
- **Prevents:** Bad models being marked as "successful"

### 7.3 NOT Included (Yet)

- Data validation (Great Expectations — later)
- Performance regression tracking (DVC — later)
- Model explainability (SHAP/LIME — later)

---

## 8. Outputs & Observability

### 8.1 What's Visible After Each Run

**In GitHub Actions Dashboard:**
- ✅ Workflow status (green/red)
- ⏱️ Total duration
- 📊 Job logs (train, eval, test output)
- 📥 Artifacts (model.pkl, metrics.json)

**In Workflow Output:**
- Accuracy percentage
- Per-class Precision/Recall/F1
- Sample predictions from inference test

### 8.2 Artifact Retention

- Models from successful runs: downloadable
- Metrics from each run: logged in GitHub
- Can compare accuracy across commits

---

## 9. Success Criteria

✅ Pipeline runs automatically on code/data changes  
✅ Model trains, evaluates, and tests without manual intervention  
✅ Artifacts (model.pkl, metrics.json) are downloadable from GitHub  
✅ Unit tests pass  
✅ Inference script can load and use the model  
✅ Accuracy > 0.90 (Iris is easy)  

---

## 10. Future Iterations

**Iteration 2:** REST API wrapper (Flask/FastAPI)  
**Iteration 3:** Model registry (MLflow) + deployment  
**Iteration 4:** Data validation + monitoring  
**Iteration 5:** DVC for data/model versioning  

---

## 11. Key Files to Create

| File | Purpose |
|------|---------|
| `src/train.py` | Load data, train model, save to .pkl |
| `src/evaluate.py` | Load model, compute metrics, save to JSON |
| `src/inference.py` | Load model, make predictions, log output |
| `tests/test_train.py` | Unit tests for training |
| `tests/test_inference.py` | Unit tests for inference |
| `.github/workflows/mlops-pipeline.yml` | GitHub Actions workflow definition |
| `requirements.txt` | Python dependencies (scikit-learn, pandas, pytest, etc.) |
| `README.md` | How to use the pipeline |

---

## Notes

- **Git Ignore:** `.pkl` files, `__pycache__`, `.pytest_cache`, `.env`
- **Python Version:** 3.11+
- **Dependencies:** scikit-learn, pandas, pytest, pyyaml
- **Estimated Runtime:** ~2 minutes per pipeline run (mostly GitHub overhead)
