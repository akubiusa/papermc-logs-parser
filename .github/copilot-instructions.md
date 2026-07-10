# Copilot code review instructions

Guidance for reviewing pull requests in `papermc-logs-parser`, a small Python 3
tool that parses PaperMC/Spigot/Bukkit server logs into structured JSON.

## Project facts

- Pure Python 3, standard library only (`os`, `json`, `re`). There is no
  dependency manifest and no test suite.
- Entry point: `python -m src` (`src/__main__.py` -> `src/__init__.py:parser`).

## What to check

- Keep the code dependency-free. Flag any new third-party import or added
  dependency manifest that is not clearly justified.
- The parser regex in `src/__init__.py` defines the record schema. If a change
  alters the capture groups or the output keys (`time`, `threadName`, `level`,
  `messages`, `raws`), confirm downstream JSON consumers are updated too.
- File I/O: `main()` reads `config.json` and writes `output.json` / `data.json`.
  Verify missing-file and malformed-JSON cases are still handled (currently it
  exits with a clear error when `config.json` is absent).
- Watch for logs, sample data, or generated `output.json` / `data.json` being
  committed; they can contain personal data (player names, IP addresses).

## Style

- Follow the existing style of the file being edited; do not reformat unrelated
  lines.
- Prefer small, focused changes with clear intent over broad rewrites.

## Do not flag

- The absence of a test suite or a dependency manifest is intentional for this
  project; do not raise it as an issue on unrelated PRs.
