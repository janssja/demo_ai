import streamlit as st
import openai

OPENAI_API_KEY = st.secrets["openai_api_key"]
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def app():
    st.title("Deze pagina bevat de applicatie om een tekening te maken")

    st.write("Voer een prompt in om een tekst te genereren:")
    prompt = st.text_area("Prompt")

    if st.button("Genereer tekening"):
        with st.spinner("Bezig met genereren..."):
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                quality="standard",
            n=1,
            )

        image_url = response.data[0].url
        st.image(image_url, width=512)