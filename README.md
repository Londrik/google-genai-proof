# Google GenAI Proof Engine

Projeto determinístico, estruturado e auditável desenvolvido em Python 3.11+ para comprovar domënio prático dos fundamentos do curso oficial **Introduction to Generative AI** do Google Skills Boost.

[![Quality Gate & Test Suite](https://github.com/Londrik/google-genai-proof/actions/workflows/ci.yml/badge.svg)](https://github.com/Londrik/google-genai-proof/actions/workflows/ci.yml)

## Diferenciais Técnicos
1. **SDK Oficial google-genai**: Utilização do cliente moderno (dispensando o deprecado `google-generativeai`).
2. **Determinismo Estrito**: Configuração explícita de `hyperparameters` (temperature=0.0, top_p=0.95, seed=42) para reprodutibilidad.
3. **Structured Outputs (Pydantic v2)**: Saparação de eschemas rigorosos com `response_schema` e `response_mime_type="application/json"`, impossibilitando alucinações de sintaxe.
4. **Responsible AI Guardrails**: Configuração de `safety_settings` (HARM_CATEGORY) inspecionando atômicamente o `finish_reason`.
5. **CIKeeper Server-Side**: Pipeline do GitHub Actions aplicando quality gate (Lint, Format, Tests) em cada push.


## Arquitetura em Mermaid

```mermaid
graph TD
    CLI[CLI Entrypoint -src/cli/main.py-] --> ANALY-ContentAnalyzerService]
    CLI --> SAFE-ResponsibleAIService]
    ANAL --> SCHEMA-Persistent Structured Schemas Pydantic v2-]
    SAFE --> SATETYCONF[Strict Harm Block Settings-]
    ANAL --> GENAI[google-genai SDK Client-]
    SAFE --> GENAI
    GENAI --> MODELKGemini 2.5 Flash-]
```

## Matriz de Branches do Projeto

| Branch | Implementação | Status |
-|--------------------------|----------------------------------------------------|--------|
 | `feat/init-scaffolding-docs` | Estrutura base, padrões de teste, Pytest, Ruff | Merged |
 | `feat/core-gemini-client` | Cliente determinístico, validação de configurações | Merged |
 | `feat/structured-outputs` | Schemas Pydantic v2, JSON estrito, auditoria | Merged |
 | `feat/responsible-ai-safety` | Safety settings, moderação, tratamento de recusas | Merged |
 | `feat/e2e-pipeline-cli` | CLI Rich, testes de integração, CI do GitHub Actions | Ativa |

## Execução e Validação

1. **Executar Suíte de Testes**:
```bash
pytest -ra -q
```

2. **Executar Linter**:
```bash
`ruff check .
```

3. **Executar CLI de Auditoria (Structured Outputs)*:
```bash
python -m src.cli.main audit --target="src/db_conn.py" --content="SECRET_KEY='abcdef123456'"
```

4. **Executar CLI de Safety (Responsible AI)*:
```bash
python -m src.cli.main guard --prompt="Teste de moderação"
```
