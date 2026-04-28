from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QGridLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QVBoxLayout, QWidget

from styles import COLORS, PALETTE


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
        layout.setSpacing(12)

        # Subject Switcher Layout
        self.switcher_layout = QHBoxLayout()
        self.switcher_layout.setSpacing(6)
        layout.addLayout(self.switcher_layout)

        # Container for subject grids
        self.grid_container = QWidget()
        self.grid_container_layout = QVBoxLayout(self.grid_container)
        self.grid_container_layout.setContentsMargins(0, 0, 0, 0)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setWidget(self.grid_container)
        
        layout.addWidget(scroll, 1)

        self.subject_buttons = {}
        self.subject_grids = {}

        # Build Sectioned Question Grid
        sections_map = {}
        for idx, q in enumerate(self.questions):
            sec = q["section"]
            if sec not in sections_map:
                sections_map[sec] = []
            sections_map[sec].append((idx, q))

        for sec in sections_map.keys():
            # Create Subject Tab Button
            btn = QPushButton(sec)
            btn.setMinimumHeight(32)
            btn.setCheckable(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked=False, s=sec: self._switch_subject(s))
            self.switcher_layout.addWidget(btn)
            self.subject_buttons[sec] = btn

            grid_widget = QWidget()
            grid_layout = QGridLayout(grid_widget)
            grid_layout.setContentsMargins(0, 8, 0, 0)
            grid_layout.setSpacing(8)

            for i, (idx, q) in enumerate(sections_map[sec]):
                row_idx = i // 4
                col_idx = i % 4

                button = QPushButton(str(idx + 1))
                button.setFixedSize(52, 48)
                button.setCursor(Qt.CursorShape.PointingHandCursor)
                button.clicked.connect(lambda checked=False, g_idx=idx: self.question_selected.emit(g_idx))
                grid_layout.addWidget(button, row_idx, col_idx)
                self.buttons[q["id"]] = button
                
                # Initial styling
                self._style_button(button, "not_visited", False, sec)

            grid_widget.hide()
            self.grid_container_layout.addWidget(grid_widget)
            self.subject_grids[sec] = grid_widget

        self.grid_container_layout.addStretch()

        # Switch to first subject
        if self.sections:
            self._switch_subject(self.sections[0])

    def _switch_subject(self, section_name: str):
        for sec, btn in self.subject_buttons.items():
            if sec == section_name:
                btn.setChecked(True)
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {COLORS['accent']};
                        color: #121212;
                        font-weight: bold;
                        border: none;
                        border-radius: 4px;
                    }}
                """)
            else:
                btn.setChecked(False)
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: #222222;
                        color: #D0D0D0;
                        font-weight: normal;
                        border: 1px solid {COLORS['border']};
                        border-radius: 4px;
                    }}
                """)

        for sec, grid in self.subject_grids.items():
            if sec == section_name:
                grid.show()
            else:
                grid.hide()

    def get_summary_text(self) -> str:
        totals = {sec: {"answered": 0, "total": 0} for sec in self.sections}
        for q in self.questions:
            sec = q["section"]
            totals[sec]["total"] += 1
            btn = self.buttons.get(q["id"])
            if btn:
                status = btn.property("status") or "not_visited"
                if status in ("answered", "answered_marked"):
                    totals[sec]["answered"] += 1
        return "   ".join(f"{s}: {totals[s]['answered']}/{totals[s]['total']}" for s in self.sections)

    def _style_button(self, button: QPushButton, status: str, current: bool, section_name: str):
        color_map = {
            "physics": {"border": "#FFE066", "bg": "#2A2610", "fg": "#FFE066"},
            "chemistry": {"border": "#FFB366", "bg": "#2A1E10", "fg": "#FFB366"},
            "maths": {"border": "#66B2FF", "bg": "#101E2A", "fg": "#66B2FF"},
            "mathematics": {"border": "#66B2FF", "bg": "#101E2A", "fg": "#66B2FF"},
        }
        sec_style = color_map.get(section_name.lower(), {"border": "#555555", "bg": "#222222", "fg": "#CCCCCC"})
        
        if status == "not_visited":
            bg = sec_style["bg"]
            border = sec_style["border"]
            fg = sec_style["fg"]
        elif status == "answered":
            bg = PALETTE.get("answered", "#27AE60")
            fg = "#FFFFFF"
            border = bg
        elif status == "not_answered":
            bg = PALETTE.get("not_answered", "#C0392B")
            fg = "#FFFFFF"
            border = bg
        elif status == "marked_review":
            bg = PALETTE.get("marked_review", "#8E44AD")
            fg = "#FFFFFF"
            border = bg
        elif status == "answered_marked":
            bg = PALETTE.get("answered_marked", "#E67E22")
            fg = "#FFFFFF"
            border = bg
        else:
            bg = sec_style["bg"]
            border = sec_style["border"]
            fg = sec_style["fg"]

        if current:
            border = COLORS['accent']

        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg}; 
                color: {fg};
                border: 2px solid {border}; 
                border-radius: 6px; 
                font-size: 15px;
                font-weight: bold;
                padding: 0px;
            }}
        """)

    def update_status(self, question_id: str, status: str):
        button = self.buttons.get(question_id)
        if button:
            button.setProperty("status", status)
            question = next((q for q in self.questions if q["id"] == question_id), None)
            sec = question["section"] if question else self.sections[0]
            self._style_button(button, status, question_id == self.current_question_id, sec)

    def set_current(self, question_id: str):
        previous = self.current_question_id
        self.current_question_id = question_id
        if previous and previous in self.buttons:
            prev_question = next((q for q in self.questions if q["id"] == previous), None)
            prev_sec = prev_question["section"] if prev_question else self.sections[0]
            self._style_button(self.buttons[previous], self.buttons[previous].property("status") or "not_visited", False, prev_sec)
        button = self.buttons.get(question_id)
        if button:
            status = button.property("status") or "not_visited"
            question = next((q for q in self.questions if q["id"] == question_id), None)
            sec = question["section"] if question else self.sections[0]
            self._style_button(button, status, True, sec)
            
            if question and sec in self.subject_buttons and not self.subject_buttons[sec].isChecked():
                self._switch_subject(sec)

    def update_section_summary(self, states: dict):
        pass

    def sync_states(self, states: dict):
        for question_id, state in states.items():
            button = self.buttons.get(question_id)
            if button:
                button.setProperty("status", state.get("status", "not_visited"))
                question = next((q for q in self.questions if q["id"] == question_id), None)
                sec = question["section"] if question else self.sections[0]
                self._style_button(button, state.get("status", "not_visited"), question_id == self.current_question_id, sec)
