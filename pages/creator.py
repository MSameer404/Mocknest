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

        heading = QLabel("Create Mock")
        heading.setProperty("role", "heading")
        layout.addWidget(heading)

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

        self.duration_combo = QComboBox()
        for duration in (60, 90, 120, 180, 210):
            self.duration_combo.addItem(f"{duration} min", duration)
        self.duration_combo.setCurrentIndex(3)
        form.addRow("Duration:", self.duration_combo)

        marking_row = QHBoxLayout()
        self.correct_spin = QDoubleSpinBox()
        self.correct_spin.setRange(0, 20)
        self.correct_spin.setValue(4)
        self.correct_spin.setPrefix("+")
        self.correct_spin.setDecimals(2)
        self.incorrect_spin = QDoubleSpinBox()
        self.incorrect_spin.setRange(-20, 0)
        self.incorrect_spin.setValue(-1)
        self.incorrect_spin.setDecimals(2)
        marking_row.addWidget(QLabel("Correct"))
        marking_row.addWidget(self.correct_spin)
        marking_row.addWidget(QLabel("Incorrect"))
        marking_row.addWidget(self.incorrect_spin)
        form.addRow("Marking:", marking_row)

        sections_row = QHBoxLayout()
        self.section_checks = []
        for section in ("Physics", "Chemistry", "Maths"):
            check = QCheckBox(section)
            check.setChecked(True)
            self.section_checks.append(check)
            sections_row.addWidget(check)
        sections_row.addStretch()
        form.addRow("Sections:", sections_row)

        form_layout.addLayout(form)
        submit = QPushButton("Create Mock & Add Questions")
        submit.setProperty("role", "primary")
        submit.clicked.connect(self._create_mock)
        form_layout.addWidget(submit)
        layout.addWidget(card)
        layout.addStretch()

    def _create_mock(self):
        title = self.title_input.text().strip()
        sections = [check.text() for check in self.section_checks if check.isChecked()]
        if not title:
            QMessageBox.warning(self, "Validation", "Mock title is required.")
            return
        if not sections:
            QMessageBox.warning(self, "Validation", "Select at least one section.")
            return
        mock_id = self.db.create_mock(
            title=title,
            duration=self.duration_combo.currentData(),
            marks_correct=self.correct_spin.value(),
            marks_incorrect=self.incorrect_spin.value(),
            sections=sections,
        )
        if mock_id:
            self.navigate_to_add_questions(mock_id)
        else:
            QMessageBox.warning(self, "Create Failed", "Could not create the mock.")
