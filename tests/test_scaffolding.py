import os


def test_environment_fixture() -> None:
    assert os.getenv("GEMINI_API_KEY") == "test-api-key-mock"
    assert os.getenv("ENVIRONMENT") == "test"
