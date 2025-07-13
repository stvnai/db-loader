from app.db.connection import get_db_connection
from werkzeug.security import check_password_hash

    
def auth_user(username:str, password:str) -> bool:

    query= """
        SELECT password_hashed 
        FROM admin
        WHERE username=%s
        LIMIT 1    
    """

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (username,))
                result = cur.fetchone()

                if result:
                    stored_hash= result["password_hashed"]
                    return check_password_hash(stored_hash, password)
                else:
                    return False
                
    except Exception as e:
        print("Error during authentication.")
        return False
