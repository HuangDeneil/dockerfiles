from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# 建立 SQLite 資料庫
conn = sqlite3.connect('node_status.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS nodes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    node_id TEXT,
                    status TEXT,
                    timestamp TEXT
                )''')
conn.commit()
conn.close()

# 定義 API 路由
@app.route('/nodes', methods=['POST'])
def add_node_status():
    data = request.get_json()
    node_id = data['node_id']
    status = data['status']

    conn = sqlite3.connect('node_status.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO nodes (node_id, status, timestamp) VALUES (?, ?, datetime('now'))", (node_id, status))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Node status added successfully'}), 201

@app.route('/nodes/<node_id>', methods=['GET', 'DELETE'])
def get_or_delete_node_status(node_id):
    conn = sqlite3.connect('node_status.db')
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor.execute("SELECT * FROM nodes WHERE node_id=?", (node_id,))
        result = cursor.fetchone()
        if result:
            return jsonify({'node_id': result[1], 'status': result[2], 'timestamp': result[3]})
        else:
            return jsonify({'message': 'Node not found'}), 404

    elif request.method == 'DELETE':
        cursor.execute("DELETE FROM nodes WHERE node_id=?", (node_id,))
        conn.commit()
        return jsonify({'message': 'Node status deleted successfully'}), 200

    conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)