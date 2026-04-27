import json
from datetime import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
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
        self.filter_combo = QComboBox()
        self.filter_combo.setMinimumWidth(240)
        self.filter_combo.currentIndexChanged.connect(self._load)
        top.addWidget(self.filter_combo)
        layout.addLayout(top)

        self.stats_row = QHBoxLayout()
        layout.addLayout(self.stats_row)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["Date", "Mock Title", "Score", "Percentage", "Duration"])
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.cellClicked.connect(self._open_attempt)
        layout.addWidget(self.table, 1)

        self._populate_filter()

    def _populate_filter(self):
        current = self.filter_combo.currentData()
        self.filter_combo.blockSignals(True)
        self.filter_combo.clear()
        self.filter_combo.addItem("All Mocks", "")
        for mock in self.db.get_all_mocks():
            self.filter_combo.addItem(mock["title"], mock["id"])
        if current:
            index = self.filter_combo.findData(current)
            if index >= 0:
                self.filter_combo.setCurrentIndex(index)
        self.filter_combo.blockSignals(False)

    def _stat_card(self, label, value):
        card = QFrame()
        card.setMinimumHeight(80)
        layout = QVBoxLayout(card)
        title = QLabel(label)
        title.setProperty("role", "muted")
        number = QLabel(value)
        number.setStyleSheet("font-size: 23px; font-weight: 800;")
        layout.addWidget(title)
        layout.addWidget(number)
        return card

    def _clear_stats(self):
        while self.stats_row.count():
            item = self.stats_row.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def _load(self):
        if not hasattr(self, "table"):
            return
        selected_mock = self.filter_combo.currentData() if hasattr(self, "filter_combo") else ""
        attempts = [attempt for attempt in self.db.get_all_attempts() if attempt.get("finished_at")]
        if selected_mock:
            attempts = [attempt for attempt in attempts if attempt.get("mock_id") == selected_mock]

        percentages = [
            ((attempt.get("total_score") or 0) / attempt["max_score"] * 100)
            for attempt in attempts
            if attempt.get("max_score")
        ]
        self._clear_stats()
        total = len(attempts)
        best = max(percentages) if percentages else 0.0
        average = sum(percentages) / len(percentages) if percentages else 0.0
        for label, value in (
            ("Total Attempts", str(total)),
            ("Best Score", f"{best:.1f}%"),
            ("Average Score", f"{average:.1f}%"),
        ):
            self.stats_row.addWidget(self._stat_card(label, value))

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
                self.table.setItem(row, col, item)
        self.table.resizeColumnsToContents()

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
