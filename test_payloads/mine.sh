curl -X GET -H "Content-Type: application/json" -d '{
    "hash": "akjsdflkasdg9a09g8098320940i234123958f",
    "index": 4,
    "message": "new block forged",
    "proof": 35089,
    "transactions": [
        {
            "amount": 1,
            "recipient": "832941082351jaskdjfkasdf9a7889",
            "sender": 0
        }
    ]
}' "http://0.0.0.0:5000/mine"
