import json

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from styles import BUTTON_DANGER, BUTTON_PRIMARY, CARD_STYLE, COLORS


class AddQuestionsPage(QWidget):
    def __init__(self, db, mock_id: str, navigate_to_library, parent=None):
        super().__init__(parent)
        self.db = db
        self.mock_id = mock_id
        self.mock = db.get_mock(mock_id)
        self.navigate_to_library = navigate_to_library
        self.section_buttons = {}
        self.current_section = ""
        self.question_list_layout = None
        self.count_label = None
        self._build()
        self._refresh()

    def _sections(self):
        try:
            return json.loads(self.mock.get("sections", "[]"))
        except Exception:
            return []

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 20, 28, 20)
        layout.setSpacing(14)

        top = QHBoxLayout()
        title = QLabel(self.mock.get("title", "Add Questions"))
        title.setProperty("role", "heading")
        top.addWidget(title, 1)
        self.count_label = QLabel()
        self.count_label.setProperty("role", "muted")
        top.addWidget(self.count_label)
        done = QPushButton("Done")
        done.setStyleSheet(BUTTON_PRIMARY)
        done.clicked.connect(self.navigate_to_library)
        top.addWidget(done)
        layout.addLayout(top)

        tabs = QHBoxLayout()
        sections = self._sections()
        self.current_section = sections[0] if sections else ""
        for section in sections:
            button = QPushButton(section)
            button.clicked.connect(lambda checked=False, name=section: self._select_section(name))
            self.section_buttons[section] = button
            tabs.addWidget(button)
        tabs.addStretch()
        layout.addLayout(tabs)

        form_card = QFrame()
        form_card.setStyleSheet(CARD_STYLE)
        form_layout = QVBoxLayout(form_card)
        form_layout.setContentsMargins(18, 18, 18, 18)
        form_layout.setSpacing(12)

        row = QHBoxLayout()
        self.type_combo = QComboBox()
        self.type_combo.addItem("Single Correct", "single")
        self.type_combo.addItem("Multiple Correct", "multiple")
        self.type_combo.addItem("Numerical", "numerical")
        self.type_combo.currentIndexChanged.connect(self._sync_type_visibility)
        self.section_combo = QComboBox()
        for section in sections:
            self.section_combo.addItem(section)
        row.addWidget(QLabel("Type:"))
        row.addWidget(self.type_combo)
        row.addWidget(QLabel("Section:"))
        row.addWidget(self.section_combo)
        row.addStretch()
        form_layout.addLayout(row)

        form_layout.addWidget(QLabel("Question Text:"))
        self.question_text = QTextEdit()
        self.question_text.setMinimumHeight(90)
        form_layout.addWidget(self.question_text)

        self.options_widget = QWidget()
        options_grid = QGridLayout(self.options_widget)
        options_grid.setContentsMargins(0, 0, 0, 0)
        self.option_inputs = []
        for index, letter in enumerate(("A", "B", "C", "D")):
            options_grid.addWidget(QLabel(f"{letter}:"), index, 0)
            line = QLineEdit()
            line.setPlaceholderText(f"Option {letter}")
            self.option_inputs.append(line)
            options_grid.addWidget(line, index, 1)
        self.single_correct = QComboBox()
        for letter in ("A", "B", "C", "D"):
            self.single_correct.addItem(letter)
        options_grid.addWidget(QLabel("Correct Answer:"), 0, 2)
        options_grid.addWidget(self.single_correct, 0, 3)
        self.multiple_checks = []
        multi_box = QWidget()
        multi_row = QHBoxLayout(multi_box)
        multi_row.setContentsMargins(0, 0, 0, 0)
        for letter in ("A", "B", "C", "D"):
            check = QCheckBox(letter)
            self.multiple_checks.append(check)
            multi_row.addWidget(check)
        options_grid.addWidget(QLabel("Multiple Correct:"), 1, 2)
        options_grid.addWidget(multi_box, 1, 3)
        form_layout.addWidget(self.options_widget)

        self.numerical_widget = QWidget()
        numerical_row = QHBoxLayout(self.numerical_widget)
        numerical_row.setContentsMargins(0, 0, 0, 0)
        self.numerical_answer = QLineEdit()
        self.numerical_answer.setPlaceholderText("Value")
        tolerance = QLineEdit("±0.01")
        tolerance.setReadOnly(True)
        numerical_row.addWidget(QLabel("Answer Value:"))
        numerical_row.addWidget(self.numerical_answer)
        numerical_row.addWidget(QLabel("Tolerance:"))
        numerical_row.addWidget(tolerance)
        numerical_row.addStretch()
        form_layout.addWidget(self.numerical_widget)

        add = QPushButton("+ Add Question")
        add.setStyleSheet(BUTTON_PRIMARY)
        add.clicked.connect(self._add_question)
        form_layout.addWidget(add)
        layout.addWidget(form_card)

        list_title = QLabel("Added Questions")
        list_title.setProperty("role", "subheading")
        layout.addWidget(list_title)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        list_content = QWidget()
        self.question_list_layout = QVBoxLayout(list_content)
        self.question_list_layout.setContentsMargins(0, 0, 0, 0)
        self.question_list_layout.setSpacing(8)
        scroll.setWidget(list_content)
        layout.addWidget(scroll, 1)
        self._sync_type_visibility()
        self._style_tabs()

    def _style_tabs(self):
        for section, button in self.section_buttons.items():
            active = section == self.current_section
            color = COLORS["accent"] if active else COLORS["bg_secondary"]
            border = COLORS["accent"] if active else COLORS["border"]
            button.setStyleSheet(
                f"background-color: {color}; border: 1px solid {border}; border-radius: 6px; font-weight: 800;"
            )

    def _select_section(self, section):
        self.current_section = section
        index = self.section_combo.findText(section)
        if index >= 0:
            self.section_combo.setCurrentIndex(index)
        self._style_tabs()
        self._refresh()

    def _sync_type_visibility(self):
        qtype = self.type_combo.currentData()
        self.options_widget.setVisible(qtype in ("single", "multiple"))
        self.single_correct.setVisible(qtype == "single")
        for check in self.multiple_checks:
            check.setVisible(qtype == "multiple")
        self.numerical_widget.setVisible(qtype == "numerical")

    def _add_question(self):
        qtype = self.type_combo.currentData()
        section = self.section_combo.currentText()
        text = self.question_text.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "Validation", "Question text is required.")
            return

        options = None
        correct_answer = ""
        if qtype in ("single", "multiple"):
            values = [line.text().strip() for line in self.option_inputs]
            if any(not value for value in values):
                QMessageBox.warning(self, "Validation", "All four options are required for MCQ questions.")
                return
            options = json.dumps([f"{letter}) {value}" for letter, value in zip(("A", "B", "C", "D"), values)])
            if qtype == "single":
                correct_answer = self.single_correct.currentText()
            else:
                selected = [check.text() for check in self.multiple_checks if check.isChecked()]
                if not selected:
                    QMessageBox.warning(self, "Validation", "Select at least one correct option.")
                    return
                correct_answer = json.dumps(selected)
        else:
            correct_answer = self.numerical_answer.text().strip()
            if not correct_answer:
                QMessageBox.warning(self, "Validation", "Numerical answer is required.")
                return

        order_index = len(self.db.get_questions(self.mock_id))
        question_id = self.db.add_question(
            mock_id=self.mock_id,
            section=section,
            type_=qtype,
            text=text,
            options=options,
            correct_answer=correct_answer,
            order_index=order_index,
        )
        if question_id:
            self._clear_form()
            self._refresh()
        else:
            QMessageBox.warning(self, "Save Failed", "Could not add this question.")

    def _clear_form(self):
        self.question_text.clear()
        for line in self.option_inputs:
            line.clear()
        for check in self.multiple_checks:
            check.setChecked(False)
        self.numerical_answer.clear()

    def _refresh(self):
        questions = self.db.get_questions(self.mock_id)
        sections = self._sections()
        counts = {section: 0 for section in sections}
        for question in questions:
            counts[question["section"]] = counts.get(question["section"], 0) + 1
        self.count_label.setText(" | ".join(f"{section}: {counts.get(section, 0)}" for section in sections))

        while self.question_list_layout.count():
            item = self.question_list_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        filtered = [question for question in questions if not self.current_section or question["section"] == self.current_section]
        if not filtered:
            empty = QLabel("No questions added in this section yet.")
            empty.setProperty("role", "muted")
            self.question_list_layout.addWidget(empty)
        for index, question in enumerate(filtered, start=1):
            self.question_list_layout.addWidget(self._question_row(index, question))
        self.question_list_layout.addStretch()

    def _question_row(self, index: int, question: dict):
        card = QFrame()
        card.setStyleSheet(CARD_STYLE)
        row = QHBoxLayout(card)
        badge = QLabel(question["type"].upper())
        badge.setStyleSheet(
            f"background-color: {COLORS['accent']}; color: white; border-radius: 4px; padding: 4px 7px; font-weight: 800;"
        )
        text = question["text"][:60] + ("..." if len(question["text"]) > 60 else "")
        label = QLabel(f"{index}. {text}")
        label.setWordWrap(True)
        delete = QPushButton("Delete")
        delete.setStyleSheet(BUTTON_DANGER)
        delete.clicked.connect(lambda checked=False, qid=question["id"]: self._delete_question(qid))
        row.addWidget(badge)
        row.addWidget(label, 1)
        row.addWidget(delete)
        return card

    def _delete_question(self, question_id: str):
        self.db.delete_question(question_id)
        self._refresh()
