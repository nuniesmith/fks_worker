"""Internal logging helper without shadowing stdlib logging."""
import logging

def get_logger(name: str = "shared") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] %(name)s: %(message)s')
        handler.setFormatter(fmt)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
