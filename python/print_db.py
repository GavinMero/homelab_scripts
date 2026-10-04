import psycopg
import os

conn = psycopg.connect(
    host="192.168.68.64",
    dbname="homelab",
    user="dummy_user",
    password=os.environ["PGPASSWORD"]
)

cur = conn.cursor()
cur.execute("SELECT hostname, device_type, operating_system, status FROM assets;")

for row in cur.fetchall():
    print(row)

cur.close()
conn.close()