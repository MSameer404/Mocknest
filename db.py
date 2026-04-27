import json
import os
import sqlite3
import uuid
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path


DB_PATH = Path.home() / ".jee_mock_app" / "app.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


class Database:
    def __init__(self):
        self.init_db()

    @contextmanager
    def connect(self):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def init_db(self):
        try:
            with self.connect() as conn:
                conn.executescript(
                    """
                    CREATE TABLE IF NOT EXISTS mocks (
                        id TEXT PRIMARY KEY,
                        title TEXT NOT NULL,
                        duration_minutes INTEGER NOT NULL,
                        marks_correct REAL NOT NULL DEFAULT 4,
                        marks_incorrect REAL NOT NULL DEFAULT -1,
                        sections TEXT NOT NULL DEFAULT '["Physics","Chemistry","Maths"]',
                        created_at TEXT NOT NULL,
                        author TEXT NOT NULL DEFAULT 'Anonymous',
                        source TEXT NOT NULL DEFAULT 'local'
                    );

                    CREATE TABLE IF NOT EXISTS questions (
                        id TEXT PRIMARY KEY,
                        mock_id TEXT NOT NULL,
                        section TEXT NOT NULL,
                        type TEXT NOT NULL,
                        text TEXT NOT NULL,
                        options TEXT,
                        correct_answer TEXT NOT NULL,
                        order_index INTEGER NOT NULL,
                        FOREIGN KEY (mock_id) REFERENCES mocks(id) ON DELETE CASCADE
                    );

                    CREATE TABLE IF NOT EXISTS attempts (
                        id TEXT PRIMARY KEY,
                        mock_id TEXT NOT NULL,
                        started_at TEXT NOT NULL,
                        finished_at TEXT,
                        total_score REAL,
                        max_score REAL,
                        answers TEXT NOT NULL DEFAULT '{}',
                        FOREIGN KEY (mock_id) REFERENCES mocks(id) ON DELETE CASCADE
                    );
                    """
                )
                
                # Migration: add author column if it doesn't exist
                try:
                    conn.execute("ALTER TABLE mocks ADD COLUMN author TEXT NOT NULL DEFAULT 'Anonymous'")
                except sqlite3.OperationalError:
                    pass  # Column already exists
                    
        except Exception as exc:
            print(f"Database init error: {exc}")

    def _row_to_dict(self, row):
        return dict(row) if row else {}

    def get_all_mocks(self) -> list[dict]:
        try:
            with self.connect() as conn:
                rows = conn.execute(
                    "SELECT * FROM mocks ORDER BY datetime(created_at) DESC"
                ).fetchall()
                return [dict(row) for row in rows]
        except Exception as exc:
            print(f"get_all_mocks error: {exc}")
            return []

    def get_mock(self, mock_id: str) -> dict:
        try:
            with self.connect() as conn:
                row = conn.execute("SELECT * FROM mocks WHERE id = ?", (mock_id,)).fetchone()
                return self._row_to_dict(row)
        except Exception as exc:
            print(f"get_mock error: {exc}")
            return {}

    def get_questions(self, mock_id: str) -> list[dict]:
        try:
            with self.connect() as conn:
                rows = conn.execute(
                    "SELECT * FROM questions WHERE mock_id = ? ORDER BY order_index ASC",
                    (mock_id,),
                ).fetchall()
                return [dict(row) for row in rows]
        except Exception as exc:
            print(f"get_questions error: {exc}")
            return []

    def create_mock(self, title, author) -> str:
        mock_id = str(uuid.uuid4())
        try:
            with self.connect() as conn:
                conn.execute(
                    """
                    INSERT INTO mocks
                    (id, title, author, duration_minutes, marks_correct, marks_incorrect, sections, created_at, source)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        mock_id,
                        str(title).strip(),
                        str(author).strip() or "Anonymous",
                        int(180),
                        float(4.0),
                        float(-1.0),
                        json.dumps(["Physics", "Chemistry", "Maths"]),
                        datetime.now().isoformat(timespec="seconds"),
                        "local",
                    ),
                )
            return mock_id
        except Exception as exc:
            print(f"create_mock error: {exc}")
            return ""

    def insert_mock_record(self, mock: dict) -> str:
        mock_id = mock.get("id") or str(uuid.uuid4())
        try:
            with self.connect() as conn:
                conn.execute(
                    """
                    INSERT INTO mocks
                    (id, title, author, duration_minutes, marks_correct, marks_incorrect, sections, created_at, source)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        mock_id,
                        mock.get("title", "Imported Mock"),
                        mock.get("author") or mock.get("creator") or "Anonymous",
                        int(180),
                        float(4.0),
                        float(-1.0),
                        json.dumps(["Physics", "Chemistry", "Maths"]),
                        mock.get("created_at") or datetime.now().isoformat(timespec="seconds"),
                        mock.get("source", "imported"),
                    ),
                )
            return mock_id
        except Exception as exc:
            print(f"insert_mock_record error: {exc}")
            return ""

    def add_question(self, mock_id, section, type_, text, options, correct_answer, order_index) -> str:
        question_id = str(uuid.uuid4())
        try:
            with self.connect() as conn:
                conn.execute(
                    """
                    INSERT INTO questions
                    (id, mock_id, section, type, text, options, correct_answer, order_index)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        question_id,
                        mock_id,
                        section,
                        type_,
                        text.strip(),
                        options,
                        str(correct_answer),
                        int(order_index),
                    ),
                )
            return question_id
        except Exception as exc:
            print(f"add_question error: {exc}")
            return ""

    def insert_question_record(self, question: dict, mock_id: str | None = None) -> str:
        question_id = question.get("id") or str(uuid.uuid4())
        try:
            with self.connect() as conn:
                conn.execute(
                    """
                    INSERT INTO questions
                    (id, mock_id, section, type, text, options, correct_answer, order_index)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        question_id,
                        mock_id or question.get("mock_id"),
                        question.get("section", "General"),
                        question.get("type", "single"),
                        question.get("text", ""),
                        question.get("options"),
                        str(question.get("correct_answer", "")),
                        int(question.get("order_index", 0)),
                    ),
                )
            return question_id
        except Exception as exc:
            print(f"insert_question_record error: {exc}")
            return ""

    def update_question(self, question_id, text, options, correct_answer):
        try:
            with self.connect() as conn:
                conn.execute(
                    """
                    UPDATE questions
                    SET text = ?, options = ?, correct_answer = ?
                    WHERE id = ?
                    """,
                    (text.strip(), options, str(correct_answer), question_id),
                )
        except Exception as exc:
            print(f"update_question error: {exc}")

    def prefill_jee_main_questions(self, mock_id):
        try:
            with self.connect() as conn:
                order = 0
                for section in ("Physics", "Chemistry", "Maths"):
                    for i in range(25):
                        qtype = "single" if i < 20 else "numerical"
                        question_id = str(uuid.uuid4())
                        conn.execute(
                            """
                            INSERT INTO questions
                            (id, mock_id, section, type, text, options, correct_answer, order_index)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                            """,
                            (question_id, mock_id, section, qtype, "", None, "", order),
                        )
                        order += 1
        except Exception as exc:
            print(f"prefill_jee_main_questions error: {exc}")

    def delete_mock(self, mock_id: str):
        try:
            with self.connect() as conn:
                conn.execute("DELETE FROM attempts WHERE mock_id = ?", (mock_id,))
                conn.execute("DELETE FROM mocks WHERE id = ?", (mock_id,))
        except Exception as exc:
            print(f"delete_mock error: {exc}")

    def delete_question(self, question_id: str):
        try:
            with self.connect() as conn:
                conn.execute("DELETE FROM questions WHERE id = ?", (question_id,))
        except Exception as exc:
            print(f"delete_question error: {exc}")

    def start_attempt(self, mock_id: str) -> str:
        attempt_id = str(uuid.uuid4())
        try:
            with self.connect() as conn:
                conn.execute(
                    """
                    INSERT INTO attempts (id, mock_id, started_at, answers)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        attempt_id,
                        mock_id,
                        datetime.now().isoformat(timespec="seconds"),
                        "{}",
                    ),
                )
            return attempt_id
        except Exception as exc:
            print(f"start_attempt error: {exc}")
            return ""

    def save_answer(self, attempt_id, question_id, answer, time_spent_seconds, marked_for_review):
        try:
            with self.connect() as conn:
                row = conn.execute(
                    "SELECT answers FROM attempts WHERE id = ?", (attempt_id,)
                ).fetchone()
                if not row:
                    return
                answers = json.loads(row["answers"] or "{}")
                answers[question_id] = {
                    "answer": answer,
                    "time_spent_seconds": int(time_spent_seconds),
                    "marked_for_review": bool(marked_for_review),
                }
                conn.execute(
                    "UPDATE attempts SET answers = ? WHERE id = ?",
                    (json.dumps(answers), attempt_id),
                )
        except Exception as exc:
            print(f"save_answer error: {exc}")

    def finish_attempt(self, attempt_id, total_score, max_score) -> dict:
        try:
            with self.connect() as conn:
                conn.execute(
                    """
                    UPDATE attempts
                    SET finished_at = ?, total_score = ?, max_score = ?
                    WHERE id = ?
                    """,
                    (
                        datetime.now().isoformat(timespec="seconds"),
                        float(total_score),
                        float(max_score),
                        attempt_id,
                    ),
                )
                row = conn.execute("SELECT * FROM attempts WHERE id = ?", (attempt_id,)).fetchone()
                return self._row_to_dict(row)
        except Exception as exc:
            print(f"finish_attempt error: {exc}")
            return {}

    def get_attempts_for_mock(self, mock_id: str) -> list[dict]:
        try:
            with self.connect() as conn:
                rows = conn.execute(
                    "SELECT * FROM attempts WHERE mock_id = ? ORDER BY datetime(started_at) DESC",
                    (mock_id,),
                ).fetchall()
                return [dict(row) for row in rows]
        except Exception as exc:
            print(f"get_attempts_for_mock error: {exc}")
            return []

    def get_all_attempts(self) -> list[dict]:
        try:
            with self.connect() as conn:
                rows = conn.execute(
                    """
                    SELECT attempts.*, mocks.title AS mock_title
                    FROM attempts
                    LEFT JOIN mocks ON mocks.id = attempts.mock_id
                    ORDER BY datetime(attempts.started_at) DESC
                    """
                ).fetchall()
                return [dict(row) for row in rows]
        except Exception as exc:
            print(f"get_all_attempts error: {exc}")
            return []

    def get_attempt(self, attempt_id: str) -> dict:
        try:
            with self.connect() as conn:
                row = conn.execute("SELECT * FROM attempts WHERE id = ?", (attempt_id,)).fetchone()
                return self._row_to_dict(row)
        except Exception as exc:
            print(f"get_attempt error: {exc}")
            return {}

    def mock_exists(self, mock_id: str) -> bool:
        try:
            with self.connect() as conn:
                row = conn.execute("SELECT 1 FROM mocks WHERE id = ?", (mock_id,)).fetchone()
                return row is not None
        except Exception as exc:
            print(f"mock_exists error: {exc}")
            return False

    def attempt_count(self) -> int:
        try:
            with self.connect() as conn:
                row = conn.execute("SELECT COUNT(*) AS count FROM attempts WHERE finished_at IS NOT NULL").fetchone()
                return int(row["count"] if row else 0)
        except Exception as exc:
            print(f"attempt_count error: {exc}")
            return 0

    def question_count(self, mock_id: str) -> int:
        try:
            with self.connect() as conn:
                row = conn.execute("SELECT COUNT(*) AS count FROM questions WHERE mock_id = ?", (mock_id,)).fetchone()
                return int(row["count"] if row else 0)
        except Exception as exc:
            print(f"question_count error: {exc}")
            return 0
