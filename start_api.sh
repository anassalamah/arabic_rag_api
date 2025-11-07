#!/bin/bash
# Quick script to start the Arabic RAG API

cd /workspace/arabic_rag_api
source venv/bin/activate
python main.py &

echo "API starting..."
sleep 3

# Test if it's running
if curl -s http://localhost:8000/ | grep -q "ok"; then
    echo "✅ API is running successfully!"
    echo "📍 Internal: http://localhost:8000"
    echo "📍 External: http://203.57.40.119:PORT (check RunPod dashboard for public port)"
else
    echo "❌ API failed to start. Check logs above."
fi

