# Graph Report - Mocknest  (2026-04-27)

## Corpus Check
- 20 files · ~8,271 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 173 nodes · 415 edges · 11 communities detected
- Extraction: 67% EXTRACTED · 33% INFERRED · 0% AMBIGUOUS · INFERRED: 139 edges (avg confidence: 0.77)
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
1. `connect()` - 35 edges
2. `Database` - 25 edges
3. `TakeTestPage` - 23 edges
4. `MainWindow` - 18 edges
5. `AddQuestionsPage` - 15 edges
6. `AnalysisPage` - 14 edges
7. `HistoryPage` - 13 edges
8. `LibraryPage` - 13 edges
9. `QuestionCard` - 11 edges
10. `QuestionPalette` - 11 edges

## Surprising Connections (you probably didn't know these)
- `Database` --uses--> `MainWindow`  [INFERRED]
  db.py → main.py
- `Database` --uses--> `Insert sample mock if no mocks exist yet`  [INFERRED]
  db.py → data\seed.py
- `MainWindow` --uses--> `AddQuestionsPage`  [INFERRED]
  main.py → pages\add_questions.py
- `MainWindow` --uses--> `AnalysisPage`  [INFERRED]
  main.py → pages\analysis.py
- `MainWindow` --uses--> `HistoryPage`  [INFERRED]
  main.py → pages\history.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.12
Nodes (3): QuestionCard, TakeTestPage, TimerWidget

### Community 1 - "Community 1"
Cohesion: 0.13
Nodes (6): connect(), Database, export_mock(), import_mock(), Insert sample mock if no mocks exist yet, seed_database()

### Community 2 - "Community 2"
Cohesion: 0.16
Nodes (6): AnalysisPage, ScoreTrendChart, HomePage, QFrame, QLabel, QWidget

### Community 3 - "Community 3"
Cohesion: 0.18
Nodes (6): CreatorPage, load_theme(), main(), MainWindow, QMainWindow, Sidebar

### Community 4 - "Community 4"
Cohesion: 0.3
Nodes (1): AddQuestionsPage

### Community 5 - "Community 5"
Cohesion: 0.36
Nodes (1): HistoryPage

### Community 6 - "Community 6"
Cohesion: 0.29
Nodes (8): AttemptAnswer, AttemptResult, Mock, Question, calculate_score(), _normal_answer(), _parse_correct(), _value_from_question()

### Community 7 - "Community 7"
Cohesion: 0.31
Nodes (1): QuestionPalette

### Community 8 - "Community 8"
Cohesion: 0.36
Nodes (1): LibraryPage

### Community 9 - "Community 9"
Cohesion: 0.5
Nodes (4): SQLite Database, .jmock Format, MockNest Application, Scoring System

### Community 10 - "Community 10"
Cohesion: 1.0
Nodes (1): Color palette and minimal style definitions for MockNest.  For full theming, use

## Knowledge Gaps
- **5 isolated node(s):** `Mock`, `Color palette and minimal style definitions for MockNest.  For full theming, use`, `.jmock Format`, `SQLite Database`, `Scoring System`
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 4`** (14 nodes): `AddQuestionsPage`, `._add_question()`, `._build()`, `._clear_form()`, `._delete_question()`, `.__init__()`, `._question_row()`, `._refresh()`, `._sections()`, `._select_section()`, `._style_tabs()`, `._sync_type_visibility()`, `.add_question()`, `add_questions.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 5`** (10 nodes): `HistoryPage`, `._build()`, `._clear_stats()`, `._duration_text()`, `._format_date()`, `.__init__()`, `._load()`, `._populate_filter()`, `._stat_card()`, `history.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 7`** (10 nodes): `question_palette.py`, `QuestionPalette`, `.get_summary_text()`, `.__init__()`, `.set_current()`, `._style_button()`, `.sync_states()`, `.update_section_summary()`, `.update_status()`, `._show_palette_info()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 8`** (9 nodes): `.delete_mock()`, `LibraryPage`, `._build()`, `._clear_grid()`, `._delete_mock()`, `.__init__()`, `._on_search()`, `._render_cards()`, `library.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 10`** (2 nodes): `styles.py`, `Color palette and minimal style definitions for MockNest.  For full theming, use`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `connect()` connect `Community 1` to `Community 0`, `Community 2`, `Community 3`, `Community 4`, `Community 5`, `Community 7`, `Community 8`?**
  _High betweenness centrality (0.178) - this node is a cross-community bridge._
- **Why does `TakeTestPage` connect `Community 0` to `Community 1`, `Community 2`, `Community 3`, `Community 7`?**
  _High betweenness centrality (0.157) - this node is a cross-community bridge._
- **Why does `MainWindow` connect `Community 3` to `Community 0`, `Community 1`, `Community 2`, `Community 4`, `Community 5`, `Community 8`?**
  _High betweenness centrality (0.143) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `connect()` (e.g. with `.__init__()` and `.__init__()`) actually correct?**
  _`connect()` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `Database` (e.g. with `MainWindow` and `Insert sample mock if no mocks exist yet`) actually correct?**
  _`Database` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 22 inferred relationships involving `QLabel` (e.g. with `.__init__()` and `.__init__()`) actually correct?**
  _`QLabel` has 22 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `TakeTestPage` (e.g. with `MainWindow` and `QuestionCard`) actually correct?**
  _`TakeTestPage` has 5 INFERRED edges - model-reasoned connections that need verification._