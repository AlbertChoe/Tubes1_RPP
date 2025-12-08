# BMW Knowledge Graph RAG System

## Project Structure
- **TP1/**: Contains domain files (`bmw.ttl`, `bmw.pl`, `data.json`).
- **TP2/**: Contains the application code (`app.py`, `rag.py`, etc.).

## Setup
1. Install uv:
   ```bash
   pip install uv
   ```

2. Navigate to the application directory:
   ```bash
   cd TP2
   ```

3. Generate Cypher Data (if needed for seeding):
   ```bash
   uv run generate_cypher.py
   ```

4. Load Data to Neo4j (if needed for seeding):
   ```bash
   uv run graph_loader.py
   ```

## Running the RAG System

### Option 1: Web Interface (Recommended)
Run the Streamlit app:
```bash
uv run streamlit run app.py
```

### Option 2: CLI Interface
Start the command-line tool:
```bash
uv run rag.py
```

## Testing
Run the test suite:
```bash
uv run test_rag.py
```
