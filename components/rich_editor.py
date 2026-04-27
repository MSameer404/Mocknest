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
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        toolbar = QHBoxLayout()
        toolbar.setContentsMargins(0, 0, 0, 0)
        
        lbl = QLabel("Markdown / LaTeX ($$...$$)")
        lbl.setProperty("role", "muted")
        toolbar.addWidget(lbl)
        toolbar.addStretch()
        
        add_img_btn = QPushButton("📷 Add Image")
        add_img_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_img_btn.clicked.connect(self._add_image)
        toolbar.addWidget(add_img_btn)
        
        layout.addLayout(toolbar)

        # Splitter for raw edit vs preview
        splitter = QSplitter(Qt.Orientation.Vertical)
        
        self.editor = QTextEdit()
        self.editor.setPlaceholderText(placeholder)
        self.editor.textChanged.connect(self._on_text_changed)
        splitter.addWidget(self.editor)

        self.preview = QTextBrowser()
        self.preview.setOpenExternalLinks(False)
        self.preview.setStyleSheet("background-color: #FAFAFA; border: 1px solid #E0E0E0;")
        splitter.addWidget(self.preview)

        layout.addWidget(splitter)

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
        raw_text = self.editor.toPlainText()
        html = text_to_html(raw_text)
        self.preview.setHtml(html)

    def toPlainText(self) -> str:
        return self.editor.toPlainText()

    def setText(self, text: str):
        self.editor.setText(text)
        self._update_preview()
        
    def clear(self):
        self.editor.clear()
