import os
import shutil
import uuid
from pathlib import Path

from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSplitter,
    QTextBrowser,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from utils_render import text_to_html

# Directory to store images used in the mock
IMAGES_DIR = Path.home() / ".jee_mock_app" / "images"
IMAGES_DIR.mkdir(parents=True, exist_ok=True)


class RichEditor(QWidget):
    """A dual-pane editor (raw text + live preview) supporting images and LaTeX."""
    
    text_changed = pyqtSignal()

    def __init__(self, placeholder: str = "", min_height: int = 150, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(min_height)
        self._build(placeholder)
        
        # Use a timer to debounce rendering to avoid lag on every keystroke
        self._render_timer = QTimer(self)
        self._render_timer.setSingleShot(True)
        self._render_timer.setInterval(500)
        self._render_timer.timeout.connect(self._update_preview)

    def _build(self, placeholder):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        self.editor = QTextEdit()
        self.editor.setPlaceholderText(placeholder)
        self.editor.textChanged.connect(self._on_text_changed)
        layout.addWidget(self.editor, 1)
        
        self.add_img_btn = QPushButton("📷")
        self.add_img_btn.setToolTip("Add Image")
        self.add_img_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_img_btn.clicked.connect(self._add_image)
        self.add_img_btn.setFixedWidth(40)
        layout.addWidget(self.add_img_btn)

    def _add_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.gif *.bmp)"
        )
        if not file_path:
            return

        # Copy image to app's image directory
        ext = os.path.splitext(file_path)[1]
        new_filename = f"{uuid.uuid4().hex}{ext}"
        dest_path = IMAGES_DIR / new_filename
        
        try:
            shutil.copy2(file_path, dest_path)
            # Insert markdown image tag
            md_tag = f"![Image]({dest_path.as_posix()})"
            cursor = self.editor.textCursor()
            cursor.insertText(md_tag)
        except Exception as exc:
            print(f"Failed to copy image: {exc}")

    def _on_text_changed(self):
        self._render_timer.start()
        self.text_changed.emit()

    def _update_preview(self):
        pass

    def toPlainText(self) -> str:
        return self.editor.toPlainText()

    def setText(self, text: str):
        self.editor.setText(text)
        self._update_preview()
        
    def clear(self):
        self.editor.clear()
