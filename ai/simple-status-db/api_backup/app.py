from flask import Flask, request, jsonify
import sqlite3
import json

app = Flask(__name__)

# 建立 SQLite 資料庫
conn = sqlite3.connect('node_status.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS nodes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    node_id TEXT,
                    status TEXT,
                    timestamp DEFAULT CURRENT_TIMESTAMP,
                    notes TEXT
                )''')
conn.commit()
conn.close()

# 定義 API 路由
@app.route('/nodes', methods=['GET', 'POST'])
def add_node_status():
    conn = sqlite3.connect('node_status.db')
    cursor = conn.cursor()
    
    if request.method == 'POST':
        data = request.get_json()
        node_id = data['node_id']
        status = data['status']
        try:
            notes = data['notes']
        except:
            notes = ""
        
        cursor.execute("INSERT INTO nodes (node_id, status, timestamp, notes) VALUES (?, ?, datetime('now'), ?)", (node_id, status, notes))
        conn.commit()
        
        return jsonify({'message': 'Node status added successfully'}), 201

    elif request.method == 'GET':
        
        cursor.execute("SELECT * FROM nodes ")
        result = cursor.fetchall()
        if result:
            columns = ['index', 'name', 'status', 'time', 'notes']
            data = []
            for row in result:
                # 將每個元組轉換為字典
                record = dict(zip(columns, row))
                data.append(record)

            # 將 JSON 資料轉換為字串並輸出
            json_data = json.dumps(data, indent=4)
            return (json_data), 200

        else:
            return jsonify({'message': 'Node not found'}), 404
    
    conn.close()

@app.route('/nodes/<node_id>', methods=['GET', 'DELETE'])
def get_or_delete_node_status(node_id):
    conn = sqlite3.connect('node_status.db')
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor.execute("SELECT * FROM nodes WHERE node_id=?", (node_id,))
        result = cursor.fetchall()
        if result:
            columns = ['index', 'name', 'status', 'time', 'notes']
            data = []
            for row in result:
                # 將每個元組轉換為字典
                record = dict(zip(columns, row))
                data.append(record)

            # 將 JSON 資料轉換為字串並輸出
            json_data = json.dumps(data, indent=4)
            return (json_data), 200
        else:
            return jsonify({'message': 'Node not found'}), 404

    elif request.method == 'DELETE':
        cursor.execute("DELETE FROM nodes WHERE node_id=?", (node_id,))
        conn.commit()
        return jsonify({'message': 'Node status deleted successfully'}), 200

    conn.close()

@app.route('/nodes/status/<node_id>', methods=['GET'])
def get_node_status_only(node_id):
    conn = sqlite3.connect('node_status.db')
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor.execute("SELECT * FROM nodes WHERE node_id=?", (node_id,))
        result = cursor.fetchone()
        if result:
            
            return (str(result[2])), 200
        else:
            return jsonify({'message': 'Node not found'}), 404
    conn.close()



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)