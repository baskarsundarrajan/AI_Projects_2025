from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import subprocess
import re



app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def convert_backticks_to_html(response):
    # Convert code blocks to <pre><code> with a placeholder so we can exclude them later
    code_blocks = []

    def repl(match):
        lang = match.group(1) or ""
        code = match.group(2)
        placeholder = f"__CODEBLOCK_{len(code_blocks)}__"
        code_blocks.append((code, lang))
        # print(code_blocks)
        return placeholder

    # Step 1: Replace code blocks with placeholders
    pattern = r"```(\w+)?\n(.*?)```"
    response = re.sub(pattern, repl, response, flags=re.DOTALL)

    # Step 2: Replace newlines with <br/> only in non-code areas
    response = response.replace("\n", "<br/>")

    # # Step 3: Restore code blocks
    # for i, block in enumerate(code_blocks):
    #     response = response.replace(f"__CODEBLOCK_{i}__", block)

    return response, code_blocks


def query_ollama(prompt: str, prev, option) -> str:
    options = {
        "Auto": "General idea of topic",
        "Explain": "Code Explaination on topic or given code", 
        "Generate": "Code Generation on topic",
        "Ask": "Explanation of topic with example in Detail"
    }
    try:
        prompt = f"""
    You are a coding assistant.
    
    Here are the previous messages to get context from the conversation (If empty, ignore it):
    {prev}
    
    IMPORTANT: User wants to focus more on {options[option]}.

    Instructions:
    1. Do NOT include excessive assumptions, over-detailed comments, or verbose explanations inside the code.
    2. Follow best practices, but keep the output minimal, clear, and focused.
    3. If the code is long, break it into manageable parts and provide them sequentially.
    4. If the input is not a code request, respond in a clear and helpful conversational tone.
    5. If user greets be friendly and ask how you can help (dont greet unnecessarily).

    Input:
    {prompt}
"""



        result = subprocess.run(
            ["ollama", "run", "llama3.2", prompt],
            capture_output=True,
            text=True,
            check=True,
        )
        formatted_response, code_block = convert_backticks_to_html(
            result.stdout.strip()
        )
        return formatted_response, code_block
        # return result.stdout.strip(), []
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"



class Message(BaseModel):
    user: str
    message: str
    prev: list
    option: str


@app.get("/")
async def root():
    return {"message": "Welcome to the Chat-AI app!"}


@app.post("/chat")
async def chat(message: Message):
    user_input = message.message
    prev = message.prev
    option = message.option
    model_output, code_block = query_ollama(user_input, prev, option)
    return {"response": model_output, "code": code_block}
