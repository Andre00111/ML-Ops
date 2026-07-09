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
