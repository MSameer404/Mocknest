# Graph Report - .  (2026-04-28)

## Corpus Check
- Corpus is ~10,405 words - fits in a single context window. You may not need a graph.

## Summary
- 227 nodes · 519 edges · 13 communities detected
- Extraction: 67% EXTRACTED · 33% INFERRED · 0% AMBIGUOUS · INFERRED: 169 edges (avg confidence: 0.77)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Database & Seeding|Database & Seeding]]
- [[_COMMUNITY_Test Execution & Timer|Test Execution & Timer]]
- [[_COMMUNITY_Question Rendering & LaTeX|Question Rendering & LaTeX]]
- [[_COMMUNITY_Question Palette & Creation|Question Palette & Creation]]
- [[_COMMUNITY_Result Analysis & Review|Result Analysis & Review]]
- [[_COMMUNITY_Main App & Navigation|Main App & Navigation]]
- [[_COMMUNITY_Rich Text Editor & Mock Creator|Rich Text Editor & Mock Creator]]
- [[_COMMUNITY_Dashboard & File ImportExport|Dashboard & File Import/Export]]
- [[_COMMUNITY_Data Models & Scoring Logic|Data Models & Scoring Logic]]
- [[_COMMUNITY_Attempt History|Attempt History]]
- [[_COMMUNITY_Mock Test Library|Mock Test Library]]
- [[_COMMUNITY_Project Documentation|Project Documentation]]
- [[_COMMUNITY_UI Styling|UI Styling]]

## God Nodes (most connected - your core abstractions)
1. `connect()` - 40 edges
2. `Database` - 29 edges
3. `TakeTestPage` - 23 edges
4. `MainWindow` - 22 edges
5. `QuestionPalette` - 15 edges
6. `AddQuestionsPage` - 15 edges
7. `RichEditor` - 14 edges
8. `DeepAnalysisPage` - 14 edges
9. `HistoryPage` - 14 edges
10. `LibraryPage` - 14 edges

## Surprising Connections (you probably didn't know these)
- `MainWindow` --uses--> `Database`  [INFERRED]
  C:\Users\MOHAMMAD SAMEER\Core Data\Computer Science\Projects\Mocknest\main.py → C:\Users\MOHAMMAD SAMEER\Core Data\Computer Science\Projects\Mocknest\db.py
- `Insert sample mock if no mocks exist yet` --uses--> `Database`  [INFERRED]
  C:\Users\MOHAMMAD SAMEER\Core Data\Computer Science\Projects\Mocknest\data\seed.py → C:\Users\MOHAMMAD SAMEER\Core Data\Computer Science\Projects\Mocknest\db.py
- `MainWindow` --uses--> `AddQuestionsPage`  [INFERRED]
  C:\Users\MOHAMMAD SAMEER\Core Data\Computer Science\Projects\Mocknest\main.py → C:\Users\MOHAMMAD SAMEER\Core Data\Computer Science\Projects\Mocknest\pages\add_questions.py
- `MainWindow` --uses--> `AnalysisPage`  [INFERRED]
  C:\Users\MOHAMMAD SAMEER\Core Data\Computer Science\Projects\Mocknest\main.py → C:\Users\MOHAMMAD SAMEER\Core Data\Computer Science\Projects\Mocknest\pages\analysis.py
- `MainWindow` --uses--> `CreatorPage`  [INFERRED]
  C:\Users\MOHAMMAD SAMEER\Core Data\Computer Science\Projects\Mocknest\main.py → C:\Users\MOHAMMAD SAMEER\Core Data\Computer Science\Projects\Mocknest\pages\creator.py

## Communities

### Community 0 - "Database & Seeding"
Cohesion: 0.11
Nodes (4): connect(), Database, Insert sample mock if no mocks exist yet, seed_database()

### Community 1 - "Test Execution & Timer"
Cohesion: 0.16
Nodes (2): TakeTestPage, TimerWidget

### Community 2 - "Question Rendering & LaTeX"
Cohesion: 0.14
Nodes (6): OptionCard, QuestionCard, Renders a LaTeX math string to a base64 encoded PNG image., Converts raw text containing markdown images ![alt](path) and LaTeX $$math$$ int, render_latex_to_base64(), text_to_html()

### Community 3 - "Question Palette & Creation"
Cohesion: 0.17
Nodes (3): AddQuestionsPage, QuestionPalette, QWidget

### Community 4 - "Result Analysis & Review"
Cohesion: 0.16
Nodes (4): AnalysisPage, DeepAnalysisPage, QFrame, QLabel

### Community 5 - "Main App & Navigation"
Cohesion: 0.21
Nodes (5): load_theme(), main(), MainWindow, QMainWindow, Sidebar

### Community 6 - "Rich Text Editor & Mock Creator"
Cohesion: 0.15
Nodes (3): CreatorPage, A dual-pane editor (raw text + live preview) supporting images and LaTeX., RichEditor

### Community 7 - "Dashboard & File Import/Export"
Cohesion: 0.23
Nodes (5): DashboardPage, export_mock(), import_mock(), _process_export_images(), _process_import_images()

### Community 8 - "Data Models & Scoring Logic"
Cohesion: 0.28
Nodes (8): AttemptAnswer, AttemptResult, Mock, Question, calculate_score(), _normal_answer(), _parse_correct(), _value_from_question()

### Community 9 - "Attempt History"
Cohesion: 0.3
Nodes (1): HistoryPage

### Community 10 - "Mock Test Library"
Cohesion: 0.33
Nodes (1): LibraryPage

### Community 11 - "Project Documentation"
Cohesion: 0.29
Nodes (7): Database, Features, Installation, MockNest, Project Structure, Scoring System, Usage

### Community 12 - "UI Styling"
Cohesion: 0.67
Nodes (1): Color palette and minimal style definitions for MockNest.  For full theming, use

## Knowledge Gaps
- **9 isolated node(s):** `Renders a LaTeX math string to a base64 encoded PNG image.`, `Converts raw text containing markdown images ![alt](path) and LaTeX $$math$$ int`, `A dual-pane editor (raw text + live preview) supporting images and LaTeX.`, `Features`, `Installation` (+4 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Test Execution & Timer`** (25 nodes): `timer_widget.py`, `take_test.py`, `timer_widget.py`, `.save_answer()`, `take_test.py`, `TakeTestPage`, `._auto_submit()`, `._build()`, `._enter_question()`, `._go_to_section()`, `._mark_review_next()`, `._next_question()`, `._previous_question()`, `._record_current_question()`, `._save_next()`, `._sections()`, `._submit()`, `._sync_nav_buttons()`, `TimerWidget`, `.__init__()`, `._render()`, `.set_duration()`, `.start()`, `.stop()`, `._tick()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Attempt History`** (12 nodes): `history.py`, `HistoryPage`, `._attempt_card()`, `._build()`, `._clear_grid()`, `._delete_attempt()`, `._duration_text()`, `._format_date()`, `.__init__()`, `._load()`, `._on_search()`, `history.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Mock Test Library`** (11 nodes): `library.py`, `LibraryPage`, `._build()`, `._clear_grid()`, `._delete_mock()`, `._export_mock()`, `.__init__()`, `._mock_card()`, `._on_search()`, `._render_cards()`, `library.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `UI Styling`** (3 nodes): `styles.py`, `styles.py`, `Color palette and minimal style definitions for MockNest.  For full theming, use`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `connect()` connect `Database & Seeding` to `Test Execution & Timer`, `Question Palette & Creation`, `Result Analysis & Review`, `Main App & Navigation`, `Rich Text Editor & Mock Creator`, `Attempt History`, `Mock Test Library`?**
  _High betweenness centrality (0.164) - this node is a cross-community bridge._
- **Why does `MainWindow` connect `Main App & Navigation` to `Database & Seeding`, `Test Execution & Timer`, `Question Palette & Creation`, `Result Analysis & Review`, `Rich Text Editor & Mock Creator`, `Dashboard & File Import/Export`, `Data Models & Scoring Logic`, `Attempt History`, `Mock Test Library`?**
  _High betweenness centrality (0.148) - this node is a cross-community bridge._
- **Why does `TakeTestPage` connect `Test Execution & Timer` to `Database & Seeding`, `Question Rendering & LaTeX`, `Question Palette & Creation`, `Result Analysis & Review`, `Main App & Navigation`?**
  _High betweenness centrality (0.117) - this node is a cross-community bridge._
- **Are the 16 inferred relationships involving `connect()` (e.g. with `.__init__()` and `.__init__()`) actually correct?**
  _`connect()` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `Database` (e.g. with `MainWindow` and `Insert sample mock if no mocks exist yet`) actually correct?**
  _`Database` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `TakeTestPage` (e.g. with `MainWindow` and `QuestionCard`) actually correct?**
  _`TakeTestPage` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `MainWindow` (e.g. with `Sidebar` and `Database`) actually correct?**
  _`MainWindow` has 10 INFERRED edges - model-reasoned connections that need verification._