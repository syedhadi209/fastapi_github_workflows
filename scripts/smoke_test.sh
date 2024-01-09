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
    "https://jsonplaceholder.typicode.com/posts/1,GET,"
    "https://jsonplaceholder.typicode.com/comments/1,GET,"
    "https://jsonplaceholder.typicode.com/posts,POST,'{\"title\":\"foo\",\"body\":\"bar\",\"userId\":1}'"
)

# Perform smoke test
perform_smoke_test
