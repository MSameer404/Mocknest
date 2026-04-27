from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget

from styles import COLORS


class Sidebar(QWidget):
    nav_clicked = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setFixedWidth(200)
        self.buttons = {}

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 24, 16, 16)
        layout.setSpacing(10)

        logo = QLabel("Mocknest")
        logo.setStyleSheet("font-size: 25px; font-weight: 800; padding: 4px 0 18px 0;")
        layout.addWidget(logo)

        for page, label in (
            ("home", "Home"),
            ("library", "Library"),
            ("creator", "Creator"),
            ("history", "History"),
        ):
            button = QPushButton(label)
            button.setCursor(button.cursor().shape())
            button.clicked.connect(lambda checked=False, page_name=page: self.nav_clicked.emit(page_name))
            layout.addWidget(button)
            self.buttons[page] = button

        layout.addStretch()
        version = QLabel("v1.0")
        version.setStyleSheet(f"color: {COLORS['text_secondary']}; padding: 10px;")
        layout.addWidget(version)
        self.set_active("home")

    def set_active(self, page_name: str):
        for name, button in self.buttons.items():
            button.setProperty("active", "true" if name == page_name else "false")
            button.style().unpolish(button)
            button.style().polish(button)
