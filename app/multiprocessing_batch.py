import time
import multiprocessing as mp
from app.fitextractor.fit_data_extractor import extract_data
from app.db.inserts_database import populate_db

def process_and_insert(filepath, athlete_df):

    data_df, metadata_df= extract_data(filepath)
    populate_db(athlete_df, metadata_df, data_df)

def process_batch(filepaths:list, athlete_df)-> None:

    '''
    Description
    ----
        Creates a multiprocessing pool to execute insertion tasks
    :param list filepaths: List with absolute paths to uploaded files.
    :return: 
    :rtype: None
    '''

    try:     
        if filepaths:
            max_processes= mp.cpu_count()
            with mp.Pool(processes=max_processes) as pool:
                pool.starmap(process_and_insert,[(fp,athlete_df) for fp in filepaths])
        return True
    except Exception as e:
        print(f"Error with processing batch: {e.args}")
        return False







