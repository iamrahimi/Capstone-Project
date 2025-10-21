import sqlite3
import pandas as pd

DB_NAME = "./db/mlb_history.db"

def connect_db(db_name=DB_NAME):
    """Connect to the SQLite database."""
    try:
        conn = sqlite3.connect(db_name)
        print(f"Connected to database: {db_name}")
        return conn
    except Exception as e:
        print(f"Could not connect to database: {e}")
        return None


def show_tables(conn):
    """List all tables available in the database."""
    query = "SELECT name FROM sqlite_master WHERE type='table';"
    tables = pd.read_sql(query, conn)
    print("\n Available tables:")
    print(tables)
    return tables


def run_query(conn, query):
    """Run a user-provided query and display the results."""
    try:
        df = pd.read_sql(query, conn)
        if df.empty:
            print("⚠️ No results found.")
        else:
            print("\n Query results:")
            print(df.to_string(index=False))
    except Exception as e:
        print(f" SQL Error: {e}")


def main():
    conn = connect_db()
    if not conn:
        return

    show_tables(conn)

    print("\n Example Queries:")
    print("- SELECT * FROM table_data LIMIT 5;")
    print("- SELECT * FROM table_title;")
    print("- Example JOIN:")
    print("  SELECT t.Title, d.Team, d.Statistic, d.Number "
          "FROM table_title t JOIN table_data d "
          "ON 1=1 WHERE d.Team='Chicago';\n")

    while True:
        query = input(" Enter SQL query (or type 'exit' to quit): ").strip()
        if query.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break
        if not query:
            continue

        run_query(conn, query)

    conn.close()


if __name__ == "__main__":
    main()