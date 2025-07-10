from app.db.connection import get_db_connection
from werkzeug.security import generate_password_hash


username=  input("Enter username: ")
email=  input("Enter email: ")
password=  input("Enter password: ")
password_hashed= generate_password_hash(password)

try:
    with get_db_connection() as conn:
        with conn.cursor() as cur:

            query= """
            INSERT INTO admin (username, email, password_hashed)
            VALUES (%s, %s, %s)
            """

            cur.execute(query, (username, email, password_hashed))

            conn.commit()
            print("INSERT Executed successfully.")

except Exception as e:
    print(f"Error occured with database {e}")


