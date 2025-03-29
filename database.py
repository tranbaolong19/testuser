from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Kết nối với PostgreSQL trên Render
DB_URL = "postgresql://user_player:U7Ic44CSFx6JaLLsal7fGCcsMdA5nixb@dpg-cvjlf13uibrs73ecgneg-a.oregon-postgres.render.com/user_player"
conn = psycopg2.connect(DB_URL)
cursor = conn.cursor()

# API lấy danh sách tất cả tài khoản + trạng thái
@app.route("/all-users", methods=["GET"])
def all_users():
    cursor.execute("SELECT username, is_online FROM users")
    users = cursor.fetchall()
    
    result = []
    for user, status in users:
        color = "🟢" if status else "🔴"  # Online: xanh, Offline: đỏ
        result.append(f"{color} {user}")

    return jsonify({"all_users": result})

if __name__ == "__main__":
    app.run(debug=True)
