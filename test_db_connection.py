import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="datapipeline_dev",
        user="postgres",
        password="postgres_dev_password_123"
    )
    print("✅ Successfully connected to PostgreSQL!")
    conn.close()
except Exception as e:
    print(f"❌ Connection failed: {e}")