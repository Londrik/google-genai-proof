from unittest.mock import MagicMock

import pytest
from pydantic import ValidationError

from src.schemas.audit import AuditReport, RiskSeverity
from src.services.analyzer import ContentAnalyzerService


def test_audit_schema_valid_instantiation() -> None:
    data = {
        "target_name": "config/database.py",
        "summary": "Hardcoded credentials detectadas no script.",
        "score": 40,
        "passed": False,
        "findings": [
            {
                "category": "Segurança",
                "severity": "CRITICAL",
                "description": "Senha de banco exposta em texto claro.",
                "remediation": "Utilizar variáveis de ambiente injetadas via Vault/Secret Manager.",
            }
        ],
    }
    report = AuditReport.model_validate(data)
    assert report.score == 40
    assert report.passed is False
    assert len(report.findings) == 1
    assert report.findings[0].severity == RiskSeverity.CRITICAL


def test_audit_schema_rejects_out_of_range_score() -> None:
    data = {
        "target_name": "auth.py",
        "summary": "Score inválido para teste de validação",
        "score": 101,
        "passed": True,
        "findings": [],
    }
    with pytest.raises(ValidationError):
        AuditReport.model_validate(data)


def test_analyzer_service_parses_json_into_pydantic_model() -> None:
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.text = (
        '{"target_name": "jwt_service.py", "summary": "Nenhuma falha crítica.", '
        '"score": 98, "passed": true, "findings": []}'
    )
    mock_client.models.generate_content.return_value = mock_response

    service = ContentAnalyzerService(client=mock_client)
    report = service.analyze_text("jwt_service.py", "def verify_token(): pass")

    assert isinstance(report, AuditReport)
    assert report.target_name == "jwt_service.py"
    assert report.score == 98
    assert report.passed is True
    assert report.findings == []
