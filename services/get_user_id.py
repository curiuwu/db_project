from app.db import get_db_connetction


def get_user_id(user_name):
    connection = get_db_connetction()
    cur = connection.cursor()
    cur.execute("""
        SELECT users.user_id
        FROM users
        WHERE users.email = %s
        """, (user_name,))  # Ensure parameter is a tuple

    result = cur.fetchone()
    cur.close()
    connection.close()
    return result[0] if result else None  # Extract user_id or return None
