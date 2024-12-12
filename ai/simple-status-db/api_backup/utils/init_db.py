import sqlite3
import json


def init_table(talbe_name, db_name, table_define_json):
    # 建立 SQLite 資料庫
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    sql_str = f"""CREATE TABLE {talbe_name} ("""
    for key, value in table_define_json.items():
        sql_str += f"{key} {value}, "
    
    # 去除最後一個逗號並添加右括號
    sql_str = sql_str[:-2] + ")"
    
    cursor.execute(f'''{sql_str}''')
    conn.commit()
    conn.close()



