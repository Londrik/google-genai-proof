from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    api_key: str = os.getenv("GEMINI_API_KEY", "")
    model_name: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    environment: str = os.getenv("ENVIRONMENT", "development")
    default_temperature: float = 0.0
    default_top_p: float = 0.95
    default_seed: int = 42

    def validate(self) -> None:
        if not self.api_key:
            raise ValueError("A variável de ambiente 'GEMINI_API_KEY' não está configurada.")

settings = Settings()
