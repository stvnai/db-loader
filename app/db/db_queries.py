from datetime import datetime
from typing import List, Dict
from sqlalchemy import text
from sqlalchemy import Engine
from pandas import DataFrame
from app.set_logging import set_module_logger
from app.db.connection import get_sqlachemy_engine
from werkzeug.security import check_password_hash


logger= set_module_logger(__name__)


try:
    ENGINE= get_sqlachemy_engine()
except Exception as e:
    ENGINE= None
    logger.critical(f"Something goes wrong connecting with database: {e}.")


def auth_user(username:str, password:str, engine:Engine=ENGINE):
    if ENGINE is None:
        print("No database engine available.")
        return None
    
    query= text(
        """ SELECT user_id, password_hashed
            FROM admin
            WHERE username= :username
            LIMIT 1
        """
    )

    values= {"username":username}

    try:
        with engine.connect() as conn:
            result= conn.execute(query, values)
            user_credentials= result.fetchone()
            user_id= user_credentials[0]
            stored_hash= user_credentials[1]

            if user_credentials:
                if check_password_hash(stored_hash, password):
                    return user_id
            else:
                return None

    except Exception as e:
        print(f"Error authenticating user: {e}")
        return None


def get_user_by_id(user_id, engine:Engine=ENGINE):

    if engine is None:
        print("No database engine available")
        return None
    
    query= text(
        """
        SELECT user_id, username
        FROM admin
        WHERE user_id = :user_id        
        """
    )

    values= {"user_id": user_id}

    try:
        with engine.connect() as conn:
            result= conn.execute(query, values)
            user_data= result.fetchone()
            return user_data
        
    except Exception as e:
        print(f"Error retrieving data from user: {e}")
        return None



def athlete_query(athlete_df: DataFrame, engine: Engine = ENGINE) -> int:
    
    if engine is None:
        logger.critical("No database engine available.")    
        return None
    
    select_query= text("""
                      SELECT athlete_id
                      FROM athlete.athlete
                      WHERE name = :name AND last_name = :last_name AND date_of_birth = :dob
                      """)
    
    select_query_values= {
        "name": athlete_df["name"].iloc[0],
        "last_name": athlete_df["last_name"].iloc[0],
        "dob": athlete_df["date_of_birth"].iloc[0]
    }


    try:

        with engine.begin() as conn:
            check_athlete_result= conn.execute(select_query, select_query_values)
            athlete_id= check_athlete_result.scalar_one_or_none()
            
            return athlete_id

    except Exception as e:
        logger.error(f"Error inserting data into athlete table: {e}.")
        return None
            

def insert_metadata_query(athlete_id:int | None, metadata_df: DataFrame, engine:Engine = ENGINE) -> int:

    if engine is None:
        logger.critical("No database engine available.")
        return None
    
    if athlete_id is None:
        logger.warning("No athelete_id data. INSERT INTO metadata table will not be executed.")
        return None
    
    try:
        metadata_df["athlete_id"] = athlete_id
        metadata_columns= ", ".join(metadata_df.columns)
        metadata_placeholders= ", ".join([f":{c}" for c in metadata_df.columns])
        metadata_values= {col: metadata_df[col].iloc[0] for col in metadata_df.columns}

    except Exception as e:
        logger.error(f"Error preparing metadata before inserting into metadata table: {e}")
        return None
    
    insert_metadata= text(f"""
                          INSERT INTO metadata.metadata ({metadata_columns})
                          VALUES ({metadata_placeholders})
                          ON CONFLICT
                          ON CONSTRAINT unique_athlete_and_timestamp DO NOTHING
                          RETURNING activity_id  
                          """)
    
    try:
        with engine.begin() as conn:
            result_insert_metadata= conn.execute(insert_metadata, metadata_values)
            activity_id= result_insert_metadata.scalar_one_or_none()
            
            if activity_id is None:
                logger.warning(f"An activity with identical athlete ID and timestamp already exists.")
                return None
            
            return activity_id
    
    except Exception as e:
        logger.error(f"Error inserting data into metadata table: {e}.")
        return None
    

def insert_data_query(activity_id: int | None, data_df:DataFrame, engine:Engine = ENGINE) -> bool:

    if engine is None:
        logger.critical("No database engine available.")
        return False
    
    if activity_id is None:
        logger.warning("No activity_id data. INSERT INTO activity table will not be executed.")
        return False
    
    try:
        data_df["activity_id"] = activity_id
        data_columns= ", ".join(data_df.columns)
        data_placeholders= ", ".join([f":{c}" for c in data_df.columns])
        data_values= data_df.to_dict("records")

    except Exception as e:
        logger.error(f"Error preparing data before inserting into activity table: {e}")
        return False

    insert_data= text(f"""
                      INSERT INTO activity.activity ({data_columns})
                      VALUES ({data_placeholders})
                      """) 

    with engine.begin() as conn:
        try:
            conn.execute(insert_data, data_values)

        except Exception as e:
            logger.error(f"Error inserting data into activity table: {e}.")
            return False
        
    return True

def athlete_list(engine:Engine= ENGINE):

    """
    Description
    -----

        Retrieve athletes from database and creates a list of dictionaries
        and a list of athletes to display in select HTML.

    :param Engine ENGINE: Database engine.
    :return: List of athletes and list of dictionaries.
    :rtype: [list, list[dict]]
    """

    

    visible_labels= []
    raw_data= []

    if engine is None:
        logger.critical("No database engine available.")
        return visible_labels, raw_data 

    query= text("""
                SELECT name, last_name, date_of_birth, gender
                FROM athlete.athlete
                ORDER BY last_name, name
                """)
    try:
        with engine.connect() as conn:
            result= conn.execute(query)
            rows= result.fetchall()

    except Exception as e:
        logger.error(f"Error retrieving athletes from database: {e}.")
        return visible_labels, raw_data


    today= datetime.today()
    for athlete in rows:

        dob= athlete.date_of_birth
        age= f"{today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))} years."

        full_name= f"{athlete.name} {athlete.last_name}".title()
        label= f"{full_name}, {age}"
       
        visible_labels.append(label)
        raw_data.append(
            {
                "name":athlete.name,
                "last_name":athlete.last_name,
                "date_of_birth": dob.strftime("%Y-%m-%d"),
                "gender":athlete.gender
            }
        )

    return visible_labels, raw_data


def insert_new_athlete(athlete_df:DataFrame, engine:Engine =  ENGINE):

    if engine is None:
        logger.critical("No database engine available.")    
        return None
    
    select_query= text("""
                      SELECT athlete_id
                      FROM athlete.athlete
                      WHERE name = :name AND last_name = :last_name AND date_of_birth = :dob
                      """)
    
    select_query_values= {
        "name": athlete_df["name"].iloc[0],
        "last_name": athlete_df["last_name"].iloc[0],
        "dob": athlete_df["date_of_birth"].iloc[0]
    }

    insert_query= text("""
                         INSERT INTO athlete.athlete (name, last_name, date_of_birth, gender)
                         VALUES (:name, :last_name, :dob, :gender)
                         RETURNING
                         athlete_id
                         """)

    insert_query_values= {
        "name": athlete_df["name"].iloc[0],
        "last_name": athlete_df["last_name"].iloc[0],
        "dob": athlete_df["date_of_birth"].iloc[0],
        "gender": athlete_df["gender"].iloc[0]    
    }

    try:

        with engine.begin() as conn:

            check_athlete_result= conn.execute(select_query, select_query_values)
            athlete_id= check_athlete_result.scalar_one_or_none()

            if athlete_id:
                return False
            
            if athlete_id is None:
                    insert_athlete_result= conn.execute(insert_query, insert_query_values)
                    athlete_id= insert_athlete_result.scalar_one_or_none()
            
            return True

    except Exception as e:
        logger.error(f"Error selecting or inserting data into athlete table: {e}.")
        return None

