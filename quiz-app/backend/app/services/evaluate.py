from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv

load_dotenv()

def evaluate_batch(data):
    # Define the output parser for multiple evaluations
    parser = JsonOutputParser(
        pydantic_object={
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "evaluation": {"type": "string"},  # "correct" or "incorrect"
                    "justification": {"type": "string"},  # Reasoning for the evaluation
                },
                "required": ["evaluation", "justification"],
            }
        }
    )

    # Define the prompt that evaluates multiple questions and answers
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a helpful assistant tasked with evaluating multiple question-answer pairs.
                For each question, evaluate if the provided answer is correct or not and provide a justification for your evaluation.
                Respond with a JSON array, where each entry contains 'evaluation' as 'correct' or 'incorrect', and 'justification' explaining why."""
            ),
            ("user", "Questions and Answers: {input}. For each pair, evaluate if the answer is correct and provide justification."),
        ]
    )

    # Format the input data as a string for all question-answer pairs
    formatted_input = "\n".join([f"Question: {qa['question']}, Answer: {qa['answer']}" for qa in data])

    # Instantiate the LLM model with Groq
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=1,
    )

    # Chain the prompt, LLM, and output parser
    chain = prompt | llm | parser

    # Run the chain and return the evaluations
    evaluation_results = chain.invoke(formatted_input)
    return evaluation_results


if __name__ == "__main__":
# Example of sending multiple questions and answers
    data = [
        {"question": "What is the capital of France?", "answer": "Paris"},
        {"question": "What is 2+2?", "answer": "4"},
        # {"question": "Who is the president of the USA?", "answer": "Joe Mama"}
    ]

    result = evaluate_batch(data)
    print(result)
