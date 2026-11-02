# Enterprise Terraform Architecture & Best Practices

## 1. Remote State Management & Locking
- **Architecture:** S3 / Google Cloud Storage for state files + DynamoDB / Cloud Storage native object locks for state locking.
- **Encryption:** Server-Side Encryption with AWS KMS (Customer Managed Key - CMK) or GCP Cloud KMS.
- **Access Control:** Strict IAM bucket policies preventing public access and enforcing TLS (`aws:SecureTransport`).
- **State Segregation:** Never maintain a single monolithic state file. Divide state by:
  - Account boundary (mgmt, dev, staging, prod)
  - Lifecycle / rate of change (network/VPC -> data layers/DB -> compute/EKS -> app services)

## 2. Infrastructure Delivery Pipeline Patterns (Atlantis vs GitHub Actions)
- **Atlantis Pattern:**
  - Pull Request based workflow.
  - Comment-driven: Developers comment `atlantis plan` and `atlantis apply`.
  - Automatic locking: Locks the Terraform directory on PR open to prevent conflicting plans.
- **GitHub Actions (OIDC + Plan/Apply split):**
  - Use AWS IAM / GCP Workload Identity Federation (OIDC) instead of static long-lived credentials.
  - Pull Request trigger: Runs `terraform fmt -check`, `tflint`, `trivy/tfsec`, and `terraform plan -out=tfplan`.
  - The plan file is encrypted and saved as an artifact.
  - Main merge trigger: Downloads the exact approved `tfplan` and executes `terraform apply tfplan`.

## 3. Drift Detection & Reconciliation Automation
- **The Problem:** Manual changes made via Cloud Console create state drift.
- **Automated Solution:**
  - A nightly scheduled workflow runs:
    ```bash
    terraform plan -detailed-exitcode -no-color
    ```
  - Exit code meanings:
    - `0`: Succeeded, no changes (In Sync).
    - `1`: Error occurred.
    - `2`: Succeeded, but differences / drift detected!
  - If exit code is `2`, an alert is dispatched to Slack/PagerDuty or an automated reconciliation PR/ticket is created.

## 4. Multi-Environment DRY Architecture (Terragrunt vs Workspaces)
- **Terraform Workspaces:** Good for identical transient ephemeral environments, but risky for dev vs prod (shared backend state key, easy to accidentally apply prod changes).
- **Terragrunt / File-Tree Structuring:**
  - Separate directories per environment (`environments/prod/vpc`, `environments/dev/vpc`).
  - Common root `terragrunt.hcl` handles backend generation and provider configurations.
  - Eliminates duplicate boilerplate across accounts.

## 5. Security & Policy as Code
- **Pre-commit:** `pre-commit-terraform` (hooks for `terraform_fmt`, `terraform_docs`, `terraform_tflint`).
- **Static Analysis:** Trivy, Checkov, or tfsec scanning for CVEs and misconfigurations.
- **Dynamic Guardrails:** Open Policy Agent (OPA) / Conftest or custom Python plan analyzers to enforce enterprise compliance.

