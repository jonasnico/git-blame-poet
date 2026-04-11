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

Both `git-blame-poet` and the shorter `gbp` command are installed. `gbp` is the recommended shortcut:

```bash
# Shakespearean tragedy (default style, Gemini provider)
gbp src/main.py

# Film noir detective story
gbp -s noir app/routes.py

# Epic fantasy quest using OpenAI
gbp -s epic -p openai lib/database.rb

# Horror story about legacy code at a specific revision
gbp -s horror --revision main utils/auth.py

# Use a specific model
gbp -p openai -m gpt-4o app/routes.py

# Pipe existing blame output
git blame src/index.ts | gbp

# Plain text output (no colors)
gbp --raw src/main.py
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

List all styles: `gbp --list-styles`

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
