#!/bin/bash

perform_smoke_test() {
    for endpoint in "${endpoints[@]}"; do
        url=$(echo "$endpoint" | cut -d',' -f1)
        method=$(echo "$endpoint" | cut -d',' -f2)
        data=$(echo "$endpoint" | cut -d',' -f3)

        if [ "$method" == "GET" ]; then
            response=$(curl -s -o /dev/null -w "%{http_code}" "$url")
        elif [ "$method" == "POST" ]; then
            response=$(curl -s -o /dev/null -w "%{http_code}" -X POST -H "Content-Type: application/json" -d "$data" "$url")
        else
            echo "Unsupported HTTP method: $method"
            continue
        fi

        if [ "$response" -eq 200 ]; then
            echo "SUCCESS: $url ($method) returned a status code of 200 OK"
        else
            echo "FAILURE: $url ($method) returned a status code of $response"
            exit 1
        fi
    done
}

# List of endpoints to test (url,method,data)
endpoints=(
    "http://127.0.0.1:8000/get-endpoint/1,GET,"
    "http://127.0.0.1:8000/post-endpoint,POST,'{\"item_id\": 1, \"item_data\": \"data\"}'"
    "http://127.0.0.1:8000/patch-endpoint/1,PATCH,'{\"item_data\": \"updated_data\"}'"
    "http://127.0.0.1:8000/put-endpoint/1,PUT,'{\"item_data\": \"replaced_data\"}'"
    "http://127.0.0.1:8000/delete-endpoint/1,DELETE,"
    "http://127.0.0.1:8000/,GET,"
    "http://127.0.0.1:8000/items/2,GET,"
    "http://127.0.0.1:8000/items/,POST,'{\"item\": {\"key\": \"value\"}}'"
    "http://127.0.0.1:8000/items/test/test1,POST,'{\"item\": {\"key\": \"value\"}}'"
)

# Perform smoke test
perform_smoke_test
