from neo4j import GraphDatabase
import toml

class Neo4jDatabase:
    def __init__(self, config_path="config.toml"):
        self.config = toml.load(config_path)
        self._connect()

    def _connect(self):
        try:
            self.driver = GraphDatabase.driver(
                self.config["neo4j"]["uri"],
                auth=(self.config["neo4j"]["user"], self.config["neo4j"]["password"])
            )
        except Exception as e:
            print(f"Failed to connect to Neo4j: {e}")
            self.driver = None

    def close(self):
        if self.driver:
            self.driver.close()

    def query(self, query, parameters=None):
        if not self.driver:
            self._connect()

        try:
            with self.driver.session() as session:
                result = session.run(query, parameters)
                return [record.data() for record in result]
        except Exception as e:
            print(f"Query failed ({e}), attempting to reconnect...")
            self.close()
            self._connect()
            try:
                with self.driver.session() as session:
                    result = session.run(query, parameters)
                    return [record.data() for record in result]
            except Exception as e2:
                print(f"Retry failed: {e2}")
                raise e2
