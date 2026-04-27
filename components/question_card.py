import json

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtWidgets import (
    QButtonGroup,
    QCheckBox,
    QFrame,
    QLabel,
    QLineEdit,
    QRadioButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from styles import COLORS
from utils_render import text_to_html


class QuestionCard(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.question = None
        self.option_widgets = []
        self.button_group = None
        self.numerical_input = None

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.content = QWidget()
        self.layout = QVBoxLayout(self.content)
        self.layout.setContentsMargins(22, 22, 22, 22)
        self.layout.setSpacing(14)

        self.number_label = QLabel()
        self.number_label.setStyleSheet(f"color: {COLORS['warning']}; font-weight: 800;")
        self.text_label = QLabel()
        self.text_label.setTextFormat(Qt.TextFormat.RichText)
        self.text_label.setWordWrap(True)
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.text_label.setStyleSheet("font-size: 17px; line-height: 1.35;")
        self.layout.addWidget(self.number_label)
        self.layout.addWidget(self.text_label)
        self.options_container = QVBoxLayout()
        self.options_container.setSpacing(8)
        self.layout.addLayout(self.options_container)
        self.layout.addStretch()

        self.scroll.setWidget(self.content)
        outer_layout.addWidget(self.scroll)

    def _clear_options(self):
        while self.options_container.count():
            item = self.options_container.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        self.option_widgets = []
        self.button_group = None
        self.numerical_input = None

    def _parse_options(self, raw_options):
        if raw_options is None:
            return []
        if isinstance(raw_options, list):
            return raw_options
        try:
            return json.loads(raw_options)
        except Exception:
            return []

    def set_question(self, question: dict, index: int):
        self.question = question
        self._clear_options()
        qtype = question.get("type", "single")
        type_label = {
            "single": "Single Correct",
            "multiple": "Multiple Correct",
            "numerical": "Numerical",
        }.get(qtype, qtype.title())
        self.number_label.setText(f"Q.{index + 1}  {question.get('section', '')} · {type_label}")
        self.text_label.setText(text_to_html(question.get("text", "")))

        if qtype == "single":
            self.button_group = QButtonGroup(self)
            self.button_group.setExclusive(True)
            for option_index, option in enumerate(self._parse_options(question.get("options"))):
                letter = chr(65 + option_index)
                container = QWidget()
                row = QHBoxLayout(container)
                row.setContentsMargins(0, 0, 0, 0)
                
                radio = QRadioButton()
                radio.setProperty("answer_value", letter)
                self.button_group.addButton(radio)
                self.option_widgets.append(radio)
                
                lbl = QLabel(text_to_html(option))
                lbl.setTextFormat(Qt.TextFormat.RichText)
                lbl.setWordWrap(True)
                
                row.addWidget(radio)
                row.addWidget(lbl, 1)
                self.options_container.addWidget(container)
        elif qtype == "multiple":
            for option_index, option in enumerate(self._parse_options(question.get("options"))):
                letter = chr(65 + option_index)
                container = QWidget()
                row = QHBoxLayout(container)
                row.setContentsMargins(0, 0, 0, 0)
                
                checkbox = QCheckBox()
                checkbox.setProperty("answer_value", letter)
                self.option_widgets.append(checkbox)
                
                lbl = QLabel(text_to_html(option))
                lbl.setTextFormat(Qt.TextFormat.RichText)
                lbl.setWordWrap(True)
                
                row.addWidget(checkbox)
                row.addWidget(lbl, 1)
                self.options_container.addWidget(container)
        else:
            self.numerical_input = QLineEdit()
            self.numerical_input.setPlaceholderText("Enter numerical answer")
            validator = QDoubleValidator(self)
            validator.setNotation(QDoubleValidator.Notation.StandardNotation)
            self.numerical_input.setValidator(validator)
            self.options_container.addWidget(self.numerical_input)

    def get_answer(self):
        if not self.question:
            return None
        qtype = self.question.get("type")
        if qtype == "single":
            for widget in self.option_widgets:
                if widget.isChecked():
                    return widget.property("answer_value")
            return None
        if qtype == "multiple":
            values = [widget.property("answer_value") for widget in self.option_widgets if widget.isChecked()]
            return values or None
        text = self.numerical_input.text().strip() if self.numerical_input else ""
        if not text:
            return None
        try:
            return float(text)
        except Exception:
            return None

    def set_answer(self, answer):
        if not self.question:
            return
        self.clear_answer()
        qtype = self.question.get("type")
        if answer in (None, ""):
            return
        if qtype == "single":
            for widget in self.option_widgets:
                if widget.property("answer_value") == answer:
                    widget.setChecked(True)
                    return
        elif qtype == "multiple":
            selected = set(answer if isinstance(answer, list) else [answer])
            for widget in self.option_widgets:
                widget.setChecked(widget.property("answer_value") in selected)
        elif self.numerical_input:
            self.numerical_input.setText(str(answer))

    def clear_answer(self):
        if self.button_group:
            self.button_group.setExclusive(False)
        for widget in self.option_widgets:
            widget.setChecked(False)
        if self.button_group:
            self.button_group.setExclusive(True)
        if self.numerical_input:
            self.numerical_input.clear()
