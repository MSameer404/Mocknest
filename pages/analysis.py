import json
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHeaderView,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from scoring import calculate_score
from styles import COLORS


class AnalysisPage(QWidget):
    def __init__(self, db, attempt_id: str, navigate_to_test, navigate_to_library, navigate_to_deep_analysis, parent=None):
        super().__init__(parent)
        self.db = db
        self.attempt_id = attempt_id
        self.navigate_to_test = navigate_to_test
        self.navigate_to_library = navigate_to_library
        self.navigate_to_deep_analysis = navigate_to_deep_analysis
        self.attempt = db.get_attempt(attempt_id)
        self.mock = db.get_mock(self.attempt.get("mock_id", "")) if self.attempt else {}
        self.questions = db.get_questions(self.attempt.get("mock_id", "")) if self.attempt else []
        self.answers = json.loads(self.attempt.get("answers", "{}")) if self.attempt else {}
        self.result = calculate_score(
            self.questions,
            self.answers,
            self.mock.get("marks_correct", 4),
            self.mock.get("marks_incorrect", -1),
        )
        self.result.attempt_id = attempt_id
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(16)

        if not self.attempt:
            missing = QLabel("Attempt not found.")
            missing.setProperty("role", "heading")
            layout.addWidget(missing)
            return

        top = QHBoxLayout()
        heading = QLabel(self.mock.get("title", "Test Analysis"))
        heading.setProperty("role", "heading")
        top.addWidget(heading)
        top.addStretch()
        
        deep_analysis = QPushButton("Deep Analysis")
        deep_analysis.setProperty("role", "primary")
        deep_analysis.clicked.connect(self._open_deep_analysis)
        
        back = QPushButton("Back")
        back.clicked.connect(self.navigate_to_library)
        
        top.addWidget(deep_analysis)
        top.addWidget(back)
        layout.addLayout(top)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(20)
        content_layout.addWidget(self._score_hero())
        content_layout.addWidget(self._section_table())
        scroll.setWidget(content)
        layout.addWidget(scroll, 1)

    def _open_deep_analysis(self):
        self.navigate_to_deep_analysis(self.attempt_id)

    def _score_hero(self):
        container = QFrame()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        # 1. Total Score Card (Deep Blue Background)
        score_card = QFrame()
        score_card.setObjectName("totalScoreCard")
        score_card.setStyleSheet(f"""
            QFrame#totalScoreCard {{
                background-color: #1A1A2E; 
                border-left: 5px solid {COLORS['accent']}; 
                border-radius: 8px;
            }}
            QLabel {{
                border: none;
                background: transparent;
            }}
        """)
        score_layout = QVBoxLayout(score_card)
        score_layout.setContentsMargins(20, 20, 20, 20)
        
        score_title = QLabel("Total Score")
        score_title.setStyleSheet("color: #A0A0A0; font-weight: bold; font-size: 18px;")
        
        score_value = QLabel(f"{self.result.total_score:g} / {self.result.max_score:g}")
        score_value.setStyleSheet(f"font-size: 48px; font-weight: 900; color: {COLORS['accent']};")
        
        score_layout.addWidget(score_title)
        score_layout.addWidget(score_value)
        layout.addWidget(score_card, 2)

        # 2. Grid for other metrics
        metrics_grid = QGridLayout()
        metrics_grid.setSpacing(12)
        
        def _metric_card(card_id, title, value, color, bg_color):
            card = QFrame()
            card.setObjectName(card_id)
            card.setStyleSheet(f"""
                QFrame#{card_id} {{
                    background-color: {bg_color}; 
                    border-left: 4px solid {color}; 
                    border-radius: 6px;
                }}
                QLabel {{
                    border: none;
                    background: transparent;
                }}
            """)
            l = QVBoxLayout(card)
            l.setContentsMargins(16, 12, 16, 12)
            t = QLabel(title)
            t.setStyleSheet("font-size: 12px; color: #D0D0D0; font-weight: bold;")
            v = QLabel(str(value))
            v.setStyleSheet(f"font-size: 20px; font-weight: 800; color: {color};")
            l.addWidget(t)
            l.addWidget(v)
            return card

        total_qs = len(self.questions)
        attempted_qs = total_qs - self.result.unattempted_count - self.result.not_visited_count
        accuracy = (self.result.correct_count / attempted_qs * 100) if attempted_qs > 0 else 0.0
        
        pos_marks = self.mock.get("marks_correct", 4)
        neg_marks = abs(self.mock.get("marks_incorrect", -1))
        pos_score = self.result.correct_count * pos_marks
        neg_score = self.result.wrong_count * neg_marks

        metrics_grid.addWidget(_metric_card("attemptedCard", "Attempted", f"{attempted_qs} / {total_qs}", "#00D2FF", "#112233"), 0, 0)
        metrics_grid.addWidget(_metric_card("accuracyCard", "Accuracy", f"{accuracy:.1f}%", "#FFD700", "#2A2A10"), 0, 1)
        metrics_grid.addWidget(_metric_card("positiveCard", "Positive Score", f"+{pos_score:g}", COLORS.get("success", "#00FF87"), "#0A251D"), 1, 0)
        metrics_grid.addWidget(_metric_card("negativeCard", "Negative Score", f"-{neg_score:g}", COLORS.get("danger", "#FF0055"), "#2D0A15"), 1, 1)
        
        metrics_container = QFrame()
        metrics_container.setLayout(metrics_grid)
        layout.addWidget(metrics_container, 3)

        return container

    def _section_table(self):
        container = QFrame()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        
        title = QLabel("Test Breakdown")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #FFFFFF; margin-bottom: 8px;")
        layout.addWidget(title)

        table = QTableWidget(len(self.result.section_breakdown) + 1, 6)
        table.setHorizontalHeaderLabels(["Subject", "Total Score", "Attempted Correct", "Attempted Wrong", "Not Attempted", "Not Visited Qs"])
        table.verticalHeader().setVisible(False)
        table.setAlternatingRowColors(True)

        total_qs = len(self.questions)

        overall_data = [
            "Overall",
            f"{self.result.total_score:g} / {self.result.max_score:g}",
            f"{self.result.correct_count} / {total_qs}",
            f"{self.result.wrong_count} / {total_qs}",
            f"{self.result.unattempted_count} / {total_qs}",
            f"{self.result.not_visited_count} / {total_qs}",
        ]

        def set_row(row_idx, data, text_color, is_overall=False):
            for col, value in enumerate(data):
                item = QTableWidgetItem(value)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                if col == 0:
                    font = item.font()
                    font.setBold(True)
                    item.setFont(font)
                    item.setForeground(QColor(text_color))
                else:
                    item.setForeground(QColor("#E0E0E0"))
                table.setItem(row_idx, col, item)

        set_row(0, overall_data, "#00D2FF", is_overall=True)

        color_map = {
            "physics": "#00FF87",
            "chemistry": "#FF7F00",
            "maths": "#007FFF",
            "mathematics": "#007FFF",
        }

        for row, (section, data) in enumerate(self.result.section_breakdown.items(), start=1):
            sec_total = data["total"]
            row_data = [
                section,
                f"{data['score']:g} / {sec_total * self.mock.get('marks_correct', 4):g}",
                f"{data['correct']} / {sec_total}",
                f"{data['wrong']} / {sec_total}",
                f"{data['unattempted']} / {sec_total}",
                f"{data.get('not_visited', 0)} / {sec_total}",
            ]
            sec_color = color_map.get(section.lower(), "#FFFFFF")
            set_row(row, row_data, sec_color)

        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setMinimumHeight(320)
        table.setStyleSheet(f"""
            QTableWidget {{
                background-color: #121212;
                gridline-color: #222222;
                border: 2px solid {COLORS['accent']};
                border-radius: 8px;
            }}
            QHeaderView::section {{
                background-color: #1A1A1A;
                color: #A0A0A0;
                padding: 10px;
                font-weight: bold;
                border: 1px solid #222222;
            }}
        """)
        layout.addWidget(table)
        return container
