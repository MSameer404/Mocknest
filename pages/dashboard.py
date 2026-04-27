import json

from PyQt6.QtWidgets import (
    QFileDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from mock_format import import_mock
from styles import COLORS


class DashboardPage(QWidget):
    def __init__(self, db, navigate_to_test, refresh_page, parent=None):
        super().__init__(parent)
        self.db = db
        self.navigate_to_test = navigate_to_test
        self.refresh_page = refresh_page
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(20)

        top = QHBoxLayout()
        heading = QLabel("Ready to Practice?")
        heading.setProperty("role", "heading")
        top.addWidget(heading)
        top.addStretch()
        layout.addLayout(top)



        instructions_box = QFrame()
        instructions_layout = QVBoxLayout(instructions_box)
        instructions_layout.setContentsMargins(20, 20, 20, 20)
        
        placeholder = QLabel("Welcome to Mocknest!\n\nInstructions on how to use the app will be added here soon.")
        placeholder.setProperty("role", "subheading")
        placeholder.setWordWrap(True)
        placeholder.setStyleSheet("color: #FFFFFF; font-weight: 700;")
        
        instructions_layout.addWidget(placeholder)
        layout.addWidget(instructions_box, 1)





    def _import_mock(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Import Mock", "", "Mocknest Files (*.jmock)")
        if not file_path:
            return
        mock_id = import_mock(self.db, file_path)
        if mock_id:
            QMessageBox.information(self, "Import Complete", "Mock imported successfully.")
            self.refresh_page("dashboard")
        else:
            QMessageBox.warning(self, "Import Failed", "Could not import this .jmock file.")
