import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from urllib.parse import quote_plus

load_dotenv()

def get_sqlachemy_engine():

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
        pool_size= 10,
        max_overflow=5,
        pool_timeout=30)
