from db.database import connect_db

conn = connect_db()
cursor = conn.cursor()

cursor.execute("SELECT * FROM pricing_monitoring")  # Example query
data = cursor.fetchall()
print(data)

cursor.close()
conn.close()