import streamlit as st
import openai
import os

# Haal de API-sleutel op uit de Streamlit secrets en initialiseer de OpenAI-client
OPENAI_API_KEY = st.secrets["openai_api_key"]
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Bepaal de paden naar de afbeeldingen
current_dir = os.path.dirname(__file__)
image_path = os.path.join(current_dir, "bord_512.png")
mock_path = os.path.join(current_dir, "bord_mock_512.png")

def app():
    st.title("Een bord vullen met een ander gerecht")

    # Controleer of de knop al is ingedrukt
    if 'image_generated' not in st.session_state:
        st.session_state.image_generated = False

    if not st.session_state.image_generated:
        st.image(image_path)
        prompt = st.text_area("Hoe wilt u dit bord vullen:")

        if st.button("Gerecht bereiden"):
            with st.spinner("Bezig met het bereiden van het gerecht..."):
                response = client.images.edit(
                    model="dall-e-2",
                    image=open(image_path, "rb"),
                    mask=open(mock_path, "rb"),
                    prompt=prompt,
                    n=1,
                    size="512x512"
                )

            # Bewaar de URL van het bewerkte beeld
            st.session_state.image_url = response.data[0].url
            col1, col2 = st.columns(2)
            with col1:
                st.write("Origineel")
                st.image(image_path, use_column_width=True)
            with col2:
                st.write("Bewerkt")
                st.image(st.session_state.image_url, use_column_width=True)
        
