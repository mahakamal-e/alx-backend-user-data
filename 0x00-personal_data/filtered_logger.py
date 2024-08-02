#!/usr/bin/env python3
"""filtered_logger Module """
import re
from typing import List
import logging
import os
import mysql.connector


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Returns the log message obfuscated."""
    for field in fields:
        pattern = rf'{field}=[^{separator}]*{separator}'
        replacement = f'{field}={redaction}{separator}'
        message = re.sub(pattern, replacement, message)
    return message


def get_logger() -> logging.Logger:
    """Returns a logging.Logger object."""
    logger_obj = logging.getLogger("user_data")
    logger_obj.setLevel(logging.INFO)
    logger_obj.propagate = False

    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)

    formatter = RedactingFormatter(fields=PII_FIELDS)
    handler.setFormatter(formatter)

    logger_obj.addHandler(handler)

    return logger_obj


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ Returns a connector to db """
    db_user = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    db_password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    db_host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    conn = mysql.connector.connect(
        user=db_user,
        password=db_password,
        host=db_host,
        port=3306,
        database=db_name
    )

    return conn


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
