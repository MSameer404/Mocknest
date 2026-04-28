from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFileDialog,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from mock_format import export_mock
from styles import COLORS



class CreatorPage(QWidget):
    def __init__(self, db, navigate_to_add_questions, parent=None):
        super().__init__(parent)
        self.db = db
        self.navigate_to_add_questions = navigate_to_add_questions
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(18)

        heading_layout = QHBoxLayout()
        heading_layout.addStretch()
        heading = QLabel("Create Mock")
        heading.setProperty("role", "heading")
        heading_layout.addWidget(heading)
        heading_layout.addStretch()
        layout.addLayout(heading_layout)
        
        warning_lbl = QLabel("⚠️ WARNING: This section is for test creators only. Please stay away if you are not a creator!")
        warning_lbl.setStyleSheet(f"color: {COLORS['danger']}; font-weight: bold; font-size: 14px; background-color: #2A1015; padding: 12px; border: 1px solid {COLORS['danger']}; border-radius: 6px;")
        warning_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(warning_lbl)
        
        center_row = QHBoxLayout()
        center_row.addStretch()

        card = QFrame()
        card.setMaximumWidth(720)
        form_layout = QVBoxLayout(card)
        form_layout.setContentsMargins(24, 24, 24, 24)
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form.setHorizontalSpacing(18)
        form.setVerticalSpacing(16)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Mock title")
        form.addRow("Mock Title:", self.title_input)

        self.author_input = QLineEdit()
        self.author_input.setPlaceholderText("Creator name")
        form.addRow("Creator Name:", self.author_input)

        self.exam_combo = QComboBox()
        self.exam_combo.addItem("JEE Main")
        self.exam_combo.addItem("JEE Advanced (Coming soon)")
        # Disable the JEE Advanced option so it's view-only
        self.exam_combo.model().item(1).setEnabled(False)
        self.exam_combo.currentIndexChanged.connect(self._toggle_submit)
        form.addRow("Exam:", self.exam_combo)

        info_label = QLabel("Format: JEE Mains (180 mins, +4/-1, 75 spots)")
        info_label.setProperty("role", "muted")
        info_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        form.addRow(info_label)

        form_layout.addLayout(form)
        self.submit = QPushButton("Create Mock & Add Questions")
        self.submit.setProperty("role", "primary")
        self.submit.clicked.connect(self._create_mock)
        form_layout.addWidget(self.submit)
        
        center_row.addWidget(card)
        center_row.addStretch()
        layout.addLayout(center_row)

        tests_heading = QLabel("Your Created Tests")
        tests_heading.setProperty("role", "heading")
        tests_heading.setStyleSheet("font-size: 18px; margin-top: 10px;")
        layout.addWidget(tests_heading)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.tests_widget = QWidget()
        self.tests_layout = QVBoxLayout(self.tests_widget)
        self.tests_layout.setContentsMargins(0, 0, 0, 0)
        self.tests_layout.setSpacing(10)
        self.tests_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        scroll.setWidget(self.tests_widget)
        layout.addWidget(scroll, 1)

        self._render_tests()

    def _toggle_submit(self):
        is_advanced = self.exam_combo.currentText().startswith("JEE Advanced")
        self.submit.setDisabled(is_advanced)
        if is_advanced:
            self.submit.setText("Coming Soon")
        else:
            self.submit.setText("Create Mock & Add Questions")

    def _create_mock(self):
        title = self.title_input.text().strip()
        author = self.author_input.text().strip() or "Anonymous"
        if not title:
            QMessageBox.warning(self, "Validation", "Mock title is required.")
            return
        mock_id = self.db.create_mock(
            title=title,
            author=author
        )
        if mock_id:
            self.db.prefill_jee_main_questions(mock_id)
            self.navigate_to_add_questions(mock_id)
        else:
            QMessageBox.warning(self, "Create Failed", "Could not create the mock.")

    def _render_tests(self):
        while self.tests_layout.count():
            item = self.tests_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        mocks = [m for m in self.db.get_all_mocks() if m.get("source", "local") == "local"]
        if not mocks:
            empty = QLabel("No created tests found.")
            empty.setProperty("role", "muted")
            self.tests_layout.addWidget(empty)
            return

        for mock in mocks:
            card = QFrame()
            card.setProperty("role", "mock-card")
            card_layout = QHBoxLayout(card)
            card_layout.setContentsMargins(20, 16, 20, 16)

            mock_name = mock["title"]
            if len(mock_name) > 50:
                mock_name = mock_name[:47] + "..."
            title = QLabel(mock_name)
            title.setStyleSheet("font-size: 16px; font-weight: 800;")
            title.setWordWrap(False)
            card_layout.addWidget(title)
            card_layout.addStretch()

            buttons = QHBoxLayout()
            buttons.setSpacing(8)

            edit = QPushButton("Edit")
            edit.setProperty("role", "primary")
            edit.setMinimumHeight(32)
            edit.clicked.connect(lambda checked=False, mock_id=mock["id"]: self._edit_mock(mock_id))

            export = QPushButton("Export")
            export.setMinimumHeight(32)
            export.clicked.connect(lambda checked=False, mock_id=mock["id"], t=mock["title"]: self._export_mock(mock_id, t))

            delete = QPushButton("Delete")
            delete.setProperty("role", "danger")
            delete.setMinimumHeight(32)
            delete.clicked.connect(lambda checked=False, mock_id=mock["id"]: self._delete_mock(mock_id))

            buttons.addWidget(edit)
            buttons.addWidget(export)
            buttons.addWidget(delete)
            card_layout.addLayout(buttons)

            self.tests_layout.addWidget(card)

    def _edit_mock(self, mock_id: str):
        self.navigate_to_add_questions(mock_id)

    def _export_mock(self, mock_id: str, title: str):
        safe_title = "".join(ch if ch.isalnum() or ch in (" ", "-", "_") else "_" for ch in title).strip()
        file_path, _ = QFileDialog.getSaveFileName(self, "Export Mock", f"{safe_title}.jmock", "Mocknest Files (*.jmock)")
        if not file_path:
            return
        if export_mock(self.db, mock_id, file_path):
            QMessageBox.information(self, "Export Complete", "Mock exported as a .jmock file.")
        else:
            QMessageBox.warning(self, "Export Failed", "Could not export this mock.")

    def _delete_mock(self, mock_id: str):
        reply = QMessageBox.question(
            self,
            "Delete Mock",
            "Delete this mock and all its questions?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.db.delete_mock(mock_id)
            self._render_tests()
