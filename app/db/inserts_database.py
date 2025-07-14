import logging
from app.db.db_queries import athlete_query, insert_metadata_query, insert_data_query

logger= logging.getLogger(__name__)

def populate_db(athlete_df, metadata_df, data_df):

    athlete_id= athlete_query(athlete_df)
    activity_id= insert_metadata_query(athlete_id, metadata_df)
    result= insert_data_query(activity_id, data_df)
    if result:
        logger.info("Query executed sucessfully.")

    else:
        logger.warning("Query could not be executed.")
       









    
    
    
        