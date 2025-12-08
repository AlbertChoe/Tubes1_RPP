#!/bin/bash
set -e

echo "Generating Cypher queries..."
uv run src/generate_cypher.py
 
echo "Seeding database..."
uv run src/graph_loader.py

echo "Starting Streamlit..."
exec "$@"
