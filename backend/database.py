import mysql.connector


def get_database_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="rag_app"
    )

    return connection