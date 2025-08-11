import os
import re
import deepl
import time
import requests
from mistralai import Mistral


bert_API_call_counter = 0
def ask_bert_for_scores(endpoint:str="", fr_input:str|None=None) -> dict|str|None:

    def retry(error_message:str) -> str|None:
        global bert_API_call_counter
        bert_API_call_counter += 1
        if bert_API_call_counter <= 4:
            time.sleep(5)
            ask_bert_for_scores(endpoint, fr_input)
        else:
            print(error_message)
            return "Pardon, je suis un peu confus. Réessayez plus tard.\nExplication :\nEssayez d'actualiser la page."
    
    headers = {"Authorization": os.environ["BERT_API_TOKEN"]}
    url = os.environ["BERT_API_URL"] + endpoint

    if fr_input:
        try:
            translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
            to_translate = re.sub(r"[\r\n\t]", "", fr_input) # I want to keep the escaped characters in the original fr_input
            en_input = translator.translate_text(to_translate, target_lang="EN-US")
            print(f"Translated text: {en_input}")

            user_input = en_input.text.encode('unicode-escape').decode() # To avoid getting errors about illegal characters
            data = {"user_input": user_input}
            response = requests.post(url, headers=headers, json=data)

            global bert_API_call_counter
            if response.status_code == 200:
                bert_API_call_counter = 0
                return response.json()
            else:
                print(f"Personality score API request failed with status code {response.status_code}.\nTrying again in a few seconds")
                if fallback := retry("Something went wrong when calling the Bert API for scores. Falling back to a social answer."):
                    return fallback
        except deepl.DeepLException as e:
            print(e)
            if fallback := retry("The DeepL API encountered an issue. Falling back to a social answer."):
                return fallback
        except Exception as e:
            print(e)
            if fallback := retry("Something went wrong when calling the DeepL API. Falling back to a social answer."):
                return fallback
    else:   # An empty function call is done severa times in the process of running the app so the LightningAI session doesn't stop.
        _ = requests.get(url, headers=headers)

def mistral_explain_and_recommend(scores_dict, user_text):
    try:
        model = "mistral-large-latest"

        client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])

        system_prompt = """
        Tu es un assistant sympathique, mais peu bavard, qui explique les résultats de tests de personnalité Big-5 ou OCEAN de l'utilisateur,
        et lui donne des conseils sur la base de ses résultats, et sur la base du texte que l'utilisateur te fournit avec ses scores.
        L'utilisateur vient de passer un test de personnalité basé sur la théorie OCEAN, aussi connue sous le nom de Big-5.
        Sur la base d'un texte que l'utilisateur a écrit, cinq scores binaires de 0 ou 1 lui ont été attribués dans les catégories suivantes:
        - « Ouverture d'esprit », ou « O »
        - « Conscienciosité », ou « C »
        - « Extraversion », ou « E »
        - « Amabilité », ou « A »
        - « Névrotisme », ou « N »

        Instructions:
        - N'écris aucun bloc de code.
        - Tutoie l'utilisateur.
        - Ne prédis pas les scores toi-même : Utilise exactement les scores de O, C, E, A et N donnés par l'utilisateur.
        - Dans ton analyse, fais référence au texte fourni.
        
        Ta réponse doit strictement être structurée comme suit :
        - Une liste des scores donnés par l'utilisateur.
        - La séquence de caractères exacte « Explication : », puis un saut de ligne.
        - Une explication des scores de l'utilisateur, puis des conseils de vie basés sur ces scores.
        """

        user_scores_and_text = f"""
        J'ai passé le test Big-5, et j'ai obtenus les scores suivants :
        - O: {scores_dict["O"]}
        - C: {scores_dict["C"]}
        - E: {scores_dict["E"]}
        - A: {scores_dict["A"]}
        - N: {scores_dict["N"]}

        J'ai obtenu ces scores sur la base de ce texte :
        {user_text}
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
                    "content": user_scores_and_text,
                }
            ]
        )
        output = chat_response.choices[0].message.content #type: ignore
        if output:
            return output
        else:
            raise Exception("Something went wrong when calling the Mistral API. Trying again in a few seconds...")
    
    except Exception as e:
        print(f"An error was caught just in time when retrieving a response from the LLM:\n{e}")
        time.sleep(5)
        mistral_explain_and_recommend(scores_dict, user_text)


if __name__ == "__main__":
    print("Hi! This script is meant to be imported and not run directly. There should be some app.py somewhere to be run with `streamlit run app.py`")