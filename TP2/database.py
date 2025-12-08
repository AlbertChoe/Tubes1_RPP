from neo4j import GraphDatabase
import os
import logging

logger = logging.getLogger(__name__)


class Neo4jDatabase:
    def __init__(self):
        self._connect()

    def _connect(self):
        try:
            uri = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
            user = os.environ.get("NEO4J_USER", "neo4j")
            password = os.environ.get("NEO4J_PASSWORD", "password")

            self.driver = GraphDatabase.driver(
                uri,
                auth=(user, password),
            )
            logger.info("Successfully connected to Neo4j.")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            self.driver = None

    def close(self):
        if self.driver:
            self.driver.close()
            logger.info("Neo4j connection closed.")

    def query(self, query, parameters=None):
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
