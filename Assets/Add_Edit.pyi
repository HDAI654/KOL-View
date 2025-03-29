from typing import Optional, Callable, Dict, Any
from PyQt5.QtWidgets import QMainWindow

class ASE_win(QMainWindow):
    def __init__(
        self,
        db: str,
        table: str,
        add_edit_sts: str,
        back_func: Callable[[], None],
        custom_data: Dict[str, Any],
        page_title: Optional[str] = None,
        df: str = "yyyy/MM/dd",
        row_data: Optional[list] = None,
        TTS_sts: bool = False,
        custom_field_name: Optional[list] = None,
        **kwargs: Any
    ) -> None:
        """
        Initialize the Add/Edit window.

        :param db: Database name.
        :param table: Table name.
        :param add_edit_sts: Add or edit status.
        :param back_func: Function to call when going back.
        :param custom_data: Custom data for the window.
        :param page_title: Optional page title.
        :param df: Date format.
        :param row_data: Row data to edit.
        :param TTS_sts: Text-to-speech status.
        :param custom_field_name: Optional custom field names.
        """
        ...

    def FormUI(self) -> None:
        """Setup the form UI components."""
        ...

    def SubmitClick(self) -> None:
        """Handle the submit button click event."""
        ...
