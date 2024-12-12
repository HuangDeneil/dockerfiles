from flask import Flask, request, jsonify
import sqlite3
import json

from utils.init_db import init_table

app = Flask(__name__)

# 建立 SQLite 資料庫
talbe_name="nodes"
db_name="node_status.db"
table_define_json = {
    "id" : "INTEGER PRIMARY KEY AUTOINCREMENT",
    "node_name" : "TEXT",
    "status" : "TEXT",
    "timestamp" : "DEFAULT CURRENT_TIMESTAMP",
    "notes" : "TEXT"
}
init_table(talbe_name, db_name, table_define_json)


# 定義 API 路由
@app.route('/nodes', methods=['GET', 'POST'])
def add_node_status():
    conn = sqlite3.connect('node_status.db')
    cursor = conn.cursor()
    
    if request.method == 'POST':
        data = request.get_json()
        node_name = data['node_name']
        status = data['status']
        try:
            notes = data['notes']
        except:
            notes = ""
        
        cursor.execute("SELECT * FROM nodes WHERE node_name=?", (node_name,))
        result = cursor.fetchone()
        if result:
            cursor.execute("UPDATE nodes SET status = ?, timestamp = datetime('now'), notes = ? WHERE node_name = ?", (status, notes, node_name))
        else:
            cursor.execute("INSERT INTO nodes (node_name, status, timestamp, notes) VALUES (?, ?, datetime('now'), ?)", (node_name, status, notes))
        conn.commit()
        
        return jsonify({'message': 'Node status update successfully'}), 201

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
            return jsonify({'message': 'No any node found'}), 404
    
    conn.close()

@app.route('/nodes/<node_name>', methods=['GET', 'DELETE'])
def get_or_delete_node_status(node_name):
    conn = sqlite3.connect('node_status.db')
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor.execute("SELECT * FROM nodes WHERE node_name=?", (node_name,))
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
        cursor.execute("DELETE FROM nodes WHERE node_name=?", (node_name,))
        conn.commit()
        return jsonify({'message': 'Node status deleted successfully'}), 200

    conn.close()

@app.route('/nodes/status/<node_name>', methods=['GET'])
def get_node_status_only(node_name):
    conn = sqlite3.connect('node_status.db')
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor.execute("SELECT * FROM nodes WHERE node_name=?", (node_name,))
        result = cursor.fetchone()
        if result:
            
            return (str(result[2])), 200
        else:
            return jsonify({'message': 'Node not found'}), 404
    conn.close()



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)