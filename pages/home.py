import json

from PyQt6.QtWidgets import (
    QFileDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from mock_format import import_mock
from styles import COLORS


class HomePage(QWidget):
    def __init__(self, db, navigate_to_test, refresh_page, parent=None):
        super().__init__(parent)
        self.db = db
        self.navigate_to_test = navigate_to_test
        self.refresh_page = refresh_page
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(20)

        top = QHBoxLayout()
        heading = QLabel("Ready to Practice?")
        heading.setProperty("role", "heading")
        top.addWidget(heading)
        top.addStretch()
        import_button = QPushButton("Quick Import")
        import_button.setProperty("role", "primary")
        import_button.clicked.connect(self._import_mock)
        top.addWidget(import_button)
        layout.addLayout(top)

        stats = QHBoxLayout()
        mocks = self.db.get_all_mocks()
        attempts = [attempt for attempt in self.db.get_all_attempts() if attempt.get("finished_at")]
        best = 0.0
        for attempt in attempts:
            if attempt.get("max_score"):
                best = max(best, (attempt.get("total_score") or 0) / attempt["max_score"] * 100)
        for label, value in (
            ("Total Mocks", str(len(mocks))),
            ("Tests Taken", str(len(attempts))),
            ("Best Score", f"{best:.1f}%"),
        ):
            stats.addWidget(self._stat_card(label, value))
        layout.addLayout(stats)

        section = QLabel("Recent Mocks")
        section.setProperty("role", "subheading")
        layout.addWidget(section)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        grid = QGridLayout(content)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(16)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(2, 1)

        recent = mocks[:6]
        if not recent:
            empty = QLabel("No mocks yet. Create a mock or import a .jmock file to begin.")
            empty.setProperty("role", "muted")
            grid.addWidget(empty, 0, 0)
        for index, mock in enumerate(recent):
            grid.addWidget(self._mock_card(mock), index // 3, index % 3)

        scroll.setWidget(content)
        layout.addWidget(scroll, 1)

    def _stat_card(self, label: str, value: str):
        card = QFrame()
        card.setMinimumHeight(100)
        layout = QVBoxLayout(card)
        title = QLabel(label)
        title.setProperty("role", "muted")
        number = QLabel(value)
        number.setStyleSheet("font-size: 30px; font-weight: 800;")
        layout.addWidget(title)
        layout.addWidget(number)
        return card

    def _mock_card(self, mock: dict):
        card = QFrame()
        card.setMinimumHeight(165)
        layout = QVBoxLayout(card)
        title = QLabel(mock["title"])
        title.setStyleSheet("font-size: 18px; font-weight: 800;")
        title.setWordWrap(True)
        layout.addWidget(title)

        sections = ", ".join(json.loads(mock.get("sections", "[]")))
        question_count = self.db.question_count(mock["id"])
        details = QLabel(f"{question_count} questions · {mock['duration_minutes']} min\n{sections}")
        details.setProperty("role", "muted")
        layout.addWidget(details)
        layout.addStretch()

        button = QPushButton("Start Test")
        button.setProperty("role", "primary")
        button.clicked.connect(lambda checked=False, mock_id=mock["id"]: self.navigate_to_test(mock_id))
        layout.addWidget(button)
        return card

    def _import_mock(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Import Mock", "", "Mocknest Files (*.jmock)")
        if not file_path:
            return
        mock_id = import_mock(self.db, file_path)
        if mock_id:
            QMessageBox.information(self, "Import Complete", "Mock imported successfully.")
            self.refresh_page("home")
        else:
            QMessageBox.warning(self, "Import Failed", "Could not import this .jmock file.")
