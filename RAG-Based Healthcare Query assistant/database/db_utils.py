import sqlite3

from config import DATABASE_PATH

# =====================================================
# EXECUTE SQL
# =====================================================

def execute_query(query):

    connection = None

    try:

        connection = sqlite3.connect(DATABASE_PATH)

        cursor = connection.cursor()

        cursor.execute(query)

        rows = cursor.fetchall()

        return rows

    except sqlite3.Error as error:

        raise Exception(
            f"SQLite Error:\n{error}"
        )

    finally:

        if connection:

            connection.close()

# =====================================================
# TEST CONNECTION
# =====================================================

def test_connection():

    try:

        connection = sqlite3.connect(DATABASE_PATH)

        connection.close()

        return True

    except:

        return False

# =====================================================
# TEST
# =====================================================

if __name__ == "__main__":

    print("=" * 60)

    print("Database Test")

    print("=" * 60)

    if test_connection():

        print("Database Connected Successfully.")

        rows = execute_query(
            "SELECT COUNT(*) FROM patients;"
        )

        print(rows)

    else:

        print("Database Connection Failed.")