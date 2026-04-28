import sys
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QMainWindow, QStackedWidget, QWidget, QFrame, QMessageBox

from components.sidebar import Sidebar
from data.seed import seed_database
from db import Database
from pages.add_questions import AddQuestionsPage
from pages.analysis import AnalysisPage
from pages.creator import CreatorPage
from pages.history import HistoryPage
from pages.dashboard import DashboardPage
from pages.library import LibraryPage
from pages.take_test import TakeTestPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mocknest")
        icon_path = Path(__file__).parent / "assets" / "app.ico"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
        self.db = Database()
        seed_database(self.db)

        central = QWidget()
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.sidebar = Sidebar()
        self.sidebar.nav_clicked.connect(self.navigate_to)
        
        # Vertical Separator Line
        self.sidebar_sep = QFrame()
        self.sidebar_sep.setFixedWidth(1)
        self.sidebar_sep.setStyleSheet("background-color: #222222; border: none;")
        
        self.stack = QStackedWidget()
        layout.addWidget(self.sidebar)
        layout.addWidget(self.sidebar_sep)
        layout.addWidget(self.stack, 1)
        self.setCentralWidget(central)
        self.resize(1200, 800)
        self._center_on_screen()
        self.navigate_to("dashboard")

    def _center_on_screen(self):
        screen = QApplication.primaryScreen()
        if screen:
            geometry = screen.availableGeometry()
            self.move(
                geometry.center().x() - self.width() // 2,
                geometry.center().y() - self.height() // 2,
            )

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            "Quit Application?",
            "Are you sure you want to close Mocknest?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()

    def _restore_ui(self):
        self.showMaximized()
        self.sidebar.show()
        if hasattr(self, "sidebar_sep"):
            self.sidebar_sep.show()

    def _enter_protected_mode(self):
        self.sidebar.hide()
        if hasattr(self, "sidebar_sep"):
            self.sidebar_sep.hide()
        self.showFullScreen()
        QMessageBox.information(
            self, 
            "Protected Window", 
            "You are in a protected window now. Your work will be lost if you force quit. Submit for test giving and Done for creating."
        )

    def _expand_editor_mode(self):
        self.sidebar.hide()
        if hasattr(self, "sidebar_sep"):
            self.sidebar_sep.hide()

    def _set_page(self, widget: QWidget):
        while self.stack.count():
            old = self.stack.widget(0)
            self.stack.removeWidget(old)
            old.deleteLater()
        self.stack.addWidget(widget)
        self.stack.setCurrentWidget(widget)

    def navigate_to(self, page_name: str, **kwargs):
        if page_name in self.sidebar.buttons:
            self.sidebar.set_active(page_name)
        if page_name == "dashboard":
            page = DashboardPage(self.db, self.navigate_to_test, self.navigate_to)
        elif page_name == "library":
            page = LibraryPage(
                self.db,
                self.navigate_to_test,
                lambda: self.navigate_to("creator"),
                self.navigate_to,
            )
        elif page_name == "creator":
            page = CreatorPage(self.db, lambda mock_id: self.navigate_to("add_questions", mock_id=mock_id))
        elif page_name == "history":
            page = HistoryPage(self.db, self.navigate_to_analysis)
        elif page_name == "add_questions":
            self._expand_editor_mode()
            page = AddQuestionsPage(self.db, kwargs.get("mock_id", ""), self._exit_add_questions)
        else:
            page = DashboardPage(self.db, self.navigate_to_test, self.navigate_to)
            self.sidebar.set_active("dashboard")
        self._set_page(page)

    def _exit_add_questions(self):
        self._restore_ui()
        self.navigate_to("creator")

    def navigate_to_test(self, mock_id: str):
        self._enter_protected_mode()
        page = TakeTestPage(self.db, mock_id, self._exit_test)
        self._set_page(page)

    def _exit_test(self, attempt_id: str):
        self._restore_ui()
        self.navigate_to_analysis(attempt_id)

    def navigate_to_analysis(self, attempt_id: str):
        page = AnalysisPage(
            self.db,
            attempt_id,
            self.navigate_to_test,
            lambda: self.navigate_to("history"),
            self.navigate_to_deep_analysis,
        )
        self._set_page(page)

    def navigate_to_deep_analysis(self, attempt_id: str):
        from pages.deep_analysis import DeepAnalysisPage
        page = DeepAnalysisPage(
            self.db,
            attempt_id,
            lambda: self.navigate_to_analysis(attempt_id)
        )
        self._set_page(page)


def load_theme(app: QApplication):
    theme_path = Path(__file__).parent / "theme.qss"
    if theme_path.exists():
        app.setStyleSheet(theme_path.read_text(encoding="utf-8"))


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Mocknest")
    app.setApplicationVersion("1.0.0")
    icon_path = Path(__file__).parent / "assets" / "app.ico"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))
    if hasattr(Qt.ApplicationAttribute, "AA_UseHighDpiPixmaps"):
        app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)
    load_theme(app)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
