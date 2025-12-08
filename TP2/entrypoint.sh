#!/bin/bash
set -e

echo "Generating Cypher queries..."
uv run python generate_cypher.py

echo "Seeding database..."
uv run python graph_loader.py

echo "Starting Streamlit..."
exec "$@"
