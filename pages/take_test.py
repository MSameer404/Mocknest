import json
import time

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from components.question_card import QuestionCard
from components.question_palette import QuestionPalette
from components.timer_widget import TimerWidget
from scoring import calculate_score
from styles import BUTTON_DANGER, BUTTON_PRIMARY, CARD_STYLE, COLORS


class TakeTestPage(QWidget):
    def __init__(self, db, mock_id: str, navigate_to_analysis, parent=None):
        super().__init__(parent)
        self.db = db
        self.mock_id = mock_id
        self.navigate_to_analysis = navigate_to_analysis
        self.mock = db.get_mock(mock_id)
        self.questions = db.get_questions(mock_id)
        self.attempt_id = ""
        self.question_states = {}
        self.current_index = None
        self.current_section = ""
        self.section_positions = {}
        self.section_buttons = {}
        self.question_enter_time = None
        self.submitted = False
        self.question_card = None
        self.palette = None
        self.timer_widget = None
        self.prev_button = None
        self.next_button = None
        self._build()

    def _sections(self):
        try:
            return json.loads(self.mock.get("sections", "[]"))
        except Exception:
            return []

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(12)

        if not self.mock:
            message = QLabel("Mock not found.")
            message.setProperty("role", "heading")
            layout.addWidget(message)
            return
        if not self.questions:
            message = QLabel("This mock has no questions yet.")
            message.setProperty("role", "heading")
            layout.addWidget(message)
            return

        self.attempt_id = self.db.start_attempt(self.mock_id)
        for index, question in enumerate(self.questions):
            self.question_states[question["id"]] = {
                "status": "not_visited",
                "answer": None,
                "time_spent": 0,
                "marked_for_review": False,
            }
            self.section_positions.setdefault(question["section"], index)

        header = QHBoxLayout()
        title = QLabel(self.mock["title"])
        title.setStyleSheet("font-size: 22px; font-weight: 900;")
        header.addWidget(title)
        header.addStretch()

        for section in self._sections():
            button = QPushButton(section)
            button.clicked.connect(lambda checked=False, name=section: self._go_to_section(name))
            self.section_buttons[section] = button
            header.addWidget(button)

        palette_info = QPushButton("ℹ")
        palette_info.setFixedSize(32, 32)
        palette_info.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['bg_secondary']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
                font-size: 14px;
                font-weight: 700;
            }}
            QPushButton:hover {{
                border-color: {COLORS['accent']};
                background-color: {COLORS['bg_card']};
            }}
        """)
        palette_info.setToolTip("Question Palette Info")
        palette_info.clicked.connect(self._show_palette_info)
        header.addWidget(palette_info)

        self.timer_widget = TimerWidget()
        self.timer_widget.set_duration(self.mock["duration_minutes"])
        self.timer_widget.time_up.connect(self._auto_submit)
        header.addWidget(self.timer_widget)
        layout.addLayout(header)

        body = QHBoxLayout()
        body.setSpacing(14)
        left = QFrame()
        left.setStyleSheet(CARD_STYLE)
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(16, 16, 16, 16)
        left_layout.setSpacing(12)
        self.question_card = QuestionCard()
        left_layout.addWidget(self.question_card, 1)

        action_row = QHBoxLayout()
        self.mark_button = QPushButton("Mark for Review & Next")
        self.mark_button.clicked.connect(self._mark_review_next)
        self.clear_button = QPushButton("Clear Response")
        self.clear_button.clicked.connect(self._clear_response)
        self.save_button = QPushButton("Save & Next")
        self.save_button.setStyleSheet(BUTTON_PRIMARY)
        self.save_button.clicked.connect(self._save_next)
        action_row.addWidget(self.mark_button)
        action_row.addWidget(self.clear_button)
        action_row.addStretch()
        action_row.addWidget(self.save_button)
        left_layout.addLayout(action_row)

        nav_row = QHBoxLayout()
        self.prev_button = QPushButton("◄ Prev")
        self.prev_button.clicked.connect(self._previous_question)
        self.next_button = QPushButton("Next ►")
        self.next_button.clicked.connect(self._next_question)
        nav_row.addWidget(self.prev_button)
        nav_row.addStretch()
        nav_row.addWidget(self.next_button)
        left_layout.addLayout(nav_row)
        body.addWidget(left, 1)

        right = QFrame()
        right.setFixedWidth(270)
        right.setStyleSheet(CARD_STYLE)
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(0, 0, 0, 0)
        self.palette = QuestionPalette(self.questions)
        self.palette.question_selected.connect(lambda index: self._enter_question(index, save_current=True))
        right_layout.addWidget(self.palette)
        body.addWidget(right)
        layout.addLayout(body, 1)

        submit = QPushButton("Submit Test")
        submit.setStyleSheet(BUTTON_DANGER)
        submit.clicked.connect(lambda checked=False: self._submit(auto=False))
        layout.addWidget(submit)

        self._enter_question(0, save_current=False)
        self.timer_widget.start()

    def _show_palette_info(self):
        from styles import PALETTE

        dialog = QDialog(self)
        dialog.setWindowTitle("Question Palette Legend")
        dialog.setMinimumWidth(260)
        dialog.setStyleSheet(f"background-color: {COLORS['bg_primary']}; color: {COLORS['text_primary']};")

        layout = QVBoxLayout(dialog)
        layout.setSpacing(12)

        legend_title = QLabel("Legend")
        legend_title.setStyleSheet("font-weight: 700; font-size: 16px;")
        layout.addWidget(legend_title)

        for key, label_text in (
            ("not_visited", "Not Visited"),
            ("not_answered", "Not Answered"),
            ("answered", "Answered"),
            ("marked_review", "Marked Review"),
            ("answered_marked", "Ans+Marked"),
        ):
            row = QHBoxLayout()
            swatch = QLabel()
            swatch.setFixedSize(14, 14)
            swatch.setStyleSheet(f"background-color: {PALETTE[key]}; border-radius: 3px;")
            row.addWidget(swatch)
            label = QLabel(label_text)
            row.addWidget(label)
            row.addStretch()
            layout.addLayout(row)

        layout.addSpacing(16)

        summary_title = QLabel("Progress")
        summary_title.setStyleSheet("font-weight: 700; font-size: 16px;")
        layout.addWidget(summary_title)

        summary = QLabel(self.palette.get_summary_text())
        summary.setStyleSheet(f"color: {COLORS['text_secondary']};")
        layout.addWidget(summary)

        close_btn = QPushButton("Close")
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent']};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: 700;
            }}
            QPushButton:hover {{
                background-color: {COLORS['accent_hover']};
            }}
        """)
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)

        dialog.exec()

    def _style_section_tabs(self):
        for section, button in self.section_buttons.items():
            active = section == self.current_section
            section_colors = {"Physics": "#E74C3C", "Chemistry": "#3498DB", "Math": "#27AE60", "Mathematics": "#27AE60"}
            section_color = section_colors.get(section, COLORS["accent"])
            bg = section_color if active else COLORS["bg_secondary"]
            border = section_color if active else COLORS["border"]
            button.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: {bg};
                    border: 2px solid {border};
                    border-radius: 6px;
                    font-weight: 800;
                    padding: 4px 12px;
                }}
                QPushButton:hover {{
                    border-color: {section_color};
                    background-color: {COLORS['bg_card']};
                }}
                """
            )

    def _record_current_question(self, mode: str = "preserve"):
        if self.current_index is None or not self.questions:
            return
        question = self.questions[self.current_index]
        question_id = question["id"]
        state = self.question_states[question_id]
        if self.question_enter_time is not None:
            elapsed = int(time.monotonic() - self.question_enter_time)
            state["time_spent"] += max(0, elapsed)
        answer = None if mode == "clear" else self.question_card.get_answer()
        if answer == []:
            answer = None

        if mode == "save":
            state["marked_for_review"] = False
            state["status"] = "answered" if answer is not None else "not_answered"
        elif mode == "mark":
            state["marked_for_review"] = True
            state["status"] = "answered_marked" if answer is not None else "marked_review"
        elif mode == "clear":
            state["marked_for_review"] = False
            state["status"] = "not_answered"
        else:
            if answer is not None:
                state["status"] = "answered_marked" if state["marked_for_review"] else "answered"
            else:
                state["status"] = "marked_review" if state["marked_for_review"] else "not_answered"

        state["answer"] = answer
        self.db.save_answer(
            self.attempt_id,
            question_id,
            state["answer"],
            state["time_spent"],
            state["marked_for_review"],
        )
        self.palette.update_status(question_id, state["status"])
        self.palette.update_section_summary(self.question_states)
        self.question_enter_time = time.monotonic()

    def _enter_question(self, index: int, save_current: bool):
        if index < 0 or index >= len(self.questions):
            return
        if save_current:
            self._record_current_question("preserve")
        self.current_index = index
        question = self.questions[index]
        self.current_section = question["section"]
        self.section_positions[self.current_section] = index
        state = self.question_states[question["id"]]
        if state["status"] == "not_visited":
            state["status"] = "not_answered"
            self.db.save_answer(self.attempt_id, question["id"], None, state["time_spent"], False)
        self.question_card.set_question(question, index)
        self.question_card.set_answer(state["answer"])
        self.palette.sync_states(self.question_states)
        self.palette.set_current(question["id"])
        self._style_section_tabs()
        self._sync_nav_buttons()
        self.question_enter_time = time.monotonic()

    def _sync_nav_buttons(self):
        self.prev_button.setEnabled((self.current_index or 0) > 0)
        self.next_button.setEnabled((self.current_index or 0) < len(self.questions) - 1)

    def _go_to_section(self, section: str):
        indices = [index for index, question in enumerate(self.questions) if question["section"] == section]
        if not indices:
            return
        target = self.section_positions.get(section, indices[0])
        if target not in indices:
            target = indices[0]
        self._enter_question(target, save_current=True)

    def _next_question(self):
        if self.current_index is not None and self.current_index < len(self.questions) - 1:
            self._enter_question(self.current_index + 1, save_current=True)

    def _previous_question(self):
        if self.current_index is not None and self.current_index > 0:
            self._enter_question(self.current_index - 1, save_current=True)

    def _save_next(self):
        self._record_current_question("save")
        if self.current_index is not None and self.current_index < len(self.questions) - 1:
            self._enter_question(self.current_index + 1, save_current=False)

    def _mark_review_next(self):
        self._record_current_question("mark")
        if self.current_index is not None and self.current_index < len(self.questions) - 1:
            self._enter_question(self.current_index + 1, save_current=False)

    def _clear_response(self):
        self.question_card.clear_answer()
        self._record_current_question("clear")
        self.question_card.set_answer(None)

    def _auto_submit(self):
        self._submit(auto=True)

    def _submit(self, auto: bool = False):
        if self.submitted:
            return
        self._record_current_question("preserve")
        unanswered = sum(1 for state in self.question_states.values() if state.get("answer") in (None, "", []))
        if not auto:
            reply = QMessageBox.question(
                self,
                "Submit Test",
                f"{unanswered} questions unanswered. Sure?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if reply != QMessageBox.StandardButton.Yes:
                self.question_enter_time = time.monotonic()
                return

        self.submitted = True
        self.timer_widget.stop()
        for question_id, state in self.question_states.items():
            self.db.save_answer(
                self.attempt_id,
                question_id,
                state["answer"],
                state["time_spent"],
                state["marked_for_review"],
            )
        answer_payload = {
            question_id: {
                "answer": state["answer"],
                "time_spent_seconds": state["time_spent"],
                "marked_for_review": state["marked_for_review"],
            }
            for question_id, state in self.question_states.items()
        }
        result = calculate_score(
            self.questions,
            answer_payload,
            self.mock["marks_correct"],
            self.mock["marks_incorrect"],
        )
        self.db.finish_attempt(self.attempt_id, result.total_score, result.max_score)
        self.navigate_to_analysis(self.attempt_id)
