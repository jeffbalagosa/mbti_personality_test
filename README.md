# MBTI Personality Test – Python CLI

A simple, modular MBTI (Myers–Briggs Type Indicator) personality test that runs in the terminal.

## Quick start

1. Create a virtual environment and install dependencies.
2. Run the CLI:

```
mbti --questions config/mbti_questionnaire.yaml
```

Or run via python:

```
python -m mbti_cli.cli --questions config/mbti_questionnaire.yaml
```

Use `--pdf` to generate a PDF (requires optional dependencies).

## Project layout

- src/mbti_cli/ … core modules
- config/mbti_questionnaire.yaml … questions
- tests/ … unit tests

## License

MIT
