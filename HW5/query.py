import psycopg2

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
    # Отримати всі завдання певного користувача
    user_id = 1
    cur.execute("SELECT * FROM tasks WHERE user_id = %s", (user_id,))
    user_tasks = cur.fetchall()
    print("Завдання користувача:", user_tasks)

    # Вибрати завдання за певним статусом 'new'
    cur.execute("SELECT * FROM tasks WHERE status_id = (SELECT id FROM status WHERE name = 'new')")
    tasks_by_status = cur.fetchall()
    print("Завдання зі статусом 'new':", tasks_by_status)

    # Оновити статус конкретного завдання
    task_id = 1
    new_status_id = 2  # Наприклад, id для 'in progress'
    cur.execute("UPDATE tasks SET status_id = %s WHERE id = %s", (new_status_id, task_id))
    conn.commit()
    print("Статус завдання оновлено.")

    # Отримати список користувачів, які не мають жодного завдання
    cur.execute("SELECT * FROM users WHERE id NOT IN (SELECT user_id FROM tasks)")
    users_without_tasks = cur.fetchall()
    print("Користувачі без завдань:", users_without_tasks)

    # Додати нове завдання для конкретного користувача
    title = "New Task Title"
    description = "Description of the task"
    status_id = 1  # Наприклад, id для 'new'
    cur.execute("INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)", 
                (title, description, status_id, user_id))
    conn.commit()
    print("Нове завдання додано.")

    # Отримати всі завдання, які ще не завершено
    cur.execute("SELECT * FROM tasks WHERE status_id != (SELECT id FROM status WHERE name = 'completed')")
    unfinished_tasks = cur.fetchall()
    print("Незавершені завдання:", unfinished_tasks)

    # Видалити конкретне завдання
    task_id = 3
    cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()
    print("Завдання видалено.")

    # Знайти користувачів з певною електронною поштою
    email_pattern = '%@example.com'
    cur.execute("SELECT * FROM users WHERE email LIKE %s", (email_pattern,))
    users_with_email = cur.fetchall()
    print("Користувачі з певною електронною поштою:", users_with_email)

    # Оновити ім'я користувача
    new_fullname = "Updated Name"
    user_id = 2
    cur.execute("UPDATE users SET fullname = %s WHERE id = %s", (new_fullname, user_id))
    conn.commit()
    print("Ім'я користувача оновлено.")

    # Отримати кількість завдань для кожного статусу
    cur.execute("SELECT status.name, COUNT(tasks.id) FROM status LEFT JOIN tasks ON status.id = tasks.status_id GROUP BY status.name")
    task_count_by_status = cur.fetchall()
    print("Кількість завдань за статусами:", task_count_by_status)

    # Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти
    domain = '%@example.com'
    cur.execute("SELECT tasks.* FROM tasks JOIN users ON tasks.user_id = users.id WHERE users.email LIKE %s", (domain,))
    tasks_for_domain_emails = cur.fetchall()
    print("Завдання для користувачів з доменом '@example.com':", tasks_for_domain_emails)

    # Отримати список завдань, що не мають опису
    cur.execute("SELECT * FROM tasks WHERE description = '' OR description IS NULL")
    tasks_without_description = cur.fetchall()
    print("Завдання без опису:", tasks_without_description)

    # Вибрати користувачів та їхні завдання, які є у статусі 'in progress'
    cur.execute("SELECT users.fullname, tasks.title FROM tasks INNER JOIN users ON tasks.user_id = users.id INNER JOIN status ON tasks.status_id = status.id WHERE status.name = 'in progress'")
    users_tasks_in_progress = cur.fetchall()
    print("Користувачі та їхні завдання в статусі 'in progress':", users_tasks_in_progress)

    # Отримати користувачів та кількість їхніх завдань
    cur.execute("SELECT users.fullname, COUNT(tasks.id) FROM users LEFT JOIN tasks ON users.id = tasks.user_id GROUP BY users.id")
    users_with_task_count = cur.fetchall()
    print("Користувачі та кількість їхніх завдань:", users_with_task_count)

except psycopg2.Error as e:
    print(f"Помилка бази даних: {e}")
finally:
    cur.close()
    conn.close()