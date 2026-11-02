terraform {
  required_version = ">= 1.5.0"
  required_providers {
    github = {
      source  = "integrations/github"
      version = "~> 6.0"
    }
  }
}

# 1. Standardized Repository
resource "github_repository" "repo" {
  name        = var.repository_name
  description = var.description
  visibility  = var.visibility

  has_issues      = true
  has_projects    = false
  has_wiki        = false
  has_discussions = false

  # Enforce squash merging for clean, linear Git history
  allow_squash_merge = true
  allow_merge_commit = false
  allow_rebase_merge = false
  delete_branch_on_merge = true

  # Security & Compliance Features
  vulnerability_alerts = true

  security_and_analysis {
    secret_scanning {
      status = "enabled"
    }
    secret_scanning_push_protection {
      status = "enabled"
    }
  }

  topics = var.topics
}

# 2. Modern GitHub Repository Ruleset (Rulesets > Legacy Branch Protection)
resource "github_repository_ruleset" "default_branch_rules" {
  name        = "Enterprise Default Branch Protection"
  repository  = github_repository.repo.name
  target      = "branch"
  enforcement = "active"

  conditions {
    ref_name {
      include = ["~DEFAULT_BRANCH"]
      exclude = []
    }
  }

  rules {
    # Block force pushes and branch deletion
    non_fast_forward = true
    deletion         = true

    # Pull Request Requirements
    pull_request {
      required_approving_review_count = var.required_approvals
      dismiss_stale_reviews_on_push   = true
      require_code_owner_review       = true
      require_last_push_approval      = true
    }

    # Required CI Status Checks before merging
    required_status_checks {
      strict_required_status_checks_policy = true
      required_check {
        context = "ci/unit-tests"
      }
      required_check {
        context = "security/trivy-scan"
      }
    }
  }
}

