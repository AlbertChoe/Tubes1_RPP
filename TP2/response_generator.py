import textwrap

import toml
from openai import OpenAI

from database import Neo4jDatabase


class ResponseGenerator:
    def __init__(self):
        self.db = Neo4jDatabase()

        try:
            config = toml.load("config.toml")
            self.api_key = config["llm"]["api_key"]
            self.model = config["llm"]["model"]
            self.base_url = config["llm"].get("base_url", "https://api.openai.com/v1")
        except Exception as e:
            print(f"Error loading config: {e}")
            self.api_key = None
            self.model = "gpt-3.5-turbo"

        if self.api_key:
            self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        else:
            print("Warning: No API key found in config.toml")
            self.client = None

        # Load Schema for Context
        self.schema = self._load_schema()

    def _load_schema(self):
        try:
            with open("schema.txt", "r") as f:
                return f.read()
        except Exception:
            return "Schema file not found."

    def generate_cypher(self, question):
        if not self.client:
            return "MATCH (n) RETURN n LIMIT 5"  # Fallback

        system_prompt = textwrap.dedent(f"""
            You are an expert Neo4j Cypher query generator.
            Your task is to convert the user's natural language question into a valid Cypher query based on the schema below.

            SCHEMA:
            {self.schema}

            GUIDELINES:
            1. **Output:** Generate ONLY the Cypher query string. No markdown, no explanations, no code blocks.
            2. **Root Node:** Always start matching with the node `(m:BMWModel)`.
            3. **Value Formatting:** The database uses Title Case for specific values.
               - If user asks for "suv", match `{{name: 'SUV'}}`.
               - If user asks for "3 series", match `{{name: '3 Series'}}`.
               - If user asks for "electric", match `{{name: 'Electric'}}`.
            4. **Structural Matching (Priority):**
               - Prefer matching attributes via relationships defined in the schema.
               - Example: `MATCH (m)-[:HAS_BODY_TYPE]->(:BodyType {{name: 'SUV'}})` is safer than guessing a label like `:SUVCar`.
            5. **Label Shortcuts:** You MAY use specific labels (e.g., `:ElectricCar`, `:MSeries`) in combination with the main label IF they simplify the query and exist in the schema.
               - Example: `MATCH (m:BMWModel:ElectricCar)` is valid.
            6. **Return Clause:** You MUST end the query with a `RETURN` clause showing the relevant model names or properties.
               - Default: `RETURN m.name`

            EXAMPLE INPUT:
            "Show me all electric SUVs"

            EXAMPLE OUTPUT:
            MATCH (m:BMWModel:ElectricCar)-[:HAS_BODY_TYPE]->(:BodyType {{name: 'SUV'}}) RETURN m.name
        """)

        try:
            print(self.client.base_url)
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question},
                ],
                temperature=0.5,
            )
            cypher = response.choices[0].message.content.strip()
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
            return (
                "I couldn't find any information matching your request in the database."
            )

        # Generate Natural Language Response
        if not self.client:
            return str(results)

        system_prompt = textwrap.dedent("""
            You are a knowledgeable and professional BMW assistant.
            Answer the user's question directly using the provided context.
            Maintain a formal and polite tone.
            Do not explain that you corrected the user's spelling.
            ** IMPORTANT: Do not mention "Based on the provided database" or similar phrases. **
            Provide the answer naturally, as if you possess this knowledge inherently.
            If the results are a list of cars, present them in a clean, structured format.
        """)

        user_content = textwrap.dedent(f"""
            Question:
            {question}

            ----

            Database Results:
            {results}
        """)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content},
                ],
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error generating response: {e}"

    def close(self):
        self.db.close()
