import os
import psycopg
from app.db.connection import get_sqlachemy_engine

engine= get_sqlachemy_engine()

if engine:
    print("Connected")
else:
    print("Not connected")

