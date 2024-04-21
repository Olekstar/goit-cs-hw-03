import psycopg2
from faker import Faker
import random

fake = Faker()

# Connection details
dbname = "postgres"
user = "postgres"
password = "753951"
host = "localhost"
port = "5432"

# Connect to the database
conn = psycopg2.connect(
    dbname=dbname,
    user=user,
    password=password,
    host=host,
    port=port
)
cur = conn.cursor()

try:
    # Clear existing data
    cur.execute("DELETE FROM tasks;")
    cur.execute("ALTER SEQUENCE tasks_id_seq RESTART WITH 1;")  # Reset sequence for tasks
    cur.execute("DELETE FROM users;")
    cur.execute("ALTER SEQUENCE users_id_seq RESTART WITH 1;")
    conn.commit()
    
    # Inserting data into the users table
    for _ in range(20):
        fullname = fake.name()
        email = fake.unique.email()
        cur.execute("INSERT INTO users (fullname, email) VALUES (%s, %s)", (fullname, email))
    conn.commit()

    # Fetch valid status IDs
    cur.execute("SELECT id FROM status;")
    valid_status_ids = [row[0] for row in cur.fetchall()]

    # Inserting data into the tasks table using only valid status and user IDs
    cur.execute("SELECT id FROM users;")
    valid_user_ids = [row[0] for row in cur.fetchall()]
    for _ in range(10):
        title = fake.sentence(nb_words=6)
        description = fake.text(max_nb_chars=200)
        status_id = random.choice(valid_status_ids)
        user_id = random.choice(valid_user_ids)
        cur.execute("INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)",
                    (title, description, status_id, user_id))
    conn.commit()

except psycopg2.Error as e:
    print(f"An error occurred: {e}")
    conn.rollback()
finally:
    cur.close()
    conn.close()

print("Database seeding completed successfully.")
