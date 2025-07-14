import os
import logging
import multiprocessing as mp
from app.fitextractor.fit_data_extractor import extract_data
from app.db.inserts_database import populate_db


logger= logging.getLogger(__name__)


def process_and_insert(filepath, athlete_df):

    filename= os.path.basename(filepath)

    try:
        data_df, metadata_df= extract_data(filepath)
        populate_db(athlete_df, metadata_df, data_df)
        return True
    except Exception as e:
        logger.error(f"Error processing {filename}: {e}")
        return False

def process_batch(filepaths:list, athlete_df)-> None:

    '''
    Description
    ----
        Creates a multiprocessing pool to execute insertion tasks
    :param list filepaths: List with absolute paths to uploaded files.
    :return: Boolean, number of succeed processes and number of failed processes
    :rtype: tuple
    '''

    try: 

        if filepaths:
            max_processes= mp.cpu_count()
            
            with mp.Pool(processes=max_processes) as pool:

                results= pool.starmap(process_and_insert,
                                      [(fp,athlete_df) for fp in filepaths]
                                    )
                successes= sum(results)
                failures= len(results) - successes
        
        return True, successes, failures
    except Exception as e:
        logger.error(f"Error processing batch: {e.args}")
        return False

    finally:
        for fp in filepaths:
            try:
                os.remove(fp)
            except Exception as e:
                logger.error(f"Could not delete file {fp}: {e}")
                





