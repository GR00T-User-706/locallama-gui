from PySide6.QtCore import Qt

from locallama_gui.ui.main_window import _build_readonly_table_item


def test_model_metadata_table_items_are_non_editable_and_selectable():
    item = _build_readonly_table_item("metadata value")

    assert not (item.flags() & Qt.ItemFlag.ItemIsEditable)
    assert item.flags() & Qt.ItemFlag.ItemIsSelectable
    assert item.flags() & Qt.ItemFlag.ItemIsEnabled
