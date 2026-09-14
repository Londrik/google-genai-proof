
from google import genai
from google.genai import types

from src.core.config import Settings, settings


class GeminiClientFactory:
    """Fábrica determinística de clientes do SDK oficial google-genai."""

    @staticmethod
    def create_client(cfg: Settings | None = None) -> genai.Client:
        active_settings = cfg or settings
        active_settings.validate()
        return genai.Client(api_key=active_settings.api_key)

    @staticmethod
    def get_deterministic_config(
        system_instruction: str | None = None,
        temperature: float | None = None,
        seed: int | None = None,
    ) -> types.GenerateContentConfig:
        return types.GenerateContentConfig(
            temperature=temperature if temperature is not None else settings.default_temperature,
            top_p=settings.default_top_p,
            seed=seed if seed is not None else settings.default_seed,
            system_instruction=system_instruction,
        )
