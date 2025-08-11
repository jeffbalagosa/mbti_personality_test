# **MBTI Personality Test – Product Requirements Document (PRD)**

## 1. Overview & Goals

**Purpose:**
Develop a Python-based **MBTI Personality Test** script for terminal/CLI use. The script will present a series of MBTI questions, collect user responses, calculate personality type (e.g., INTJ, ESFP), and display or export the result.

**Intended Audience:**

* Individuals seeking self-assessment using MBTI methodology.
* Educators, coaches, and trainers who want a quick, offline MBTI test.
* Developers looking for an MBTI module that follows the modular structure of the provided Big-5 codebase.

**Goals:**

* Maintain **modular architecture** consistent with the Big-5 script (separate modules for CLI, scoring, data loading, and reporting).
* Ensure **accuracy** in MBTI type determination based on established scoring rules from the provided MBTI questionnaire.
* Provide **clear, interactive** CLI experience.
* Enable **optional PDF report generation** similar to the Big-5 project.

---

## 2. Functional Requirements

1. **Questionnaire Loading**

   * Load MBTI questions from an external file (`config/mbti_questionnaire.yaml`).
   * Each question has:

     * `text` (string)
     * `dimension` (E/I, S/N, T/F, J/P)
     * `reverse` (optional boolean)

2. **CLI Interface**

   * Display instructions and Likert scale (1–5).
   * Allow `z` to undo last answer.
   * Allow `done` to finish after all questions.

3. **Scoring**

   * Map answers to MBTI dimensions using scoring rules:

     * Reverse scoring where specified.
     * Aggregate totals for each dimension pair (e.g., E vs I).
   * Determine dominant trait in each dimension pair to form MBTI type.

4. **Results Display**

   * Print MBTI type and brief description to console.
   * Show percentage breakdown for each dimension.

5. **PDF Report Generation** (optional)

   * Include MBTI type, description, and dimension scores.
   * Bar graph visualizing percentages for each side of the four dichotomies.

6. **Command-Line Arguments**

   * `--pdf <path>`: Export PDF report.
   * `--author <name>`: Author name in PDF.

---

## 3. Non-Functional Requirements

* **Performance:** Must handle up to 100 questions with instant scoring.
* **Compatibility:** Python 3.8+.
* **Maintainability:** Modular design, following Big-5 script structure.
* **Extensibility:** Easy to swap in different MBTI question sets.
* **Reliability:** Validation to ensure all questions answered before scoring.

---

## 4. Data & Input Requirements

* **Question File Format:** YAML, structured as:

```yaml
items:
  - text: "You enjoy large social gatherings."
    dimension: "E"
  - text: "You prefer quiet time alone."
    dimension: "I"
    reverse: true
```

* **Storage Location:** `config/mbti_questionnaire.yaml`
* **Parsing:** Use `data_loader` module pattern from Big-5.

---

## 5. Scoring & Logic

* **Scoring Steps:**

  1. For each question, assign 1–5 points (reverse if `reverse: true`).
  2. Aggregate scores by dimension:

     * **E** vs **I**
     * **S** vs **N**
     * **T** vs **F**
     * **J** vs **P**
  3. For each pair, select the higher score’s letter.
  4. Concatenate 4 letters → MBTI type (e.g., `ENTP`).

* **Example:**

  * E=45, I=35 → E
  * S=28, N=42 → N
  * T=50, F=30 → T
  * J=37, P=43 → P
    → **ENTP**

---

## 6. User Interaction Flow

1. Launch script:

   ```
   python mbti_test.py --pdf results.pdf --author "John Doe"
   ```
2. Script displays instructions and Likert scale.
3. User answers questions (1–5).
4. User types `done` after all answered.
5. Script calculates MBTI type.
6. Results displayed in console; PDF generated if requested.

---

## 7. Output Format

**Console Output Example:**

```
Your MBTI Type: INTJ
Description: Strategic, independent thinker with a strong vision for the future.

Scores:
E: 35%  I: 65%
S: 40%  N: 60%
T: 75%  F: 25%
J: 68%  P: 32%
```

**PDF Output Example:**

* Title: "MBTI Personality Test Results"
* MBTI type and description
* Bar chart of percentages for each side of the four dimensions
* Date and author

---

## 8. Technical Constraints

* **Dependencies:**

  * `PyYAML` (load YAML)
  * `matplotlib` (bar graph)
  * `reportlab` (PDF output)
  * `pandas` (data handling)
* **Environment:**

  * Python 3.8+
  * Runs in standard terminal/CLI (Windows, macOS, Linux)

---

## 9. Future Enhancements

* Web-based version using Flask/FastAPI.
* CSV/JSON export of results.
* Adaptive questioning (skip redundant questions).
* Expanded personality descriptions with career advice.
* Integration with Big-5 results for hybrid report.
