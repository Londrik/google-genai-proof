import argparse
import sys

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from src.services.analyzer import ContentAnalyzerService
from src.services.safety import ResponsibleAIService

console = Console()


def run_audit(target: str, content: str) -> None:
    console.print(
        Panel.fit("[bold blue]Iniciando Auditoria com Gemini Structured Outputs[/bold blue]")
    )
    service = ContentAnalyzerService()
    try:
        report = service.analyze_text(target_name=target, raw_content=content)

        status_color = "green" if report.passed else "red"
        console.print(
            f"\n[bold]Status Geral:[/bold] [{status_color}]{'APROVADO' if report.passed else 'REPROVADO'}[/{status_color}]"
        )
        console.print(f"[bold]Score de Conformidade:[/bold] {report.score}/100")
        console.print(f"[bold]Resumo Executivo:[/bold] {report.summary}\n")

        if report.findings:
            table = Table(title="Inconformidades Técnicas Mapeadas")
            table.add_column("Categoria", style="cyan", no_wrap=True)
            table.add_column("Severidade", style="magenta")
            table.add_column("Descrição", style="white")
            table.add_column("Remediação", style="green")

            for finding in report.findings:
                table.add_row(
                    finding.category,
                    finding.severity.value,
                    finding.description,
                    finding.remediation,
                )
            console.print(table)
        else:
            console.print("[green]Nenhuma inconformidade encontrada no artefato.[/green]")

    except Exception as exc:
        console.print(
            f"[bold red]Falha na execução da auditoria:[/bold red] {exc}", file=sys.stderr
        )
        sys.exit(1)


def run_safety_check(prompt: str) -> None:
    console.print(Panel.fit("[bold yellow]Validando Guardrails de Responsible AI[/bold yellow]"))
    service = ResponsibleAIService()
    try:
        result = service.generate_with_guardrails(prompt)
        if result.is_blocked:
            console.print(f"[bold red]Conteúdo Bloqueado:[/bold red] {result.block_reason}")
            console.print(f"[yellow]Aviso:[/yellow] {result.disclaimer}")
        else:
            console.print("[green]Conteúdo Aprovado na Moderação:[/green]")
            console.print(result.content)
    except Exception as exc:
        console.print(
            f"[bold red]Falha na verificação de segurança:[/bold red] {exc}", file=sys.stderr
        )
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Google GenAI Proof Engine - CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    audit_parser = subparsers.add_parser("audit", help="Auditar artefato com Structured Outputs")
    audit_parser.add_argument("--target", required=True, help="Nome do arquivo ou componente")
    audit_parser.add_argument("--content", required=True, help="Texto ou código para validação")

    safety_parser = subparsers.add_parser("guard", help="Testar filtros de Responsible AI")
    safety_parser.add_argument("--prompt", required=True, help="Texto para avaliação de moderação")

    args = parser.parse_args()

    if args.command == "audit":
        run_audit(args.target, args.content)
    elif args.command == "guard":
        run_safety_check(args.prompt)


if __name__ == "__main__":
    main()
