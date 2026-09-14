from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class RiskSeverity(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class Finding(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    category: str = Field(
        description="Categoria técnica do achado (ex: Segurança, Compliance, Performance)"
    )
    severity: RiskSeverity = Field(
        description="Nível de severidade do risco identificado"
    )
    description: str = Field(
        description="Descrição objetiva da inconformidade encontrada"
    )
    remediation: str = Field(
        description="Ação prescritiva e atômica para correção do problema"
    )


class AuditReport(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    target_name: str = Field(
        description="Identificador ou nome do artefato avaliado"
    )
    summary: str = Field(
        description="Resumo executivo do diagnóstico realizado"
    )
    score: int = Field(
        ge=0,
        le=100,
        description="Score técnico de qualidade e conformidade de 0 a 100",
    )
    passed: bool = Field(
        description="Booleano determinando conformidade geral mínima aceitável"
    )
    findings: list[Finding] = Field(
        default_factory=list,
        description="Lista de inconformidades técnicas mapeadas",
    )
