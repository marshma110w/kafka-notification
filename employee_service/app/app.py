from flask import Flask, request, jsonify
from db_config import DB_CONFIG
import psycopg2

app = Flask(__name__)
conn = psycopg2.connect(**DB_CONFIG)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/employees', methods=['POST'])
def add_employee():
    data = request.get_json()

    # Проверка, что пришли все нужные поля
    required_fields = ['name', 'department', 'notification_type', 'email']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO employee (name, department, notification_type, email)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """, (
                data['name'],
                data['department'],
                data['notification_type'],
                data['email']
            ))
            employee_id = cur.fetchone()[0]
            conn.commit()
            return jsonify({
                "message": "Employee added successfully",
                "id": employee_id
            }), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500


@app.route('/employees', methods=['GET'])
def get_employees():
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, name, department, notification_type, email
                FROM employee
            """)
            employees = cur.fetchall()
        
        # Формируем список сотрудников в формате JSON
        result = [
            {
                "id": emp[0],
                "name": emp[1],
                "department": emp[2],
                "notification_type": emp[3],
                "email": emp[4]
            } for emp in employees
        ]
        
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
            

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
