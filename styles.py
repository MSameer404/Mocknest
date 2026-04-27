"""Color palette and minimal style definitions for MockNest.

For full theming, use theme.qss which is loaded at application startup.
This module exports color constants used by components that need runtime colors.
"""

COLORS = {
    "bg_primary": "#1A1A1A",
    "bg_secondary": "#2D2D2D",
    "bg_card": "#3D3D3D",
    "accent": "#E67E22",
    "accent_hover": "#D35400",
    "text_primary": "#EAEAEA",
    "text_secondary": "#A0A0A0",
    "success": "#27AE60",
    "danger": "#C0392B",
    "warning": "#F39C12",
    "border": "#4D4D4D",
}

PALETTE = {
    "not_visited": "#555555",
    "not_answered": "#C0392B",
    "answered": "#27AE60",
    "marked_review": "#8E44AD",
    "answered_marked": "#E67E22",
}

# Legacy style exports (kept for compatibility, prefer using theme.qss)
MAIN_STYLE = ""
SIDEBAR_STYLE = ""
BUTTON_PRIMARY = ""
BUTTON_DANGER = ""
CARD_STYLE = ""
