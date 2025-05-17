from app.db import get_db_connetction


def get_user_info(user_name):
    connection = get_db_connetction()
    cur = connection.cursor()
    cur.execute("""
        SELECT users.first_name, users.second_name, users.age, users.email
        FROM users
        WHERE users.email = %s
        """, (user_name,))

    user = cur.fetchone()
    cur.close()
    connection.close()
    return user  # Return user info or None if not found
