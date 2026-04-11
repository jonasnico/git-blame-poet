# 🎭 git-blame-poet

Turn any file's `git blame` into a dramatic literary narrative using AI.

## Install

```bash
pipx install git-blame-poet
# or
pip install git-blame-poet
```

## Setup

Set your API key for the provider you want to use.

**Google Gemini** (default):
```bash
export GOOGLE_API_KEY=...
```

**OpenAI**:
```bash
export OPENAI_API_KEY=sk-...
```

## Usage

```bash
# Shakespearean tragedy (default style, Gemini provider)
git-blame-poet src/main.py

# Film noir detective story
git-blame-poet -s noir app/routes.py

# Epic fantasy quest using OpenAI
git-blame-poet -s epic -p openai lib/database.rb

# Horror story about legacy code at a specific revision
git-blame-poet -s horror --revision main utils/auth.py

# Use a specific model
git-blame-poet -p openai -m gpt-4o app/routes.py

# Pipe existing blame output
git blame src/index.ts | git-blame-poet

# Plain text output (no colors)
git-blame-poet --raw src/main.py
```

## Styles

| Style         | Vibe                              |
|---------------|-----------------------------------|
| `shakespeare` | 🎭 Iambic pentameter tragedy      |
| `noir`        | 🕵️ Hard-boiled detective case     |
| `soap`        | 📺 Melodramatic soap opera        |
| `epic`        | ⚔️ Tolkien-esque fantasy quest    |
| `nature`      | 🐧 Attenborough nature documentary|
| `horror`      | 👻 Haunted codebase horror story  |

List all styles: `git-blame-poet --list-styles`

## Providers

| Provider | Flag            | Default model           | Env var          |
|----------|-----------------|-------------------------|------------------|
| `gemini` | `-p gemini`     | `gemini-3-flash-preview`| `GOOGLE_API_KEY` |
| `openai` | `-p openai`     | `gpt-4o-mini`           | `OPENAI_API_KEY` |

Default provider is **Gemini**.

## Options

```
-s, --style     Narrative style (default: shakespeare)
-r, --revision  Git revision to blame against
-p, --provider  LLM provider: gemini or openai (default: gemini)
-m, --model     Model override (defaults to provider's recommended model)
--list-styles   Show available styles
--raw           Plain text output
-h, --help      Show help
```

## License

MIT
