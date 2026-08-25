import os

UI_DIST_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..", "..", "..", "..",
        "mcp_ui",
        "dist",
        "src"
    )
)

def load_html(filename: str) -> str:
    """Load a UI HTML file once and cache it for the process lifetime."""
    path = os.path.join(UI_DIST_DIR, filename)
    if not os.path.isfile(path):
        raise FileNotFoundError(
            f"MCP App UI {filename!r} not found in {UI_DIST_DIR}. "
            "Run `npm install && npm run build` inside mail_mcp_app/mcp_ui to produce the bundle."
        )
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

async def get_generate_mail_ui() -> str:
    return load_html("DraftEmailView.html")