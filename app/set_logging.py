import os
import tempfile
import logging
from logging import Logger

log_filename= "db_log.log"
temp_path= tempfile.gettempdir()
log_path= os.path.join(temp_path,log_filename)

def set_logging(log_path= log_path, level=logging.INFO, mode="a"):

    logging.basicConfig(
            filename=log_path,
            level=level,
            filemode= mode,
            format="{'timestamp':'%(asctime)s', 'module':'%(name)s', 'level':'%(levelname)s', 'description':'%(message)s'}"
    )

    


def set_module_logger(module_name: str) -> Logger:

    logger= logging.getLogger(module_name)

    return logger

