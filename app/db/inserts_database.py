from app.set_logging import set_module_logger
from app.db.db_queries import athlete_query, insert_metadata_query, insert_data_query

logger= set_module_logger(__name__)

def populate_db(athlete_df, metadata_df, data_df):

    athlete_id= athlete_query(athlete_df)
    activity_id= insert_metadata_query(athlete_id, metadata_df)
    result= insert_data_query(activity_id, data_df)
    if result:
        logger.info("Query commited sucessfully.")
        return result
    else:
        logger.warning("Query not commited.")
        return False
       









    
    
    
        