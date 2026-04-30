import json

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox,
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

from components.question_palette import QuestionPalette
from components.rich_editor import RichEditor
from styles import COLORS


class AddQuestionsPage(QWidget):
    def __init__(self, db, mock_id: str, navigate_to_library, parent=None):
        super().__init__(parent)
        self.db = db
        self.mock_id = mock_id
        self.mock = db.get_mock(mock_id)
        self.navigate_to_library = navigate_to_library
        self.questions = db.get_questions(mock_id)
        
        self.current_index = None
        self.question_states = {}
        for q in self.questions:
            status = "answered" if q.get("text", "").strip() else "not_answered"
            self.question_states[q["id"]] = {"status": status}
            
        self.section_buttons = {}
        self.section_positions = {}
        for idx, q in enumerate(self.questions):
            self.section_positions.setdefault(q["section"], idx)

        self.palette = None
        self._build()
        if self.questions:
            self._enter_question(0)

    def _sections(self):
        try:
            return json.loads(self.mock.get("sections", "[]"))
        except Exception:
            return []

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(12)

        header = QHBoxLayout()
        title = QLabel(self.mock.get("title", "Add Questions"))
        title.setStyleSheet("font-size: 22px; font-weight: 900;")
        header.addWidget(title)
        header.addStretch()
        
        exit_btn = QPushButton("Exit without Save")
        exit_btn.setProperty("role", "danger")
        exit_btn.clicked.connect(self._handle_exit_without_save)
        header.addWidget(exit_btn)

        done = QPushButton("Done")
        done.setProperty("role", "primary")
        done.clicked.connect(self._handle_done)
        header.addWidget(done)
        layout.addLayout(header)

        body = QHBoxLayout()
        body.setSpacing(14)
        
        left_scroll = QScrollArea()
        left_scroll.setWidgetResizable(True)
        left_scroll.setFrameShape(QFrame.Shape.NoFrame)
        
        left = QFrame()
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(16, 16, 16, 16)
        left_layout.setSpacing(12)
        
        meta_row = QHBoxLayout()
        self.meta_section = QLabel("Section: ")
        self.meta_section.setStyleSheet("font-weight: bold; color: " + COLORS['accent'])
        self.meta_type = QLabel("Type: ")
        self.meta_type.setStyleSheet("font-weight: bold;")
        meta_row.addWidget(self.meta_section)
        meta_row.addStretch()
        meta_row.addWidget(self.meta_type)
        left_layout.addLayout(meta_row)
        
        left_layout.addWidget(QLabel("Question Text (Live Preview Below):"))
        self.question_text = RichEditor("Enter question text here. Use $$...$$ for LaTeX.", 140)
        left_layout.addWidget(self.question_text)

        self.options_widget = QWidget()
        options_grid = QGridLayout(self.options_widget)
        options_grid.setContentsMargins(0, 0, 0, 0)
        self.option_inputs = []
        for index, letter in enumerate(("A", "B", "C", "D")):
            options_grid.addWidget(QLabel(f"{letter}:"), index, 0, Qt.AlignmentFlag.AlignTop)
            editor = RichEditor(f"Option {letter}", 80)
            self.option_inputs.append(editor)
            options_grid.addWidget(editor, index, 1)
        left_layout.addWidget(self.options_widget)
        
        self.mcq_ans_widget = QWidget()
        mcq_ans_layout = QHBoxLayout(self.mcq_ans_widget)
        mcq_ans_layout.setContentsMargins(0, 0, 0, 0)
        self.single_correct = QComboBox()
        for letter in ("A", "B", "C", "D"):
            self.single_correct.addItem(letter)
        mcq_ans_layout.addWidget(QLabel("Correct Answer:"))
        mcq_ans_layout.addWidget(self.single_correct)
        
        self.numerical_widget = QWidget()
        numerical_row = QHBoxLayout(self.numerical_widget)
        numerical_row.setContentsMargins(0, 0, 0, 0)
        self.numerical_answer = QLineEdit()
        self.numerical_answer.setPlaceholderText("Value")
        tolerance = QLineEdit("±0.01")
        tolerance.setReadOnly(True)
        tolerance.setFixedWidth(60)
        numerical_row.addWidget(QLabel("Answer Value:"))
        numerical_row.addWidget(self.numerical_answer)
        numerical_row.addWidget(QLabel("Tolerance:"))
        numerical_row.addWidget(tolerance)
        
        action_row = QHBoxLayout()
        action_row.addWidget(self.mcq_ans_widget)
        action_row.addWidget(self.numerical_widget)
        action_row.addStretch()
        
        self.lock_btn = QPushButton("🔒 Lock Question")
        self.lock_btn.clicked.connect(self._toggle_lock)
        action_row.addWidget(self.lock_btn)
        
        self.clear_btn = QPushButton("Clear Question")
        self.clear_btn.clicked.connect(self._clear_question)
        action_row.addWidget(self.clear_btn)

        self.preview_btn = QPushButton("👁️ Preview Question")
        self.preview_btn.clicked.connect(self._preview_question)
        action_row.addWidget(self.preview_btn)
        
        self.save_btn = QPushButton("Save Question")
        self.save_btn.setProperty("role", "primary")
        self.save_btn.clicked.connect(self._save_question)
        action_row.addWidget(self.save_btn)
        left_layout.addLayout(action_row)
        
        left_layout.addStretch()
        left_scroll.setWidget(left)
        body.addWidget(left_scroll, 1)

        right = QFrame()
        right.setFixedWidth(270)
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(0, 0, 0, 0)
        self.palette = QuestionPalette(self.questions)
        self.palette.question_selected.connect(self._enter_question)
        self.palette.sync_states(self.question_states)
        right_layout.addWidget(self.palette)
        body.addWidget(right)

        layout.addLayout(body, 1)

    def _go_to_section(self, section: str):
        if section in self.section_positions:
            self._enter_question(self.section_positions[section])

    def _enter_question(self, index: int):
        if index < 0 or index >= len(self.questions):
            return
        self.current_index = index
        question = self.questions[index]
        
        self.meta_section.setText(f"Section: {question['section']}")
        qtype_label = "Single Correct (MCQ)" if question["type"] == "single" else "Numerical"
        self.meta_type.setText(f"Type: {qtype_label}")
        
        self.options_widget.setVisible(question["type"] == "single")
        self.mcq_ans_widget.setVisible(question["type"] == "single")
        self.numerical_widget.setVisible(question["type"] == "numerical")

        is_locked = bool(question.get("locked", 0))
        self.lock_btn.setText("🔓 Unlock" if is_locked else "🔒 Lock")
        
        self.question_text.setEnabled(not is_locked)
        for line in self.option_inputs:
            line.setEnabled(not is_locked)
        self.single_correct.setEnabled(not is_locked)
        self.numerical_answer.setEnabled(not is_locked)
        
        self.clear_btn.setEnabled(not is_locked)
        self.save_btn.setEnabled(not is_locked)
        
        self.question_text.setText(question.get("text", ""))
        
        if question["type"] == "single":
            options = []
            try:
                options = json.loads(question.get("options", "[]")) or []
            except:
                pass
            for i, line in enumerate(self.option_inputs):
                if i < len(options):
                    val = options[i]
                    if val.startswith(f"{chr(65+i)}) "):
                        val = val[3:]
                    line.setText(val)
                else:
                    line.clear()
            
            correct = question.get("correct_answer", "")
            idx = self.single_correct.findText(correct)
            if idx >= 0:
                self.single_correct.setCurrentIndex(idx)
        else:
            self.numerical_answer.setText(question.get("correct_answer", ""))
            
        self.palette.set_current(question["id"])
        
        for section, btn in self.section_buttons.items():
            active = section == question["section"]
            btn.setProperty("active", "true" if active else "false")
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    def _toggle_lock(self):
        if self.current_index is None:
            return
        question = self.questions[self.current_index]
        is_locked = not bool(question.get("locked", 0))
        
        self.db.lock_question(question["id"], is_locked)
        question["locked"] = 1 if is_locked else 0
        
        self._enter_question(self.current_index)

    def _clear_question(self):
        self.question_text.clear()
        for line in self.option_inputs:
            line.clear()
        self.numerical_answer.clear()
        self._save_question()

    def _save_question(self):
        if self.current_index is None:
            return
            
        question = self.questions[self.current_index]
        text = self.question_text.toPlainText().strip()
        
        options_json = None
        correct_answer = ""
        
        if question["type"] == "single":
            if text:
                values = []
                for i, letter in enumerate(("A", "B", "C", "D")):
                    val = self.option_inputs[i].toPlainText().strip()
                    if not val:
                        val = f"Option {letter}"
                    values.append(val)
                options_json = json.dumps([f"{letter}) {value}" for letter, value in zip(("A", "B", "C", "D"), values)])
                correct_answer = self.single_correct.currentText()
        else:
            if text:
                correct_answer = self.numerical_answer.text().strip()
                if not correct_answer:
                    QMessageBox.warning(self, "Validation", "Numerical answer is required.")
                    return
                    
        self.db.update_question(question["id"], text, options_json, correct_answer)
        
        question["text"] = text
        question["options"] = options_json
        question["correct_answer"] = correct_answer
        
        status = "answered" if text else "not_answered"
        self.question_states[question["id"]]["status"] = status
        self.palette.update_status(question["id"], status)
        self.palette.update_section_summary(self.question_states)

    def _preview_question(self):
        if self.current_index is None:
            return
            
        question = self.questions[self.current_index]
        text = self.question_text.toPlainText().strip()
        
        preview_q = {
            "id": question["id"],
            "mock_id": question["mock_id"],
            "section": question["section"],
            "type": question["type"],
            "text": text or "No question text entered yet.",
            "locked": question.get("locked", 0)
        }
        
        if question["type"] == "single":
            values = []
            for i, letter in enumerate(("A", "B", "C", "D")):
                val = self.option_inputs[i].toPlainText().strip()
                if not val:
                    val = f"Option {letter}"
                values.append(val)
            preview_q["options"] = [f"{letter}) {value}" for letter, value in zip(("A", "B", "C", "D"), values)]
        else:
            preview_q["options"] = None
            
        from PyQt6.QtWidgets import QDialog, QVBoxLayout
        from components.question_card import QuestionCard
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Question Preview")
        dialog.resize(800, 500)
        
        dlg_layout = QVBoxLayout(dialog)
        dlg_layout.setContentsMargins(10, 10, 10, 10)
        
        q_card = QuestionCard(dialog)
        q_card.set_question(preview_q, self.current_index)
        dlg_layout.addWidget(q_card)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(dialog.accept)
        dlg_layout.addWidget(close_btn)
        
        dialog.exec()

    def _handle_exit_without_save(self):
        reply = QMessageBox.question(
            self,
            "Exit Without Saving?",
            "Are you sure you want to exit? Unsaved changes to the current question will be lost.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.navigate_to_library()

    def _handle_done(self):
        empty_count = sum(1 for state in self.question_states.values() if state["status"] == "not_answered")
        if empty_count > 0:
            QMessageBox.warning(
                self, 
                "Incomplete Mock", 
                f"You still have {empty_count} empty question spots. Please fill or clear all spots before finishing."
            )
            return
        self.navigate_to_library()
