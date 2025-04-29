from core.vector_operations import VectorDBOperations as db
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv

load_dotenv()


def generate_question(client, user_id):
    parser = JsonOutputParser(
        pydantic_object={
            "type": "object",
            "properties": {
                "question_1": {"type": "string"},
                "question_2": {"type": "string"},
            },
            "required": ["question_1", "question_2"],
        }
    )

    # Create a simple prompt for generating questions
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """Based on the content provided, generate one or two relevant, thought-provoking and only important questions. 
            Return the output in this JSON format.
            NOTE:ONLY GIVE THE QUESTIONS AND NOTHING MORE THAN THAT:
            {{
                "question_1": "first question here",
                "question_2": "second question here"
                ...
            }}""",
            ),
            ("user", "{input}"),
        ]
    )

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=1,
    )
    chain = prompt | llm | parser

    collection = db.read(client, user_id)
    print("retrived:", len(collection))

    num = len(collection) // 5
    response = []
    res = ""
    for idx, item in enumerate(collection.iterator()):
        res = res+" "+item.properties["content"]
        if not (idx % num):
            questions = chain.invoke({"input":res})
            res = ""
            for _, value in questions.items():
                response.append(value)
    client.close()
            

    # for idx, item in enumerate(collection.iterator()):
    #     res = chain.invoke({"input": item.properties["content"]})
    #     print(res, end="\n\n")
    #     for key, value in res.items():
    #         response[f"{idx}_{key}"] = value
            # yield json.dumps(response)

    return response
