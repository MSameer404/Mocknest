COLORS = {
    "bg_primary": "#1A1A2E",
    "bg_secondary": "#16213E",
    "bg_card": "#0F3460",
    "accent": "#6C5CE7",
    "accent_hover": "#5A4BD1",
    "text_primary": "#EAEAEA",
    "text_secondary": "#A0A0B0",
    "success": "#00B894",
    "danger": "#D63031",
    "warning": "#FDCB6E",
    "border": "#2D2D4E",
}

PALETTE = {
    "not_visited": "#555555",
    "not_answered": "#C0392B",
    "answered": "#27AE60",
    "marked_review": "#8E44AD",
    "answered_marked": "#2980B9",
}

MAIN_STYLE = f"""
* {{
    font-family: Segoe UI, Arial, sans-serif;
    font-size: 14px;
    color: {COLORS["text_primary"]};
}}
QMainWindow, QWidget {{
    background-color: {COLORS["bg_primary"]};
}}
QFrame {{
    background-color: {COLORS["bg_card"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 8px;
}}
QLabel {{
    background: transparent;
    border: none;
}}
QLabel[role="heading"] {{
    font-size: 28px;
    font-weight: 700;
}}
QLabel[role="subheading"] {{
    font-size: 18px;
    font-weight: 600;
}}
QLabel[role="muted"] {{
    color: {COLORS["text_secondary"]};
}}
QPushButton {{
    background-color: {COLORS["bg_secondary"]};
    color: {COLORS["text_primary"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 6px;
    padding: 8px 12px;
    font-weight: 600;
}}
QPushButton:hover {{
    border-color: {COLORS["accent"]};
    background-color: #1C2C52;
}}
QPushButton:pressed {{
    background-color: {COLORS["accent_hover"]};
}}
QPushButton:disabled {{
    color: #77778A;
    background-color: #25253B;
}}
QLineEdit, QTextEdit, QComboBox, QSpinBox, QDoubleSpinBox {{
    background-color: {COLORS["bg_secondary"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 6px;
    padding: 8px;
    selection-background-color: {COLORS["accent"]};
}}
QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {{
    border-color: {COLORS["accent"]};
}}
QComboBox::drop-down {{
    border: none;
    width: 28px;
}}
QComboBox QAbstractItemView {{
    background-color: {COLORS["bg_secondary"]};
    border: 1px solid {COLORS["border"]};
    selection-background-color: {COLORS["accent"]};
}}
QScrollArea {{
    background-color: transparent;
    border: none;
}}
QScrollBar:vertical {{
    background: {COLORS["bg_primary"]};
    width: 12px;
    margin: 0;
}}
QScrollBar::handle:vertical {{
    background: {COLORS["border"]};
    border-radius: 6px;
    min-height: 24px;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}
QRadioButton, QCheckBox {{
    spacing: 10px;
    padding: 7px 4px;
    background: transparent;
}}
QRadioButton::indicator, QCheckBox::indicator {{
    width: 18px;
    height: 18px;
}}
QRadioButton::indicator:checked, QCheckBox::indicator:checked {{
    background-color: {COLORS["accent"]};
    border: 2px solid {COLORS["accent"]};
}}
QRadioButton::indicator:unchecked, QCheckBox::indicator:unchecked {{
    background-color: {COLORS["bg_secondary"]};
    border: 2px solid {COLORS["text_secondary"]};
}}
QTableWidget {{
    background-color: {COLORS["bg_secondary"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 8px;
    gridline-color: {COLORS["border"]};
    alternate-background-color: #1D2A4A;
}}
QHeaderView::section {{
    background-color: {COLORS["bg_card"]};
    color: {COLORS["text_primary"]};
    border: none;
    padding: 8px;
    font-weight: 700;
}}
QTableWidget::item {{
    padding: 6px;
}}
QTableWidget::item:selected {{
    background-color: {COLORS["accent"]};
}}
QProgressBar {{
    background-color: {COLORS["bg_secondary"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 6px;
    height: 18px;
    text-align: center;
    font-weight: 700;
}}
QProgressBar::chunk {{
    background-color: {COLORS["accent"]};
    border-radius: 5px;
}}
QMessageBox {{
    background-color: {COLORS["bg_primary"]};
}}
"""

BUTTON_PRIMARY = f"""
QPushButton {{
    background-color: {COLORS["accent"]};
    color: white;
    border: 1px solid {COLORS["accent"]};
    border-radius: 6px;
    padding: 9px 14px;
    font-weight: 700;
}}
QPushButton:hover {{
    background-color: {COLORS["accent_hover"]};
    border-color: {COLORS["accent_hover"]};
}}
"""

BUTTON_DANGER = f"""
QPushButton {{
    background-color: {COLORS["danger"]};
    color: white;
    border: 1px solid {COLORS["danger"]};
    border-radius: 6px;
    padding: 9px 14px;
    font-weight: 700;
}}
QPushButton:hover {{
    background-color: #B92829;
    border-color: #B92829;
}}
"""

SIDEBAR_STYLE = f"""
QWidget#sidebar {{
    background-color: {COLORS["bg_secondary"]};
    border-right: 1px solid {COLORS["border"]};
}}
QPushButton {{
    text-align: left;
    background-color: transparent;
    border: none;
    border-radius: 8px;
    padding: 11px 14px;
    font-size: 15px;
    font-weight: 600;
}}
QPushButton:hover {{
    background-color: #22345E;
}}
QPushButton[active="true"] {{
    background-color: {COLORS["accent"]};
    color: white;
}}
"""

CARD_STYLE = f"""
QFrame {{
    background-color: {COLORS["bg_card"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 8px;
}}
QFrame:hover {{
    border-color: {COLORS["accent"]};
}}
"""
