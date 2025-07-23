import os
from mistralai import Mistral


def get_personality_type(user_text):
    api_key = os.environ["MISTRAL_API_KEY"]
    model = "mistral-large-latest"

    client = Mistral(api_key=api_key)

    system_prompt = """
    You are a friendly, yet not very chatty assistant that provides users with their personality type based on text they write to you.
    The personality type should be based on the OCEAN, or Big-5, theory of personality types.
    Your response should be structured as follows:
    Assign a 1 or zero value to each of the five labels (namely "Openness", "Conscientiousness", "Extraversion", "Agreeableness", and "Neuroticism") on the basis of the text you were given by the user.
    """

    chat_response = client.chat.complete(
        model= model,
        messages = [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_text,
            }
        ]
    )
    return chat_response.choices[0].message.content #type: ignore


if __name__ == "__main__":
    print("Hi! This script is meant to be imported and not run directly. There should be some app.py somewhere to be run with `streamlit run app.py`")