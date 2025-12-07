from database import Neo4jDatabase
from openai import OpenAI
import toml
import os

class ResponseGenerator:
    def __init__(self):
        self.db = Neo4jDatabase()

        try:
            config = toml.load("config.toml")
            self.api_key = config["llm"]["api_key"]
            self.model = config["llm"]["model"]
        except Exception as e:
            print(f"Error loading config: {e}")
            self.api_key = None
            self.model = "gpt-3.5-turbo"

        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            print("Warning: No API key found in config.toml")
            self.client = None

        # Load Schema for Context
        self.schema = self._load_schema()

    def _load_schema(self):
        try:
            with open("schema.txt", "r") as f:
                return f.read()
        except:
            return "Schema file not found."

    def generate_cypher(self, question):
        if not self.client:
            return "MATCH (n) RETURN n LIMIT 5" # Fallback

        system_prompt = f"""
You are an expert Neo4j Cypher query generator.
Use the following Graph Schema to answer the user's question.
Do NOT hallucinate relationships or labels that are not in the schema.

SCHEMA:
{self.schema}

INSTRUCTIONS:
1. Generate ONLY the Cypher query. No markdown, no explanation.
2. Use case-insensitive matching for string properties (e.g., toLower(n.name) CONTAINS ...). Properties name can be inferred from the question to match the properties name in the schema.
3. The node label 'BMWModel' is the main entity.
4. Use the specific labels (e.g., :ElectricCar, :SUV) if they are relevant to the question.
5. Infer the relationships between nodes based on the schema. For example, if the question is about the fastest car, use the :HighPerformanceCar label.
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                ],
                temperature=1
            )
            cypher = response.choices[0].message.content.strip()
            # Clean up markdown if present
            cypher = cypher.replace("```cypher", "").replace("```", "").strip()
            return cypher
        except Exception as e:
            print(f"Error generating Cypher: {e}")
            return ""

    def generate_response(self, question):
        # Generate Cypher
        cypher_query = self.generate_cypher(question)
        print(f"[DEBUG] Generated Cypher: {cypher_query}")

        if not cypher_query:
            return "Sorry, I couldn't generate a query for that request."

        # Execute Query
        try:
            results = self.db.query(cypher_query)
        except Exception as e:
            return f"Error executing query: {e}\nQuery: {cypher_query}"

        if not results:
            return "I couldn't find any information matching your request in the database."

        # Generate Natural Language Response
        if not self.client:
            return str(results)

        system_prompt = """
You are a knowledgeable and professional BMW assistant.
Answer the user's question directly using the provided context.
Maintain a formal and polite tone.
Do not explain that you corrected the user's spelling.
** IMPORTANT: Do not mention "Based on the provided database" or similar phrases. **
Provide the answer naturally, as if you possess this knowledge inherently.
If the results are a list of cars, present them in a clean, structured format.
"""

        user_content = f"""
Question: {question}
Database Results: {results}
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error generating response: {e}"

    def close(self):
        self.db.close()
