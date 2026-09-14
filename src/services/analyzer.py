from google import genai
from google.genai import types

from src.core.client import GeminiClientFactory
from src.core.config import Settings, settings
from src.schemas.audit import AuditReport

SYSTEM_INSTRUCTION_AUDIT = (
    "Você é um Auditor Sênior Especialista em Arquitetura de Software e Compliance Técnico. "
    "Sua função é analisar código, logs ou contratos técnicos com rigor absoluto, "
    "zero tolerância a alucinações e conformidade estrita ao schema JSON fornecido. "
    "Seja analítico, determinístico e direto."
)


class ContentAnalyzerService:
    def __init__(self, client: genai.Client | None = None, cfg: Settings | None = None) -> None:
        self.config = cfg or settings
        self.client = client or GeminiClientFactory.create_client(self.config)

    def analyze_text(self, target_name: str, raw_content: str) -> AuditReport:
        prompt = f"Artefato a ser auditado: {target_name}\n\nConteúdo:\n{raw_content}"

        gen_config = types.GenerateContentConfig(
            temperature=self.config.default_temperature,
            top_p=self.config.default_top_p,
            seed=self.config.default_seed,
            system_instruction=SYSTEM_INSTRUCTION_AUDIT,
            response_mime_type="application/json",
            response_schema=AuditReport,
        )

        response = self.client.models.generate_content(
            model=self.config.model_name,
            contents=prompt,
            config=gen_config,
        )

        if not response.text:
            raise ValueError("O modelo retornou uma resposta textual vazia.")

        return AuditReport.model_validate_json(response.text)
