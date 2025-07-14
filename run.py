import os
import logging 
import tempfile
from app import create_app
from datetime import datetime

date= datetime.now()
log_filename= "db_log.log"
temp_path= tempfile.gettempdir()

log_path= os.path.join(temp_path,log_filename)

if os.path.exists(log_path):

    try:

        os.remove(log_path)

    except (PermissionError, Exception):
        print("Can't delete log file")


logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format="{timestamp : %(asctime)s , module : %(name)s , level:  %(levelname)s description : %(message)s}"
)

app= create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, use_reloader=False)
 