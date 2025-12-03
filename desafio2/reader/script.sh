#!/bin/bash

echo "Waiting for application to start..."
sleep 10

request_counter=0

while true; do
    request_counter=$((request_counter + 1))
    current_time=$(date '+%Y-%m-%d %H:%M:%S')

    echo "=========================================="
    echo "Read #$request_counter - $current_time"
    echo "=========================================="

    # Check application status
    echo "📊 Application status:"
    curl -s http://app:5000/status
    echo -e "\n"

    # List users
    echo "👥 Users in database:"
    curl -s http://app:5000/users
    echo -e "\n"

    # List logs
    echo "📝 Application logs:"
    curl -s http://app:5000/logs
    echo -e "\n"
    
    sleep 15
done