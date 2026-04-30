import json

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtWidgets import (
    QButtonGroup,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from styles import COLORS
from utils_render import text_to_html


class OptionCard(QFrame):
    def __init__(self, letter, text, is_multiple, on_clicked, parent=None):
        super().__init__(parent)
        self.letter = letter
        self.is_multiple = is_multiple
        self.selected = False
        self.on_clicked = on_clicked
        self.setProperty("answer_value", letter)
        
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        
        self.prefix = QLabel(f"{letter}.")
        self.prefix.setStyleSheet("font-weight: 800; font-size: 16px;")
        self.prefix.setFixedWidth(24)
        self.prefix.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        
        display_text = text
        if text.startswith(f"{letter}) "):
            display_text = text[3:]
            
        self.text_lbl = QLabel(text_to_html(display_text))
        self.text_lbl.setTextFormat(Qt.TextFormat.RichText)
        self.text_lbl.setWordWrap(True)
        self.text_lbl.setStyleSheet("font-size: 16px; background: transparent; border: none;")
        self.text_lbl.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        
        layout.addWidget(self.prefix)
        layout.addWidget(self.text_lbl, 1)
        
        self.update_style()
        
    def update_style(self):
        if self.selected:
            bg_color = "#122A1E" 
            border_color = COLORS.get('success', '#00FF87')
        else:
            bg_color = "#1A1A1A"
            border_color = COLORS['border']
            
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border: 2px solid {border_color};
                border-radius: 8px;
            }}
        """)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.on_clicked(self)
            
    def setChecked(self, checked):
        self.selected = checked
        self.update_style()
        
    def isChecked(self):
        return self.selected


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
        self.number_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-weight: 800;")
        self.text_label = QLabel()
        self.text_label.setTextFormat(Qt.TextFormat.RichText)
        self.text_label.setWordWrap(True)
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.text_label.setStyleSheet("font-size: 17px; line-height: 1.35;")
        self.layout.addWidget(self.number_label)
        self.layout.addWidget(self.text_label)
        self.options_container = QVBoxLayout()
        self.options_container.setSpacing(12)
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
        if self.button_group:
            self.button_group.deleteLater()
        self.button_group = QButtonGroup()
        self.button_group.setExclusive(True)
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

        if qtype in ("single", "multiple"):
            is_multiple = (qtype == "multiple")
            for option_index, option in enumerate(self._parse_options(question.get("options"))):
                letter = chr(65 + option_index)
                card = OptionCard(letter, option, is_multiple, self._handle_card_click)
                self.option_widgets.append(card)
                self.options_container.addWidget(card)
        else:
            self.numerical_input = QLineEdit()
            self.numerical_input.setPlaceholderText("Enter numerical answer")
            validator = QDoubleValidator(self)
            validator.setNotation(QDoubleValidator.Notation.StandardNotation)
            self.numerical_input.setValidator(validator)
            self.options_container.addWidget(self.numerical_input)

    def _handle_card_click(self, clicked_card):
        if clicked_card.is_multiple:
            clicked_card.setChecked(not clicked_card.isChecked())
        else:
            for card in self.option_widgets:
                if card == clicked_card:
                    card.setChecked(True)
                else:
                    card.setChecked(False)

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
        for widget in self.option_widgets:
            widget.setChecked(False)
        if self.numerical_input:
            self.numerical_input.clear()
