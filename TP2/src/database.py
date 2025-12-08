import logging
import os
from typing import Any

from neo4j import GraphDatabase

logger = logging.getLogger(__name__)

# Default connection settings
DEFAULT_URI = "bolt://localhost:7687"
DEFAULT_USER = "neo4j"
DEFAULT_PASSWORD = "password"


class Neo4jDatabase:

    def __init__(self) -> None:
        self.driver = None
        self._connect()

    def _connect(self) -> None:
        try:
            uri = os.environ.get("NEO4J_URI", DEFAULT_URI)
            user = os.environ.get("NEO4J_USER", DEFAULT_USER)
            password = os.environ.get("NEO4J_PASSWORD", DEFAULT_PASSWORD)

            self.driver = GraphDatabase.driver(uri, auth=(user, password))
            logger.info("Successfully connected to Neo4j.")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            self.driver = None

    def close(self) -> None:
        if self.driver:
            self.driver.close()
            logger.info("Neo4j connection closed.")

    def query(self, query: str, parameters: dict[str, Any] | None = None) -> list[dict]:
        if not self.driver:
            self._connect()

        try:
            with self.driver.session() as session:
                result = session.run(query, parameters)
                return [record.data() for record in result]
        except Exception as e:
            logger.warning(f"Query failed ({e}), attempting to reconnect...")
            self.close()
            self._connect()

            try:
                with self.driver.session() as session:
                    result = session.run(query, parameters)
                    return [record.data() for record in result]
            except Exception as e2:
                logger.error(f"Retry failed: {e2}")
                raise e2
