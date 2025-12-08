import logging
import os
import textwrap

from openai import OpenAI

from database import Neo4jDatabase

logger = logging.getLogger(__name__)


class ResponseGenerator:
    def __init__(self):
        self.db = Neo4jDatabase()

        self.api_key = os.environ.get("LLM_API_KEY")
        self.model = os.environ.get("LLM_MODEL", "gpt-3.5-turbo")
        self.base_url = os.environ.get("LLM_BASE_URL", "https://api.openai.com/v1")

        if self.api_key:
            self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        else:
            logger.warning("No API key found in environment variables")
            self.client = None

        # Load Schema for Context
        self.schema = self._load_schema()

    def _load_schema(self):
        try:
            with open("schema.txt", "r") as f:
                return f.read()
        except Exception:
            logger.error("Schema file not found.")
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
            3. **Entity Resolution (CRITICAL):**
               - Check the "KNOWN ENTITIES" list in the schema.
               - If the user asks for a specific model (e.g., "iX", "M3"), you MUST use the EXACT string from the list (e.g., "BMW iX xDrive50", "BMW M3 G80").
               - Use `WHERE m.name = 'Exact Name from List'`.
            4. **Value Formatting:** The database uses Title Case for specific values.
               - If user asks for "suv", match `{{name: 'SUV'}}`.
               - If user asks for "3 series", match `{{name: '3 Series'}}`.
               - If user asks for "electric", match `{{name: 'Electric'}}`.
            5. **Structural Matching (Priority):**
               - Prefer matching attributes via relationships defined in the schema.
               - Example: `MATCH (m)-[:HAS_BODY_TYPE]->(:BodyType {{name: 'SUV'}})` is safer than guessing a label like `:SUVCar`.
            6. **Label Shortcuts:** You MAY use specific labels (e.g., `:ElectricCar`, `:MSeries`) in combination with the main label IF they simplify the query and exist in the schema.
               - Example: `MATCH (m:BMWModel:ElectricCar)` is valid.
            7. **Return Clause:** You MUST end the query with a `RETURN` clause showing the relevant model names or properties.
               - Default: `RETURN m.name`

            EXAMPLE INPUT:
            "Show me all electric SUVs"

            EXAMPLE OUTPUT:
            MATCH (m:BMWModel:ElectricCar)-[:HAS_BODY_TYPE]->(:BodyType {{name: 'SUV'}}) RETURN m.name
        """)

        try:
            # logger.debug(f"Using base_url: {self.client.base_url}") # Optional verbose log
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
            logger.error(f"Error generating Cypher: {e}")
            return ""

    def fix_cypher(self, question, invalid_cypher, error_message):
        logger.info(f"Attempting to fix Cypher. Error: {error_message}")
        system_prompt = textwrap.dedent(f"""
            You are an expert Neo4j Cypher query corrector.
            Your task is to FIX the Cypher query based on the error message and the schema.

            SCHEMA:
            {self.schema}

            GUIDELINES:
            1. Analyze the error message to understand what went wrong (e.g., syntax error, invalid relationship type).
            2. Correct the query to be valid Cypher and consistent with the schema.
            3. **Output:** Generate ONLY the corrected Cypher query string. No markdown, no explanations.
        """)

        user_content = textwrap.dedent(f"""
            ORIGINAL QUESTION: "{question}"
            INVALID CYPHER: "{invalid_cypher}"
            ERROR MESSAGE: "{error_message}"
        """)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content},
                ],
                temperature=0.2,
            )
            cypher = response.choices[0].message.content.strip()
            cypher = cypher.replace("```cypher", "").replace("```", "").strip()
            return cypher
        except Exception as e:
            logger.error(f"Error fixing Cypher: {e}")
            return ""

    def generate_response(self, question):
        # Generate Initial Cypher
        cypher_query = self.generate_cypher(question)
        logger.info(f"Generated Cypher: {cypher_query}")

        if not cypher_query:
            return "Sorry, I couldn't generate a query for that request."

        # Execute Query with Retry Loop
        results = None
        max_retries = 3

        for attempt in range(max_retries + 1):
            try:
                results = self.db.query(cypher_query)
                break  # Success!
            except Exception as e:
                error_message = str(e)
                logger.warning(
                    f"Query failed (Attempt {attempt + 1}/{max_retries + 1}): {error_message}"
                )

                if attempt < max_retries:
                    # Try to fix it
                    new_cypher = self.fix_cypher(question, cypher_query, error_message)
                    if new_cypher:
                        logger.info(f"Retrying with fixed Cypher: {new_cypher}")
                        cypher_query = new_cypher
                    else:
                        return f"I encountered an error and couldn't fix it automatically. Error: {error_message}"
                else:
                    logger.error(
                        f"Final query failure after retries. Last error: {error_message}"
                    )
                    return f"I tried to answer your question multiple times but encountered errors. Last error: {error_message}"

        if not results:
            if results is None:
                logger.error("Unexpected None results from db query.")
                return "An unexpected error occurred during query execution."

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

            Answer ONLY in English or Bahasa Indonesia depending on the user's language preference.
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
            logger.error(f"Error generating response: {e}")
            return f"Error generating response: {e}"

    def close(self):
        self.db.close()
