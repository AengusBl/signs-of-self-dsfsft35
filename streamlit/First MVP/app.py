import streamlit as st
from mistral_personalities import get_personality_type

st.set_page_config(
    page_title="Test de personnalité",
    page_icon="🥸",
    layout="centered"
  )

st.markdown("# Signs of Self")

questions = [
    "If you had the opportunity to learn a new skill or change jobs, what would you choose? Explain why.",
    "Say a colleague or friend of yours is having a hard time. What is your spontaneous reaction, and how far would you go to help them?",
    "What do you typically do when stressed or under pressure?",
    "How do you get organised if you have to take on an important project?",
    "Do you prefer to spend your free time alone or around others? What do you like to do then?",
    "If something unexpected throws a wrench in some plans you had, what is your reaction?",
    "Tell a story about a time when you stepped out of your confort zone. Did you get anything out of it?",
    "Imagine you unexpectedly just acquired a huge amount of money (through legal means, of course). What would be your first course of action? Explain why."
]

# The French questions we agreed on, before translation:
#   Si vous aviez l’opportunité d’apprendre une nouvelle compétence ou de changer de voie professionnelle, que choisiriez-vous ? Et pourquoi ?
#   Un collègue ou un ami traverse une période difficile. Quelle est votre réaction spontanée, et jusqu’où êtes-vous prêt(e) à l’aider ?
#   Que faites-vous généralement lorsque vous vous sentez stressé(e) ou sous pression ?
#   Comment vous organisez-vous lorsque vous avez un projet important à mener ?
#   Lorsque vous avez du temps libre, préférez-vous passer du temps seul(e) ou entouré(e) ? Que faites-vous alors ?
#   Comment réagissez-vous lorsqu’un événement imprévu bouleverse vos plans ?
#   Racontez une situation où vous êtes sorti(e) de votre zone de confort. Qu’est-ce que cela vous a apporté ?
#   Si vous receviez une somme importante d’argent de manière inattendue, que feriez-vous en premier ? Pourquoi ?

inputs = dict()

progress = 1
progress_bar = st.progress(progress)
progress_step = 100 // len(questions)

def take_in_response(answer, progress, question_index):
    if answer:
        st.write(f"Done!")
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

st.write(f"Character count: {total_input_len}/4,000")

if all(input_values) and ("" not in input_values) and (total_input_len <= 4_000):
    with st.spinner(text="Hang in there while I read your mind..."):
        merged_input = ""
        for input in input_values:
            merged_input += input + "\n"
        full_response = get_personality_type(merged_input)
        try:
            response, explanation = full_response.split("Explanation:")
        except Exception as e:
            print(f"An error was encountered when parsing a response from the LLM:\n{e}")
            response = full_response[:]
            with open("./fallback_explanation.md", "r") as f:
                explanation = f.read()
        progress_bar.progress(100)
        st.markdown("### Your scores:")
        st.markdown(response)
    with st.expander("Why these scores?"):
        st.markdown(explanation)