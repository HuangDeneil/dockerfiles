
docker build . -t status-record-api:3.9-slim-buster

docker-compose up -d


# POST 新增節點狀態
## node1
curl -X POST http://localhost:5000/nodes \
-H "Content-Type: application/json" \
-d '
{
    "node_id": "node1", 
    "status": "online",
    "notes": ""
}' 

# node2
curl -X POST http://localhost:5000/nodes \
-H "Content-Type: application/json" \
-d '{"node_id": "node2", "status": "online"}' 

# GET 查詢節點狀態
curl -X GET http://localhost:5000/nodes/node1
curl -X GET http://localhost:5000/nodes/node2


curl -X GET http://localhost:5000/nodes 


# DELETE 刪除節點狀態
curl -X DELETE http://localhost:5000/nodes/node1

