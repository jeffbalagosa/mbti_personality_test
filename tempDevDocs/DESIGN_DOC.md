# **MBTI Personality Test – Detailed Technical Design Document**

## 1. Title & Overview

**Title:** MBTI Personality Test – Python CLI Implementation
**Overview:**
This document translates the Product Requirements Document (PRD) into a detailed technical design for implementing a Python-based MBTI Personality Test. The system will load MBTI questions from a YAML configuration file, present them in a command-line interface, record user responses, calculate the MBTI type based on scoring rules, and output results to the console with an optional PDF export.

---

## 2. Objectives & Scope

**Objectives:**

* Implement a modular MBTI Personality Test script modeled after the existing Big-5 script structure.
* Provide accurate MBTI type determination using provided scoring rules.
* Enable optional PDF report generation.
* Ensure compatibility across platforms and maintain code readability.

**In-Scope:**

* CLI-based test execution.
* YAML-based question storage and parsing.
* Likert-scale question answering.
* Scoring for MBTI dimensions (E/I, S/N, T/F, J/P).
* Console and PDF output.

**Out-of-Scope:**

* GUI or web-based interface (possible future enhancement).
* Adaptive question flow or AI-based analysis.

---

## 3. System Architecture

**High-Level Architecture Diagram:**

```
+--------------------+       +------------------+
| CLI Interface      | <-->  | Controller Logic |
+--------------------+       +------------------+
        |                            |
        v                            v
+--------------------+       +------------------+
| Data Loader Module |       | Scoring Engine   |
+--------------------+       +------------------+
        |                            |
        v                            v
+--------------------+       +------------------+
| YAML Questionnaire |       | PDF Generator    |
+--------------------+       +------------------+
                                     |
                                     v
                           +--------------------+
                           | Output (Console/   |
                           | PDF Report)        |
                           +--------------------+
```

**Data Flow:**

1. User runs the script with optional CLI arguments.
2. CLI interface loads questions from YAML via Data Loader.
3. Controller handles user input, navigation, and answer recording.
4. Scoring Engine processes responses to determine MBTI type.
5. Output generated on console; optional PDF created if requested.

---

## 4. Component Details

### 4.1 CLI Interface (`cli.py`)

* Presents instructions and Likert scale.
* Accepts numeric responses (1–5), `z` for undo, `done` for finish.
* Passes responses to Controller.

### 4.2 Controller (`controller.py`)

* Manages question sequence.
* Validates responses.
* Triggers scoring after completion.
* Passes results to output module.

### 4.3 Data Loader (`data_loader.py`)

* Reads `config/mbti_questionnaire.yaml`.
* Validates YAML structure (must include `text`, `dimension`, `reverse` keys where applicable).

### 4.4 Scoring Engine (`scoring.py`)

* Aggregates scores for each dimension.
* Applies reverse scoring where specified.
* Determines MBTI type from four dimension winners.

### 4.5 PDF Generator (`pdf_generator.py`)

* Uses `reportlab` and `matplotlib` to create a styled PDF.
* Includes bar chart of percentages.

---

## 5. Data Models & APIs

### 5.1 Data Model: Question

```python
class Question:
    def __init__(self, text: str, dimension: str, reverse: bool = False):
        self.text = text
        self.dimension = dimension
        self.reverse = reverse
```

### 5.2 Data Model: Response

```python
class Response:
    def __init__(self, question_id: int, score: int):
        self.question_id = question_id
        self.score = score
```

### 5.3 API: `load_questions(path: str) -> List[Question]`

* **Input:** Path to YAML file.
* **Output:** List of `Question` objects.

### 5.4 API: `score_responses(responses: List[Response]) -> Dict[str, int]`

* **Output:** Dictionary mapping each dimension letter to a score.

### 5.5 API: `generate_pdf(results: Dict, output_path: str, author: str)`

* **Output:** PDF file with results.

---

## 6. Error Handling & Edge Cases

* **Invalid Input:** Non-integer or out-of-range scores trigger prompt to re-enter.
* **Undo with No History:** Ignore and re-prompt.
* **YAML Format Error:** Exit gracefully with error message.
* **Incomplete Questionnaire:** Prevent scoring until all questions answered.
* **Empty PDF Path:** Skip PDF generation.

---

## 7. Security & Performance Considerations

* No sensitive data collected.
* Ensure YAML parsing uses `safe_load` to avoid code execution risks.
* Minimal performance concerns; operations are O(n) relative to number of questions.

---

## 8. Dependencies & Assumptions

**Dependencies:**

* `PyYAML` – Load questions.
* `matplotlib` – Charts for PDF.
* `reportlab` – PDF generation.
* `pandas` – Optional aggregation and table formatting.

**Assumptions:**

* YAML question file will follow agreed schema.
* User has Python 3.8+ installed.
* CLI execution environment supports UTF-8 characters.

---

## 9. Appendices

### Appendix A – YAML Example

```yaml
items:
  - text: "You enjoy social gatherings."
    dimension: "E"
  - text: "You value introspection."
    dimension: "I"
    reverse: true
```

### Appendix B – MBTI Scoring Logic Table

| Dimension | Positive Pole | Negative Pole |
| --------- | ------------- | ------------- |
| E/I       | Extraversion  | Introversion  |
| S/N       | Sensing       | Intuition     |
| T/F       | Thinking      | Feeling       |
| J/P       | Judging       | Perceiving    |
