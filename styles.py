"""Color palette and minimal style definitions for MockNest.

For full theming, use theme.qss which is loaded at application startup.
This module exports color constants used by components that need runtime colors.
"""

COLORS = {
    "bg_primary": "#000000",
    "bg_secondary": "#0F0F0F",
    "bg_card": "#1A1A1A",
    "accent": "#00D2FF",
    "accent_hover": "#3A7BD5",
    "text_primary": "#FFFFFF",
    "text_secondary": "#A0A0A0",
    "success": "#00FF87",
    "danger": "#FF0055",
    "warning": "#FFD700",
    "border": "#222222",
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
