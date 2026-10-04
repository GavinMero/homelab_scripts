import os
import subprocess
import psycopg
from datetime import datetime

conn = psycopg.connect(
    host="192.168.68.64",
    dbname="homelab",
    user="dummy_user",
    password=os.environ["PGPASSWORD"]
)

cur = conn.cursor()

cur.execute("SELECT id, hostname, ip_address FROM assets;")
assets = cur.fetchall()

for asset_id, hostname, ip_address in assets:
    result = subprocess.run(
        ["ping", "-n", "1", ip_address],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        status = "Online"
        last_seen = datetime.now()
    else:
        status = "Uh oh, Offline"
        last_seen = None

    cur.execute(
        """
        UPDATE assets
        SET status = %s,
            last_seen = COALESCE(%s, last_seen)
        WHERE id = %s
        """,
        (status, last_seen, asset_id)
    )

    print(f"{hostname}: {status}")

conn.commit()
cur.close()
conn.close()