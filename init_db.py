import pymysql

# 1. Connect to MySQL (without specifying a database yet)
try:
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='admin' # <--- CHANGE THIS TO YOUR MYSQL PASSWORD
    )
    
    with connection.cursor() as cursor:
        # 2. Create the database
        cursor.execute("CREATE DATABASE IF NOT EXISTS bookdb;")
        print("✅ Success! 'bookdb' has been created.")
        
    connection.close()

except Exception as e:
    print(f"❌ Error: {e}")
    print("\nDouble check your password and make sure MySQL is running!")