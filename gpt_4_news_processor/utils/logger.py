import logging
import os


def get_logger(name):
    os.makedirs("logs", exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    f= logging.FileHandler("/logs/fetch_newslogger.log")
    format = logging.Formatter("%(asctime)s-%(levelname)s-%(message)s")

    if not logger.handlers:
        logger.addHandler(f)

    return logger
