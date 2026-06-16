import pymysql
try:
    # Test Root
    conn = pymysql.connect(host='localhost', user='root', password='admin')
    print("✅ Connection successful with user: root")
    conn.close()
except:
    try:
        # Test Admin
        conn = pymysql.connect(host='localhost', user='admin', password='admin')
        print("✅ Connection successful with user: admin")
        conn.close()
    except Exception as e:
        print(f"❌ Both failed. Error: {e}")