import os
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import psycopg2
from psycopg2.extras import RealDictCursor
from db import connection

load_dotenv()

def get_db_connection():


    return psycopg2.connect(
        dbname= os.getenv("DB_NAME"),
        user= os.getenv("DB_USER"),
        password= os.getenv("DB_PASS"),
        host= os.getenv("DB_HOST"),
        port= os.getenv("DB_PORT"),
        cursor_factory=RealDictCursor

    )
 

def populate_db(athlete_df, metadata_df, data_df):
    with get_db_connection() as conn:
         with conn.cursor() as cursor:

    
            cursor.execute(
                """
            SELECT athlete_id
            FROM athlete.athlete 
            WHERE name = %s AND date_of_birth = %s
            """,
            (athlete_df["name"], athlete_df["date_of_birth"])
            )

            result= cursor.fetchone()

            if result:
                athlete_id = result["athlete_id"]

            else:
                cursor.execute(
                    """
                INSERT INTO athlete.athlete (name, date_of_bith, gender)
                VALUES (%s, %s, %s)
                RETURNING athlete_id    
                """,
                (athlete_df["name"], athlete_df["date_of_bith"], athlete_df["gender"])
                )
                athlete_id = cursor.fetchone().get["athlete_id"]

            metadata_columns= tuple(metadata_df.columns)
            metadata_placeholders= ", ".join(["%s"] * len(metadata_columns))
            metadata_column_names = ", ".join(metadata_df.columns)

            values= (athlete_id,) + tuple(metadata_df[c] for c in metadata_df.columns)

            cursor.execute(
                f"""
            INSERT INTO metadata.metadata (athlete_id, {metadata_column_names})
            VALUES (%s, {metadata_placeholders})
            RETURNING activity_id
            """,
            values
            )

            activity_id = cursor.fetchone()["activity_id"]

            data_df["activity_id"] = activity_id
            
            data_columns= data_df.columns.tolist()
            data_placeholders= ", ".join(["%s"] * len(data_columns))
            data_column_names= ", ".join(data_columns)

            insert_query = f"""
            INSERT INTO activity.activity ({data_column_names})
            VALUES ({data_placeholders})
            """

            values= [tuple(row) for row in data_df.to_numpy()]

            cursor.executemany(insert_query, values)
            conn.commit()






    
    
    
        