import streamlit as st
import importlib

# Set layout
st.set_page_config(layout='wide')

# Show AI_banner.jpg on the main page
st.sidebar.image("AI_banner.jpg", use_column_width=True)

# Import pages modules dynamically
pages_dict = {
    "Prompt": "pages.prompt",
    "Tekening": "pages.tekening",
    "Vul mijn bord": "pages.vul_mijn_bord",
    "Een artikel schrijven": "pages.een_artikel_schrijven",
    "QR-code": "pages.qr_code",
    "download youtube video": "pages.download_youtube",
}

# Sidebar navigation
st.sidebar.title('Navigatie')
selection = st.sidebar.radio("Ga naar:", list(pages_dict.keys()))

# Load the selected page
page = importlib.import_module(pages_dict[selection])
page.app()

