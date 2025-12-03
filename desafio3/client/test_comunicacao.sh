#!/bin/bash

sleep 15

test_counter=0

while true; do
    test_counter=$((test_counter + 1))
    current_time=$(date '+%Y-%m-%d %H:%M:%S')

    echo "=========================================="
    echo "Test #$test_counter - $current_time"
    echo "=========================================="

    echo "🏥 Health Check (Web):"
    curl -s http://web:5000/health
    echo -e "\n"

    echo "📊 Connection Status (DB + Cache):"
    curl -s http://web:5000/status | python3 -m json.tool 2>/dev/null || curl -s http://web:5000/status
    echo -e "\n"

    echo "📝 Posts in Database:"
    curl -s http://web:5000/api/posts | python3 -m json.tool 2>/dev/null || curl -s http://web:5000/api/posts
    echo -e "\n"

    echo "💾 Posts with Cache:"
    curl -s http://web:5000/api/posts/cache | python3 -m json.tool 2>/dev/null || curl -s http://web:5000/api/posts/cache
    echo -e "\n"

    echo "📈 Request Counter (Redis):"
    curl -s http://web:5000/api/counter | python3 -m json.tool 2>/dev/null || curl -s http://web:5000/api/counter
    echo -e "\n"

    echo "📊 General Statistics:"
    curl -s http://web:5000/api/stats | python3 -m json.tool 2>/dev/null || curl -s http://web:5000/api/stats
    echo -e "\n"
    
    sleep 15
done