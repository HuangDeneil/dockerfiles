
docker run -dit --name python-test python:3.9-slim-buster


# docker build . -t status-record-api:3.11-slim-buster


docker build . -t status-record-api:3.9-slim-buster

docker-compose up -d

# POST 请求
# POST 新增節點狀態
curl -X POST http://localhost:5000/nodes \
-H "Content-Type: application/json" \
-d '{"node_id": "node1", "status": "online"}' 

# GET 查詢節點狀態
curl http://localhost:5000/nodes/node1

# DELETE 刪除節點狀態
curl -X DELETE http://localhost:5000/nodes/node1

