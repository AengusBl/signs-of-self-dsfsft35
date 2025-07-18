import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Test de personnalité",
    page_icon="🥸",
    layout="centered"
  )

progress = 1
progress_bar = st.progress(progress)
progress_step = 100 // 5

def display_response(answer, progress):
    if answer:
        st.write(f"Compris! Vous avez dit {answer}")
        new_progress = progress + progress_step
        progress_bar.progress(new_progress)
        return new_progress
    else:
        st.write("")
        return 0

q_1 = st.text_input("### À quel type de personnalité pensez-vous appartenir&nbsp;?")
progress = display_response(q_1, progress)

q_2 = st.text_input("### Question 2")
progress = display_response(q_2, progress)

q_3 = st.text_input("### Question 3")
progress = display_response(q_3, progress)

q_4 = st.text_input("### Question 4")
progress = display_response(q_4, progress)

q_5 = st.text_input("### Question 5")
progress = 100 - progress_step
display_response(q_5, progress)

if q_1 and q_2 and q_3 and q_4 and q_5:
    st.write("### Voilà votre résultat:")
    st.image("src/wzrd.jpg")