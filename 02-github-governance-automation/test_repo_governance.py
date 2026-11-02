import unittest
from unittest.mock import MagicMock
from repo_governance_auditor import RepoGovernanceAuditor, GitHubAPIClient


class TestRepoGovernanceAuditor(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock(spec=GitHubAPIClient)
        self.auditor = RepoGovernanceAuditor(self.mock_client)

    def test_compliant_repo(self):
        self.mock_client.request.side_effect = [
            # 1. repo metadata
            {
                "default_branch": "main",
                "security_and_analysis": {
                    "secret_scanning": {"status": "enabled"}
                }
            },
            # 2. branch protection
            {
                "enforce_admins": {"enabled": True},
                "required_pull_request_reviews": {
                    "required_approving_review_count": 2,
                    "dismiss_stale_reviews": True,
                    "require_code_owner_reviews": True,
                }
            }
        ]

        result = self.auditor.audit_repository("woven-by-toyota", "autonomous-nav")
        self.assertTrue(result["compliant"])
        self.assertEqual(len(result["findings"]), 0)

    def test_non_compliant_repo_flags_violations(self):
        self.mock_client.request.side_effect = [
            # 1. repo metadata
            {
                "default_branch": "main",
                "security_and_analysis": {
                    "secret_scanning": {"status": "disabled"}
                }
            },
            # 2. branch protection
            {
                "enforce_admins": {"enabled": False},
                "required_pull_request_reviews": {
                    "required_approving_review_count": 1,
                    "dismiss_stale_reviews": False,
                    "require_code_owner_reviews": False,
                }
            }
        ]

        result = self.auditor.audit_repository("woven-by-toyota", "legacy-service")
        self.assertFalse(result["compliant"])
        controls_failed = [f["control"] for f in result["findings"]]
        self.assertIn("SECRET_SCANNING", controls_failed)
        self.assertIn("REQUIRED_PR_APPROVALS", controls_failed)
        self.assertIn("DISMISS_STALE_REVIEWS", controls_failed)
        self.assertIn("ENFORCE_ADMINS", controls_failed)


if __name__ == "__main__":
    unittest.main()

