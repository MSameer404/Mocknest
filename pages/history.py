import json
from datetime import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QHeaderView,
)



class HistoryPage(QWidget):
    def __init__(self, db, navigate_to_analysis, parent=None):
        super().__init__(parent)
        self.db = db
        self.navigate_to_analysis = navigate_to_analysis
        self.attempt_ids = []
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

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["Date", "Mock Title", "Score", "Percentage", "Duration"])
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setMinimumHeight(45)
        self.table.verticalHeader().setDefaultSectionSize(45)
        self.table.cellClicked.connect(self._open_attempt)
        layout.addWidget(self.table, 1)

    def _load(self):
        if not hasattr(self, "table"):
            return
        attempts = [attempt for attempt in self.db.get_all_attempts() if attempt.get("finished_at")]

        self.table.setRowCount(len(attempts))
        self.attempt_ids = []
        for row, attempt in enumerate(attempts):
            self.attempt_ids.append(attempt["id"])
            percent = ((attempt.get("total_score") or 0) / attempt["max_score"] * 100) if attempt.get("max_score") else 0
            duration = self._duration_text(attempt)
            values = [
                self._format_date(attempt.get("finished_at") or attempt.get("started_at")),
                attempt.get("mock_title") or "Deleted Mock",
                f"{attempt.get('total_score') or 0:g} / {attempt.get('max_score') or 0:g}",
                f"{percent:.1f}%",
                duration,
            ]
            for col, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                if col == 1:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                else:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, col, item)

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

    def _open_attempt(self, row, column):
        if 0 <= row < len(self.attempt_ids):
            self.navigate_to_analysis(self.attempt_ids[row])
