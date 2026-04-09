from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__)
CORS(app)


def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        user=os.environ.get('DB_USER', 'root'),
        password=os.environ.get('DB_PASSWORD', 'password'),
        database=os.environ.get('DB_NAME', 'todo_db')
    )


@app.route('/api/tasks', methods=['GET', 'POST'])
def manage_tasks():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        task_content = request.json.get('task')
        cursor.execute(
            'INSERT INTO tasks (task_name) VALUES (%s)', (task_content,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Task added!'}), 201

    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    conn.close()
    return jsonify(tasks)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
