from unittest.mock import MagicMock, patch

from src.cli.main import run_audit, run_safety_check
from src.schemas.audit import AuditReport
from src.schemas.safety import SafetyCheckResult


@patch("src.cli.main.ContentAnalyzerService")
def test_cli_run_audit_success(mock_service_class: MagicMock) -> None:
    mock_service = MagicMock()
    mock_service.analyze_text.return_value = AuditReport(
        target_name="cli_test.py",
        summary="Auditoria concluída com sucesso.",
        score=100,
        passed=True,
        findings=[],
    )
    mock_service_class.return_value = mock_service

    # Não deve lançar exceção
    run_audit(target="cli_test.py", content="print('clean code')")
    mock_service.analyze_text.assert_called_once_with(
        target_name="cli_test.py", raw_content="print('clean code')"
    )


@patch("src.cli.main.ResponsibleAIService")
def test_cli_run_safety_check_blocked(mock_safety_class: MagicMock) -> None:
    mock_service = MagicMock()
    mock_service.generate_with_guardrails.return_value = SafetyCheckResult(
        is_blocked=True, block_reason="SAFETY", disclaimer="Blocked by policy"
    )
    mock_safety_class.return_value = mock_service

    # Não deve lançar exceção
    run_safety_check(prompt="unsafe content")
    mock_service.generate_with_guardrails.assert_called_once_with("unsafe content")
