import json
from datetime import datetime

from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import (
    QFileDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from mock_format import export_mock, import_mock
from styles import COLORS


class LibraryPage(QWidget):
    def __init__(self, db, navigate_to_test, navigate_to_creator, refresh_page, parent=None):
        super().__init__(parent)
        self.db = db
        self.navigate_to_test = navigate_to_test
        self.navigate_to_creator = navigate_to_creator
        self.refresh_page = refresh_page
        self.search_text = ""
        self.grid = None
        self.content = None
        self._build()
        self._render_cards()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(16)

        top = QHBoxLayout()
        heading = QLabel("Mock Library")
        heading.setProperty("role", "heading")
        top.addWidget(heading)
        
        top.addStretch()

        import_button = QPushButton("Import Mock")
        import_button.setProperty("role", "success")
        import_button.setMinimumHeight(36)
        import_button.clicked.connect(self._import_mock)
        top.addWidget(import_button)

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
        self.search.setPlaceholderText("Search mocks by title")
        self.search.textChanged.connect(self._on_search)
        layout.addWidget(self.search)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.content = QWidget()
        self.grid = QVBoxLayout(self.content)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(4)
        self.grid.setAlignment(Qt.AlignmentFlag.AlignTop)
        scroll.setWidget(self.content)
        layout.addWidget(scroll, 1)

    def _on_search(self, text):
        self.search_text = text.lower().strip()
        self._render_cards()

    def _clear_grid(self):
        while self.grid.count():
            item = self.grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def _render_cards(self):
        self._clear_grid()
        mocks = self.db.get_all_mocks()
        if self.search_text:
            mocks = [mock for mock in mocks if self.search_text in mock["title"].lower()]
        if not mocks:
            empty = QLabel("No mocks match this view.")
            empty.setProperty("role", "muted")
            self.grid.addWidget(empty, 0, 0)
            return
        for mock in mocks:
            self.grid.addWidget(self._mock_card(mock))

    def _mock_card(self, mock: dict):
        card = QFrame()
        card.setProperty("role", "mock-card")
        layout = QHBoxLayout(card)
        layout.setContentsMargins(20, 16, 20, 16)

        info_layout = QVBoxLayout()
        header = QHBoxLayout()
        title = QLabel(mock["title"])
        title.setStyleSheet("font-size: 18px; font-weight: 800;")
        title.setWordWrap(True)
        badge = QLabel(mock.get("source", "local").upper())
        badge.setStyleSheet(
            f"background-color: {COLORS['accent']}; color: white; border-radius: 6px; padding: 4px 10px; font-size: 11px; font-weight: 800;"
        )
        header.addWidget(title)
        header.addWidget(badge)
        header.addStretch()
        info_layout.addLayout(header)

        sections = ", ".join(json.loads(mock.get("sections", "[]")))
        date_text = mock.get("created_at", "")[:10]
        try:
            date_text = datetime.fromisoformat(mock["created_at"]).strftime("%d %b %Y")
        except Exception:
            date_text = mock.get("created_at", "")[:10]
        question_count = self.db.question_count(mock["id"])
        author = mock.get("author") or "Anonymous"
        details = QLabel(
            f"Creator: {author} | Sections: {sections} | Questions: {question_count} | Duration: {mock['duration_minutes']} min | Created: {date_text}"
        )
        details.setProperty("role", "muted")
        info_layout.addWidget(details)
        layout.addLayout(info_layout, 1)

        buttons = QHBoxLayout()
        buttons.setSpacing(8)
        start = QPushButton("Start Test")
        start.setProperty("role", "primary")
        start.setMinimumHeight(36)
        start.clicked.connect(lambda checked=False, mock_id=mock["id"]: self.navigate_to_test(mock_id))
        export = QPushButton("Export")
        export.setMinimumHeight(36)
        export.clicked.connect(lambda checked=False, mock_id=mock["id"], title=mock["title"]: self._export_mock(mock_id, title))
        delete = QPushButton("Delete")
        delete.setProperty("role", "danger")
        delete.setMinimumHeight(36)
        delete.clicked.connect(lambda checked=False, mock_id=mock["id"]: self._delete_mock(mock_id))
        buttons.addWidget(start)
        buttons.addWidget(export)
        buttons.addWidget(delete)
        layout.addLayout(buttons)
        return card

    def _export_mock(self, mock_id: str, title: str):
        safe_title = "".join(ch if ch.isalnum() or ch in (" ", "-", "_") else "_" for ch in title).strip()
        file_path, _ = QFileDialog.getSaveFileName(self, "Export Mock", f"{safe_title}.jmock", "Mocknest Files (*.jmock)")
        if not file_path:
            return
        if export_mock(self.db, mock_id, file_path):
            QMessageBox.information(self, "Export Complete", "Mock exported as a .jmock file.")
        else:
            QMessageBox.warning(self, "Export Failed", "Could not export this mock.")

    def _import_mock(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Import Mock", "", "Mocknest Files (*.jmock)")
        if not file_path:
            return
        if import_mock(self.db, file_path):
            QMessageBox.information(self, "Import Complete", "Mock imported successfully.")
            self.refresh_page("library")
        else:
            QMessageBox.warning(self, "Import Failed", "Could not import this .jmock file.")

    def _delete_mock(self, mock_id: str):
        reply = QMessageBox.question(
            self,
            "Delete Mock",
            "Delete this mock and all its questions?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.db.delete_mock(mock_id)
            self._render_cards()
