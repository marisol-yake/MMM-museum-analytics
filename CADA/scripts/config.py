import logging


def setup_logging(name: str) -> logging.Logger:
    """Set up basic logging configuration."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)  # Set the minimum logging level

    # Create handlers
    file_handler = logging.FileHandler(f"{name}.log")  # Separate log file for each script
    console_handler = logging.StreamHandler()  # Log to console

    # Create formatters and add them to the handlers
    formatter = logging.Formatter("%(asctime)s ::: %(levelname)s -- %(name)s - %(message)s",
                                  datefmt = "%m/%d/%Y %I:%M:%S %p")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
