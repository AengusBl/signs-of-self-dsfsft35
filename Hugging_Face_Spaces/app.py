import streamlit as st
from llm_calls import mistral_explain_and_recommend, ask_bert_for_scores
import threading

st.set_page_config(
    page_title="Test de personnalité",
    page_icon= "images/favicon_big5.png",
    layout="centered"
  )

def fire_and_forget_api_call():
    thread = threading.Thread(target=ask_bert_for_scores)
    thread.daemon = True
    thread.start()


# Our LightningAI Bert API takes a long time to fire up and shuts down easily:
# We want to start it up early and keep it awake so it's ready when needed.
fire_and_forget_api_call()

st.markdown("# Signs of Self")

questions = [
    "Si vous aviez l’opportunité d’apprendre une nouvelle compétence ou de changer de voie professionnelle, que choisiriez-vous&nbsp;? Pourquoi&nbsp;?",
    "Un collègue ou un ami traverse une période difficile. Quelle est votre réaction spontanée, et jusqu’où êtes-vous prêt(e) à l’aider&nbsp;?",
    "Que faites-vous généralement lorsque vous vous sentez stressé(e) ou sous pression&nbsp;?",
    "Comment vous organisez-vous lorsque vous avez un projet important à mener&nbsp;?",
    "Lorsque vous avez du temps libre, préférez-vous passer du temps seul(e) ou entouré(e)&nbsp;? Que faites-vous alors&nbsp;?",
    "Comment réagissez-vous lorsqu’un événement imprévu bouleverse vos plans&nbsp;?",
    "Racontez une situation où vous êtes sorti(e) de votre zone de confort. Qu’est-ce que cela vous a apporté&nbsp;?",
    "Si vous receviez une somme importante d’argent de manière inattendue (légalement&nbsp;!), que feriez-vous en premier&nbsp;? Pourquoi&nbsp;?"
]

progress = 1
progress_bar = st.progress(progress)
progress_step = 100 // len(questions)

inputs = dict()

def take_in_response(answer, progress, question_index) -> int:
    if answer:
        st.write(f"Compris !")
        inputs[question_index] = answer
        new_progress = progress + progress_step
        progress_bar.progress(new_progress)
        return new_progress
    else:
        inputs[question_index] = False
        st.write(" ")
        return 0 # no progress
    
for q_index, question in enumerate(questions):
    response = st.text_input(question)
    progress = take_in_response(response, progress, q_index)

input_values = inputs.values()

total_input_len = sum([len(value) for value in input_values if value])

st.write(f"Nombre de caractères&nbsp;: {total_input_len}/4,000")

if all(input_values) and ("" not in input_values) and (total_input_len <= 4_000):
    with st.spinner(text="Veuillez patienter, je lis vos pensées..."):
        merged_input = ""
        for input in input_values:
            merged_input += input + "\n"
        bert_scores = ask_bert_for_scores(endpoint="predict",fr_input=merged_input)

        if isinstance(bert_scores, str): # This would mean there was an error that couldn't be bypassed, and we need parse a fallback output instead
            full_response = bert_scores
        else:
            full_response = mistral_explain_and_recommend(bert_scores, merged_input)

        try:
            response, explanation = full_response.split("Explication :")
        except Exception as e:
            print(f"An error was encountered when parsing a response from the LLM:\n{e}")
            response = full_response[:]
            with open("./fallback_explanation.md", "r") as f:
                explanation = f.read()

        progress_bar.progress(100)
        st.markdown("### Vos scores&nbsp;:")
        st.markdown(response)

    with st.expander("### Explication et conseils&nbsp;:"):
        st.markdown(explanation)