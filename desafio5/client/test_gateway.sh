#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

GATEWAY_URL="http://api-gateway:5000"
RESULT=0

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}    API GATEWAY TESTS${NC}"
echo -e "${BLUE}========================================${NC}"

echo -e "\n${YELLOW}[*] Waiting for gateway availability...${NC}"
for i in {1..30}; do
    if curl -s "$GATEWAY_URL/health" > /dev/null; then
        echo -e "${GREEN}[✓] Gateway is available${NC}"
        break
    fi
    echo -n "."
    sleep 1
done

echo -e "\n${BLUE}\n[TEST] Health Check${NC}"
echo -e "${YELLOW}GET /health${NC}"
RESPONSE=$(curl -s "$GATEWAY_URL/health")
echo "$RESPONSE" | python3 -m json.tool
if echo "$RESPONSE" | grep -q "healthy\|degraded"; then
    echo -e "${GREEN}✓ Health check OK${NC}"
else
    echo -e "${RED}✗ Health check FAILED${NC}"
    RESULT=1
fi

echo -e "\n${BLUE}\n[TEST] List Users${NC}"
echo -e "${YELLOW}GET /users${NC}"
curl -s "$GATEWAY_URL/users" | python3 -m json.tool

echo -e "\n${BLUE}\n[TEST] Get Specific User${NC}"
echo -e "${YELLOW}GET /users/1${NC}"
curl -s "$GATEWAY_URL/users/1" | python3 -m json.tool

echo -e "\n${BLUE}\n[TEST] Create New User${NC}"
echo -e "${YELLOW}POST /users${NC}"
NEW_USER=$(curl -s -X POST "$GATEWAY_URL/users" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Frank Wilson",
    "email": "frank@email.com",
    "profile": "client",
    "active": true
  }')
echo "$NEW_USER" | python3 -m json.tool

NEW_USER_ID=$(echo "$NEW_USER" | python3 -c "import sys, json; print(json.load(sys.stdin).get('user', {}).get('id', ''))" 2>/dev/null)

if [ -n "$NEW_USER_ID" ]; then
    echo -e "${GREEN}✓ User created with ID: $NEW_USER_ID${NC}"

    echo -e "\n${BLUE}\n[TEST] Update User${NC}"
    echo -e "${YELLOW}PUT /users/$NEW_USER_ID${NC}"
    curl -s -X PUT "$GATEWAY_URL/users/$NEW_USER_ID" \
      -H "Content-Type: application/json" \
      -d '{
        "name": "Frank Wilson Updated",
        "profile": "editor"
      }' | python3 -m json.tool
else
    echo -e "${YELLOW}[!] Could not extract new user ID${NC}"
fi

echo -e "\n${BLUE}\n[TEST] Filter Active Users${NC}"
echo -e "${YELLOW}GET /users?active=true${NC}"
curl -s "$GATEWAY_URL/users?active=true" | python3 -m json.tool

echo -e "\n${BLUE}\n[TEST] Filter Users by Profile${NC}"
echo -e "${YELLOW}GET /users?profile=editor${NC}"
curl -s "$GATEWAY_URL/users?profile=editor" | python3 -m json.tool

echo -e "\n${BLUE}\n[TEST] User Statistics${NC}"
echo -e "${YELLOW}GET /users/stats${NC}"
curl -s "$GATEWAY_URL/users/stats" | python3 -m json.tool

echo -e "\n${BLUE}\n[TEST] List Orders${NC}"
echo -e "${YELLOW}GET /orders${NC}"
curl -s "$GATEWAY_URL/orders" | python3 -m json.tool

echo -e "\n${BLUE}\n[TEST] Get Specific Order${NC}"
echo -e "${YELLOW}GET /orders/101${NC}"
curl -s "$GATEWAY_URL/orders/101" | python3 -m json.tool

echo -e "\n${BLUE}\n[TEST] List User Orders${NC}"
echo -e "${YELLOW}GET /orders/user/1${NC}"
curl -s "$GATEWAY_URL/orders/user/1" | python3 -m json.tool

echo -e "\n${BLUE}\n[TEST] Create New Order${NC}"
echo -e "${YELLOW}POST /orders${NC}"
NEW_ORDER=$(curl -s -X POST "$GATEWAY_URL/orders" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 2,
    "items": [
      {
        "product": "Webcam",
        "quantity": 1,
        "price": 79.99
      }
    ]
  }')
echo "$NEW_ORDER" | python3 -m json.tool

NEW_ORDER_ID=$(echo "$NEW_ORDER" | python3 -c "import sys, json; print(json.load(sys.stdin).get('order', {}).get('id', ''))" 2>/dev/null)

if [ -n "$NEW_ORDER_ID" ]; then
    echo -e "${GREEN}✓ Order created with ID: $NEW_ORDER_ID${NC}"

    echo -e "\n${BLUE}\n[TEST] Update Order Status${NC}"
    echo -e "${YELLOW}PUT /orders/$NEW_ORDER_ID${NC}"
    curl -s -X PUT "$GATEWAY_URL/orders/$NEW_ORDER_ID" \
      -H "Content-Type: application/json" \
      -d '{"status": "processing"}' | python3 -m json.tool
else
    echo -e "${YELLOW}[!] Could not extract new order ID${NC}"
fi

echo -e "\n${BLUE}\n[TEST] Filter Orders by Status${NC}"
echo -e "${YELLOW}GET /orders?status=delivered${NC}"
curl -s "$GATEWAY_URL/orders?status=delivered" | python3 -m json.tool

echo -e "\n${BLUE}\n[TEST] Order Statistics${NC}"
echo -e "${YELLOW}GET /orders/stats${NC}"
curl -s "$GATEWAY_URL/orders/stats" | python3 -m json.tool

echo -e "\n${BLUE}\n[TEST] Consolidated Dashboard${NC}"
echo -e "${YELLOW}GET /dashboard${NC}"
curl -s "$GATEWAY_URL/dashboard" | python3 -m json.tool

echo -e "\n${BLUE}\n[TEST] Users with Orders${NC}"
echo -e "${YELLOW}GET /users-with-orders${NC}"
curl -s "$GATEWAY_URL/users-with-orders" | python3 -m json.tool | head -100
echo "..."

echo -e "\n${BLUE}\n[TEST] API Documentation${NC}"
echo -e "${YELLOW}GET /${NC}"
curl -s "$GATEWAY_URL/" | python3 -m json.tool

echo -e "\n${BLUE}========================================${NC}"
if [ $RESULT -eq 0 ]; then
    echo -e "${GREEN}    TESTS COMPLETED SUCCESSFULLY${NC}"
else
    echo -e "${RED}    SOME TESTS FAILED${NC}"
fi
echo -e "${BLUE}========================================${NC}"

exit $RESULT