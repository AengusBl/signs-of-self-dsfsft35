import streamlit as st
from mistral_personalities import get_personality_type

st.set_page_config(
    page_title="Test de personnalité",
    page_icon="🥸",
    layout="centered"
  )

progress = 1
progress_bar = st.progress(progress)

q_1 = st.text_input("### Écrivez quelque chose:")
if q_1:
    st.write("Compris!")
    progress_bar.progress(50)
    with st.spinner(text="Patientez un instant pendant que je lis vos pensées..."):
        response = get_personality_type(q_1)
        progress_bar.progress(100)
        st.write("### Voilà votre résultat:")
        st.markdown(response)
    with st.expander("Pourquoi ce résultat?"):
        st.write("Parce que.")
else:
    st.write("")