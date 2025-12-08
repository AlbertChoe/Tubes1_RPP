import os
from typing import LiteralString, cast

from neo4j import GraphDatabase

import logging

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Suppress Neo4j driver notifications
logging.getLogger("neo4j.notifications").setLevel(logging.WARNING)

# Load configuration
NEO4J_URI = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.environ.get("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD", "password")


class GraphLoader:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def clear_database(self):
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            logger.info("Database cleared.")

    def load_cypher(self, file_path):
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


def main():
    loader = GraphLoader(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    try:
        loader.clear_database()
        loader.load_cypher("graph_data.cypher")
    finally:
        loader.close()


if __name__ == "__main__":
    main()
