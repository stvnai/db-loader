import os
import logging
from logging import Logger

log_dir = "/app/logs"
os.makedirs(log_dir, exist_ok=True)

log_path= os.path.join(log_dir, "db-log.log")

def set_logging(log_path= log_path, level=logging.INFO, mode="a"):

    """"
    Description
    -----
        Configure the loggin system for data loading process.
    """

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
    """"
    Description
    -----
        Configure the module loger for data loading process across different modules and functions.
    """



    logger= logging.getLogger(module_name)

    return logger

