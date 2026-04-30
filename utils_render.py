import base64
import hashlib
import re
from io import BytesIO

import matplotlib
matplotlib.rcParams['savefig.facecolor'] = 'none'
matplotlib.rcParams['figure.facecolor'] = 'none'
from matplotlib.mathtext import math_to_image

_CACHE = {}


def render_latex_to_base64(latex_str: str) -> str:
    """Renders a LaTeX math string to a base64 encoded PNG image."""
    hash_key = hashlib.md5(latex_str.encode("utf-8")).hexdigest()
    if hash_key in _CACHE:
        return _CACHE[hash_key]

    buf = BytesIO()
    try:
        # math_to_image requires $...$ around the expression
        expr = latex_str.replace("\n", " ").replace("\r", " ").strip()
        expr = expr.replace(r"\lvert", r"\vert").replace(r"\rvert", r"\vert")
        expr = expr.replace(r"\lVert", r"\Vert").replace(r"\rVert", r"\Vert")
        if not expr.startswith("$"):
            expr = f"${expr}$"
        math_to_image(expr, buf, dpi=120, format="png", color="white")
        buf.seek(0)
        b64 = base64.b64encode(buf.read()).decode("utf-8")
        _CACHE[hash_key] = b64
        return b64
    except Exception as exc:
        print(f"LaTeX render error for '{latex_str}': {exc}")
        return ""


def text_to_html(text: str) -> str:
    """
    Converts raw text containing markdown images ![alt](path) and LaTeX $$math$$ into HTML.
    """
    if not text:
        return ""

    # Replace $$...$$ with base64 images
    # Use a non-greedy regex to find $$math$$
    def latex_repl(match):
        latex_str = match.group(1)
        b64 = render_latex_to_base64(latex_str)
        if b64:
            return f'<img src="data:image/png;base64,{b64}" style="vertical-align: middle;">'
        return f'<span style="color: red;">[Math Error: {latex_str}]</span>'

    html = re.sub(r"\$\$(.*?)\$\$", latex_repl, text, flags=re.DOTALL)
    html = re.sub(r"(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)", latex_repl, html, flags=re.DOTALL)

    # Replace ![alt](path) with <img src="file:///path">
    def img_repl(match):
        path = match.group(2)
        # Ensure path is properly formatted for HTML
        safe_path = path.replace("\\", "/")
        return f'<br><img src="file:///{safe_path}" style="max-width: 100%;"><br>'

    html = re.sub(r"!\[(.*?)\]\((.*?)\)", img_repl, html)

    # Convert newlines to <br> for HTML rendering, except where we just added <br>
    # We'll just wrap the whole thing in a p tag and replace \n with <br>
    html = html.replace("\n", "<br>")

    return f"<div>{html}</div>"
