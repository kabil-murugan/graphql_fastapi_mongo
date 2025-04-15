"""A logger config module to log messages on both file and console."""

import logging


def get_logger(name: str) -> logging.Logger:
    """Get a logger.

    Args:
        name (str): name of the logger

    Returns:
        logging.Logger: a logger
    """
    logger: logging.Logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Add file handler for the logger.
    file_handler = logging.FileHandler(f"src\\{name.replace('.', '\\')}.log")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Add stream handler for the logger.
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger
