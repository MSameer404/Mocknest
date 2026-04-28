import json
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from styles import COLORS
from utils_render import text_to_html


class DeepAnalysisPage(QWidget):
    def __init__(self, db, attempt_id: str, navigate_to_analysis, parent=None):
        super().__init__(parent)
        self.db = db
        self.attempt_id = attempt_id
        self.navigate_to_analysis = navigate_to_analysis
        
        self.attempt = db.get_attempt(attempt_id)
        self.mock = db.get_mock(self.attempt.get("mock_id", "")) if self.attempt else {}
        self.questions = db.get_questions(self.attempt.get("mock_id", "")) if self.attempt else []
        self.answers = json.loads(self.attempt.get("answers", "{}")) if self.attempt else {}
        
        self.current_index = 0
        self.question_states = {}
        self.buttons = {}
        
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(16)

        if not self.attempt:
            missing = QLabel("Attempt data not found.")
            missing.setProperty("role", "heading")
            layout.addWidget(missing)
            return

        # Header
        top = QHBoxLayout()
        back = QPushButton("◄ Back to Analysis")
        back.clicked.connect(self.navigate_to_analysis)
        top.addWidget(back)
        
        title = QLabel(f"Deep Analysis: {self.mock.get('title', 'Mock Test')}")
        title.setStyleSheet("font-size: 22px; font-weight: 800; margin-left: 14px;")
        top.addWidget(title)
        top.addStretch()
        layout.addLayout(top)

        # Body Layout
        body = QHBoxLayout()
        body.setSpacing(18)

        # --- LEFT PANEL: Question Display ---
        left_panel = QFrame()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(14)

        # Status Banner
        self.status_banner = QLabel()
        self.status_banner.setStyleSheet("font-size: 16px; font-weight: bold; padding: 12px; border-radius: 6px;")
        self.status_banner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(self.status_banner)

        # Question Content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        
        content_widget = QWidget()
        self.question_layout = QVBoxLayout(content_widget)
        self.question_layout.setContentsMargins(18, 12, 18, 12)
        self.question_layout.setSpacing(16)
        
        header_row = QHBoxLayout()
        self.q_header = QLabel()
        self.q_header.setStyleSheet(f"color: {COLORS['warning']}; font-weight: 800; font-size: 15px;")
        header_row.addWidget(self.q_header)
        header_row.addStretch()
        
        self.time_lbl = QLabel()
        self.time_lbl.setStyleSheet(f"color: {COLORS['accent']}; font-weight: 800; font-size: 15px;")
        header_row.addWidget(self.time_lbl)
        
        self.question_layout.addLayout(header_row)

        self.q_text = QLabel()
        self.q_text.setTextFormat(Qt.TextFormat.RichText)
        self.q_text.setWordWrap(True)
        self.q_text.setStyleSheet("font-size: 18px; line-height: 1.4;")
        self.question_layout.addWidget(self.q_text)

        self.options_container = QVBoxLayout()
        self.options_container.setSpacing(10)
        self.question_layout.addLayout(self.options_container)
        self.question_layout.addStretch()

        scroll_area.setWidget(content_widget)
        left_layout.addWidget(scroll_area, 1)

        # Navigation row
        nav_row = QHBoxLayout()
        self.prev_button = QPushButton("◄ Previous")
        self.prev_button.setMinimumHeight(38)
        self.prev_button.clicked.connect(self._previous_question)
        
        self.next_button = QPushButton("Next ►")
        self.next_button.setProperty("role", "primary")
        self.next_button.setMinimumHeight(38)
        self.next_button.clicked.connect(self._next_question)
        
        nav_row.addWidget(self.prev_button)
        nav_row.addStretch()
        nav_row.addWidget(self.next_button)
        left_layout.addLayout(nav_row)

        body.addWidget(left_panel, 1)

        # --- RIGHT PANEL: Question Palette ---
        right_panel = QFrame()
        right_panel.setFixedWidth(290)
        right_panel.setStyleSheet(f"background-color: {COLORS['bg_card']}; border-radius: 12px; border: 1px solid {COLORS['border']};")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(14, 16, 14, 16)
        right_layout.setSpacing(12)

        legend = QLabel("Question Palette")
        legend.setStyleSheet("font-weight: bold; font-size: 16px; color: #E0E0E0; margin-bottom: 4px;")
        right_layout.addWidget(legend)

        # Subject Switcher Layout
        switcher_layout = QHBoxLayout()
        switcher_layout.setSpacing(6)
        right_layout.addLayout(switcher_layout)

        palette_scroll = QScrollArea()
        palette_scroll.setWidgetResizable(True)
        palette_scroll.setFrameShape(QFrame.Shape.NoFrame)
        palette_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        palette_container = QWidget()
        self.palette_container_layout = QVBoxLayout(palette_container)
        self.palette_container_layout.setContentsMargins(0, 0, 0, 0)
        palette_scroll.setWidget(palette_container)
        
        right_layout.addWidget(palette_scroll, 1)

        # Build Sectioned Question Grid
        sections = {}
        for idx, q in enumerate(self.questions):
            sec = q["section"]
            if sec not in sections:
                sections[sec] = []
            sections[sec].append((idx, q))

        # Load overall score metrics
        for question in self.questions:
            qid = question["id"]
            ans_info = self.answers.get(qid)
            raw_ans = ans_info.get("answer") if isinstance(ans_info, dict) else ans_info
            
            if raw_ans not in (None, "", []):
                qtype = question["type"]
                correct = question["correct_answer"]
                status = self._evaluate_answer(qtype, correct, raw_ans)
            elif (isinstance(ans_info, dict) and ans_info.get("status") == "not_visited"):
                status = "not_visited"
            else:
                status = "unattempted"
                
            self.question_states[qid] = {
                "status": status,
                "answer": raw_ans
            }

        self.subject_buttons = {}
        self.subject_grids = {}
        
        color_map = {
            "physics": {"border": "#FFE066", "bg": "#2A2610", "fg": "#FFE066"},
            "chemistry": {"border": "#FFB366", "bg": "#2A1E10", "fg": "#FFB366"},
            "maths": {"border": "#66B2FF", "bg": "#101E2A", "fg": "#66B2FF"},
            "mathematics": {"border": "#66B2FF", "bg": "#101E2A", "fg": "#66B2FF"},
        }

        for sec in sections.keys():
            btn = QPushButton(sec)
            btn.setMinimumHeight(32)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked=False, s=sec: self._switch_subject(s))
            switcher_layout.addWidget(btn)
            self.subject_buttons[sec] = btn

            grid_widget = QWidget()
            grid_layout = QGridLayout(grid_widget)
            grid_layout.setContentsMargins(0, 8, 0, 0)
            grid_layout.setSpacing(8)
            
            for i, (idx, q) in enumerate(sections[sec]):
                row_idx = i // 4
                col_idx = i % 4
                
                q_btn = QPushButton(str(idx + 1))
                q_btn.setFixedSize(52, 48)
                
                status = self.question_states[q["id"]]["status"]
                
                if status == "correct":
                    bg = COLORS.get("success", "#00FF87")
                    fg = "#121212"
                    border = bg
                elif status == "wrong":
                    bg = COLORS.get("danger", "#FF0055")
                    fg = "#FFFFFF"
                    border = bg
                else:
                    sec_style = color_map.get(sec.lower(), {"border": "#555555", "bg": "#222222", "fg": "#CCCCCC"})
                    bg = sec_style["bg"]
                    border = sec_style["border"]
                    fg = sec_style["fg"]

                q_btn.setStyleSheet(f"""
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
                q_btn.clicked.connect(lambda checked=False, i=idx: self._enter_question(i))
                grid_layout.addWidget(q_btn, row_idx, col_idx)
                self.buttons[idx] = q_btn
                
            grid_widget.hide()
            self.palette_container_layout.addWidget(grid_widget)
            self.subject_grids[sec] = grid_widget

        self.palette_container_layout.addStretch()
        body.addWidget(right_panel)

        layout.addLayout(body, 1)

        if sections:
            first_sec = list(sections.keys())[0]
            self._switch_subject(first_sec)
            
        self._enter_question(0)

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

    def _evaluate_answer(self, qtype, correct, answer):
        if qtype == "multiple":
            try:
                correct_set = set(json.loads(correct) if isinstance(correct, str) and correct.startswith("[") else [correct])
            except:
                correct_set = {correct}
            answer_set = set(answer if isinstance(answer, list) else [answer])
            return "correct" if answer_set == correct_set else "wrong"
        if qtype == "numerical":
            try:
                return "correct" if abs(float(answer) - float(correct)) <= 0.01 else "wrong"
            except:
                return "wrong"
        return "correct" if str(answer) == str(correct) else "wrong"

    def _parse_options(self, raw_options):
        if isinstance(raw_options, list):
            return raw_options
        try:
            return json.loads(raw_options) if raw_options else []
        except:
            return []

    def _clear_options(self):
        while self.options_container.count():
            item = self.options_container.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def _enter_question(self, index: int):
        if index < 0 or index >= len(self.questions):
            return
        self.current_index = index
        question = self.questions[index]
        state = self.question_states[question["id"]]
        
        qtype = question.get("type", "single")
        type_str = {"single": "Single Choice", "multiple": "Multiple Choice", "numerical": "Numerical"}.get(qtype, qtype.title())
        
        ans_info = self.answers.get(question["id"])
        time_spent = ans_info.get("time_spent_seconds", 0) if isinstance(ans_info, dict) else 0
        m, s = divmod(time_spent, 60)
        time_str = f"{m}m {s}s" if m > 0 else f"{s}s"
        
        self.q_header.setText(f"Question {index + 1} · {question.get('section', '')} · {type_str}")
        self.time_lbl.setText(f"Time Spent: {time_str}")
        self.q_text.setText(text_to_html(question.get("text", "")))
        
        self._clear_options()
        
        # Style Status Banner
        if state["status"] == "correct":
            self.status_banner.setText(f"Outcome: Correct (+{self.mock.get('marks_correct', 4):g})")
            self.status_banner.setStyleSheet("background-color: #00FF87; color: #121212;")
        elif state["status"] == "wrong":
            self.status_banner.setText(f"Outcome: Incorrect ({self.mock.get('marks_incorrect', -1):g})")
            self.status_banner.setStyleSheet("background-color: #FF0055; color: white;")
        else:
            self.status_banner.setText("Outcome: Unattempted (0)")
            self.status_banner.setStyleSheet("background-color: #333333; color: #D0D0D0;")

        # Render options with explicit highlighting
        correct_ans = question.get("correct_answer")
        user_ans = state["answer"]
        
        if qtype in ("single", "multiple"):
            options_list = self._parse_options(question.get("options"))
            
            # Form standard set of user answers & correct answers for mapping
            if qtype == "multiple":
                try:
                    correct_set = set(json.loads(correct_ans) if isinstance(correct_ans, str) and correct_ans.startswith("[") else [correct_ans])
                except:
                    correct_set = {correct_ans}
                user_set = set(user_ans if isinstance(user_ans, list) else [user_ans]) if user_ans else set()
            else:
                correct_set = {str(correct_ans)}
                user_set = {str(user_ans)} if user_ans else set()

            for opt_idx, opt_text in enumerate(options_list):
                letter = chr(65 + opt_idx)
                opt_frame = QFrame()
                opt_layout = QHBoxLayout(opt_frame)
                opt_layout.setContentsMargins(12, 12, 12, 12)
                
                # Determine state
                is_correct = letter in correct_set
                is_selected = letter in user_set
                
                bg_color = "#1A1A1A"
                border_color = COLORS['border']
                
                if is_correct:
                    bg_color = "#0B2D1E"
                    border_color = "#00FF87"
                elif is_selected: # Wrong selection
                    bg_color = "#3D121B"
                    border_color = "#FF0055"

                opt_frame.setStyleSheet(f"""
                    QFrame {{
                        background-color: {bg_color};
                        border: 2px solid {border_color};
                        border-radius: 6px;
                    }}
                """)
                
                prefix = QLabel(f"{letter}.")
                prefix.setStyleSheet("font-weight: 800; font-size: 16px;")
                prefix.setFixedWidth(24)
                
                text_lbl = QLabel(text_to_html(opt_text))
                text_lbl.setTextFormat(Qt.TextFormat.RichText)
                text_lbl.setWordWrap(True)
                text_lbl.setStyleSheet("font-size: 16px; background: transparent; border: none;")
                
                opt_layout.addWidget(prefix)
                opt_layout.addWidget(text_lbl, 1)
                
                # Add checkmarks/cross markers
                if is_correct:
                    marker = QLabel("✓")
                    marker.setStyleSheet("color: #00FF87; font-size: 18px; font-weight: bold; background: transparent; border: none;")
                    opt_layout.addWidget(marker)
                elif is_selected:
                    marker = QLabel("✗")
                    marker.setStyleSheet("color: #FF0055; font-size: 18px; font-weight: bold; background: transparent; border: none;")
                    opt_layout.addWidget(marker)

                self.options_container.addWidget(opt_frame)
        else:
            # Numerical Answers
            num_frame = QFrame()
            num_layout = QVBoxLayout(num_frame)
            num_frame.setStyleSheet(f"background-color: #1A1A1A; border: 1px solid {COLORS['border']}; border-radius: 6px; padding: 14px;")
            
            u_ans_str = str(user_ans) if user_ans not in (None, "") else "Not Provided"
            c_ans_str = str(correct_ans)
            
            lbl_user = QLabel(f"<b>Your Response:</b> {u_ans_str}")
            lbl_user.setStyleSheet(f"font-size: 16px; color: {'#00FF87' if state['status'] == 'correct' else ('#FF0055' if user_ans else '#D0D0D0')};")
            
            lbl_correct = QLabel(f"<b>Correct Answer:</b> {c_ans_str}")
            lbl_correct.setStyleSheet("font-size: 16px; color: #00FF87;")
            
            num_layout.addWidget(lbl_user)
            num_layout.addWidget(lbl_correct)
            self.options_container.addWidget(num_frame)

        # Update button borders on Palette to show currently active question
        for i, btn in self.buttons.items():
            if i == index:
                btn.setStyleSheet(btn.styleSheet() + f"border: 2px solid {COLORS['accent']};")
            else:
                # Remove active state
                btn.setStyleSheet(btn.styleSheet().replace(f"border: 2px solid {COLORS['accent']};", ""))

        self.prev_button.setEnabled(index > 0)
        self.next_button.setEnabled(index < len(self.questions) - 1)

    def _previous_question(self):
        self._enter_question(self.current_index - 1)

    def _next_question(self):
        self._enter_question(self.current_index + 1)
