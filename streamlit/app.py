import streamlit as st
import pandas as pd

progress = 1
progress_bar = st.progress(progress)
progress_step = 100 // 6

def display_response(answer, progress):
    if answer:
        st.write(f"Done! you said {answer}")
        new_progress = progress + progress_step
        progress_bar.progress(new_progress)
        return new_progress
    else:
        st.write("")
        return 0

q_1 = st.text_input("### What personality type do you think you are?")
progress = display_response(q_1, progress)

q_2 = st.text_input("### Question 2")
progress = display_response(q_2, progress)

q_3 = st.text_input("### Question 3")
progress = display_response(q_3, progress)

q_4 = st.text_input("### Question 4")
progress = display_response(q_4, progress)

q_5 = st.text_input("### Question 5")
progress = display_response(q_5, progress)

if q_1 and q_2 and q_3 and q_4 and q_5:
    progress_bar.progress(100)
    st.write("### Here is your result:")
    st.image("src/wzrd.jpg")