import pytest
import os

@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch: pytest.MonkeyPatch) -> None:
    """Garante que a suíte de testes execute com variáveis seguras por padrão."""
    monkeypatch.setenv("GEMINI_API_KEY", "test-api-key-mock")
    monkeypatch.setenv("GEMINI_MODEL", "gemini-2.5-flash")
    monkeypatch.setenv("ENVIRONMENT", "test")
