# 🎭 git-blame-poet

> *"In the beginning was the commit, and the commit was with git."*

Turn any file's `git blame` into a dramatic literary narrative using AI.
Because every line of code has a story — and that story deserves to be *told*.

## Install

```bash
pipx install git-blame-poet
# or
pip install git-blame-poet
```

## Setup

Set your OpenAI API key:

```bash
export OPENAI_API_KEY=sk-...
```

## Usage

```bash
# Shakespearean tragedy (default)
git-blame-poet src/main.py

# Film noir detective story
git-blame-poet -s noir app/routes.py

# Epic fantasy quest
git-blame-poet -s epic lib/database.rb

# Horror story about legacy code
git-blame-poet -s horror --revision main utils/auth.py

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

## Options

```
-s, --style     Narrative style (default: shakespeare)
-r, --revision  Git revision to blame against
-m, --model     OpenAI model (default: gpt-4o-mini)
--list-styles   Show available styles
--raw           Plain text output
-h, --help      Show help
```

## License

MIT
