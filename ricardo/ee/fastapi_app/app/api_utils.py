"""API utility functions."""

import logging


class ApiLogHandler(logging.StreamHandler):
    """Custom log handler class for the API server which writes logs to a stream."""

    def __init__(self) -> None:
        """Initialise the handler with an empty queue."""
        logging.StreamHandler.__init__(self)
        self.queue: list[str] = []

    def emit(self, record: logging.LogRecord) -> None:
        """Emit a record with the specified format."""
        msg = self.format(record)
        self.queue.append(msg)
