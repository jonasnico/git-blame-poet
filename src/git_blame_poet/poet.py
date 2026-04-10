"""The dramatic engine — turns blame data into literary gold."""

from __future__ import annotations

from google import genai
from openai import OpenAI
from openai.types.chat import (
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)

from git_blame_poet.blame_parser import BlameResult

STYLES = {
    "shakespeare": {
        "label": "🎭 Shakespearean Tragedy",
        "instruction": (
            "You are William Shakespeare. Rewrite this git blame as a dramatic "
            "five-act tragedy in iambic pentameter. Each author is a character in "
            "the play. Commits are plot points. Merge conflicts are betrayals. "
            "Deleted lines are deaths. The CI pipeline is fate itself."
        ),
    },
    "noir": {
        "label": "🕵️ Film Noir Detective",
        "instruction": (
            "You are a hard-boiled 1940s detective narrating a case. Each author "
            "is a suspect. Each commit is a clue. The codebase is a crime scene. "
            "Use moody metaphors about rain, shadows, and broken promises. "
            "The linter warnings are red herrings. The real culprit? Technical debt."
        ),
    },
    "soap": {
        "label": "📺 Soap Opera",
        "instruction": (
            "You are a melodramatic soap opera narrator. Each author is a character "
            "with secret motivations and forbidden desires. Commits are dramatic "
            "reveals. Merge conflicts are love triangles. Reverted commits are "
            "characters returning from the dead. Every refactor is a betrayal."
        ),
    },
    "epic": {
        "label": "⚔️ Epic Fantasy",
        "instruction": (
            "You are a fantasy narrator in the style of Tolkien. Each author is a "
            "warrior or wizard. The codebase is a mystical realm. Commits are quests. "
            "Bug fixes are battles against dark forces. The main branch is the throne. "
            "Feature branches are expeditions into uncharted lands. Deprecation "
            "warnings are ancient prophecies."
        ),
    },
    "nature": {
        "label": "🐧 Nature Documentary",
        "instruction": (
            "You are Sir David Attenborough narrating a nature documentary. Each "
            "author is a different species of developer in their natural habitat. "
            "Commits are mating rituals, territorial displays, or migration patterns. "
            "Code reviews are predator–prey dynamics. The IDE is the ecosystem. "
            "Speak with quiet wonder and British understatement."
        ),
    },
    "horror": {
        "label": "👻 Horror Story",
        "instruction": (
            "You are a horror narrator. The codebase is a haunted house. Each "
            "author unknowingly left behind cursed artifacts (their code). Old "
            "commits whisper from the git log. TODO comments are warnings from "
            "the dead. The legacy code in the basement must never be refactored — "
            "for it holds an ancient evil. The build fails at midnight."
        ),
    },
}

DEFAULT_STYLE = "shakespeare"


def _format_blame_for_prompt(blame: BlameResult) -> str:
    """Condense blame data into an LLM-friendly summary."""
    lines: list[str] = [f"File: {blame.file_path}", f"Stats: {blame.summary()}", ""]

    # Group by author for a cleaner narrative seed
    by_author: dict[str, list[str]] = {}
    for bl in blame.lines:
        by_author.setdefault(bl.author, []).append(
            f"  L{bl.line_number} ({bl.date}, {bl.commit[:8]}): {bl.content.strip()}"
        )

    for author, contributions in by_author.items():
        lines.append(f"Author: {author}")
        # Limit per-author lines to keep the prompt reasonable
        for c in contributions[:30]:
            lines.append(c)
        if len(contributions) > 30:
            lines.append(f"  ... and {len(contributions) - 30} more lines")
        lines.append("")

    return "\n".join(lines)


PROVIDERS = {
    "openai": {
        "label": "OpenAI",
        "default_model": "gpt-4o-mini",
        "env_var": "OPENAI_API_KEY",
    },
    "gemini": {
        "label": "Google Gemini",
        "default_model": "gemini-3-flash-preview",
        "env_var": "GOOGLE_API_KEY",
    },
}

DEFAULT_PROVIDER = "gemini"


def dramatize(
    blame: BlameResult,
    style: str = DEFAULT_STYLE,
    provider: str = DEFAULT_PROVIDER,
    model: str | None = None,
) -> str:
    """Send blame data to an LLM and return a dramatic narrative."""
    style_cfg = STYLES.get(style, STYLES[DEFAULT_STYLE])
    system_prompt = (
        f"{style_cfg['instruction']}\n\n"
        "Rules:\n"
        "- Keep it under 600 words.\n"
        "- Reference real author names, dates, and commit hashes from the data.\n"
        "- Be funny, creative, and over-the-top dramatic.\n"
        "- Use the actual code content for comedic effect where possible.\n"
        "- End with a moral or dramatic cliffhanger.\n"
    )

    user_prompt = (
        "Here is the git blame data. Turn it into a dramatic narrative:\n\n"
        f"{_format_blame_for_prompt(blame)}"
    )

    provider_cfg = PROVIDERS[provider]
    resolved_model = model or provider_cfg["default_model"]

    if provider == "gemini":
        return _call_gemini(system_prompt, user_prompt, resolved_model)
    return _call_openai(system_prompt, user_prompt, resolved_model)


def _call_openai(system_prompt: str, user_prompt: str, model: str) -> str:
    client = OpenAI()
    response = client.chat.completions.create(
        model=model,
        messages=[
            ChatCompletionSystemMessageParam(role="system", content=system_prompt),
            ChatCompletionUserMessageParam(role="user", content=user_prompt),
        ],
        temperature=1.0,
        max_tokens=1500,
    )
    return response.choices[0].message.content or "(The muse was silent.)"


def _call_gemini(system_prompt: str, user_prompt: str, model: str) -> str:
    client = genai.Client()
    response = client.models.generate_content(
        model=model,
        config=genai.types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=1.0,
            max_output_tokens=1500,
        ),
        contents=user_prompt,
    )
    return response.text or "(The muse was silent.)"
