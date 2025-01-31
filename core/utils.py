# core/utils.py

import logging
from datetime import datetime

def setup_logger(level: str = "INFO"):
    """Sets up logging with the specified level."""
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {level}')
    logging.basicConfig(level=numeric_level, 
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def format_timestamp(dt: datetime) -> str:
    """Formats a datetime object into a human-readable string."""
    return dt.strftime('%Y-%m-%d %H:%M:%S')
