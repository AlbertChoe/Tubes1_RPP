from response_generator import ResponseGenerator


def main():
    rag = ResponseGenerator()
    print("Welcome to the BMW Knowledge Graph RAG System!")
    print("Type 'exit' to quit.")

    while True:
        try:
            user_input = input("\nAsk a question: ")
            if user_input.lower() in ["exit", "quit"]:
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
