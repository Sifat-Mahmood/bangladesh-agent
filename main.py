# main.py
# Entry point — run this file to start chatting with the agent.

from agent import create_agent

def main():
    print("=" * 60)
    print("  Bangladesh Multi-Tool AI Agent")
    print("  Powered by Groq (Llama 3.3) + LangChain")
    print("=" * 60)
    print("  Tools available:")
    print("  - InstitutionsDBTool (34,901 institutions)")
    print("  - HospitalsDBTool    (38,886 hospitals)")
    print("  - RestaurantsDBTool  (12,703 restaurants)")
    print("  - WebSearchTool      (live internet search)")
    print("=" * 60)
    print("  Type your question below. Type 'quit' to exit.")
    print("=" * 60)

    # Create the agent once, reuse it for all questions
    agent = create_agent()

    while True:
        print()
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        print("\nAgent thinking...\n")

        try:
            result = agent.invoke({"input": user_input})
            print("\n" + "=" * 60)
            print("ANSWER:", result["output"])
            print("=" * 60)

        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()