# MECE Implementation Plan — MBTI Personality Test (Python CLI)

## A. Project Setup & Governance (foundation; no code yet)

1. Define success criteria

   * ✅ CLI runs locally (macOS/Windows/Linux), completes survey, prints MBTI type.
   * ✅ Optional `--pdf` creates a report with a bar chart.
   * ✅ 90%+ unit test line coverage on core logic (data loading + scoring).
   * ✅ Type-check clean (mypy), lint clean (ruff/black).
2. Choose tech baseline

   * Python 3.11+, `pyproject.toml` (poetry or pip-tools), pinned deps.
   * Libraries: `PyYAML`, `reportlab`, `matplotlib`, (`pandas` optional).
3. Repo scaffolding

   * `src/mbti_cli/{cli.py,controller.py,data_loader.py,models.py,scoring.py,plotting.py,pdf_report.py}`
   * `config/mbti_questionnaire.yaml`, `tests/`, `README.md`, `LICENSE`, `Makefile`, `.pre-commit-config.yaml`.
4. Tooling & quality gates

   * Pre-commit hooks (black, ruff, trailing-whitespace, end-of-file-fixer).
   * mypy strict on `src/mbti_cli`.
   * GitHub Actions: lint + type + test matrix (3.11/3.12, mac/win/linux).

**Exit criteria:** Repo created, CI green on “hello world”, quality gates enforced.

---

## B. Data & Configuration (input schema, validation)

1. Questionnaire schema (MECE by field)

   * `text: str` (prompt)
   * `dimension: one of ["E","I","S","N","T","F","J","P"]` (polarity of agreement)
   * `reverse: bool` (default false, invert Likert)
   * `weight: int` (default 1) — optional for future tuning
2. YAML authoring & examples

   * Provide `config/mbti_questionnaire.yaml` with \~70 items.
   * Include comments on how reverse scoring works.
3. Validation rules

   * All required fields present; dimension in allowed set; text non-empty.
   * At least one item per polarity across all four dichotomies.
4. Loader design

   * `load_questions_from_yaml(path) -> list[Question]` using `yaml.safe_load`.
   * Raise `ValueError` with actionable message on schema error; include line/idx.

**Exit criteria:** Loading a sample YAML returns validated objects; invalid YAML yields clear errors.

---

## C. Domain Models (dataclasses, types)

1. Dataclasses

   * `Question(text: str, dimension: Literal["E","I","S","N","T","F","J","P"], reverse: bool=False, weight: int=1)`
   * `Likert = Literal[1,2,3,4,5]`
   * `Response(question_idx: int, value: Likert)`
2. Internal enums & helpers

   * `Dichotomy = ("E/I","S/N","T/F","J/P")` mapping to pairs.
   * Utility to map dimension → dichotomy bucket.

**Exit criteria:** mypy-clean types; helper functions unit-tested.

---

## D. CLI & Controller (user flow, I/O, UX)

1. CLI arguments

   * `--pdf <path>` (optional), `--author <str>`, `--questions <path>` (override), `--no-color`.
   * `--version`, `--help`.
2. UX flow (MECE by state)

   * Intro + Likert scale legend.
   * Per-question loop: show index + text; accept `1..5`, `z` (undo), `done` (only when complete).
   * KeyboardInterrupt: confirm exit; discard or save partial (MVP: discard).
3. Input sanitization

   * Trim, lowercase; reject non-integers; range-check; friendly re-prompts.
   * Undo blocked when 0 answers → show “Nothing to undo.”
4. Output summary

   * After completion: show per dichotomy percentages + final four-letter type.
   * Explain tie-breaker rule (see Scoring).
5. Controller–Scoring contract

   * Controller returns `list[Likert]` aligned to `questions`.

**Exit criteria:** Manual run completes survey; undo works; pretty console output.

---

## E. Scoring Engine (deterministic, testable)

1. Item scoring

   * Score = `6 - value` if `reverse` else `value`; multiply by `weight`.
   * Assign score to the item’s **polarity letter** (E/I/S/N/T/F/J/P).
2. Aggregate to dichotomies

   * `E_vs_I = sum(E) vs sum(I)` (same for S/N, T/F, J/P).
   * Percentage per side: `side / (E+I) * 100`.
3. Type derivation

   * Pick higher of each pair → 4-letter type.
   * **Tie-breaker policy (explicit):** if equal, prefer the **non-reverse majority** across that pair; if still tied, prefer letter with higher **count of items**; else default to the first of the pair (E,S, T, J) and log “tie”.
4. API

   * `score_responses(responses, questions) -> dict` returning per-letter totals, per-pair percentages, and final type.

**Exit criteria:** Deterministic results; unit tests for normal, reverse, weighted, and tie cases.

---

## F. Visualization & PDF Report (optional output)

1. Plotting layer

   * Non-interactive (Agg); bar chart of 4 pair percentages (E/I, S/N, T/F, J/P).
   * Clear labels; values as integer % above bars; accessible font sizes.
2. PDF generator

   * ReportLab landscape letter; title, subtitle, author, date, chart image; footer.
   * File I/O errors surfaced with helpful messages.
3. CLI integration

   * If `--pdf` is passed, generate PDF after console output; confirm path.

**Exit criteria:** `--pdf` creates a readable report; smoke test loads page and checks landscape orientation.

---

## G. Error Handling & Edge Cases (consistent strategy)

1. Input errors

   * Out-of-range Likert → re-prompt; invalid command → hint text.
   * Undo when empty → info message, continue.
2. Data errors

   * YAML schema problems → fail fast with context (index/field).
   * Question/response length mismatch → raise with counts.
3. Runtime errors

   * PDF path unwritable → suggest directory and filename fix.
   * KeyboardInterrupt → graceful exit with status code 130.
4. Ties & missing data

   * Tie policy (above) consistently applied and displayed.
   * If any dichotomy has zero total (misconfigured YAML), abort with diagnostic.

**Exit criteria:** All error paths covered by tests; messages actionable and non-ambiguous.

---

## H. Testing Strategy (MECE across levels)

1. Unit tests

   * Data loader (valid/invalid YAML).
   * Scoring (reverse, weights, ties, percentages).
   * Helpers (dimension→pair mapping).
2. Component tests

   * CLI `collect_answers` (undo logic, finish conditions).
   * Plotting: annotations are percentages; figure size constraints.
3. Integration tests

   * Happy path end‑to‑end (temp YAML; simulate inputs; assert type).
   * PDF generation (file exists, landscape orientation).
4. Tooling

   * pytest, coverage (fail <90% on core), hypothesis (optional) for scoring properties.

**Exit criteria:** CI shows all tests green; coverage threshold met.

---

## I. CI/CD, Packaging & Distribution

1. CI workflows

   * `lint-type-test.yml`: ruff + black --check + mypy + pytest matrix.
   * Cache pip; upload coverage to badge (optional).
2. Packaging

   * `pyproject.toml` with console script entry point `mbti=mbti_cli.cli:main`.
   * Versioning via `__version__` or poetry version.
3. Release

   * GitHub Release on tag; attach wheel/sdist.
   * Prebuilt `requirements.txt` for pip users (export from poetry if used).

**Exit criteria:** `pip install .` exposes `mbti` command; release pipeline reproducible.

---

## J. Documentation & Examples

1. README

   * Install, run, `--pdf` example, sample output, troubleshooting.
   * YAML schema with snippet; how to add/translate questions.
2. Architecture notes

   * Short diagram (ASCII) + data flow; module responsibilities.
   * Tie-break policy explained.
3. CHANGELOG, CONTRIBUTING

   * Conventional commits; how to run tests and lint locally.

**Exit criteria:** Someone new can install, run, and extend questions without help.

---

## K. Security, Performance, Accessibility (non‑functional)

1. Security

   * Use `yaml.safe_load`; no shelling out; validate paths; no PII collected.
   * License headers; third‑party versions pinned.
2. Performance

   * O(n) on questions; negligible; ensure plotting closes figures to avoid leaks.
3. Accessibility (CLI)

   * High‑contrast, no color by default; `--no-color` flag if styling added later; avoid tiny fonts in PDF.

**Exit criteria:** Security review passes; no perf bottlenecks; PDF readable when printed.

---

## L. Timeline (indicative; small team of 1–2 devs)

* **Day 1–2:** A–C (setup, schema, models)
* **Day 3–4:** D–E (CLI + scoring)
* **Day 5:** F (plot & PDF)
* **Day 6:** G–H (error paths, tests to 90%+)
* **Day 7:** I–J–K (CI/CD, docs, polish) → v1.0.0

---

## M. Risks & Mitigations

* **Ambiguous question polarity mapping** → Add `dimension` at item level and require reviewer sign‑off; include `weight` for future tuning.
* **Tie frequency higher than expected** → Log tie diagnostics; consider adding a small neutral‑bias rule or an extra tie‑breaker item per pair.
* **PDF rendering differences across OS** → Pin reportlab/matplotlib versions; include CI artifact check.

---

## N. Definition of Done (release checklist)

* [ ] CLI completes full run; example YAML included.
* [ ] Final type printed + per‑pair percentages.
* [ ] `--pdf` produces correct landscape report with chart.
* [ ] Lint/type/test all green in CI; coverage ≥ 90% (core).
* [ ] README updated; version tagged and released.
