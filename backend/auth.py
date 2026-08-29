from database import get_database_connection


def check_login(username: str, password: str) -> bool:

    connection = get_database_connection()
    cursor = connection.cursor()

    query = """
        SELECT id
        FROM users
        WHERE username = %s
        AND password = %s
    """

    cursor.execute(query, (username, password))

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result is not None