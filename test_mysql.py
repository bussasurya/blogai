import mysql.connector

try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',  # Replace with your MySQL username (e.g., 'root')
        password='tenalirk',  # Replace with your MySQL password
        database='blog_tool'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM blogs LIMIT 1")  # Test if table exists
    conn.close()
    print("MySQL connection and table access successful!")
except Exception as e:
    print(f"Error: {e}")