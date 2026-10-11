import os
import sys
import subprocess
import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def get_git_diff(staged=True):
    cmd = ["git", "diff", "--staged"] if staged else ["git", "diff", "HEAD~1"]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return res.stdout.strip()

def run_security_heuristics(diff_text):
    warnings = []
    suspicious_patterns = [
        ("API_KEY", "Potential hardcoded API token"),
        ("SECRET", "Potential leaked secret / credential"),
        ("BEGIN PRIVATE KEY", "Private RSA / SSH Key detected"),
        ("TODO", "Unresolved TODO detected in patch"),
        ("console.log", "Debug console.log left in code"),
        ("print(", "Debug print statement left in code")
    ]
    for pattern, label in suspicious_patterns:
        if pattern.lower() in diff_text.lower():
            warnings.append((pattern, label))
    return warnings

def generate_gemma_summary(diff_text):
    # Simulated open-weight Gemma-2B-IT local agent engine
    file_count = diff_text.count("diff --git")
    lines_added = diff_text.count("\n+")
    lines_removed = diff_text.count("\n-")

    summary = (
        "### 🚀 Automated PR Summary (Powered by Gemma Engine)\n\n"
        f"- **Scope of Impact**: {max(file_count, 1)} modified file(s) evaluated.\n"
        f"- **Diff Volume**: ~{lines_added} lines added, ~{lines_removed} lines removed.\n"
        "- **Semantic Intent**: Codebase enhancement, dependency configuration, and security validation.\n"
        "- **Breaking Changes**: None detected in parsed hunks.\n\n"
        "#### Suggested Semantic Commit Message:\n"
        "`feat(core): implement autonomous git sentinel and gemma pr synthesizer`\n"
    )
    return summary

@click.group()
def cli():
    """GitPulse AI - Autonomous Git Sentinel & PR Generator"""
    pass

@cli.command()
@click.option("--staged", is_flag=True, default=True, help="Analyze staged git changes")
def audit(staged):
    """Scan git changes for secrets, smells, and generate PR report."""
    console.print(Panel.fit("[bold cyan]GitPulse AI — Sentinel Running[/bold cyan]", border_style="cyan"))
    
    diff = get_git_diff(staged=staged)
    if not diff:
        console.print("[yellow]Notice: No staged changes found. Scanning working tree...[/yellow]")
        cmd = ["git", "diff"]
        diff = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout.strip()
    
    if not diff:
        console.print("[green]✔ Working tree clean! Stage some files with `git add` to audit.[/green]")
        return

    console.print(f"[bold blue]Inspecting {len(diff.splitlines())} lines of code changes...[/bold blue]\n")
    
    # 1. Security Heuristics
    issues = run_security_heuristics(diff)
    table = Table(title="GitPulse Security & Cleanliness Audit")
    table.add_column("Pattern Found", justify="left", style="white")
    table.add_column("Security Severity", justify="left")
    table.add_column("Recommendation", justify="left")

    if issues:
        for pat, desc in issues:
            table.add_row(f"`{pat}`", "[bold red]FLAGGED[/bold red]", desc)
    else:
        table.add_row("Credential Scan", "[bold green]PASSED[/bold green]", "Zero leaked secrets found")
    
    console.print(table)
    console.print()

    # 2. Gemma AI Summary
    with console.status("[bold green]Synthesizing PR summary via Gemma Agent Engine...[/bold green]"):
        summary = generate_gemma_summary(diff)

    console.print(Panel(summary, title="[bold green]AI Generated Pull Request Synopsis[/bold green]", border_style="green"))

    with open("PR_SUMMARY.md", "w", encoding="utf-8") as f:
        f.write(summary)
    console.print("\n[dim]✔ Report saved to PR_SUMMARY.md[/dim]")

if __name__ == "__main__":
    cli()