import unittest

from database import Neo4jDatabase
from response_generator import ResponseGenerator


class TestRAGSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.db = Neo4jDatabase()
        cls.rag = ResponseGenerator()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.db.close()
        cls.rag.close()

    def test_graph_has_models(self) -> None:
        result = self.db.query("MATCH (n:BMWModel) RETURN count(n) as count")
        model_count = result[0]["count"]

        self.assertGreater(model_count, 0, "Should have BMW models in the database")
        print(f"Total BMW Models: {model_count}")

    def test_electric_car_labels(self) -> None:
        result = self.db.query("MATCH (n:ElectricCar) RETURN n.name")
        names = [r["n.name"] for r in result]

        expected_electric_cars = ["BMW i4 M50", "BMW iX xDrive50"]
        for car in expected_electric_cars:
            self.assertIn(car, names, f"{car} should have ElectricCar label")

        print(f"Electric Cars found: {len(names)}")

    def test_cypher_generation_electric_cars(self) -> None:
        question = "Show me electric cars"
        cypher = self.rag.generate_cypher(question)

        self.assertIn(
            "ElectricCar", cypher, "Query should reference ElectricCar label"
        )

    def test_cypher_generation_suv_xdrive(self) -> None:
        question = "List SUVs with xDrive"
        cypher = self.rag.generate_cypher(question)

        self.assertIn(
            "OffroadCapableSUV", cypher, "Query should reference OffroadCapableSUV label"
        )

    def test_full_response_generation(self) -> None:
        question = "What electric cars do you have?"
        response = self.rag.generate_response(question)

        self.assertIn(
            "BMW i4 M50", response, "Response should include BMW i4 M50"
        )
        print("Full response generation test passed.")


if __name__ == "__main__":
    unittest.main()
