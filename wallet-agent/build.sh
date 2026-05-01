#!/bin/bash

set -e

echo "🔧 Building wallet-agent Docker image..."

docker build -t wallet-agent:latest .

echo "✅ Build completed successfully!"