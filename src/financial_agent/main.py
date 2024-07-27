from dotenv import load_dotenv
from agent import cohere_agent, tools
from preamble import create_preamble
from data_loader import load_data

load_dotenv()

def main():
    df_grm, df_review = load_data()
    preamble = create_preamble(df_grm, df_review)

    print(preamble)

    while True:
        user_question = input("Please enter your question (or type 'exit' to quit): ")
        if user_question.lower() == 'exit':
            break
        try:
            response = cohere_agent(
                message=user_question,
                preamble=preamble,
                tools=tools,
                verbose=True,
            )
            print(f"Answer: {response}")
        except Exception as e:
            print(f"Error handling question: {e}")

if __name__ == "__main__":
    main()
