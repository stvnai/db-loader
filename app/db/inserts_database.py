import os
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import psycopg
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

load_dotenv()

def get_sqlachemy_engine():


    dbname= os.getenv("DB_NAME")
    user= os.getenv("DB_USER")
    password= quote_plus(os.getenv("DB_PASS"))
    host= os.getenv("DB_HOST")
    port= os.getenv("DB_PORT")

    db_url= f"postgresql+psycopg://{user}:{password}@{host}:{port}/{dbname}"
    return create_engine(db_url, echo=False, future=True)

engine= get_sqlachemy_engine()

def populate_db(athlete_df, metadata_df, data_df):
        with engine.connect() as conn:
            with conn.begin():
            

                try:
                    result_athlete= conn.execute(
                        text("""
                            SELECT athlete_id
                            FROM athlete.athlete
                            WHERE name = :name AND last_name = :last_name AND date_of_birth = :dob
                            """),

                        {
                            "name": athlete_df["name"].iloc[0],
                            "last_name": athlete_df["last_name"].iloc[0],
                            "dob": athlete_df["date_of_birth"].iloc[0]
                        }
                    )


                    athlete_id= result_athlete.scalar_one_or_none()

                    if athlete_id is None:
                        
                        result_athlete= conn.execute(
                            text("""
                                INSERT INTO athlete.athlete (name, last_name, date_of_birth, gender)
                                VALUES (:name, :last_name, :dob, :gender)
                                RETURNING athlete_id                             
                                """),

                            {
                                "name": athlete_df["name"].iloc[0],
                                "last_name": athlete_df["last_name"].iloc[0],
                                "dob": athlete_df["date_of_birth"].iloc[0],
                                "gender": athlete_df["gender"].iloc[0]
                            }
                        )

                        athlete_id= result_athlete.scalar_one()

                except Exception as e:
                    print(f"Error with retrieving athlete_id: {e}") 

                try:
                    metadata_df["athlete_id"]= athlete_id
                    metadata_columns = ", ".join(metadata_df.columns)
                    metadata_placeholders = ", ".join([f":{c}" for c in metadata_df.columns])
                    metadata_values= {col: metadata_df[col].loc[0] for col in metadata_df.columns}
                except Exception as e:
                    print(f"Error preparing metadata columns or placeholders: {e}")


                try:

                    result_activity= conn.execute(
                        text(f"""
                                INSERT INTO metadata.metadata ({metadata_columns})
                                VALUES ({metadata_placeholders})
                                RETURNING activity_id
                                """),
                                metadata_values
                    )
                    
                    activity_id= result_activity.scalar_one()

                except Exception as e:
                    print(f"Error inserting metadata or retrieving athlete_id: {e}")

                try:
                    data_df["activity_id"] = activity_id

                
                    data_columns = ", ".join(data_df.columns)
                    data_placeholders = ", ".join([f":{c}" for c in data_df.columns])
                    data_values= data_df.to_dict("records")
                    
                except Exception as e:
                    print(f"Error preparing data columns or placeholders: {e}")

                try:    
                    conn.execute(
                        text(f"""
                        INSERT INTO activity.activity ({data_columns})
                        VALUES ({data_placeholders})
                        """),
                        data_values
                    )
                except Exception as e:
                    print(f"Error with INSERT INTO data table: {e}")

                print("Transaccion exitosa")








    
    
    
        