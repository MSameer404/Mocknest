import json
from datetime import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
    QMessageBox,
)

from styles import COLORS
from scoring import calculate_score


class HistoryPage(QWidget):
    def __init__(self, db, navigate_to_analysis, parent=None):
        super().__init__(parent)
        self.db = db
        self.navigate_to_analysis = navigate_to_analysis
        self.search_text = ""
        self.grid = None
        self._build()
        self._load()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(16)

        top = QHBoxLayout()
        heading = QLabel("Attempt History")
        heading.setProperty("role", "heading")
        top.addWidget(heading)
        top.addStretch()
        self.mains_btn = QPushButton("JEE Mains")
        self.mains_btn.setProperty("role", "primary")
        self.mains_btn.setCheckable(True)
        self.mains_btn.setChecked(True)
        self.mains_btn.setMinimumHeight(36)
        
        self.adv_btn = QPushButton("JEE Advanced (Coming Soon)")
        self.adv_btn.setCheckable(True)
        self.adv_btn.setEnabled(False)
        self.adv_btn.setMinimumHeight(36)

        top.addWidget(self.mains_btn)
        top.addWidget(self.adv_btn)
        layout.addLayout(top)

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search attempts by mock title")
        self.search.textChanged.connect(self._on_search)
        layout.addWidget(self.search)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.content = QWidget()
        self.grid = QVBoxLayout(self.content)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(12)
        self.grid.setAlignment(Qt.AlignmentFlag.AlignTop)
        scroll.setWidget(self.content)
        layout.addWidget(scroll, 1)

    def _on_search(self, text):
        self.search_text = text.lower().strip()
        self._load()

    def _clear_grid(self):
        while self.grid.count():
            item = self.grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def _load(self):
        if not hasattr(self, "grid") or self.grid is None:
            return
        self._clear_grid()

        attempts = [attempt for attempt in self.db.get_all_attempts() if attempt.get("finished_at")]
        if self.search_text:
            attempts = [attempt for attempt in attempts if self.search_text in (attempt.get("mock_title") or "").lower()]

        if not attempts:
            empty = QLabel("No attempts found.")
            empty.setProperty("role", "muted")
            self.grid.addWidget(empty)
            return

        for attempt in attempts:
            self.grid.addWidget(self._attempt_card(attempt))

    def _attempt_card(self, attempt: dict):
        card = QFrame()
        card.setProperty("role", "mock-card")
        layout = QHBoxLayout(card)
        layout.setContentsMargins(20, 16, 20, 16)

        info_layout = QVBoxLayout()
        header = QHBoxLayout()
        
        mock_name = attempt.get("mock_title") or "Deleted Mock"
        if len(mock_name) > 50:
            mock_name = mock_name[:47] + "..."
        title = QLabel(mock_name)
        title.setStyleSheet("font-size: 18px; font-weight: 800;")
        title.setWordWrap(False)
        header.addWidget(title)
        header.addStretch()
        info_layout.addLayout(header)

        percent = ((attempt.get("total_score") or 0) / attempt["max_score"] * 100) if attempt.get("max_score") else 0
        
        accuracy_text = "N/A"
        mock_id = attempt.get("mock_id")
        questions = self.db.get_questions(mock_id) if mock_id else []
        if questions:
            mock = self.db.get_mock(mock_id)
            answers = json.loads(attempt.get("answers", "{}"))
            result = calculate_score(
                questions,
                answers,
                mock.get("marks_correct", 4),
                mock.get("marks_incorrect", -1),
            )
            total_attempted = result.correct_count + result.wrong_count
            if total_attempted > 0:
                accuracy_text = f"{(result.correct_count / total_attempted * 100):.1f}%"
        else:
            accuracy_text = f"{percent:.1f}%"
            
        date_text = self._format_date(attempt.get("finished_at") or attempt.get("started_at"))
        duration = self._duration_text(attempt)
        
        details = QLabel(
            f"Date: {date_text} | Accuracy: {accuracy_text} | Percentage: {percent:.1f}% | Time: {duration}"
        )
        details.setProperty("role", "muted")
        info_layout.addWidget(details)
        layout.addLayout(info_layout, 1)

        buttons = QHBoxLayout()
        buttons.setSpacing(8)
        
        badge = QLabel(f"SCORE: {attempt.get('total_score') or 0:g}/{attempt.get('max_score') or 0:g}")
        badge.setStyleSheet(
            f"background-color: #2D1115; color: {COLORS['danger']}; border: 1px solid {COLORS['danger']}; border-radius: 6px; padding: 4px 10px; font-size: 12px; font-weight: 800;"
        )
        
        analyze = QPushButton("Analyze")
        analyze.setProperty("role", "primary")
        analyze.setMinimumHeight(36)
        analyze.clicked.connect(lambda checked=False, att_id=attempt["id"]: self.navigate_to_analysis(att_id))
        
        delete = QPushButton("Delete")
        delete.setProperty("role", "danger")
        delete.setMinimumHeight(36)
        delete.clicked.connect(lambda checked=False, att_id=attempt["id"]: self._delete_attempt(att_id))
        
        buttons.addWidget(badge)
        buttons.addWidget(analyze)
        buttons.addWidget(delete)
        layout.addLayout(buttons)
        return card

    def _delete_attempt(self, attempt_id: str):
        reply = QMessageBox.question(
            self,
            "Delete Attempt",
            "Are you sure you want to delete this test attempt?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.db.delete_attempt(attempt_id)
            self._load()

    def _format_date(self, value):
        try:
            return datetime.fromisoformat(value).strftime("%d %b %Y, %I:%M %p")
        except Exception:
            return value or ""

    def _duration_text(self, attempt):
        try:
            start = datetime.fromisoformat(attempt["started_at"])
            end = datetime.fromisoformat(attempt["finished_at"])
            seconds = max(0, int((end - start).total_seconds()))
            return f"{seconds // 60}m {seconds % 60}s"
        except Exception:
            return "-"
