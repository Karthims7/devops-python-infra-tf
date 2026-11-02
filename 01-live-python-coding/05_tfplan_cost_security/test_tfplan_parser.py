from tfplan_parser import TerraformPlanAuditor


def test_clean_plan_passes():
    plan = {
        "resource_changes": [
            {
                "address": "aws_s3_bucket.app_data",
                "type": "aws_s3_bucket",
                "change": {
                    "actions": ["create"],
                    "after": {
                        "bucket": "toyota-wovencar-telemetry",
                        "tags": {
                            "Environment": "production",
                            "Team": "DevOps",
                            "ManagedBy": "Terraform",
                        },
                    },
                },
            }
        ]
    }

    auditor = TerraformPlanAuditor(plan)
    report = auditor.audit()
    assert report.passed is True
    assert len(report.violations) == 0


def test_detect_database_deletion():
    plan = {
        "resource_changes": [
            {
                "address": "aws_db_instance.primary",
                "type": "aws_db_instance",
                "change": {
                    "actions": ["delete"],
                    "before": {"id": "rds-1234"},
                },
            }
        ]
    }

    auditor = TerraformPlanAuditor(plan)
    report = auditor.audit()
    assert report.passed is False
    assert any(v.rule_name == "NO_STATEFUL_RESOURCE_DELETION" for v in report.violations)


def test_detect_open_ssh_security_group():
    plan = {
        "resource_changes": [
            {
                "address": "aws_security_group.web",
                "type": "aws_security_group",
                "change": {
                    "actions": ["create"],
                    "after": {
                        "tags": {
                            "Environment": "prod",
                            "Team": "Core",
                            "ManagedBy": "Terraform",
                        },
                        "ingress": [
                            {
                                "from_port": 22,
                                "to_port": 22,
                                "protocol": "tcp",
                                "cidr_blocks": ["0.0.0.0/0"],
                            }
                        ],
                    },
                },
            }
        ]
    }

    auditor = TerraformPlanAuditor(plan)
    report = auditor.audit()
    assert report.passed is False
    assert any(v.rule_name == "OPEN_INGRESS_MANAGEMENT_PORT" for v in report.violations)


def test_detect_missing_mandatory_tags():
    plan = {
        "resource_changes": [
            {
                "address": "aws_instance.worker",
                "type": "aws_instance",
                "change": {
                    "actions": ["create"],
                    "after": {
                        "tags": {"Environment": "staging"}  # missing Team and ManagedBy
                    },
                },
            }
        ]
    }

    auditor = TerraformPlanAuditor(plan)
    report = auditor.audit()
    assert report.passed is False
    assert any(v.rule_name == "MISSING_MANDATORY_TAGS" for v in report.violations)
