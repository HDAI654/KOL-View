from typing import Any
from PyQt5.QtWidgets import QMainWindow

class Viewer(QMainWindow):
    def __init__(
        self,
        db: str,
        table: str,
        custom_name: str,
        icon_address: str,
        tbl_SectionResizeMode: Any,
        toolbar_movable: bool,
        toolbar_floatable: bool,
        bottom_toolbar: bool,
        bottom_toolbar_movable: bool,
        bottom_toolbar_floatable: bool,
        style_sheet: str,
        **kwargs: Any
    ) -> None:
        """
        Initialize the Viewer window with the given parameters.

        :param db: Database name.
        :param table: Table name.
        :param custom_name: Custom name for the viewer.
        :param icon_address: Address of the icon to display.
        :param tbl_SectionResizeMode: Resize mode for table sections.
        :param toolbar_movable: Whether the toolbar is movable.
        :param toolbar_floatable: Whether the toolbar is floatable.
        :param bottom_toolbar: Whether to show a bottom toolbar.
        :param bottom_toolbar_movable: Whether the bottom toolbar is movable.
        :param bottom_toolbar_floatable: Whether the bottom toolbar is floatable.
        :param style_sheet: The style sheet for the UI.
        """
        ...

    def UI(self) -> None:
        """Setup the initial UI for the viewer."""
        ...

    def TableUI(self) -> None:
        """Setup the table UI components."""
        ...

    def Search(self) -> None:
        """Perform a search based on the query."""
        ...

    def FillTable(self, data: list) -> None:
        """Fill the table with data."""
        ...

    def RefreshAll(self) -> None:
        """Refresh the table and other UI elements."""
        ...

    def DeleteClick(self, row: int) -> None:
        """Handle the deletion of a row from the table."""
        ...

    def AddClick(self) -> None:
        """Handle the add new entry event."""
        ...

    def DeleteAll(self) -> None:
        """Delete all entries from the table."""
        ...
