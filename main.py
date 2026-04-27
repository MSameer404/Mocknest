import sys
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QMainWindow, QStackedWidget, QWidget

from components.sidebar import Sidebar
from data.seed import seed_database
from db import Database
from pages.add_questions import AddQuestionsPage
from pages.analysis import AnalysisPage
from pages.creator import CreatorPage
from pages.history import HistoryPage
from pages.home import HomePage
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
        self.stack = QStackedWidget()
        layout.addWidget(self.sidebar)
        layout.addWidget(self.stack, 1)
        self.setCentralWidget(central)
        self.resize(1200, 800)
        self._center_on_screen()
        self.navigate_to("home")

    def _center_on_screen(self):
        screen = QApplication.primaryScreen()
        if screen:
            geometry = screen.availableGeometry()
            self.move(
                geometry.center().x() - self.width() // 2,
                geometry.center().y() - self.height() // 2,
            )

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
        if page_name == "home":
            page = HomePage(self.db, self.navigate_to_test, self.navigate_to)
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
            page = AddQuestionsPage(self.db, kwargs.get("mock_id", ""), lambda: self.navigate_to("library"))
        else:
            page = HomePage(self.db, self.navigate_to_test, self.navigate_to)
            self.sidebar.set_active("home")
        self._set_page(page)

    def navigate_to_test(self, mock_id: str):
        page = TakeTestPage(self.db, mock_id, self.navigate_to_analysis)
        self._set_page(page)

    def navigate_to_analysis(self, attempt_id: str):
        page = AnalysisPage(
            self.db,
            attempt_id,
            self.navigate_to_test,
            lambda: self.navigate_to("library"),
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
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
