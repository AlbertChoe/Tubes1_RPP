"""Command-line interface for the BMW Knowledge Graph RAG System."""

from response_generator import ResponseGenerator

EXIT_COMMANDS = {"exit", "quit"}


def main() -> None:
    rag = ResponseGenerator()

    print("Welcome to the BMW Knowledge Graph RAG System!")
    print("Type 'exit' or 'quit' to end the session.")

    while True:
        try:
            user_input = input("\nAsk a question: ")
            if user_input.lower() in EXIT_COMMANDS:
                break

            response = rag.generate_response(user_input)
            print("\nResponse:")
            print(response)

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"An error occurred: {e}")

    rag.close()
    print("\nGoodbye!")


if __name__ == "__main__":
    main()
