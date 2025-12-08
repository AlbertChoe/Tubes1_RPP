"""Graph loader utility for loading Cypher files into Neo4j."""

import logging
import os
from typing import LiteralString, cast

from neo4j import GraphDatabase

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)
logging.getLogger("neo4j.notifications").setLevel(logging.WARNING)

# Default connection settings
DEFAULT_URI = "bolt://localhost:7687"
DEFAULT_USER = "neo4j"
DEFAULT_PASSWORD = "password"


class GraphLoader:
    def __init__(self, uri: str, user: str, password: str) -> None:
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self) -> None:
        self.driver.close()

    def clear_database(self) -> None:
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            logger.info("Database cleared.")

    def load_cypher(self, file_path: str) -> None:
        if not os.path.exists(file_path):
            logger.error(f"File {file_path} not found.")
            return

        with open(file_path, "r") as f:
            queries = f.read().split(";")

        with self.driver.session() as session:
            count = 0
            for query in queries:
                query = query.strip()
                if query:
                    try:
                        session.run(cast(LiteralString, query))
                        count += 1
                    except Exception as e:
                        logger.error(f"Error executing query: {query[:50]}... \n{e}")

            logger.info(f"Executed {count} queries from {file_path}")


def main() -> None:
    uri = os.environ.get("NEO4J_URI", DEFAULT_URI)
    user = os.environ.get("NEO4J_USER", DEFAULT_USER)
    password = os.environ.get("NEO4J_PASSWORD", DEFAULT_PASSWORD)

    loader = GraphLoader(uri, user, password)
    try:
        loader.clear_database()
        loader.load_cypher("data/graph_data.cypher")
    finally:
        loader.close()


if __name__ == "__main__":
    main()
