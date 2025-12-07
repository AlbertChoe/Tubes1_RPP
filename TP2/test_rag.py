import unittest
from database import Neo4jDatabase
from response_generator import ResponseGenerator

class TestRAGSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = Neo4jDatabase()
        cls.rag = ResponseGenerator()

    @classmethod
    def tearDownClass(cls):
        cls.db.close()
        cls.rag.close()

    def test_graph_counts(self):
        # Check total models
        result = self.db.query("MATCH (n:BMWModel) RETURN count(n) as count")
        self.assertGreater(result[0]['count'], 0, "Should have BMW models")
        print(f"Total BMW Models: {result[0]['count']}")

    def test_electric_cars(self):
        # Check if ElectricCar label is applied correctly
        result = self.db.query("MATCH (n:ElectricCar) RETURN n.name")
        names = [r['n.name'] for r in result]
        self.assertIn("BMW i4 M50", names)
        self.assertIn("BMW iX xDrive50", names)
        print(f"Electric Cars found: {len(names)}")

    def test_rag_cypher_generation(self):
        # Test query generation
        q1 = "Show me electric cars"
        cypher1 = self.rag.generate_cypher(q1)
        self.assertIn("ElectricCar", cypher1)

        q2 = "List SUVs with xDrive"
        cypher2 = self.rag.generate_cypher(q2)
        self.assertIn("OffroadCapableSUV", cypher2)

    def test_response_generation(self):
        # Test full response
        response = self.rag.generate_response("What electric cars do you have?")
        self.assertIn("BMW i4 M50", response)
        print("Response test passed.")

if __name__ == '__main__':
    unittest.main()
