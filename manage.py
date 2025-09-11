# manage.py

from app import create_app, db
from flask_migrate import upgrade
import pymysql

app = create_app()

def ensure_db():
    """DB接続確認＋初回マイグレーション自動適用"""
    with app.app_context():
        url = str(db.engine.url)
        host = db.engine.url.host
        port = db.engine.url.port or 3306
        user = db.engine.url.username
        password = db.engine.url.password
        database = db.engine.url.database

        conn = None
        try:
            conn = pymysql.connect(
                host=host, port=port, user=user,
                password=password, database=database,
                charset='utf8mb4'
            )
            with conn.cursor() as cur:
                cur.execute("SHOW TABLES;")
                tables = cur.fetchall()
                if not tables:
                    print("[INFO] DB が空です。初回マイグレーションを実行します。")
                    upgrade()
                else:
                    print("[INFO] DB に既存テーブルを確認。マイグレーション不要。")
        except Exception as e:
            print(f"[ERROR] DB に接続できません: {e}")
            raise
        finally:
            if conn:
                conn.close()

if __name__ == "__main__":
    ensure_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
