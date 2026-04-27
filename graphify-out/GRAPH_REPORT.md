# Graph Report - Mocknest  (2026-04-28)

## Corpus Check
- 22 files · ~8,921 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 186 nodes · 431 edges · 11 communities detected
- Extraction: 65% EXTRACTED · 35% INFERRED · 0% AMBIGUOUS · INFERRED: 150 edges (avg confidence: 0.77)
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
1. `connect()` - 36 edges
2. `Database` - 27 edges
3. `TakeTestPage` - 23 edges
4. `MainWindow` - 18 edges
5. `AddQuestionsPage` - 14 edges
6. `AnalysisPage` - 14 edges
7. `QuestionPalette` - 13 edges
8. `RichEditor` - 13 edges
9. `LibraryPage` - 13 edges
10. `QuestionCard` - 11 edges

## Surprising Connections (you probably didn't know these)
- `Database` --uses--> `MainWindow`  [INFERRED]
  db.py → main.py
- `Database` --uses--> `Insert sample mock if no mocks exist yet`  [INFERRED]
  db.py → data\seed.py
- `MainWindow` --uses--> `AddQuestionsPage`  [INFERRED]
  main.py → pages\add_questions.py
- `MainWindow` --uses--> `AnalysisPage`  [INFERRED]
  main.py → pages\analysis.py
- `MainWindow` --uses--> `CreatorPage`  [INFERRED]
  main.py → pages\creator.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.13
Nodes (4): connect(), Database, Insert sample mock if no mocks exist yet, seed_database()

### Community 1 - "Community 1"
Cohesion: 0.16
Nodes (2): QuestionCard, TakeTestPage

### Community 2 - "Community 2"
Cohesion: 0.15
Nodes (6): HistoryPage, load_theme(), main(), MainWindow, QMainWindow, Sidebar

### Community 3 - "Community 3"
Cohesion: 0.18
Nodes (3): AddQuestionsPage, QuestionPalette, QWidget

### Community 4 - "Community 4"
Cohesion: 0.19
Nodes (5): AnalysisPage, ScoreTrendChart, DashboardPage, QFrame, QLabel

### Community 5 - "Community 5"
Cohesion: 0.13
Nodes (7): CreatorPage, A dual-pane editor (raw text + live preview) supporting images and LaTeX., RichEditor, Renders a LaTeX math string to a base64 encoded PNG image., Converts raw text containing markdown images ![alt](path) and LaTeX $$math$$ int, render_latex_to_base64(), text_to_html()

### Community 6 - "Community 6"
Cohesion: 0.2
Nodes (5): LibraryPage, export_mock(), import_mock(), _process_export_images(), _process_import_images()

### Community 7 - "Community 7"
Cohesion: 0.29
Nodes (8): AttemptAnswer, AttemptResult, Mock, Question, calculate_score(), _normal_answer(), _parse_correct(), _value_from_question()

### Community 8 - "Community 8"
Cohesion: 0.33
Nodes (1): TimerWidget

### Community 9 - "Community 9"
Cohesion: 0.5
Nodes (4): SQLite Database, .jmock Format, MockNest Application, Scoring System

### Community 10 - "Community 10"
Cohesion: 1.0
Nodes (1): Color palette and minimal style definitions for MockNest.  For full theming, use

## Knowledge Gaps
- **8 isolated node(s):** `Mock`, `Color palette and minimal style definitions for MockNest.  For full theming, use`, `Renders a LaTeX math string to a base64 encoded PNG image.`, `Converts raw text containing markdown images ![alt](path) and LaTeX $$math$$ int`, `A dual-pane editor (raw text + live preview) supporting images and LaTeX.` (+3 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 1`** (27 nodes): `question_card.py`, `.save_answer()`, `take_test.py`, `QuestionCard`, `.clear_answer()`, `._clear_options()`, `.get_answer()`, `.__init__()`, `._parse_options()`, `.set_answer()`, `.set_question()`, `TakeTestPage`, `._auto_submit()`, `._build()`, `._clear_response()`, `._enter_question()`, `._go_to_section()`, `.__init__()`, `._mark_review_next()`, `._next_question()`, `._previous_question()`, `._record_current_question()`, `._save_next()`, `._sections()`, `._style_section_tabs()`, `._submit()`, `._sync_nav_buttons()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 8`** (9 nodes): `timer_widget.py`, `._on_text_changed()`, `TimerWidget`, `.__init__()`, `._render()`, `.set_duration()`, `.start()`, `.stop()`, `._tick()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 10`** (2 nodes): `styles.py`, `Color palette and minimal style definitions for MockNest.  For full theming, use`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `connect()` connect `Community 0` to `Community 1`, `Community 2`, `Community 3`, `Community 4`, `Community 5`, `Community 6`, `Community 8`?**
  _High betweenness centrality (0.179) - this node is a cross-community bridge._
- **Why does `TakeTestPage` connect `Community 1` to `Community 8`, `Community 2`, `Community 3`?**
  _High betweenness centrality (0.132) - this node is a cross-community bridge._
- **Why does `MainWindow` connect `Community 2` to `Community 0`, `Community 1`, `Community 3`, `Community 4`, `Community 5`, `Community 6`?**
  _High betweenness centrality (0.129) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `connect()` (e.g. with `.__init__()` and `.__init__()`) actually correct?**
  _`connect()` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `Database` (e.g. with `MainWindow` and `Insert sample mock if no mocks exist yet`) actually correct?**
  _`Database` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `TakeTestPage` (e.g. with `MainWindow` and `QuestionCard`) actually correct?**
  _`TakeTestPage` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 19 inferred relationships involving `QLabel` (e.g. with `.__init__()` and `.set_question()`) actually correct?**
  _`QLabel` has 19 INFERRED edges - model-reasoned connections that need verification._