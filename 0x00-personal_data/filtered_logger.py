#!/usr/bin/env python3
"""filtered_logger Module """
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Returns the log message obfuscated"""
    for field in fields:
        pattern = rf'{field}=[^{separator}]*{separator}'
        replacement = f'{field}={redaction}{separator}'
        message = re.sub(pattern, replacement, message)
    return message
