#!/bin/bash
# Manual Testing Script for C2S Gateway
# Run this after starting the gateway with: ./start.sh

BASE_URL="http://localhost:8001"

echo "=========================================="
echo "C2S Gateway Manual Testing Script"
echo "=========================================="
echo ""
echo "Make sure the gateway is running first!"
echo "Start with: ./start.sh"
echo ""
echo "Press Enter to continue..."
read

echo ""
echo "=========================================="
echo "TEST 1: Ping"
echo "=========================================="
curl -s "${BASE_URL}/TEST/ping" | python3 -m json.tool
echo ""

echo ""
echo "=========================================="
echo "TEST 2: Company Info (Authentication)"
echo "=========================================="
curl -s "${BASE_URL}/TEST/company-info" | python3 -m json.tool
echo ""

echo ""
echo "=========================================="
echo "TEST 3: List Leads"
echo "=========================================="
curl -s "${BASE_URL}/TEST/list-leads?page=1&perpage=5" | python3 -m json.tool
echo ""

echo ""
echo "=========================================="
echo "TEST 4: List Sellers"
echo "=========================================="
curl -s "${BASE_URL}/TEST/list-sellers" | python3 -m json.tool
echo ""

echo ""
echo "=========================================="
echo "TEST 5: List Tags"
echo "=========================================="
curl -s "${BASE_URL}/TEST/list-tags" | python3 -m json.tool
echo ""

echo ""
echo "=========================================="
echo "TEST 6: List Distribution Queues"
echo "=========================================="
curl -s "${BASE_URL}/TEST/list-queues" | python3 -m json.tool
echo ""

echo ""
echo "=========================================="
echo "TEST 7: Full System Test (Comprehensive)"
echo "=========================================="
curl -s "${BASE_URL}/TEST/full-system-test" | python3 -m json.tool
echo ""

echo ""
echo "=========================================="
echo "All tests completed!"
echo "=========================================="
echo ""
echo "To test WRITE operations (creates actual data!):"
echo "curl -X POST ${BASE_URL}/TEST/create-test-lead \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{\"customer\": \"TEST Customer\"}'"
echo ""
echo "⚠️  Remember to DELETE test data after testing!"
echo ""
