from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)



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
        
        layout.addStretch()
        
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
        layout.addStretch()

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
