import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime


def setup_logger(
    name: str,
    log_file: Optional[str] = "app.log",
    console_level: int = logging.INFO,
    file_level: int = logging.DEBUG,
) -> logging.Logger:
    """Configures and returns a logger instance with console and file handlers."""
    logger = logging.getLogger(name)

    # Set logger to the lowest required level to ensure messages pass to handlers
    logger.setLevel(min(console_level, file_level))

    # Return immediately if handlers are already configured to avoid duplicate logs
    if logger.hasHandlers():
        return logger

    # Shared log format layout
    log_format = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s (%(filename)s:%(lineno)d) -> %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 1. Console Output
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(console_level)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)

    # 2. File Output (Optional)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)  # Create folders if missing

        file_handler = logging.FileHandler(log_path, mode="a", encoding="utf-8")
        file_handler.setLevel(file_level)
        file_handler.setFormatter(log_format)
        logger.addHandler(file_handler)

    return logger



logger = setup_logger(__name__,  rf"src/code_generator/log/{__name__}_{datetime.now().strftime('%Y%m%d_%H%M')}.log")