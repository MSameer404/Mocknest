import json
from datetime import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont, QPainter
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from scoring import calculate_score
from styles import BUTTON_PRIMARY, CARD_STYLE, COLORS


class ScoreTrendChart(QWidget):
    def __init__(self, attempts: list[dict], current_attempt_id: str, parent=None):
        super().__init__(parent)
        self.attempts = attempts
        self.current_attempt_id = current_attempt_id
        self.setMinimumHeight(190)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect().adjusted(18, 16, -18, -28)
        painter.fillRect(self.rect(), QColor(COLORS["bg_card"]))
        painter.setPen(QColor(COLORS["text_primary"]))
        painter.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        painter.drawText(18, 20, "Score Trend")
        if not self.attempts:
            painter.setPen(QColor(COLORS["text_secondary"]))
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "No previous attempts")
            return

        chart_top = rect.top() + 28
        chart_bottom = rect.bottom() - 12
        chart_left = rect.left() + 8
        chart_right = rect.right() - 8
        painter.setPen(QColor(COLORS["border"]))
        painter.drawLine(chart_left, chart_bottom, chart_right, chart_bottom)
        painter.drawLine(chart_left, chart_top, chart_left, chart_bottom)

        count = len(self.attempts)
        gap = 14
        usable_width = max(40, chart_right - chart_left - gap * (count + 1))
        bar_width = max(18, usable_width // max(1, count))
        max_height = max(20, chart_bottom - chart_top - 10)

        for index, attempt in enumerate(self.attempts):
            percent = ((attempt.get("total_score") or 0) / attempt["max_score"] * 100) if attempt.get("max_score") else 0
            bar_height = int(max_height * percent / 100)
            x = chart_left + gap + index * (bar_width + gap)
            y = chart_bottom - bar_height
            color = COLORS["accent"] if attempt["id"] == self.current_attempt_id else COLORS["bg_secondary"]
            painter.setBrush(QColor(color))
            painter.setPen(QColor(color))
            painter.drawRoundedRect(x, y, bar_width, bar_height, 4, 4)
            painter.setPen(QColor(COLORS["text_secondary"]))
            painter.setFont(QFont("Segoe UI", 8))
            painter.drawText(x - 6, chart_bottom + 16, bar_width + 12, 12, Qt.AlignmentFlag.AlignCenter, self._short_date(attempt))
            painter.drawText(x - 6, max(chart_top, y - 16), bar_width + 12, 12, Qt.AlignmentFlag.AlignCenter, f"{percent:.0f}%")

    def _short_date(self, attempt):
        value = attempt.get("finished_at") or attempt.get("started_at")
        try:
            return datetime.fromisoformat(value).strftime("%d %b")
        except Exception:
            return ""


class AnalysisPage(QWidget):
    def __init__(self, db, attempt_id: str, navigate_to_test, navigate_to_library, parent=None):
        super().__init__(parent)
        self.db = db
        self.attempt_id = attempt_id
        self.navigate_to_test = navigate_to_test
        self.navigate_to_library = navigate_to_library
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
        heading = QLabel("Test Analysis")
        heading.setProperty("role", "heading")
        top.addWidget(heading)
        top.addStretch()
        retake = QPushButton("Retake Test")
        retake.setStyleSheet(BUTTON_PRIMARY)
        retake.clicked.connect(lambda checked=False: self.navigate_to_test(self.mock["id"]))
        back = QPushButton("Back to Library")
        back.clicked.connect(self.navigate_to_library)
        top.addWidget(retake)
        top.addWidget(back)
        layout.addLayout(top)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(16)
        content_layout.addWidget(self._score_hero())
        content_layout.addWidget(self._section_table())
        content_layout.addWidget(self._time_analysis())
        content_layout.addWidget(self._trend_chart())
        content_layout.addWidget(self._question_review())
        scroll.setWidget(content)
        layout.addWidget(scroll, 1)

    def _score_hero(self):
        card = QFrame()
        card.setStyleSheet(CARD_STYLE)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(22, 20, 22, 20)
        score = QLabel(f"Your Score: {self.result.total_score:g} / {self.result.max_score:g}")
        score.setStyleSheet("font-size: 28px; font-weight: 900;")
        percent = (self.result.total_score / self.result.max_score * 100) if self.result.max_score else 0
        progress = QProgressBar()
        progress.setRange(0, 100)
        progress.setValue(max(0, min(100, int(percent))))
        progress.setFormat(f"{percent:.1f}%")
        counts = QLabel(
            f"Correct: {self.result.correct_count}   Wrong: {self.result.wrong_count}   Skip: {self.result.unattempted_count}"
        )
        counts.setProperty("role", "muted")
        layout.addWidget(score)
        layout.addWidget(progress)
        layout.addWidget(counts)
        return card

    def _section_table(self):
        table = QTableWidget(len(self.result.section_breakdown), 6)
        table.setHorizontalHeaderLabels(["Section", "Attempted", "Correct", "Wrong", "Score", "Accuracy"])
        table.verticalHeader().setVisible(False)
        table.setAlternatingRowColors(True)
        for row, (section, data) in enumerate(self.result.section_breakdown.items()):
            values = [
                section,
                f"{data['attempted']}/{data['total']}",
                str(data["correct"]),
                str(data["wrong"]),
                f"{data['score']:g}",
                f"{data['accuracy']:.1f}%",
            ]
            for col, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                table.setItem(row, col, item)
        table.resizeColumnsToContents()
        table.setMinimumHeight(145)
        return table

    def _time_analysis(self):
        card = QFrame()
        card.setStyleSheet(CARD_STYLE)
        layout = QVBoxLayout(card)
        times = []
        for question in self.questions:
            info = self.answers.get(question["id"], {})
            times.append((question, int(info.get("time_spent_seconds", 0) or 0)))
        average = int(sum(time for _, time in times) / len(times)) if times else 0
        title = QLabel(f"Avg time per question: {average} sec")
        title.setProperty("role", "subheading")
        layout.addWidget(title)
        slowest = sorted(times, key=lambda item: item[1], reverse=True)[:3]
        if not slowest:
            empty = QLabel("No time data available.")
            empty.setProperty("role", "muted")
            layout.addWidget(empty)
        for question, seconds in slowest:
            label = QLabel(f"Q{question['order_index'] + 1} · {question['section']} · {seconds} sec")
            label.setProperty("role", "muted")
            layout.addWidget(label)
        return card

    def _trend_chart(self):
        attempts = [attempt for attempt in self.db.get_attempts_for_mock(self.mock["id"]) if attempt.get("finished_at")]
        attempts = list(reversed(attempts[:5]))
        chart = ScoreTrendChart(attempts, self.attempt_id)
        frame = QFrame()
        frame.setStyleSheet(CARD_STYLE)
        layout = QVBoxLayout(frame)
        layout.addWidget(chart)
        return frame

    def _question_review(self):
        card = QFrame()
        card.setStyleSheet(CARD_STYLE)
        layout = QVBoxLayout(card)
        title = QLabel("Question Review")
        title.setProperty("role", "subheading")
        layout.addWidget(title)
        for index, question in enumerate(self.questions, start=1):
            layout.addWidget(self._review_row(index, question))
        return card

    def _review_row(self, index: int, question: dict):
        row = QFrame()
        row.setStyleSheet(
            f"QFrame {{ background-color: {COLORS['bg_secondary']}; border: 1px solid {COLORS['border']}; border-radius: 6px; }}"
        )
        layout = QHBoxLayout(row)
        info = self.answers.get(question["id"], {})
        answer = info.get("answer")
        status = self._outcome(question, answer)
        color = {
            "correct": COLORS["success"],
            "wrong": COLORS["danger"],
            "skipped": COLORS["text_secondary"],
            "partial": COLORS["warning"],
        }.get(status, COLORS["text_secondary"])
        icon = {"correct": "✓", "wrong": "✗", "skipped": "—", "partial": "0"}.get(status, "—")
        left = QLabel(f"Q{index} · {question['section']}")
        left.setMinimumWidth(120)
        your = QLabel(f"Your answer: {self._format_answer(answer)}")
        your.setStyleSheet(f"color: {color}; font-weight: 800;")
        correct = QLabel(f"Correct: {self._format_answer(question['correct_answer'])}")
        time = QLabel(f"{int(info.get('time_spent_seconds', 0) or 0)} sec")
        outcome = QLabel(icon)
        outcome.setStyleSheet(f"color: {color}; font-size: 20px; font-weight: 900;")
        layout.addWidget(left)
        layout.addWidget(your, 1)
        layout.addWidget(correct, 1)
        layout.addWidget(time)
        layout.addWidget(outcome)
        return row

    def _format_answer(self, answer):
        if answer in (None, "", []):
            return "Skipped"
        if isinstance(answer, list):
            return ", ".join(answer)
        if isinstance(answer, str) and answer.startswith("["):
            try:
                return ", ".join(json.loads(answer))
            except Exception:
                return answer
        return str(answer)

    def _outcome(self, question, answer):
        if answer in (None, "", []):
            return "skipped"
        qtype = question["type"]
        correct = question["correct_answer"]
        if qtype == "multiple":
            try:
                correct_values = set(json.loads(correct) if isinstance(correct, str) and correct.startswith("[") else [correct])
            except Exception:
                correct_values = {correct}
            answer_values = set(answer if isinstance(answer, list) else [answer])
            if answer_values == correct_values:
                return "correct"
            if answer_values and answer_values.issubset(correct_values):
                return "partial"
            return "wrong"
        if qtype == "numerical":
            try:
                return "correct" if abs(float(answer) - float(correct)) <= 0.01 else "wrong"
            except Exception:
                return "wrong"
        return "correct" if str(answer) == str(correct) else "wrong"
