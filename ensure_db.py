# ensure_db.py

from app import create_app, db
from flask_migrate import upgrade
import time

app = create_app()

# DBがまだ起動していない場合にリトライ
retries = 5
while retries > 0:
    try:
        with app.app_context():
            upgrade()  # 自動マイグレーション
        print("[INFO] DB マイグレーション完了")
        break
    except Exception as e:
        print(f"[WARN] DB接続失敗、再試行: {e}")
        retries -= 1
        time.sleep(3)
