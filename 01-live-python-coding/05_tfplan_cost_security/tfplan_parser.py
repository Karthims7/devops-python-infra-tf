"""
Terraform Plan JSON Security & Policy Auditor
Scenario:
"In your CI/CD pipeline, you run `terraform plan -out=tfplan.binary`
followed by `terraform show -json tfplan.binary > plan.json`.
Implement a Python policy validator that parses the plan JSON to:
1. Detect accidental deletions of stateful production resources (e.g. databases, S3, KMS)
2. Flag insecure security group rules (e.g. Ingress port 22 or 3389 open to 0.0.0.0/0)
3. Enforce mandatory resource tags ('Environment', 'Team', 'ManagedBy')
4. Return a structured audit report with exit codes (0 for pass, 1 for violations)"
"""

from typing import Dict, Any, List, Set
from dataclasses import dataclass, field


PROTECTED_RESOURCE_TYPES = {
    "aws_db_instance",
    "aws_s3_bucket",
    "aws_kms_key",
    "google_sql_database_instance",
}

MANDATORY_TAGS = {"Environment", "Team", "ManagedBy"}


@dataclass
class PolicyViolation:
    rule_name: str
    severity: str  # "HIGH", "CRITICAL", "MEDIUM"
    resource_address: str
    message: str


@dataclass
class AuditReport:
    total_resources_evaluated: int = 0
    passed: bool = True
    violations: List[PolicyViolation] = field(default_factory=list)


class TerraformPlanAuditor:
    def __init__(self, plan_data: Dict[str, Any]):
        self.plan_data = plan_data
        self.resource_changes = plan_data.get("resource_changes", [])

    def audit(self) -> AuditReport:
        report = AuditReport()
        report.total_resources_evaluated = len(self.resource_changes)

        for resource in self.resource_changes:
            address = resource.get("address", "unknown")
            res_type = resource.get("type", "")
            change = resource.get("change", {})
            actions: List[str] = change.get("actions", [])
            after = change.get("after") or {}

            # Rule 1: No deletion of protected resources
            if "delete" in actions and res_type in PROTECTED_RESOURCE_TYPES:
                report.violations.append(
                    PolicyViolation(
                        rule_name="NO_STATEFUL_RESOURCE_DELETION",
                        severity="CRITICAL",
                        resource_address=address,
                        message=f"Attempting to delete protected resource of type '{res_type}'",
                    )
                )

            # Rule 2: Ingress open to 0.0.0.0/0 on sensitive ports (SSH 22, RDP 3389)
            if res_type in ("aws_security_group", "aws_security_group_rule"):
                self._check_security_group_rules(resource, report)

            # Rule 3: Enforce mandatory tags for create/update operations
            if any(act in ("create", "update") for act in actions):
                self._check_mandatory_tags(address, res_type, after, report)

        report.passed = len(report.violations) == 0
        return report

    def _check_security_group_rules(self, resource: Dict[str, Any], report: AuditReport) -> None:
        address = resource.get("address", "")
        after = resource.get("change", {}).get("after") or {}
        ingress_rules = after.get("ingress", [])

        # If it's an aws_security_group_rule directly
        if resource.get("type") == "aws_security_group_rule":
            ingress_rules = [after]

        for rule in ingress_rules:
            cidr_blocks = rule.get("cidr_blocks", [])
            from_port = rule.get("from_port", 0)
            to_port = rule.get("to_port", 0)

            if "0.0.0.0/0" in cidr_blocks:
                # Sensitive ports 22 (SSH), 3389 (RDP)
                if from_port <= 22 <= to_port or from_port <= 3389 <= to_port:
                    report.violations.append(
                        PolicyViolation(
                            rule_name="OPEN_INGRESS_MANAGEMENT_PORT",
                            severity="CRITICAL",
                            resource_address=address,
                            message=f"Ingress port {from_port}-{to_port} is wide open to 0.0.0.0/0",
                        )
                    )

    def _check_mandatory_tags(
        self, address: str, res_type: str, after: Dict[str, Any], report: AuditReport
    ) -> None:
        # Ignore tag checks on resources that do not support tags
        if res_type.endswith("_rule") or res_type.endswith("_association"):
            return

        tags = after.get("tags") or {}
        missing_tags = MANDATORY_TAGS - set(tags.keys())
        if missing_tags:
            report.violations.append(
                PolicyViolation(
                    rule_name="MISSING_MANDATORY_TAGS",
                    severity="HIGH",
                    resource_address=address,
                    message=f"Missing required tags: {', '.join(sorted(missing_tags))}",
                )
            )

