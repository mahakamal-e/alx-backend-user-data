#!/usr/bin/env python3
"""filtered_logger Module """
import re
from typing import List
import logging
import os
import mysql.connector
from mysql.connector import connection

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


def get_db() -> connection.MySQLConnection:
    """Returns a connector to the MySQL database."""
    db_user = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    db_password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    db_host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    conn = mysql.connector.connect(
        user=db_user,
        password=db_password,
        host=db_host,
        database=db_name
    )

    return conn


def main() -> None:
    """ Main function to log user data """
    logger = get_logger()

    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM users;")

    rows = cursor.fetchall()

    for row in rows:
        row_dict = {
            'name': row[0],
            'email': row[1],
            'phone': row[2],
            'ssn': row[3],
            'password': row[4],
            'ip': row[5],
            'last_login': row[6],
            'user_agent': row[7]
        }

        msg = "; ".join(f"{k}={v}" for k, v in row_dict.items())

        logger.info(msg)

    cursor.close()
    db.close()


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
