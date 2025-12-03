#!/bin/bash

echo "Cliente iniciado. Aguardando servidor"
sleep 5

REQUEST_COUNTER=0
SUCCESS_COUNT=0
FAIL_COUNT=0
SERVER_URL="http://servidor-web:8080"
ENDPOINTS=("/" "/status")
SLEEP_TIME=10

make_request() {
    local endpoint="$1"
    local response
    local http_code
    local body

    if response=$(curl -s -w "\n%{http_code}" "${SERVER_URL}${endpoint}"); then
        http_code=$(echo "$response" | tail -n1)
        body=$(echo "$response" | head -n-1)
        echo "$http_code" "$body"
        return 0
    else
        echo "CURL_ERROR" ""
        return 1
    fi
}

display_request_result() {
    local request_num="$1"
    local endpoint="$2"
    local http_code="$3"
    local body="$4"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')

    echo "=========================================="
    echo "Requisição #${request_num} - ${timestamp}"
    echo "=========================================="

    if [ "$http_code" = "200" ]; then
        echo "✓ GET ${endpoint} - HTTP ${http_code}"
        if [ -n "$body" ]; then
            if [ "$endpoint" = "/status" ]; then
                echo "$body" | python -m json.tool 2>/dev/null || echo "$body"
            else
                echo "$body"
            fi
        fi
    elif [ "$http_code" = "CURL_ERROR" ]; then
        echo "✗ Erro ao conectar em ${SERVER_URL}${endpoint}"
    else
        echo "✗ GET ${endpoint} - HTTP ${http_code}"
    fi

    echo ""
}

display_statistics() {
    echo "Estatísticas: SUCCESS=${SUCCESS_COUNT} | FAIL=${FAIL_COUNT}"
    echo ""
}

while true; do
    REQUEST_COUNTER=$((REQUEST_COUNTER + 1))

    for endpoint in "${ENDPOINTS[@]}"; do
        result=$(make_request "$endpoint")
        http_code=$(echo "$result" | cut -d' ' -f1)
        body=$(echo "$result" | cut -d' ' -f2-)

        display_request_result "$REQUEST_COUNTER" "$endpoint" "$http_code" "$body"

        if [ "$endpoint" = "/" ]; then
            if [ "$http_code" = "200" ]; then
                SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
            else
                FAIL_COUNT=$((FAIL_COUNT + 1))
            fi
        fi
    done

    display_statistics
    sleep "$SLEEP_TIME"
done