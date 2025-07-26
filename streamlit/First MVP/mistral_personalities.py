import os
from mistralai import Mistral

api_key = os.getenv("MISTRAL_API_KEY")

def get_personality_type(user_text):
    try:
        model = "mistral-large-latest"

        client = Mistral(api_key=api_key)

        system_prompt = """
        You are a friendly, yet not very chatty assistant that provides users with their personality type based on text they write to you.
        The personality type should be based on the OCEAN, or Big-5, theory of personality types.
        Assign a 1 or zero value to each of the five labels (namely "Openness", "Conscientiousness", "Extraversion", "Agreeableness", and "Neuroticism") on the basis of the text you were given by the user.
        Do not write any code blocks.
        Your response should be structured as follows:
        A list of the scores.
        The word "Explanation", then a line break, and then an explanation of the scores you gave.
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
    except Exception as e:
        from time import sleep
        print(f"An error was encountered when retrieving a response from the LLM:\n{e}")
        sleep(5)
        get_personality_type(user_text)

if __name__ == "__main__":
    print("Hi! This script is meant to be imported and not run directly. There should be some app.py somewhere to be run with `streamlit run app.py`")