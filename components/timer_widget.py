from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtWidgets import QLabel

from styles import COLORS


class TimerWidget(QLabel):
    time_up = pyqtSignal()
    ticked = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.seconds_remaining = 0
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self._tick)
        self.setMinimumWidth(86)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._render()

    def set_duration(self, minutes: int):
        self.seconds_remaining = max(0, int(minutes) * 60)
        self._render()

    def start(self):
        if self.seconds_remaining > 0:
            self.timer.start()

    def stop(self):
        self.timer.stop()

    def _tick(self):
        self.seconds_remaining = max(0, self.seconds_remaining - 1)
        self._render()
        self.ticked.emit(self.seconds_remaining)
        if self.seconds_remaining <= 0:
            self.stop()
            self.time_up.emit()

    def _render(self):
        minutes = self.seconds_remaining // 60
        seconds = self.seconds_remaining % 60
        color = COLORS["danger"] if self.seconds_remaining <= 300 else COLORS["text_primary"]
        self.setText(f"{minutes:02d}:{seconds:02d}")
        self.setStyleSheet(
            f"""
            QLabel {{
                background-color: {COLORS["bg_secondary"]};
                border: 1px solid {COLORS["border"]};
                border-radius: 8px;
                color: {color};
                font-size: 18px;
                font-weight: 800;
                padding: 8px 12px;
            }}
            """
        )
