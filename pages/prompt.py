import streamlit as st
import openai

OPENAI_API_KEY = st.secrets["openai_api_key"]
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def app():
    st.title("Deze pagina bevat een applicatie om tekst te genereren")

    st.write("Voer een prompt in om een tekst te genereren:")
    prompt = st.text_area("Prompt")

    if st.button("Genereer tekst"):
        with st.spinner("Bezig met genereren..."):
            completion = client.chat.completions.create(
                model="gpt-4-turbo-preview",
                max_tokens=1000,
                messages=[
                    {"role": "system", "content": "Jij bent een virtuele assistent en geeft een antworod aan de hand van een prompt."},
                    {"role": "user", "content": prompt}
                ]
            )
            st.write(completion.choices[0].message.content)