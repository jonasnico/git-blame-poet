"""CLI entry point for git-blame-poet."""

from __future__ import annotations

import sys

import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from git_blame_poet.blame_parser import parse_blame_text, run_git_blame
from git_blame_poet.poet import DEFAULT_STYLE, STYLES, PROVIDERS, DEFAULT_PROVIDER, dramatize

console = Console()

BANNER = r"""
   __ _ (_) | |        | |  | |                                                     | |
  / _` || | | | ______ | |__| | __ _ _ __ ___   ___   ______  _ __   ___   ___  | |_
 | (_| || | | ||______|| |_ | |/ _` | '_ ` _ \ / _ \ |______|| '_ \ / _ \ / _ \ | __|
  \__, || | | |        | |_)| | (_| | | | | | ||  __/         | |_) | (_) ||  __/ | |_
   __/ ||_| |_|        |_.__/|_|\__,_|_| |_| |_| \___|         | .__/ \___/  \___|  \__|
  |___/                                                         | |
                                                                |_|
"""


def _show_banner() -> None:
    console.print(Text(BANNER, style="bold magenta"))


def _show_styles() -> None:
    console.print("\n[bold]Available dramatic styles:[/bold]\n")
    for key, cfg in STYLES.items():
        marker = " [dim](default)[/dim]" if key == DEFAULT_STYLE else ""
        console.print(f"  [cyan]{key:<14}[/cyan] {cfg['label']}{marker}")
    console.print()


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.argument("file", required=False)
@click.option(
    "-s",
    "--style",
    type=click.Choice(list(STYLES.keys()), case_sensitive=False),
    default=DEFAULT_STYLE,
    help="Dramatic narrative style.",
    show_default=True,
)
@click.option(
    "-r",
    "--revision",
    default=None,
    help="Git revision (branch, tag, or commit) to blame against.",
)
@click.option(
    "-p",
    "--provider",
    type=click.Choice(list(PROVIDERS.keys()), case_sensitive=False),
    default=DEFAULT_PROVIDER,
    help="LLM provider to use.",
    show_default=True,
)
@click.option(
    "-m",
    "--model",
    default=None,
    help="Model to use (defaults to provider's recommended model).",
)
@click.option(
    "--list-styles",
    is_flag=True,
    help="List available narrative styles and exit.",
)
@click.option(
    "--raw",
    is_flag=True,
    help="Print the narrative as plain text (no Rich formatting).",
)
def main(
    file: str | None,
    style: str,
    revision: str | None,
    provider: str,
    model: str | None,
    list_styles: bool,
    raw: bool,
) -> None:
    """🎭 git-blame-poet — because every line of code has a story.

    Turn any file's git blame into a dramatic literary narrative.

    \b
    Examples:
        git-blame-poet src/main.py
        git-blame-poet -s noir app/routes.py
        git-blame-poet -p openai -m gpt-4o app/routes.py
        git-blame-poet -s horror --revision main lib/auth.rb
        cat blame.txt | git-blame-poet
    """
    if list_styles:
        _show_styles()
        raise SystemExit(0)

    # Read from stdin if no file provided
    if file is None:
        if sys.stdin.isatty():
            _show_banner()
            console.print(
                "[yellow]Usage:[/yellow] git-blame-poet <file> "
                "[dim]or pipe git blame output[/dim]\n"
            )
            console.print("Run [cyan]git-blame-poet --help[/cyan] for full options.\n")
            _show_styles()
            raise SystemExit(0)
        blame_text = sys.stdin.read()
        blame = parse_blame_text(blame_text)
        if not blame.lines:
            console.print("[red]Could not parse any blame lines from stdin.[/red]")
            raise SystemExit(1)
    else:
        blame = run_git_blame(file, revision=revision)
        if not blame.lines:
            console.print(f"[red]No blame data for '{file}'.[/red]")
            raise SystemExit(1)

    style_cfg = STYLES[style]
    provider_cfg = PROVIDERS[provider]
    display_model = model or provider_cfg["default_model"]

    if not raw:
        _show_banner()
        console.print(
            f"[dim]Consulting the muse ({provider_cfg['label']}: {display_model})...[/dim]\n"
            f"[dim]Style: {style_cfg['label']}[/dim]\n"
            f"[dim]{blame.summary()} in [cyan]{blame.file_path}[/cyan][/dim]\n"
        )

    try:
        narrative = dramatize(blame, style=style, provider=provider, model=model)
    except Exception as exc:
        error_msg = str(exc)
        if "api_key" in error_msg.lower() or "auth" in error_msg.lower():
            console.print(
                f"[red]Error:[/red] {provider_cfg['label']} API key not found.\n"
                f"Set it with: [cyan]export {provider_cfg['env_var']}=...[/cyan]"
            )
        else:
            console.print(f"[red]Error from LLM:[/red] {error_msg}")
        raise SystemExit(1)

    if raw:
        print(narrative)
    else:
        panel = Panel(
            narrative,
            title=f"{style_cfg['label']}",
            subtitle=f"[dim]{blame.file_path}[/dim]",
            border_style="magenta",
            padding=(1, 2),
        )
        console.print(panel)
        console.print(
            "\n[dim italic]\"In the beginning was the commit, "
            "and the commit was with git.\"[/dim italic]\n"
        )
