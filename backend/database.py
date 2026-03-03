import mysql.connector
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            user="root",
            password="root",
            database=MYSQL_DATABASE
        )
        return connection
    except mysql.connector.Error as err:
        if err.errno == 2003:
            print("Error: Cannot connect to MySQL. Make sure MySQL server is running.")
        else:
            print(f"Error: {err}")
        return None

def create_user(user_id, name, mobile, email):
    try:
        connection = get_db_connection()
        if connection is None:
            return False, "Database connection failed"
        
        cursor = connection.cursor()
        query = "INSERT INTO users (id, name, mobile, email) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (user_id, name, mobile, email))
        connection.commit()
        cursor.close()
        connection.close()
        return True, "User created successfully"
    except mysql.connector.Error as err:
        if err.errno == 1062:
            return False, "User with this ID already exists"
        return False, f"Error: {err}"
    except Exception as e:
        return False, f"Error: {str(e)}"

def fetch_all_users():
    try:
        connection = get_db_connection()
        if connection is None:
            return None
        
        cursor = connection.cursor(dictionary=True)
        query = "SELECT id, name, mobile, email FROM users"
        cursor.execute(query)
        users = cursor.fetchall()
        cursor.close()
        connection.close()
        return users
    except Exception as e:
        print(f"Error fetching users: {e}")
        return None

def database_connection_test():
    try:
        connection = get_db_connection()
        if connection:
            connection.close()
            return True
        return False
    except:
        return False
