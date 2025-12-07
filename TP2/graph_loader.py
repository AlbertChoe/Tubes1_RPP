import os
from neo4j import GraphDatabase
import toml

# Load configuration
try:
    config = toml.load("config.toml")
    NEO4J_URI = config["neo4j"]["uri"]
    NEO4J_USER = config["neo4j"]["user"]
    NEO4J_PASSWORD = config["neo4j"]["password"]
except Exception as e:
    print(f"Warning: Could not load config.toml ({e}). Using defaults.")
    NEO4J_URI = "bolt://localhost:7687"
    NEO4J_USER = "neo4j"
    NEO4J_PASSWORD = "password"

class GraphLoader:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def clear_database(self):
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            print("Database cleared.")

    def load_cypher(self, file_path):
        if not os.path.exists(file_path):
            print(f"Error: File {file_path} not found.")
            return

        with open(file_path, 'r') as f:
            queries = f.read().split(';')

        with self.driver.session() as session:
            count = 0
            for query in queries:
                query = query.strip()
                if query:
                    try:
                        session.run(query)
                        count += 1
                    except Exception as e:
                        print(f"Error executing query: {query[:50]}... \n{e}")
            print(f"Executed {count} queries from {file_path}")

def main():
    loader = GraphLoader(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    try:
        loader.clear_database()
        loader.load_cypher("graph_data.cypher")
    finally:
        loader.close()

if __name__ == "__main__":
    main()
