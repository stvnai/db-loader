import os
import time
import multiprocessing as mp
from app.set_logging import set_module_logger
from app.db.inserts_database import populate_db
from app.fitextractor.fit_data_extractor import extract_data


logger= set_module_logger(__name__)


def process_and_insert(filepath, athlete_df):

    filename= os.path.basename(filepath)

    try:

        data_df, metadata_df= extract_data(filepath)
        result= populate_db(athlete_df, metadata_df, data_df)

        return result
    
    except Exception as e:
        logger.error(f"Error processing {filename}: {e}")
        return False

def process_batch(filepaths:list, athlete_df)-> None:

    """
    Description
    ----
        Creates a multiprocessing pool to execute insertion tasks.

    Args
    -----
    :param list filepaths: List with absolute paths to uploaded files.
    :return: Boolean, number of succeed processes and number of failed processes
    :rtype: tuple
    
    """

    try: 
        batch_size=25
        total_files= len(filepaths)
        successes= 0
        failures= 0
        max_processes= (mp.cpu_count() - 1) 
        if filepaths:
            for i in range(0, total_files, batch_size):
                batch_files= filepaths[i:i +batch_size]
                with mp.Pool(processes=max_processes) as pool:

                    results= pool.starmap(process_and_insert,[(fp,athlete_df) for fp in batch_files])
                    batch_successes = sum(results)
                    batch_failures = len(results) - batch_successes
                    successes += batch_successes
                    failures+= batch_failures
                    logger.info("*** Sub-batch processed ***")
                    logger.info(f"*** Sub-batch successes= {batch_successes}. Sub-batch fails= {batch_failures} ***")
                    time.sleep(5)
        
            logger.info("##### *** Batch processed sucessfully *** #####")
            logger.info(f"*** Total success= {successes}. Total fails= {failures} ***")
            return True, successes, failures
    
    except Exception as e:
        logger.error(f"Error processing batch: {e.args}")
        return False, 0, total_files

    finally:
        for fp in filepaths:
            try:
                os.remove(fp)
            except Exception as e:
                logger.error(f"Could not delete file {fp}: {e}")
        
        logger.info("All files in batch deleted.")
                





