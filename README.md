# MockNest

A desktop application for creating and taking JEE (Joint Entrance Examination) mock tests. Built with PyQt6 and SQLite.

## Features

- **Mock Test Library** – Create, import, and manage mock tests
- **Question Management** – Add single-choice, multiple-choice, and numerical questions
- **Timed Tests** – Take tests with configurable duration and automatic timer
- **Detailed Analysis** – View section-wise breakdown, accuracy, and score after each attempt
- **Import/Export** – Share mocks using the `.jmock` file format
- **Attempt History** – Track all past attempts with scores and timestamps

## Installation

### Requirements
- Python 3.13 or higher
- PyQt6

### Setup

```bash
# Clone the repository
git clone <repository-url>
cd Mocknest

# Install dependencies
pip install pyqt6

# Or using the project configuration
pip install -e .
```

## Usage

### Running the Application

**Windows:**
```bash
run.bat
```

**Linux/macOS:**
```bash
./run.sh
```

**Direct:**
```bash
python main.py
```

### Creating a Mock Test

1. Click **"Create Mock"** in the Library page
2. Enter title, duration, marking scheme, and sections
3. Add questions to the mock (single, multiple, or numerical type)
4. Save and the mock appears in your library

### Taking a Test

1. Select a mock from the **Library** or **Dashboard** page
2. Click **"Take Test"** to start
3. Answer questions using the question palette
4. Submit when done or when time runs out

### Importing/Exporting Mocks

- **Export**: Click the export icon next to any mock to save as `.jmock` file
- **Import**: Click **"Import Mock"** and select a `.jmock` file

## Project Structure

```
Mocknest/
├── main.py              # Application entry point
├── db.py                # SQLite database operations
├── models.py            # Data classes (Question, Mock, Attempt)
├── mock_format.py       # Import/export (.jmock files)
├── scoring.py           # Test scoring and analysis logic
├── styles.py            # Application styling
├── components/          # Reusable UI components
│   ├── sidebar.py       # Navigation sidebar
│   ├── question_card.py
│   └── question_palette.py
├── pages/               # Application pages
│   ├── dashboard.py
│   ├── library.py
│   ├── creator.py       # Mock creation form
│   ├── add_questions.py
│   ├── take_test.py
│   ├── analysis.py      # Result analysis
│   └── history.py
└── data/
    └── seed.py          # Sample data initialization
```

## Database

SQLite database stored at `~/.jee_mock_app/app.db`

**Tables:**
- `mocks` – Test metadata (title, duration, marking scheme, sections)
- `questions` – Question data linked to mocks
- `attempts` – Test attempt records with answers and scores

## Scoring System

- **Single Choice**: +4 for correct, -1 for incorrect
- **Multiple Choice**: +4 if all correct, 0 if partial correct, -1 if wrong
- **Numerical**: +4 if within ±0.01 tolerance, 0 otherwise

Default marking scheme is configurable per mock.

## Building Executable

```bash
# Using PyInstaller
pyinstaller JEE\ Mock\ App.spec

# Output location
dist/JEE Mock App.exe
```

## License

[Add your license information here]
