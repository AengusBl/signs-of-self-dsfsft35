from fastapi import FastAPI
from run_Bert import predict_personality
from pydantic import BaseModel
import uvicorn

description = """
This is an API to be used in conjuction with the Signs of Self web app.
It calls the Bert model that makes score predictions based on text input by the user.
"""

tags_metadata = [
    {
        "name": "Try out the API",
        "description": "Simple endpoints to try out!",
    },
    {
        "name": "Calls by the app",
        "description": "Let's get down to business!",
    }
]

app = FastAPI(
    title="Better call Bert",
    description=description,
    version="0.1",
    openapi_tags=tags_metadata
)

class UserInput(BaseModel):
    user_input: str

@app.get("/", tags=["Try out the API"])
async def index():
    """
    Simply returns a welcome message!
    """
    return {"message": "Hi! This is an API that calls a Bert prediction model. Check out its other features!"}

@app.post("/predict", tags=["Calls by the web app"])
async def predict(data: UserInput):
    preds = predict_personality(text=data.user_input)
    print(preds)
    return preds

if __name__ == "__main__":
    uvicorn.run(app, port=8001)
