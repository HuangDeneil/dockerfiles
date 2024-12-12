
## Required file sturture
```bash
.
├── api_backup/
│   └── app.py          ## SQLite + Flask 
├── docker-compose.yml
├── dockerfile
└── requirements.txt
```

## 建立image
```bash
docker build . -t status-record-api:3.9-slim-buster
```

## 建立環境
```bash
docker compose up -d
```
- Note: 在服務啟動時，會在 api_backup/ 產生 node_status.db 的 sqlite 檔案，此檔案室可以直接做備份使用。


## 當 api_backup/app.py 更新時，constainer 重啟
```bash
docker compose restart
```

## 停止服務
```bash
docker compose down
```

## 目前預設 SQLite 收錄內容
- Table名稱: `nodes`

|  **column**   | **Required**                       |  **Description**                      |     **Example**  |
|---------------|------------------------------------|----------------------------------------|------------------|
| **index**     | $`\textcolor{red}{\text{no}}`$     | 系統給予的index                         |     0       |
| **timestamp** | $`\textcolor{red}{\text{no}}`$     | 填寫當下的系統時間 (API自動填寫，可覆寫)  | 2024-12-10 16:12:42 |
| **node_name**   | $`\textcolor{red}{\text{yes}}`$    | node名稱                                | fixoignitenode-1        |
| **status**    | $`\textcolor{red}{\text{yes}}`$    | 相要更動的狀態 (可填寫任意文字，可覆寫)    | OS_install_done    |
| **notes**     | $`\textcolor{red}{\text{no}}`$     | 備註 (可填寫任意文字或error msg)          |                   |


## API 操作資料庫

### POST 新增狀態更新
```bash
# POST 新增節點狀態
## node1
curl -X POST http://localhost:5000/nodes \
-H "Content-Type: application/json" \
-d '
{
    "node_name": "node1", 
    "status": "online",
    "notes": ""
}' 

# node2
curl -X POST http://localhost:5000/nodes \
-H "Content-Type: application/json" \
-d '
{
    "node_name": "node2", 
    "status": "online",
    "notes": ""
}' 
```


### GET 查詢節點狀態
```bash
## 所有收入的節點狀態顯示
curl -X GET http://localhost:5000/nodes 

## 單節點查詢
curl -X GET http://localhost:5000/nodes/node1
curl -X GET http://localhost:5000/nodes/node2

## 顯示單節狀態
curl -X GET http://localhost:5000/nodes/status/node1
```

### DELETE 刪除節點狀態資訊
```bash
curl -X DELETE http://localhost:5000/nodes/node1
```
