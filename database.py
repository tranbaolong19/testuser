from flask import Flask, jsonify
import psycopg2
import psycopg2.extras

app = Flask(__name__)

# Cấu hình Database
DB_URL = "postgresql://user_player:U7Ic44CSFx6JaLLsal7fGCcsMdA5nixb@dpg-cvjlf13uibrs73ecgneg-a.oregon-postgres.render.com/user_player"

# Hàm kết nối database
def get_db_connection():
    try:
        conn = psycopg2.connect(DB_URL)
        return conn
    except Exception as e:
        print(f"🔴 Lỗi kết nối database: {e}")
        return None

# API lấy danh sách tất cả tài khoản + trạng thái
@app.route("/all-users", methods=["GET"])
def all_users():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Không thể kết nối database"}), 500

    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute("SELECT username, is_online FROM users")
            users = cursor.fetchall()

        # Xử lý danh sách người dùng
        result = [{"username": user["username"], "status": "🟢 Online" if user["is_online"] else "🔴 Offline"} for user in users]

        return jsonify({"all_users": result})
    except Exception as e:
        print(f"🔴 Lỗi truy vấn database: {e}")
        return jsonify({"error": "Lỗi khi lấy danh sách người dùng"}), 500
    finally:
        conn.close()

# Chạy Flask Server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)  # Đặt port theo yêu cầu Render

