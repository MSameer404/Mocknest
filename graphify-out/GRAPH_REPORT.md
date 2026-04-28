# Graph Report - Mocknest  (2026-04-28)

## Corpus Check
- 23 files · ~10,877 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 208 nodes · 505 edges · 11 communities detected
- Extraction: 65% EXTRACTED · 35% INFERRED · 0% AMBIGUOUS · INFERRED: 175 edges (avg confidence: 0.77)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]

## God Nodes (most connected - your core abstractions)
1. `connect()` - 41 edges
2. `Database` - 29 edges
3. `MainWindow` - 26 edges
4. `TakeTestPage` - 22 edges
5. `AddQuestionsPage` - 15 edges
6. `QuestionPalette` - 14 edges
7. `RichEditor` - 13 edges
8. `DeepAnalysisPage` - 13 edges
9. `HistoryPage` - 13 edges
10. `LibraryPage` - 13 edges

## Surprising Connections (you probably didn't know these)
- `MainWindow` --uses--> `Database`  [INFERRED]
  main.py → db.py
- `Insert sample mock if no mocks exist yet` --uses--> `Database`  [INFERRED]
  data\seed.py → db.py
- `MainWindow` --uses--> `AddQuestionsPage`  [INFERRED]
  main.py → pages\add_questions.py
- `MainWindow` --uses--> `CreatorPage`  [INFERRED]
  main.py → pages\creator.py
- `MainWindow` --uses--> `HistoryPage`  [INFERRED]
  main.py → pages\history.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.11
Nodes (8): connect(), Database, export_mock(), import_mock(), _process_export_images(), _process_import_images(), Insert sample mock if no mocks exist yet, seed_database()

### Community 1 - "Community 1"
Cohesion: 0.12
Nodes (5): AddQuestionsPage, QuestionPalette, QWidget, A dual-pane editor (raw text + live preview) supporting images and LaTeX., RichEditor

### Community 2 - "Community 2"
Cohesion: 0.16
Nodes (2): TakeTestPage, TimerWidget

### Community 3 - "Community 3"
Cohesion: 0.16
Nodes (6): AnalysisPage, load_theme(), main(), MainWindow, QMainWindow, Sidebar

### Community 4 - "Community 4"
Cohesion: 0.15
Nodes (6): OptionCard, QuestionCard, Renders a LaTeX math string to a base64 encoded PNG image., Converts raw text containing markdown images ![alt](path) and LaTeX $$math$$ int, render_latex_to_base64(), text_to_html()

### Community 5 - "Community 5"
Cohesion: 0.17
Nodes (4): CreatorPage, DashboardPage, QFrame, QLabel

### Community 6 - "Community 6"
Cohesion: 0.25
Nodes (8): AttemptAnswer, AttemptResult, Mock, Question, calculate_score(), _normal_answer(), _parse_correct(), _value_from_question()

### Community 7 - "Community 7"
Cohesion: 0.35
Nodes (1): HistoryPage

### Community 8 - "Community 8"
Cohesion: 0.38
Nodes (1): LibraryPage

### Community 9 - "Community 9"
Cohesion: 0.36
Nodes (1): DeepAnalysisPage

### Community 10 - "Community 10"
Cohesion: 1.0
Nodes (1): Color palette and minimal style definitions for MockNest.  For full theming, use

## Knowledge Gaps
- **5 isolated node(s):** `Mock`, `Color palette and minimal style definitions for MockNest.  For full theming, use`, `Renders a LaTeX math string to a base64 encoded PNG image.`, `Converts raw text containing markdown images ![alt](path) and LaTeX $$math$$ int`, `A dual-pane editor (raw text + live preview) supporting images and LaTeX.`
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 2`** (25 nodes): `timer_widget.py`, `.save_answer()`, `take_test.py`, `._on_text_changed()`, `TakeTestPage`, `._auto_submit()`, `._build()`, `._enter_question()`, `._go_to_section()`, `.__init__()`, `._mark_review_next()`, `._next_question()`, `._previous_question()`, `._record_current_question()`, `._save_next()`, `._sections()`, `._submit()`, `._sync_nav_buttons()`, `TimerWidget`, `.__init__()`, `._render()`, `.set_duration()`, `.start()`, `.stop()`, `._tick()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 7`** (11 nodes): `HistoryPage`, `._attempt_card()`, `._build()`, `._clear_grid()`, `._delete_attempt()`, `._duration_text()`, `._format_date()`, `.__init__()`, `._load()`, `._on_search()`, `history.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 8`** (10 nodes): `LibraryPage`, `._build()`, `._clear_grid()`, `._delete_mock()`, `._export_mock()`, `.__init__()`, `._mock_card()`, `._on_search()`, `._render_cards()`, `library.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 9`** (10 nodes): `DeepAnalysisPage`, `._build()`, `._clear_options()`, `._enter_question()`, `._evaluate_answer()`, `._next_question()`, `._parse_options()`, `._previous_question()`, `._switch_subject()`, `deep_analysis.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 10`** (2 nodes): `styles.py`, `Color palette and minimal style definitions for MockNest.  For full theming, use`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `connect()` connect `Community 0` to `Community 1`, `Community 2`, `Community 3`, `Community 5`, `Community 7`, `Community 8`, `Community 9`?**
  _High betweenness centrality (0.185) - this node is a cross-community bridge._
- **Why does `MainWindow` connect `Community 3` to `Community 0`, `Community 1`, `Community 2`, `Community 5`, `Community 6`, `Community 7`, `Community 8`, `Community 9`?**
  _High betweenness centrality (0.179) - this node is a cross-community bridge._
- **Why does `TakeTestPage` connect `Community 2` to `Community 1`, `Community 3`, `Community 4`, `Community 5`?**
  _High betweenness centrality (0.122) - this node is a cross-community bridge._
- **Are the 17 inferred relationships involving `connect()` (e.g. with `.__init__()` and `.__init__()`) actually correct?**
  _`connect()` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `Database` (e.g. with `MainWindow` and `Insert sample mock if no mocks exist yet`) actually correct?**
  _`Database` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `MainWindow` (e.g. with `Sidebar` and `Database`) actually correct?**
  _`MainWindow` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `TakeTestPage` (e.g. with `MainWindow` and `QuestionCard`) actually correct?**
  _`TakeTestPage` has 5 INFERRED edges - model-reasoned connections that need verification._