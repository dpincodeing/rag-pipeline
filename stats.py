import sqlite3

conn = sqlite3.connect("rag_logs.db")
cursor = conn.cursor()

print("--- Recent queries ---")
cursor.execute("SELECT question, response_time_ms, created_at FROM query_logs ORDER BY created_at DESC LIMIT 5")
rows = cursor.fetchall()
for row in rows:
    print(row)

print("\n--- Average response time ---")
cursor.execute("SELECT AVG(response_time_ms) as avg_time FROM query_logs")
print(cursor.fetchone())

print("\n--- Total queries ---")
cursor.execute("SELECT COUNT(*) as total FROM query_logs")
print(cursor.fetchone())

conn.close()