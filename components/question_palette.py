from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QGridLayout, QLabel, QPushButton, QScrollArea, QVBoxLayout, QWidget

from styles import COLORS, PALETTE

SECTION_COLORS = {
    "Physics": "#E74C3C",
    "Chemistry": "#E67E22",
    "Math": "#27AE60",
    "Mathematics": "#27AE60",
}


class QuestionPalette(QWidget):
    question_selected = pyqtSignal(int)

    def __init__(self, questions: list, parent=None):
        super().__init__(parent)
        self.questions = questions
        self.buttons = {}
        self.current_question_id = ""
        self.summary_labels = {}

        self.sections = []
        for question in questions:
            section = question["section"]
            if section not in self.sections:
                self.sections.append(section)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        grid_widget = QWidget()
        grid = QGridLayout(grid_widget)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(8)
        grid.setVerticalSpacing(8)

        for idx, question in enumerate(questions):
            section_color = SECTION_COLORS.get(question["section"], COLORS["accent"])
            button = QPushButton(str(idx + 1))
            button.setFixedSize(44, 40)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(lambda checked=False, g_idx=idx: self.question_selected.emit(g_idx))
            grid.addWidget(button, idx // 5, idx % 5)
            self.buttons[question["id"]] = button
            self._style_button(button, "not_visited", False, section_color)

        scroll.setWidget(grid_widget)
        layout.addWidget(scroll)

        for section in self.sections:
            label = QLabel(f"{section}: 0/0")
            label.setStyleSheet(f"color: {COLORS['text_secondary']};")
            self.summary_labels[section] = label

    def get_summary_text(self) -> str:
        return "   ".join(f"{s}: {self.summary_labels[s].text().split(': ')[1]}" for s in self.sections)

    def _style_button(self, button: QPushButton, status: str, current: bool, section_color: str = None):
        section_color = section_color or COLORS["accent"]
        border = section_color if current else COLORS["border"]
        width = "3px" if current else "1px"
        glow = f"box-shadow: 0 0 8px {section_color};" if current else ""
        button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {PALETTE.get(status, PALETTE["not_visited"])};
                color: white;
                border: {width} solid {border};
                border-radius: 6px;
                padding: 0;
                font-weight: 800;
                font-size: 13px;
            }}
            QPushButton:hover {{
                border-color: {section_color};
                border-width: 2px;
            }}
            """
        )

    def update_status(self, question_id: str, status: str):
        button = self.buttons.get(question_id)
        if button:
            button.setProperty("status", status)
            question = next((q for q in self.questions if q["id"] == question_id), None)
            section_color = SECTION_COLORS.get(question["section"], COLORS["accent"]) if question else COLORS["accent"]
            self._style_button(button, status, question_id == self.current_question_id, section_color)

    def set_current(self, question_id: str):
        previous = self.current_question_id
        self.current_question_id = question_id
        if previous and previous in self.buttons:
            prev_question = next((q for q in self.questions if q["id"] == previous), None)
            prev_color = SECTION_COLORS.get(prev_question["section"], COLORS["accent"]) if prev_question else COLORS["accent"]
            self._style_button(self.buttons[previous], self.buttons[previous].property("status") or "not_visited", False, prev_color)
        button = self.buttons.get(question_id)
        if button:
            status = button.property("status") or "not_visited"
            question = next((q for q in self.questions if q["id"] == question_id), None)
            section_color = SECTION_COLORS.get(question["section"], COLORS["accent"]) if question else COLORS["accent"]
            self._style_button(button, status, True, section_color)

    def update_section_summary(self, states: dict):
        totals = {section: {"answered": 0, "total": 0} for section in self.summary_labels}
        for question in self.questions:
            section = question["section"]
            totals.setdefault(section, {"answered": 0, "total": 0})
            totals[section]["total"] += 1
            status = states.get(question["id"], {}).get("status", "not_visited")
            if status in ("answered", "answered_marked"):
                totals[section]["answered"] += 1
        for section, label in self.summary_labels.items():
            values = totals.get(section, {"answered": 0, "total": 0})
            label.setText(f"{section}: {values['answered']}/{values['total']}")

    def sync_states(self, states: dict):
        for question_id, state in states.items():
            button = self.buttons.get(question_id)
            if button:
                button.setProperty("status", state.get("status", "not_visited"))
                question = next((q for q in self.questions if q["id"] == question_id), None)
                section_color = SECTION_COLORS.get(question["section"], COLORS["accent"]) if question else COLORS["accent"]
                self._style_button(button, state.get("status", "not_visited"), question_id == self.current_question_id, section_color)
        self.update_section_summary(states)
