from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import ollama
import uvicorn

# Initialize FastAPI app
app = FastAPI()

# Initialize Ollama client
client = ollama.Client()

# Request model for user input
class ChatRequest(BaseModel):
    user_input: str

# Response model for chatbot output
class ChatResponse(BaseModel):
    bot_response: str
    reflection: str

# Chatbot function
def chat_with_reflection(user_input: str):
    """
    Chatbot function with reflection mechanism.
    """
    # Generate initial response
    prompt = (
        "You are a construction domain expert chatbot. Your role is to assist architects, civil engineers, "
        "and customers by answering their questions about construction. Keep your responses concise, clear, "
        "and relevant to CSI numbers, equipment, labor, materials, cost, and budgets. Do not include internal "
        "thought processes or unnecessary details.\n\n"
        f"Question: {user_input}"
    )
    response = client.generate(model="deepseek-r1:1.5b", prompt=prompt)
    bot_response = response['response']

    # Reflect on the response
    reflection_prompt = (
        "You are a construction domain expert. Reflect on the following response and suggest improvements "
        "to make it more helpful for architects, civil engineers, and customers. Focus on clarity, accuracy, "
        "and relevance to CSI numbers, equipment, labor, materials, cost, and budgets:\n\n"
        f"Response: {bot_response}"
    )
    reflection = client.generate(model="deepseek-r1:1.5b", prompt=reflection_prompt)
    reflection_response = reflection['response']

    return ChatResponse(bot_response=bot_response, reflection=reflection_response)

# API endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        response = chat_with_reflection(request.user_input)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the FastAPI app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)