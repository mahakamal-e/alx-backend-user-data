#!/usr/bin/env python3
"""filtered_logger Module """
import re
from typing import List
import logging


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Returns the log message obfuscated."""
    for field in fields:
        pattern = rf'{field}=[^{separator}]*{separator}'
        replacement = f'{field}={redaction}{separator}'
        message = re.sub(pattern, replacement, message)
    return message


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class to redact specified fields in log messages."""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize the formatter with fields to be redacted."""
        super().__init__(self.FORMAT)
        self.fields = fields  # Store the fields to be redacted

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record and redact specified fields."""
        msg = record.getMessage()
        msg = filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)
        record.msg = msg
        return super().format(record)
