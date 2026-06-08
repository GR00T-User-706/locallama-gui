import logging
from types import SimpleNamespace

from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QApplication, QPlainTextEdit

from locallama_gui.ui.diagnostics import (
    LineBufferedStream,
    OperationStreamParser,
    QtLogHandler,
    append_output,
)


def test_logging_record_uses_structured_diagnostics_format():
    emitted = []
    handler = QtLogHandler(SimpleNamespace(log_line=SimpleNamespace(emit=emitted.append)))
    record = logging.LogRecord("httpx", logging.INFO, __file__, 1, "HTTP Request: GET", (), None)

    handler.emit(record)

    assert len(emitted) == 1
    assert " INFO [httpx] HTTP Request: GET\n" in emitted[0]


def test_line_buffered_stream_emits_complete_lines_and_flushes_partial_text():
    emitted = []
    stream = LineBufferedStream(emitted.append)

    stream.write("partial")
    stream.write(" line\nsecond")
    assert emitted == ["partial line\n"]

    stream.flush()
    assert emitted == ["partial line\n", "second"]


def test_append_output_is_cursor_safe():
    app = QApplication.instance() or QApplication([])
    widget = QPlainTextEdit("first\nsecond")
    cursor = widget.textCursor()
    cursor.setPosition(0)
    cursor.setPosition(5, QTextCursor.MoveMode.KeepAnchor)
    widget.setTextCursor(cursor)

    append_output(widget, "\nthird")

    assert widget.toPlainText() == "first\nsecond\nthird"
    assert widget.textCursor().position() == len(widget.toPlainText())
    assert app is not None


def test_operation_stream_parser_assembles_partial_json_and_collapses_statuses():
    parser = OperationStreamParser()

    assert parser.feed('{"status":"pulling manifest"') == []
    first = parser.feed("}")
    repeated = parser.feed('{"status":"pulling manifest"}')
    digest = parser.feed(
        '{"status":"pulling","digest":"667b0c1932bcffff","total":100,"completed":25}'
    )

    assert first[0].history_text == "pulling manifest"
    assert repeated[0].history_text == ""
    assert digest[0].history_text == "pulling 667b0c1932bc"
    assert digest[0].completed == 25
    assert digest[0].total == 100


def test_operation_update_refreshes_live_status_and_progress_without_history_spam():
    status = SimpleNamespace(text="", setText=lambda text: setattr(status, "text", text))
    progress = SimpleNamespace(
        range=None,
        value=None,
        setRange=lambda low, high: setattr(progress, "range", (low, high)),
        setValue=lambda value: setattr(progress, "value", value),
    )
    history = []
    window = SimpleNamespace(
        operation_status=status,
        operation_progress=progress,
        append_operation_history=history.append,
    )
    parser = OperationStreamParser()
    first = parser.feed('{"status":"pulling","total":200,"completed":50}')[0]
    repeated = parser.feed('{"status":"pulling","total":200,"completed":100}')[0]

    from locallama_gui.ui.main_window import MainWindow

    MainWindow.update_operation(window, first)
    MainWindow.update_operation(window, repeated)

    assert status.text == "pulling"
    assert progress.range == (0, 100)
    assert progress.value == 50
    assert history == ["pulling"]
