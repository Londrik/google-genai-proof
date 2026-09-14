from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class SafetyBlockReason(StrEnum):
    SAFETY = "SAFETY"
    RECITATION = "RECITATION"
    OTHER = "OTHER"


class SafetyCheckResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    is_blocked: bool = Field(
        description="Indica se o conteúdo foi bloqueado por políticas de segurança"
    )
    block_reason: SafetyBlockReason | None = Field(
        default=None,
        description="Motivo do bloqueio caso acionado",
    )
    content: str | None = Field(
        default=None,
        description="Conteúdo gerado se aprovado na moderação",
    )
    disclaimer: str | None = Field(
        default=None,
        description="Aviso técnico ou instrução de remediação",
    )
