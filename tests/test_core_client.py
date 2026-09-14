import pytest
from src.core.config import Settings
from src.core.client import GeminiClientFactory

def test_settings_validation_missing_key() -> None:
    empty_settings = Settings(api_key="")
    with pytest.raises(ValueError, match="GEMINI_API_KEY"):
        empty_settings.validate()

def test_settings_default_deterministic_parameters() -> None:
    cfg = Settings(api_key="valid-mock-key")
    assert cfg.default_temperature == 0.0
    assert cfg.default_seed == 42

def test_deterministic_content_config() -> None:
    config = GeminiClientFactory.get_deterministic_config(
        system_instruction="Sistema de auditoria de código."
    )
    assert config.temperature == 0.0
    assert config.top_p == 0.95
    assert config.seed == 42
    assert config.system_instruction == "Sistema de auditoria de código."
