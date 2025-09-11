import os
from sqlalchemy import create_engine, Engine
from urllib.parse import quote_plus
from dotenv import load_dotenv
load_dotenv()


def get_sqlachemy_engine() ->Engine:

    """"
    Description
    -----
        Establish connection with PostgreSQL database to execute and commit queries.

    :return Engine: DB engine.
    """

    dbname= os.getenv("DB_NAME")
    user= os.getenv("DB_USER")
    password= quote_plus(os.getenv("DB_PASS"))
    host= os.getenv("DB_HOST")
    port= os.getenv("DB_PORT")

    db_url= f"postgresql+psycopg://{user}:{password}@{host}:{port}/{dbname}"

    
    
    return create_engine(
        db_url,
        echo=False,
        future=True,
        pool_size= 5,
        max_overflow=2,
        pool_timeout=60,
        pool_pre_ping=True,
        pool_recycle=3600,
        connect_args={
                "connect_timeout": 30,
                "application_name": "flask_app",
                "options": "-c statement_timeout=30000"
                }
            )