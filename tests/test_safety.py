from unittest.mock import MagicMock

from google.genai import types

from src.schemas.safety import SafetyBlockReason, SafetyCheckResult
from src.services.safety import ResponsibleAIService


def test_safety_settings_configuration() -> None:
    service = ResponsibleAIService(client=MagicMock())
    settings_list = service.get_strict_safety_settings()
    assert len(settings_list) == 4
    for item in settings_list:
        assert item.threshold == types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE


def test_guardrails_blocks_content_on_safety_violation() -> None:
    mock_client = MagicMock()
    mock_candidate = MagicMock()
    mock_candidate.finish_reason.name = "SAFETY"

    mock_response = MagicMock()
    mock_response.candidates = [mock_candidate]
    mock_client.models.generate_content.return_value = mock_response

    service = ResponsibleAIService(client=mock_client)
    result = service.generate_with_guardrails("prompt com injeção perigosa")

    assert isinstance(result, SafetyCheckResult)
    assert result.is_blocked is True
    assert result.block_reason == SafetyBlockReason.SAFETY
    assert result.content is None
    assert "bloqueado por violar" in (result.disclaimer or "")


def test_guardrails_returns_content_when_safe() -> None:
    mock_client = MagicMock()
    mock_candidate = MagicMock()
    mock_candidate.finish_reason.name = "STOP"

    mock_response = MagicMock()
    mock_response.candidates = [mock_candidate]
    mock_response.text = "Relatório executivo técnico seguro."
    mock_client.models.generate_content.return_value = mock_response

    service = ResponsibleAIService(client=mock_client)
    result = service.generate_with_guardrails("prompt seguro")

    assert result.is_blocked is False
    assert result.block_reason is None
    assert result.content == "Relatório executivo técnico seguro."
