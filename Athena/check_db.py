import psycopg2

try:
    conn = psycopg2.connect(
        dbname="athena_bd",
        user="postgres",
        password="6978Qwarry",
        host="localhost",
        port="5432"
    )
    print("✅ Подключение к PostgreSQL успешно!")
    conn.close()
except Exception as e:
    print(f"❌ Ошибка подключения: {e}")