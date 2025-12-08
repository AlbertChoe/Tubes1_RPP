"""Response generator using LLM and Neo4j knowledge graph."""

import logging
import os
import textwrap

from openai import OpenAI

from database import Neo4jDatabase

logger = logging.getLogger(__name__)

# Default LLM settings
DEFAULT_MODEL = "gpt-3.5-turbo"
DEFAULT_BASE_URL = "https://api.openai.com/v1"

# Retry settings
MAX_QUERY_RETRIES = 4

# LLM temperature settings
CYPHER_GENERATION_TEMPERATURE = 0.5
CYPHER_FIX_TEMPERATURE = 0.2


class ResponseGenerator:

    def __init__(self) -> None:
        self.db = Neo4jDatabase()
        self._init_llm_client()
        self.schema = self._load_schema()

    def _init_llm_client(self) -> None:
        self.api_key = os.environ.get("LLM_API_KEY")
        self.model = os.environ.get("LLM_MODEL", DEFAULT_MODEL)
        self.base_url = os.environ.get("LLM_BASE_URL", DEFAULT_BASE_URL)

        if self.api_key:
            self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        else:
            logger.warning("No API key found in environment variables")
            self.client = None

    def _load_schema(self) -> str:
        try:
            with open("data/schema.txt", "r") as f:
                return f.read()
        except FileNotFoundError:
            logger.error("Schema file not found.")
            return "Schema file not found."

    def _build_history_context(self, chat_history: list[dict] | None) -> str:
        if not chat_history:
            return ""

        history_str = "\n".join(
            [f"{msg['role'].upper()}: {msg['content']}" for msg in chat_history]
        )
        return f"\nCHAT HISTORY:\n{history_str}\n"

    def _get_cypher_system_prompt(self, history_context: str) -> str:
        return textwrap.dedent(f"""
            You are an expert Neo4j Cypher query generator.
            Your task is to convert the user's natural language question into a valid Cypher query based on the schema below.

            {history_context}

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
            8. **Context Awareness:** If the user asks a follow-up question (e.g., "What about the iX?"), use the CHAT HISTORY to resolve pronouns or incomplete context.

            EXAMPLE INPUT:
            "Show me all electric SUVs"

            EXAMPLE OUTPUT:
            MATCH (m:BMWModel:ElectricCar)-[:HAS_BODY_TYPE]->(:BodyType {{name: 'SUV'}}) RETURN m.name
        """)

    def _clean_cypher_response(self, cypher: str) -> str:
        return cypher.replace("```cypher", "").replace("```", "").strip()

    def generate_cypher(
        self, question: str, chat_history: list[dict] | None = None
    ) -> str:
        if not self.client:
            return "MATCH (n) RETURN n LIMIT 5"

        history_context = self._build_history_context(chat_history)
        system_prompt = self._get_cypher_system_prompt(history_context)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question},
                ],
                temperature=CYPHER_GENERATION_TEMPERATURE,
            )
            cypher = response.choices[0].message.content.strip()
            return self._clean_cypher_response(cypher)
        except Exception as e:
            logger.error(f"Error generating Cypher: {e}")
            return ""

    def fix_cypher(
        self, question: str, invalid_cypher: str, error_message: str
    ) -> str:
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
                temperature=CYPHER_FIX_TEMPERATURE,
            )
            cypher = response.choices[0].message.content.strip()
            return self._clean_cypher_response(cypher)
        except Exception as e:
            logger.error(f"Error fixing Cypher: {e}")
            return ""

    def _execute_query_with_retry(
        self, question: str, cypher_query: str
    ) -> tuple[list | None, str | None]:
        current_query = cypher_query

        for attempt in range(MAX_QUERY_RETRIES + 1):
            try:
                results = self.db.query(current_query)
                return results, None
            except Exception as e:
                error_message = str(e)
                logger.warning(
                    f"Query failed (Attempt {attempt + 1}/{MAX_QUERY_RETRIES + 1}): {error_message}"
                )

                if attempt < MAX_QUERY_RETRIES:
                    new_cypher = self.fix_cypher(question, current_query, error_message)
                    if new_cypher:
                        logger.info(f"Retrying with fixed Cypher: {new_cypher}")
                        current_query = new_cypher
                    else:
                        return None, f"I encountered an error and couldn't fix it automatically. Error: {error_message}"

        logger.error(f"Final query failure after retries. Last error: {error_message}")
        return None, f"I tried to answer your question multiple times but encountered errors. Last error: {error_message}"

    def _format_response_with_llm(
        self, question: str, results: list[dict]
    ) -> str:
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
            return "Sorry, I cannot answer your question because I do not have the knowledge to answer it."

    def generate_response(
        self, question: str, chat_history: list[dict] | None = None
    ) -> str:
        cypher_query = self.generate_cypher(question, chat_history)
        logger.info(f"Generated Cypher: {cypher_query}")

        if not cypher_query:
            return "Sorry, I cannot answer your question because I do not have the knowledge to answer it."

        results, error = self._execute_query_with_retry(question, cypher_query)

        if error:
            return "Sorry, I cannot answer your question because I do not have the knowledge to answer it."

        if not results:
            if results is None:
                logger.error("Unexpected None results from db query.")
            return "Sorry, I cannot answer your question because I do not have the knowledge to answer it."

        if not self.client:
            return str(results)

        return self._format_response_with_llm(question, results)

    def close(self) -> None:
        self.db.close()
