# CLAUDE.md

## Overview

`papermc-logs-parser` parses PaperMC (also Spigot/Bukkit) server log files into
structured records. Each log entry captures its timestamp, thread name, log
level, and message body, with continuation lines (stack traces, multi-line
messages) merged into the entry they belong to.

## Runtime and dependencies

- Pure Python 3, **standard library only** (`os`, `json`, `re`, `sys`). There is no
  package manifest (`requirements.txt` / `pyproject.toml`) and no third-party
  dependency. Do not introduce one without a clear need.

## Running

- Run from the repository root as a module: `python -m src`
- `config.json` must exist at the working directory; it holds `{"path": "..."}`
  pointing at the log file to parse (default `logs/latest.log`).
- Outputs are written to the working directory:
  - `output.json`: all parsed log entries.
  - `data.json`: a cursor (`count`, `firstTime`) used to emit only new entries
    on the next run. It is created if missing.

## Architecture / key files

- `src/__init__.py`: `parser(filepath)` — the core parser. Uses the regex
  `^\[(HH:MM:SS)] \[(thread)/(level)]: ?(message)$`. A line that does not match
  is appended to the current entry's message/raw buffers (continuation line).
- `src/__main__.py`: `main()` — the CLI entry point. Loads `config.json`, calls
  `parser`, writes `output.json`, and maintains the `data.json` cursor.
- `config.json`: log path configuration.
- `renovate.json`: dependency automation via a shared `book000/templates` preset.

## Coding conventions

- Keep the parser dependency-free (standard library only), matching the current
  codebase.
- Preserve the existing regex capture-group contract (`time`, `threadName`,
  `level`, `messages`, `raws`); downstream JSON consumers rely on these keys.

## Testing

- There are no automated tests. Verify changes manually by running `python -m src`
  against a sample PaperMC log and inspecting `output.json`.
- CI (`.github/workflows/python-ci.yml`) runs `ruff check`, `ruff format --check` and `pytest`; `pytest` currently collects no tests because none exist yet.

## Documentation update rules

- Update this file when the run command, `config.json` schema, output files, or
  the parsed-entry key names change.

## Prohibitions

- Never commit real server logs or `output.json` / `data.json` produced from
  private servers; they may contain player names, IPs, or other personal data.
