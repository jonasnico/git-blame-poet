# Copilot instructions

## Build, test, and lint

This project is a small Python CLI package built with Hatchling. CI installs tools ad hoc rather than through a dedicated dev extras group, so local sessions should do the same when needed:

```bash
pip install -e . pytest ruff mypy build
```

Use the same commands CI uses:

| Task | Command |
| --- | --- |
| Run tests | `pytest tests/ -v` |
| Run a single test | `pytest tests/test_blame_parser.py -k test_summary -v` |
| Check formatting | `ruff format --check src/` |
| Lint | `ruff check src/` |
| Type-check | `mypy src/ --ignore-missing-imports` |
| Build package | `python -m build` |

## High-level architecture

The package has three main layers:

1. `src/git_blame_poet/cli.py` is the only user-facing entry point. It owns Click option parsing, Rich output, style listing, stdin-vs-file branching, and user-visible error messages.
2. `src/git_blame_poet/blame_parser.py` handles all blame acquisition and structure. `run_git_blame()` shells out to `git blame --date=iso`; `parse_blame_text()` turns raw blame lines into `BlameResult` / `BlameLine`.
3. `src/git_blame_poet/poet.py` turns structured blame into an LLM prompt and dispatches to the selected provider. It groups lines by author, truncates each author's contribution list to 30 prompt lines, and routes through either the OpenAI or Gemini SDK.

The normal flow is:

`cli.main()` -> `run_git_blame()` or `parse_blame_text()` -> `dramatize()` -> provider-specific API call -> Rich panel or raw stdout.

`src/git_blame_poet/__main__.py` is only a thin `python -m git_blame_poet` shim. Packaging exposes two console scripts that both point at the same CLI entry point: `git-blame-poet` and the shorter alias `gbp`.

## Key conventions

- Keep presentation logic in `cli.py` and provider/prompt logic in `poet.py`. The CLI should decide how output is shown; `poet.py` should only return the narrative string.
- Style and provider definitions are centralized dictionaries in `poet.py` (`STYLES`, `PROVIDERS`) and are reused by the CLI for Click choices, defaults, labels, and setup guidance. When adding a style or provider, update those registries instead of duplicating metadata elsewhere.
- Defaults are intentionally mirrored across README and code: `DEFAULT_STYLE = "shakespeare"` and `DEFAULT_PROVIDER = "gemini"`. Keep docs and Click defaults aligned with those constants.
- `parse_blame_text()` is deliberately tolerant: it skips non-matching lines instead of failing. Tests in `tests/test_blame_parser.py` focus on parsed structure and summary behavior, so parser changes should preserve that fault-tolerant behavior unless the tests are updated with intent.
- `run_git_blame()` exits the process on shelling/parsing failures instead of raising rich domain exceptions. If you change that contract, you will also need to update CLI error handling.
- `--raw` is the switch between plain stdout and Rich formatting. Non-raw mode prints the banner, status text, and final Rich panel; raw mode should stay clean for piping or scripting.
- Provider authentication is implicit through SDK defaults plus the env vars documented in README and `PROVIDERS`: `GOOGLE_API_KEY` for Gemini and `OPENAI_API_KEY` for OpenAI.
