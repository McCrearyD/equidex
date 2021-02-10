curl -X POST -H "Content-Type: application/json" -d '{
    "nodes": ["http://0.0.0.0:5001"]
}' "http://0.0.0.0:5000/nodes/register"
