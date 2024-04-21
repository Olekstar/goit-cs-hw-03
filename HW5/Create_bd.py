import psycopg2

# Function to connect to the database and create tables
def create_tables():
    # Connection details
    dbname = "postgres"
    user = "postgres"
    password = "753951"
    host = "localhost"
    port = "5432"

    # Establish a connection to the database
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    cur = conn.cursor()

    try:
        # Create users table
        cur.execute("""
            CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                fullname VARCHAR(100),
                email VARCHAR(100) UNIQUE
            );
        """)

        # Create status table
        cur.execute("""
            CREATE TABLE status (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50) UNIQUE
            );
        """)

        # Create tasks table
        cur.execute("""
            CREATE TABLE tasks (
                id SERIAL PRIMARY KEY,
                title VARCHAR(100),
                description TEXT,
                status_id INTEGER REFERENCES status(id),
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
            );
        """)

        # Insert predefined statuses into the status table
        cur.execute("""
            INSERT INTO status (name) VALUES ('new'), ('in progress'), ('completed');
        """)
        
        # Commit the changes to the database
        conn.commit()
        print("Tables created and initial data inserted successfully.")

    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
        conn.rollback()  # Rollback the transaction on error

    finally:
        # Close communication with the database
        cur.close()
        conn.close()

# Run the function to create tables and insert data
create_tables()
