import os
import tempfile
import logging
from logging import Logger

log_dir = "/app/logs"
os.makedirs(log_dir, exist_ok=True)

log_path= os.path.join(log_dir, "db-log.log")


def set_logging(log_path= log_path, level=logging.INFO, mode="a"):

    try:

        logging.basicConfig(
                filename=log_path,
                level=level,
                filemode= mode,
                format="{'timestamp':'%(asctime)s', 'module':'%(name)s', 'level':'%(levelname)s', 'description':'%(message)s'}"
        )

    except Exception as e:
        print(f"Error setting logger: {e}") 


def set_module_logger(module_name: str) -> Logger:

    logger= logging.getLogger(module_name)

    return logger

