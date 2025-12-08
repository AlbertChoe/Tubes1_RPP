# BMW Knowledge Graph Assistant (TP2)

A RAG-based Knowledge Graph application for BMW cars, built with **Streamlit**, **Neo4j**, and **OpenAI**. This project demonstrates a fully dockerized, self-healing, and automated knowledge graph system.

## Features

-   **🐳 Fully Dockerized**: Uses `uv` for fast, reliable Python dependency management.
-   **🌱 Auto-Seeding**: Automatically seeds the Neo4j database with `data.json` on every startup.
-   **🛠️ Self-Healing Queries**: If a generated Cypher query is invalid, the system automatically asks the LLM to fix it (retries up to 3 times).
-   **📝 structured Logging**: Comprehensive logging replaces print statements for better observability.
-   **☁️ Cloud-Native Config**: Fully configurable via environment variables.

## Prerequisites

-   [Docker Desktop](https://www.docker.com/products/docker-desktop/)
-   An [OpenAI API Key](https://platform.openai.com/) (or compatible provider like Groq)

## Quick Start

1.  **Clone the repository** and navigate to `TP2`:
    ```bash
    cd TP2
    ```

2.  **Set up your environment variables**:
    Create a `.env` file (see `.env.example`) or export them:
    ```bash
    export LLM_API_KEY=sk-...
    ```

3.  **Run with Docker**:
    ```bash
    docker-compose up --build
    ```

4.  **Access the App**:
    -   **Streamlit UI**: [http://localhost:8501](http://localhost:8501)
    -   **Neo4j Browser**: [http://localhost:7474](http://localhost:7474) (User: `neo4j`, Password: `password`)

## Configuration

You can configure the application using the following environment variables (in `.env` or `docker-compose.yml`):

| Variable | Default | Description |
| :--- | :--- | :--- |
| `LLM_API_KEY` | **Required** | Your LLM provider API key. |
| `LLM_MODEL` | `gpt-3.5-turbo` | The model to use (e.g., `gpt-4`, `llama3-70b-8192`). |
| `LLM_BASE_URL` | `https://api.openai.com/v1` | Base URL for the LLM API (useful for Groq, LocalAI). |
| `NEO4J_URI` | `bolt://neo4j:7687` | Neo4j connection URI. |
| `NEO4J_USER` | `neo4j` | Neo4j username. |
| `NEO4J_PASSWORD` | `password` | Neo4j password. |

## Development Notes

### Auto-Seeding
The system includes `data.json`. On container startup, `entrypoint.sh` executes:
1.  `generate_cypher.py`: Converts JSON to Cypher queries (`graph_data.cypher`).
2.  `graph_loader.py`: Clears the DB and loads the new Cypher queries.

### Logs
Logs are formatted with timestamps and levels. To view them:
```bash
docker-compose logs -f app
```
Neo4j driver notifications (like constraint existence warnings) are suppressed to keep logs clean.
