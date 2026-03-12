"""Terminal size warning modal."""

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Footer, Static


class SizeWarningModal(ModalScreen):
    """Non-blocking modal shown when the terminal is below the recommended size."""

    BINDINGS = [("escape,space,enter", "dismiss_warning", "Continue")]

    def __init__(self, cols: int, rows: int, min_cols: int, min_rows: int) -> None:
        super().__init__()
        self._cols = cols
        self._rows = rows
        self._min_cols = min_cols
        self._min_rows = min_rows

    def compose(self) -> ComposeResult:
        issues = []
        if self._cols < self._min_cols:
            issues.append(f"width: {self._cols} (need {self._min_cols})")
        if self._rows < self._min_rows:
            issues.append(f"height: {self._rows} (need {self._min_rows})")
        issue_str = "  and  ".join(issues)
        with Vertical(id="size-warning-box"):
            yield Static(
                f"[bold yellow]Terminal too small[/bold yellow]\n\n"
                f"Current {issue_str}.\n\n"
                f"Recommended: [bold]{self._min_cols} × {self._min_rows}[/bold] or larger.\n\n"
                f"Resize your terminal for the best experience.\n\n"
                f"[dim]Press any key to continue anyway.[/dim]",
                id="size-warning-text",
            )
        yield Footer()

    def action_dismiss_warning(self) -> None:
        self.dismiss()
