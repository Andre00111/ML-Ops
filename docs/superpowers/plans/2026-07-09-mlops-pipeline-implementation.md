# MLOps Pipeline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a fully automated, Git-triggered MLOps pipeline that trains a Logistic Regression model on Iris data, evaluates it, and tests inference — all via GitHub Actions.

**Architecture:** Python scripts for training/evaluation/inference, GitHub Actions workflow triggered on code/data changes, model serialized as joblib pickle, metrics tracked as JSON. Smart change detection prevents unnecessary retraining.

**Tech Stack:** Python 3.11, scikit-learn, pandas, joblib, pytest, GitHub Actions, YAML

---

## File Structure

**Files to Create:**

| File | Responsibility |
|------|-----------------|
| `src/train.py` | Load Iris, train Logistic Regression, save model.pkl |
| `src/evaluate.py` | Load model, compute metrics, save metrics.json |
| `src/inference.py` | Load model, make predictions, log output |
| `tests/test_train.py` | Unit tests: training produces valid model |
| `tests/test_inference.py` | Unit tests: inference works with saved model |
| `.github/workflows/mlops-pipeline.yml` | GitHub Actions workflow definition |
| `requirements.txt` | Python dependencies |
| `.gitignore` | Ignore .pkl, __pycache__, etc. |
| `README.md` | How to run the pipeline locally |

**Files Already Created:**
- `docs/superpowers/specs/2026-07-09-mlops-pipeline-design.md` (design doc)

---

## Task Breakdown (Estimate: 8 hours)

### Task 1: Setup Project Structure & Dependencies

**Files:**
- Create: `requirements.txt`
- Create: `.gitignore`
- Modify: existing (none)

**Estimated Time:** 15 minutes

- [ ] **Step 1: Create requirements.txt with all dependencies**

```
scikit-learn==1.5.1
pandas==2.2.0
joblib==1.4.2
pytest==8.3.1
```

Save to `/Users/andre.butkevich/Desktop/Projects/ML-Ops/requirements.txt`

- [ ] **Step 2: Create .gitignore to exclude artifacts**

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/

# ML artifacts
models/*.pkl
results/*.json

# IDE
.vscode/
.idea/
*.swp

# macOS
.DS_Store

# Pytest
.pytest_cache/
```

Save to `/Users/andre.butkevich/Desktop/Projects/ML-Ops/.gitignore`

- [ ] **Step 3: Commit**

```bash
cd /Users/andre.butkevich/Desktop/Projects/ML-Ops
git add requirements.txt .gitignore
git commit -m "chore: add dependencies and gitignore"
```

---

### Task 2: Create Training Script

**Files:**
- Create: `src/train.py`
- Create: `models/` directory (implicit)

**Estimated Time:** 45 minutes

- [ ] **Step 1: Create src directory**

```bash
mkdir -p /Users/andre.butkevich/Desktop/Projects/ML-Ops/src
mkdir -p /Users/andre.butkevich/Desktop/Projects/ML-Ops/models
```

- [ ] **Step 2: Write train.py script**

```python
"""
Training script for Iris classification with Logistic Regression.
Loads Iris dataset, trains model, saves to models/model.pkl
"""
import joblib
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import os

def train():
    """Load Iris, train Logistic Regression, save model"""
    
    # Load dataset
    iris = datasets.load_iris()
    X = iris.data
    y = iris.target
    
    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train model
    model = LogisticRegression(
        max_iter=200,
        random_state=42,
        multi_class='multinomial'
    )
    model.fit(X_train, y_train)
    
    # Save model
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/model.pkl')
    
    print(f"Model trained and saved to models/model.pkl")
    print(f"Training set size: {len(X_train)}")
    print(f"Test set size: {len(X_test)}")

if __name__ == '__main__':
    train()
```

Save to `/Users/andre.butkevich/Desktop/Projects/ML-Ops/src/train.py`

- [ ] **Step 3: Test script runs locally**

```bash
cd /Users/andre.butkevich/Desktop/Projects/ML-Ops
python src/train.py
```

Expected output:
```
Model trained and saved to models/model.pkl
Training set size: 120
Test set size: 30
```

- [ ] **Step 4: Verify model.pkl was created**

```bash
ls -lh /Users/andre.butkevich/Desktop/Projects/ML-Ops/models/model.pkl
```

Expected: File exists, ~3KB

- [ ] **Step 5: Commit**

```bash
git add src/train.py
git commit -m "feat: add training script for Iris classification"
```

---

### Task 3: Create Evaluation Script

**Files:**
- Create: `src/evaluate.py`
- Create: `results/` directory (implicit)

**Estimated Time:** 45 minutes

- [ ] **Step 1: Create results directory**

```bash
mkdir -p /Users/andre.butkevich/Desktop/Projects/ML-Ops/results
```

- [ ] **Step 2: Write evaluate.py script**

```python
"""
Evaluation script for trained model.
Loads model from models/model.pkl, computes metrics, saves to results/metrics.json
"""
import joblib
import json
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
import os

def evaluate():
    """Load model and evaluate on Iris test set"""
    
    # Load dataset (same split as training)
    iris = datasets.load_iris()
    X = iris.data
    y = iris.target
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Load model
    model = joblib.load('models/model.pkl')
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_test, y_pred, average=None
    )
    
    # Prepare metrics
    metrics = {
        'accuracy': float(accuracy),
        'precision': [float(p) for p in precision],
        'recall': [float(r) for r in recall],
        'f1': [float(f) for f in f1],
        'confusion_matrix': confusion_matrix(y_test, y_pred).tolist()
    }
    
    # Save metrics
    os.makedirs('results', exist_ok=True)
    with open('results/metrics.json', 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print(f"Evaluation complete")
    print(f"Accuracy: {accuracy:.4f}")
    for i, (p, r, f) in enumerate(zip(precision, recall, f1)):
        print(f"Class {i}: P={p:.3f}, R={r:.3f}, F1={f:.3f}")
    
    # Validation: fail if accuracy < 0.70
    if accuracy < 0.70:
        raise ValueError(f"Accuracy {accuracy:.4f} is below threshold 0.70")
    
    print("✓ Accuracy above threshold (0.70)")

if __name__ == '__main__':
    evaluate()
```

Save to `/Users/andre.butkevich/Desktop/Projects/ML-Ops/src/evaluate.py`

- [ ] **Step 3: Test script runs locally**

```bash
cd /Users/andre.butkevich/Desktop/Projects/ML-Ops
python src/evaluate.py
```

Expected output:
```
Evaluation complete
Accuracy: 1.0000
Class 0: P=1.000, R=1.000, F1=1.000
Class 1: P=1.000, R=1.000, F1=1.000
Class 2: P=1.000, R=1.000, F1=1.000
✓ Accuracy above threshold (0.70)
```

- [ ] **Step 4: Verify metrics.json was created**

```bash
cat /Users/andre.butkevich/Desktop/Projects/ML-Ops/results/metrics.json
```

Expected: Valid JSON with accuracy, precision, recall, f1, confusion_matrix

- [ ] **Step 5: Commit**

```bash
git add src/evaluate.py
git commit -m "feat: add evaluation script with accuracy threshold validation"
```

---

### Task 4: Create Inference Script

**Files:**
- Create: `src/inference.py`

**Estimated Time:** 30 minutes

- [ ] **Step 1: Write inference.py script**

```python
"""
Inference script for making predictions with trained model.
Loads model from models/model.pkl and makes predictions on sample data.
"""
import joblib
import pandas as pd
from sklearn import datasets

def inference():
    """Load model and make predictions on sample data"""
    
    # Load model
    model = joblib.load('models/model.pkl')
    
    # Load Iris dataset for target names
    iris = datasets.load_iris()
    target_names = iris.target_names
    
    # Sample data for inference (5 random Iris samples)
    sample_data = pd.DataFrame({
        'sepal_length': [5.1, 7.0, 6.3, 4.6, 5.9],
        'sepal_width': [3.5, 3.2, 2.5, 3.4, 3.0],
        'petal_length': [1.4, 4.7, 5.0, 1.3, 4.2],
        'petal_width': [0.2, 1.4, 2.0, 0.2, 1.5]
    })
    
    # Make predictions
    predictions = model.predict(sample_data)
    prediction_names = [target_names[p] for p in predictions]
    
    print("Inference Results:")
    print("-" * 50)
    for i, (pred, name) in enumerate(zip(predictions, prediction_names)):
        print(f"Sample {i+1}: {name} (class {pred})")
    print("-" * 50)
    print("✓ Inference test passed")

if __name__ == '__main__':
    inference()
```

Save to `/Users/andre.butkevich/Desktop/Projects/ML-Ops/src/inference.py`

- [ ] **Step 2: Test script runs locally**

```bash
cd /Users/andre.butkevich/Desktop/Projects/ML-Ops
python src/inference.py
```

Expected output:
```
Inference Results:
--------------------------------------------------
Sample 1: setosa (class 0)
Sample 2: versicolor (class 1)
Sample 3: virginica (class 2)
Sample 4: setosa (class 0)
Sample 5: versicolor (class 1)
--------------------------------------------------
✓ Inference test passed
```

- [ ] **Step 3: Commit**

```bash
git add src/inference.py
git commit -m "feat: add inference script for making predictions"
```

---

### Task 5: Create Unit Tests

**Files:**
- Create: `tests/test_train.py`
- Create: `tests/test_inference.py`

**Estimated Time:** 60 minutes

- [ ] **Step 1: Create tests directory**

```bash
mkdir -p /Users/andre.butkevich/Desktop/Projects/ML-Ops/tests
touch /Users/andre.butkevich/Desktop/Projects/ML-Ops/tests/__init__.py
```

- [ ] **Step 2: Write test_train.py**

```python
"""
Unit tests for training script.
"""
import pytest
import joblib
import os
from sklearn.linear_model import LogisticRegression
from src.train import train

def test_train_creates_model():
    """Test that training creates a valid model.pkl file"""
    
    # Remove old model if exists
    model_path = 'models/model.pkl'
    if os.path.exists(model_path):
        os.remove(model_path)
    
    # Run training
    train()
    
    # Assert model file exists
    assert os.path.exists(model_path), "model.pkl was not created"

def test_model_is_valid():
    """Test that saved model can be loaded and is a LogisticRegression"""
    
    # Ensure model exists
    train()
    
    # Load model
    model = joblib.load('models/model.pkl')
    
    # Assert it's the right type
    assert isinstance(model, LogisticRegression), "Loaded model is not LogisticRegression"

def test_model_can_predict():
    """Test that loaded model can make predictions"""
    
    # Ensure model exists
    train()
    
    # Load model
    model = joblib.load('models/model.pkl')
    
    # Create sample data (4 features for Iris)
    sample = [[5.1, 3.5, 1.4, 0.2]]
    
    # Make prediction
    prediction = model.predict(sample)
    
    # Assert prediction is valid
    assert len(prediction) == 1, "Should return one prediction"
    assert prediction[0] in [0, 1, 2], "Prediction should be a valid Iris class (0, 1, or 2)"
```

Save to `/Users/andre.butkevich/Desktop/Projects/ML-Ops/tests/test_train.py`

- [ ] **Step 3: Write test_inference.py**

```python
"""
Unit tests for inference script.
"""
import pytest
import joblib
import os
import pandas as pd
from src.inference import inference
from src.train import train

def test_inference_with_saved_model():
    """Test that inference works with a saved model"""
    
    # Ensure model exists
    train()
    
    # Load model
    model = joblib.load('models/model.pkl')
    
    # Create sample data
    sample_data = pd.DataFrame({
        'sepal_length': [5.1, 7.0],
        'sepal_width': [3.5, 3.2],
        'petal_length': [1.4, 4.7],
        'petal_width': [0.2, 1.4]
    })
    
    # Make predictions
    predictions = model.predict(sample_data)
    
    # Assert results
    assert len(predictions) == 2, "Should return two predictions"
    assert all(p in [0, 1, 2] for p in predictions), "All predictions should be valid classes"

def test_inference_runs_without_error():
    """Test that the inference script runs without raising an exception"""
    
    # Ensure model exists
    train()
    
    # This should not raise an exception
    try:
        inference()
    except Exception as e:
        pytest.fail(f"Inference script raised exception: {e}")
```

Save to `/Users/andre.butkevich/Desktop/Projects/ML-Ops/tests/test_inference.py`

- [ ] **Step 4: Run tests to verify they pass**

```bash
cd /Users/andre.butkevich/Desktop/Projects/ML-Ops
pytest tests/ -v
```

Expected output: All tests pass (e.g., `test_train.py::test_train_creates_model PASSED`)

- [ ] **Step 5: Commit**

```bash
git add tests/test_train.py tests/test_inference.py tests/__init__.py
git commit -m "test: add unit tests for training and inference"
```

---

### Task 6: Create GitHub Actions Workflow

**Files:**
- Create: `.github/workflows/mlops-pipeline.yml`

**Estimated Time:** 60 minutes

- [ ] **Step 1: Create .github/workflows directory**

```bash
mkdir -p /Users/andre.butkevich/Desktop/Projects/ML-Ops/.github/workflows
```

- [ ] **Step 2: Write GitHub Actions workflow**

```yaml
name: MLOps Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  detect-changes:
    name: Detect Changes
    runs-on: ubuntu-latest
    outputs:
      should_train: ${{ steps.changes.outputs.should_train }}
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
      
      - name: Check for changes in training files
        id: changes
        run: |
          if git diff --name-only origin/main...HEAD | grep -E '(src/train|src/evaluate|data/)'; then
            echo "should_train=true" >> $GITHUB_OUTPUT
          else
            echo "should_train=false" >> $GITHUB_OUTPUT
          fi
        continue-on-error: true

  train:
    name: Train Model
    needs: detect-changes
    if: needs.detect-changes.outputs.should_train == 'true' || github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python 3.11
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          cache: 'pip'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      
      - name: Train model
        run: python src/train.py
      
      - name: Upload model artifact
        uses: actions/upload-artifact@v3
        with:
          name: model
          path: models/model.pkl
          retention-days: 30

  evaluate:
    name: Evaluate Model
    needs: train
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python 3.11
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          cache: 'pip'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      
      - name: Download model artifact
        uses: actions/download-artifact@v3
        with:
          name: model
          path: models/
      
      - name: Evaluate model
        run: python src/evaluate.py
      
      - name: Upload metrics artifact
        uses: actions/upload-artifact@v3
        with:
          name: metrics
          path: results/metrics.json
          retention-days: 30

  inference-test:
    name: Test Inference
    needs: evaluate
    if: always()
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python 3.11
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          cache: 'pip'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      
      - name: Download model artifact
        uses: actions/download-artifact@v3
        with:
          name: model
          path: models/
        continue-on-error: true
      
      - name: Test inference
        run: python src/inference.py

  unit-tests:
    name: Unit Tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python 3.11
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          cache: 'pip'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      
      - name: Run pytest
        run: pytest tests/ -v
```

Save to `/Users/andre.butkevich/Desktop/Projects/ML-Ops/.github/workflows/mlops-pipeline.yml`

- [ ] **Step 3: Validate YAML syntax**

```bash
cd /Users/andre.butkevich/Desktop/Projects/ML-Ops
python -c "import yaml; yaml.safe_load(open('.github/workflows/mlops-pipeline.yml'))" && echo "✓ YAML is valid"
```

Expected: `✓ YAML is valid`

- [ ] **Step 4: Review workflow logic**

Open `.github/workflows/mlops-pipeline.yml` and verify:
- ✓ Trigger on push/PR to main
- ✓ Change detection job outputs `should_train` flag
- ✓ Train job depends on detect-changes
- ✓ Evaluate job depends on train
- ✓ Inference-test job depends on evaluate
- ✓ Unit-tests job runs independently
- ✓ Artifacts uploaded with 30-day retention

- [ ] **Step 5: Commit**

```bash
git add .github/workflows/mlops-pipeline.yml
git commit -m "ci: add GitHub Actions MLOps pipeline workflow"
```

---

### Task 7: Create README and Documentation

**Files:**
- Create: `README.md`

**Estimated Time:** 30 minutes

- [ ] **Step 1: Write README.md**

```markdown
# ML-Ops: Automated MLOps Pipeline

An end-to-end machine learning pipeline for training and evaluating models with GitHub Actions CI/CD.

## Quick Start

### Local Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Train model:**
   ```bash
   python src/train.py
   ```
   Creates `models/model.pkl`

3. **Evaluate model:**
   ```bash
   python src/evaluate.py
   ```
   Creates `results/metrics.json`

4. **Test inference:**
   ```bash
   python src/inference.py
   ```

5. **Run unit tests:**
   ```bash
   pytest tests/ -v
   ```

### Full Local Pipeline

```bash
# All in one
python src/train.py && python src/evaluate.py && python src/inference.py && pytest tests/
```

## Project Structure

```
├── src/
│   ├── train.py        # Training script (Iris + Logistic Regression)
│   ├── evaluate.py     # Evaluation script (metrics + validation)
│   └── inference.py    # Inference script (predictions)
├── tests/
│   ├── test_train.py   # Unit tests for training
│   └── test_inference.py # Unit tests for inference
├── models/
│   └── model.pkl       # Trained model (generated)
├── results/
│   └── metrics.json    # Evaluation metrics (generated)
└── .github/workflows/
    └── mlops-pipeline.yml # GitHub Actions workflow
```

## Pipeline Flow

```
git push → GitHub Actions
  ├─ Detect Changes (train.py, evaluate.py, data/)
  ├─ Train Job (if changes detected)
  │  └─ Load Iris → Train Logistic Regression → Save model.pkl
  ├─ Evaluate Job (depends on Train)
  │  └─ Load model → Compute metrics → Validate (Accuracy > 0.70)
  ├─ Inference Test Job (depends on Evaluate)
  │  └─ Load model → Make predictions on samples
  └─ Unit Tests Job (always runs)
     └─ pytest tests/
```

## GitHub Actions Workflow

The pipeline is defined in `.github/workflows/mlops-pipeline.yml` and triggers on:
- Push to `main` or `develop`
- Pull request to `main`

**Jobs:**
1. **detect-changes** - Check if training files changed
2. **train** - Train model (conditional on changes)
3. **evaluate** - Evaluate and validate model (depends on train)
4. **inference-test** - Test inference (depends on evaluate)
5. **unit-tests** - Run pytest (always runs)

**Artifacts:**
- `model.pkl` - Trained model (30-day retention)
- `metrics.json` - Evaluation metrics (30-day retention)

## Model Details

- **Dataset:** Iris (150 samples, 4 features, 3 classes)
- **Algorithm:** Logistic Regression
- **Train/Test Split:** 80/20
- **Accuracy Threshold:** 0.70 (fails if lower)
- **Target Classes:** setosa, versicolor, virginica

## Next Steps (Future Iterations)

- **Iteration 2:** REST API wrapper (Flask/FastAPI)
- **Iteration 3:** Model registry (MLflow)
- **Iteration 4:** Data validation (Great Expectations)
- **Iteration 5:** Advanced models (Random Forest, XGBoost)

## Troubleshooting

### Model training fails locally
```bash
# Check Python version
python --version  # Should be 3.11+

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Run training with verbose output
python -u src/train.py
```

### Tests fail
```bash
# Run a specific test
pytest tests/test_train.py::test_train_creates_model -v

# Run with more detail
pytest tests/ -vv -s
```

### GitHub Actions not triggering
- Check that you pushed to `main` or `develop`
- Verify `.github/workflows/mlops-pipeline.yml` is on the branch
- Check **Actions** tab in GitHub for error logs

## License

MIT
```

Save to `/Users/andre.butkevich/Desktop/Projects/ML-Ops/README.md`

- [ ] **Step 2: Verify README is readable**

```bash
cat /Users/andre.butkevich/Desktop/Projects/ML-Ops/README.md
```

Expected: Readable markdown with all sections

- [ ] **Step 3: Commit**

```bash
git add README.md GITHUB_ACTIONS_VS_GITLAB_CI.md
git commit -m "docs: add README and GitHub Actions reference guide"
```

---

### Task 8: Final Testing & Verification

**Files:**
- Verify all existing files work together

**Estimated Time:** 30 minutes

- [ ] **Step 1: Run full local pipeline**

```bash
cd /Users/andre.butkevich/Desktop/Projects/ML-Ops
echo "=== Running training ===" && python src/train.py
echo -e "\n=== Running evaluation ===" && python src/evaluate.py
echo -e "\n=== Running inference ===" && python src/inference.py
echo -e "\n=== Running tests ===" && pytest tests/ -v
```

Expected output: All commands succeed, no errors

- [ ] **Step 2: Verify all artifacts exist**

```bash
ls -lh /Users/andre.butkevich/Desktop/Projects/ML-Ops/models/model.pkl
ls -lh /Users/andre.butkevich/Desktop/Projects/ML-Ops/results/metrics.json
cat /Users/andre.butkevich/Desktop/Projects/ML-Ops/results/metrics.json | head -20
```

Expected: Both files exist and contain valid data

- [ ] **Step 3: Verify git history**

```bash
git log --oneline | head -10
```

Expected: 7-8 commits from this session

- [ ] **Step 4: Verify GitHub Actions workflow syntax**

```bash
python -c "import yaml; w=yaml.safe_load(open('.github/workflows/mlops-pipeline.yml')); print(f'Workflow: {w[\"name\"]}'); print(f'Jobs: {list(w[\"jobs\"].keys())}')"
```

Expected: Workflow name and job list printed

- [ ] **Step 5: Create .github directory check**

```bash
find .github -type f -name "*.yml" -o -name "*.yaml"
```

Expected: `.github/workflows/mlops-pipeline.yml` listed

- [ ] **Step 6: Final git status**

```bash
git status
```

Expected: `nothing to commit, working tree clean`

- [ ] **Step 7: Final commit summary**

```bash
git log --oneline --all | head -15
```

Review the commits to ensure all tasks are covered

---

## Plan Review Checklist

✅ **Spec Coverage:**
- [x] Training script with Iris data
- [x] Logistic Regression model
- [x] Evaluation with metrics and validation
- [x] Inference testing
- [x] GitHub Actions workflow with change detection
- [x] Unit tests
- [x] Model serialization (.pkl)
- [x] Artifact management
- [x] README and documentation

✅ **No Placeholders:**
- [x] All code is complete and runnable
- [x] All commands are exact with expected output
- [x] All file paths are absolute or relative with full context
- [x] All YAML is syntactically valid
- [x] No "TODO", "TBD", or "implement later" statements

✅ **Type Consistency:**
- [x] Model type: LogisticRegression (consistent across all scripts)
- [x] Data format: DataFrame (pandas, consistent in inference)
- [x] Metrics format: JSON (consistent across evaluation)
- [x] File paths: Relative (models/, results/, src/, tests/)

✅ **Task Granularity:**
- [x] Each step is 2-10 minutes of work
- [x] Each step produces observable output
- [x] Each task ends with a commit
- [x] Tests verify at each stage

---

## Execution Path

This plan is ready to execute. Two options:

**Option 1: Subagent-Driven (Recommended)**
- Fresh subagent per task
- I review output between tasks
- Faster iteration, better error isolation
- Use `superpowers:subagent-driven-development`

**Option 2: Inline Execution**
- Execute all tasks sequentially in this session
- Checkpoint after each task
- More direct control
- Use `superpowers:executing-plans`

---
