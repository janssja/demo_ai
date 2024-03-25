import streamlit as st
import qrcode
from PIL import Image
import io

# Generate QR Code
def app():
    st.title("Met AI gratis een QR-code genereren")

    prompt = st.text_area("Voer de website in waar de QR-code naar moet verwijzen:")
    fill_color = st.color_picker('Kies de vulkleur voor de QR-code', '#000000')  # Zwart als standaard
    back_color = st.color_picker('Kies de achtergrondkleur voor de QR-code', '#FFFFFF')  # Wit als standaard
    
    if st.button("Genereer QR-code"):
        with st.spinner("Bezig met genereren..."):
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(prompt)
            qr.make(fit=True)

            # Create an image from the QR Code instance
            img = qr.make_image(fill_color=fill_color, back_color=back_color)

            # Convert PIL Image to bytes
            buf = io.BytesIO()
            img.save(buf, format='PNG')
            byte_im = buf.getvalue()

            st.image(byte_im)

