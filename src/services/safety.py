from google import genai
from google.genai import types

from src.core.client import GeminiClientFactory
from src.core.config import Settings, settings
from src.schemas.safety import SafetyBlockReason, SafetyCheckResult


class ResponsibleAIService:
    """Gerencia políticas de moderação, filtros de segurança e inspeção de finish_reason."""

    def __init__(self, client: genai.Client | None = None, cfg: Settings | None = None) -> None:
        self.config = cfg or settings
        self.client = client or GeminiClientFactory.create_client(self.config)

    def get_strict_safety_settings(self) -> list[types.SafetySetting]:
        return [
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            ),
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            ),
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            ),
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            ),
        ]

    def generate_with_guardrails(self, prompt: str) -> SafetyCheckResult:
        gen_config = types.GenerateContentConfig(
            temperature=self.config.default_temperature,
            top_p=self.config.default_top_p,
            seed=self.config.default_seed,
            safety_settings=self.get_strict_safety_settings(),
        )

        response = self.client.models.generate_content(
            model=self.config.model_name,
            contents=prompt,
            config=gen_config,
        )

        if not response.candidates:
            return SafetyCheckResult(
                is_blocked=True,
                block_reason=SafetyBlockReason.OTHER,
                disclaimer="Nenhum candidato retornado pelo modelo.",
            )

        candidate = response.candidates[0]
        finish_reason = candidate.finish_reason

        if finish_reason and finish_reason.name == "SAFETY":
            return SafetyCheckResult(
                is_blocked=True,
                block_reason=SafetyBlockReason.SAFETY,
                disclaimer=("Conteúdo bloqueado por violar limites de segurança (Responsible AI)."),
            )

        if not response.text:
            return SafetyCheckResult(
                is_blocked=True,
                block_reason=SafetyBlockReason.OTHER,
                disclaimer="Execução interrompida sem payload textual.",
            )

        return SafetyCheckResult(
            is_blocked=False,
            content=response.text,
        )
