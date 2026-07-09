# GitHub Actions vs. GitLab CI/CD — Quick Reference

**TL;DR:** Beide sind CI/CD-Systeme mit sehr ähnlichen Konzepten. GitHub Actions hat eigene Syntax, ist aber nicht komplizierter.

---

## Quick Comparison Table

| Aspect | GitHub Actions | GitLab CI/CD |
|--------|---|---|
| **Config File** | `.github/workflows/*.yml` | `.gitlab-ci.yml` |
| **Basic Unit** | Job | Job |
| **Job Grouping** | Workflow | Pipeline |
| **Syntax** | YAML (similar) | YAML (similar) |
| **Trigger** | `on:` keyword | `rules:` or implicit |
| **Runs On** | GitHub-hosted or self-hosted | GitLab-hosted or self-hosted |
| **Cost (Free Tier)** | 2000 mins/month | 400 mins/month |
| **Secret Management** | Repo secrets | CI/CD variables |
| **Artifact Storage** | 90 days retention | Configurable |
| **Ease of Learning** | ⭐⭐⭐⭐ (very clear) | ⭐⭐⭐ (good but more verbose) |

---

## Side-by-Side: Same Pipeline in Both

### GitLab CI/CD (.gitlab-ci.yml)

```yaml
stages:
  - train
  - evaluate
  - test

train:
  stage: train
  image: python:3.11
  script:
    - pip install -r requirements.txt
    - python src/train.py
  artifacts:
    paths:
      - models/model.pkl
  only:
    - main

evaluate:
  stage: evaluate
  image: python:3.11
  script:
    - pip install -r requirements.txt
    - python src/evaluate.py
  artifacts:
    paths:
      - results/metrics.json
  dependencies:
    - train
  only:
    - main
```

### GitHub Actions (.github/workflows/mlops.yml)

```yaml
name: MLOps Pipeline
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  train:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python src/train.py
      - uses: actions/upload-artifact@v3
        with:
          name: model
          path: models/model.pkl

  evaluate:
    needs: train
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - uses: actions/download-artifact@v3
        with:
          name: model
      - run: python src/evaluate.py
      - uses: actions/upload-artifact@v3
        with:
          name: metrics
          path: results/metrics.json
```

---

## Key Differences You'll Notice

### 1. **Trigger Syntax**

**GitLab:**
```yaml
only:
  - main
```
Simple: "only run on main branch"

**GitHub Actions:**
```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
```
More explicit: "trigger on push to main OR on pull requests"

---

### 2. **Dependencies Between Jobs**

**GitLab:**
```yaml
dependencies:
  - train  # This job depends on 'train' job
```

**GitHub Actions:**
```yaml
needs: train  # Same thing, different keyword
```

---

### 3. **Docker Image / Runner Setup**

**GitLab:**
```yaml
image: python:3.11  # Specify image at job level
```
Auto-spins Docker container with Python 3.11

**GitHub Actions:**
```yaml
runs-on: ubuntu-latest  # Runner type (machine)
- uses: actions/setup-python@v4  # Action to install Python
  with:
    python-version: '3.11'
```
You specify the runner, then explicitly set up Python

---

### 4. **Actions / Reusable Components**

**GitLab:**
- Has CI templates (limited)
- Mostly write your own scripts

**GitHub Actions:**
- **Action Marketplace** with thousands of pre-built actions
  - `actions/checkout@v3` — Clone your repo
  - `actions/setup-python@v4` — Install Python
  - `actions/upload-artifact@v3` — Store files
  - Community actions: deploy, notify, test coverage, etc.
- **Super useful:** Reduces boilerplate significantly

---

### 5. **Artifact Handling**

**GitLab:**
```yaml
artifacts:
  paths:
    - models/model.pkl
```
Artifacts auto-saved, 30-day retention by default

**GitHub Actions:**
```yaml
- uses: actions/upload-artifact@v3
  with:
    name: model
    path: models/model.pkl
```
Explicit action, 90-day retention by default

---

## Mental Model: Mapping GitLab → GitHub Actions

| GitLab Concept | GitHub Actions Equivalent |
|---|---|
| `.gitlab-ci.yml` file | `.github/workflows/file.yml` |
| `stages:` | (implicit via `needs:`) |
| `only:` | `on:` trigger |
| Job-level `image:` | Runner + `setup-*` actions |
| `artifacts:` | `actions/upload-artifact@v3` |
| `dependencies:` | `needs:` keyword |
| `variables:` | Secrets or env vars |
| `script:` | `run:` or custom actions |

---

## Learning Path for You

### Coming from GitLab, GitHub Actions is simpler because:

1. **Trigger is clearer:** `on:` is explicit about events (push, PR, schedule, etc.)
2. **Actions marketplace:** Don't reinvent the wheel, use pre-built actions
3. **Syntax is less verbose:** No `stages:` needed, just `needs:`
4. **Better for small pipelines:** Perfect for your first 8h project

### Common Gotchas:

1. **Action vs. Run:** 
   - `run:` = execute a shell command
   - `uses:` = run a pre-built action (from marketplace)
   - Easy to mix up at first

2. **Artifact Downloads:**
   - In GitLab: `dependencies:` auto-downloads
   - In GitHub: Must explicitly `download-artifact` if you need it
   - Not a big deal, just more explicit

3. **Secrets:**
   - In GitLab: `variables:` in CI/CD settings
   - In GitHub: `secrets:` in repo settings
   - Usage: `${{ secrets.MY_SECRET }}` (same idea, different syntax)

---

## For Your First 8h Project

### GitHub Actions is actually **easier** than GitLab because:

✅ Marketplace actions save you time (setup-python, upload-artifact)  
✅ Simpler trigger syntax (`on:`)  
✅ Great documentation + examples  
✅ Free tier is generous (2000 mins/month vs GitLab's 400)  

### You'll write:

1. **One workflow file** (`.github/workflows/mlops-pipeline.yml`)
2. **Basic structure:**
   ```yaml
   name: MLOps Pipeline
   on: [push, pull_request]
   jobs:
     train:
       runs-on: ubuntu-latest
       steps: [...]
     evaluate:
       needs: train
       runs-on: ubuntu-latest
       steps: [...]
   ```

That's it. Not complicated.

---

## Pro Tips for GitHub Actions

1. **Use the Action Marketplace:** 90% of what you need exists. Search [github.com/marketplace](https://github.com/marketplace)
2. **Logs are great:** Click any step to see detailed output
3. **Test locally:** Can use `act` tool to test workflows locally before pushing
4. **Reusable workflows:** Later, you can extract common patterns into `.github/workflows/shared.yml`
5. **Matrix builds:** Easy to test on multiple Python versions simultaneously

---

## Summary

**GitHub Actions vs. GitLab CI/CD:**
- **Concepts:** ~95% identical
- **Syntax:** Slightly different keywords, GitHub is clearer
- **Marketplace:** GitHub wins (huge community)
- **Free tier:** GitHub wins (2000 vs 400 mins)
- **Learning curve for you:** Lower — you already know CI/CD concepts

**Bottom line:** You'll pick it up in an hour. It's not harder, just slightly different syntax.
