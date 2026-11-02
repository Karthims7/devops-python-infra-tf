# Woven by Toyota | Senior DevOps Engineer Interview Prep Hub

**Role:** Senior DevOps Engineer (Contract / B2B)  
**Client:** Woven by Toyota (Tokyo, Japan - Remote)  
**Agency:** Hays Japan (Jun Lee)  
**Comp Band:** ¥800,000 – ¥1,100,000 / month  
**Core Pillars:**
1. **Hands-on Python Development & Tooling** (Live Coding Test focus)
2. **Infrastructure Delivery via Terraform** (Enterprise modules, state, drift, policy)
3. **GitHub Repository Controls & Governance** (GitHub API / Terraform GitHub provider / Automation)

---

## 🎯 Interview Focus Breakdown

Woven by Toyota (formerly Woven Planet / TRI-AD) operates as Toyota's advanced mobility and autonomous software arm. Their engineering culture mirrors Silicon Valley tier tech (Google, AWS, Waymo style) with Japanese principles of **Kaizen (continuous improvement)** and **Quality-First Software Craftsmanship**.

For a **Senior DevOps Engineer**, they evaluate:
- **Can you code like a Software Engineer?** Not just short bash scripts: object-oriented design, typing (`typing`), error handling, generator usage, concurrency (`asyncio`/`threading`), unit testing with `pytest`, mock fixtures, and clean architecture.
- **Can you think out loud during live coding?** Clarifying requirements, stating time/space complexity, writing tests first or alongside, and handling edge cases gracefully.
- **Terraform mastery:** Enterprise multi-environment patterns, custom automation around Terraform (parsing plans, drift detection, state management, Atlantis/GitHub Actions automation).
- **GitHub Governance as Code:** Org-level policy enforcement, branch rulesets, CODEOWNERS, secret scanning, repo provisioning at scale.

---

## 📂 Repository Structure

```text
├── 01-live-python-coding/          # High-probability live coding problems with tests & explanations
│   ├── 01_rate_limiter/            # Token bucket & sliding window (API throttling & decorators)
│   ├── 02_dag_task_scheduler/      # Topological sort / dependency resolver (CI/CD pipeline DAG)
│   ├── 03_log_metrics_analyzer/    # High-throughput log stream parser & percentile latency (P95/P99)
│   ├── 04_retry_backoff_decorator/ # Exponential backoff with jitter (resilient API integrations)
│   └── 05_tfplan_cost_security/    # Parsing Terraform plan JSON to extract security/cost violations
│
├── 02-github-governance-automation/# Production-grade GitHub governance tool in Python
│   ├── repo_governance_auditor.py  # Multi-repo branch protection & secret scanning enforcer
│   └── test_repo_governance.py     # Unit & mock test suite
│
├── 03-terraform-architecture/      # Senior-level Terraform architectures
│   ├── github-repo-standard/       # Managing GitHub repositories & rulesets via Terraform
│   └── enterprise-patterns.md      # State locking, drift detection, Terragrunt, policy-as-code
│
├── 04-cheat-sheets-and-qa/         # High-impact interview question prep & talk-tracks
│   ├── live_coding_strategy.md     # Step-by-step game plan to ace the live coding test
│   ├── python_senior_devops_qa.md  # Deep technical Python Q&A for DevOps
│   ├── terraform_deep_dive_qa.md   # Advanced Terraform Q&A
│   └── woven_toyota_culture_qa.md  # Culture fit, Japan remote collaboration & communication
│
├── requirements.txt                # Python environment setup
└── pyproject.toml                  # Linting & test config
```

---

## 🚀 Quick Start for Live Coding Practice

```bash
# 1. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run all test suites
pytest -v
```

