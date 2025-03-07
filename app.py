import streamlit as st
import requests
import io
from PIL import Image

# URL de ton API déployée sur RunPod
API_URL = st.secrets["api_url"]
API_key = st.secrets["api_key"]

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {API_key}'
}



st.title("🎨 Générateur de Styles pour vos rendus extérieur et intérieur")

# Interface de chargement d'image
uploaded_file = st.file_uploader("📤 Téléchargez une image", type=["jpg", "png", "jpeg"])
style_choice = st.selectbox("🎭 Choisissez un style", ["Moderne", "Méditerrannéen", "Moderne Tropicale"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Image originale", use_container_width=True)

    if st.button("✨ Générer le style"):
        with st.spinner("Génération en cours... ⏳"):
            # Préparer l'image pour l'API
            img_bytes = io.BytesIO()
            image.save(img_bytes, format="PNG")
            img_bytes.seek(0)

            # Envoyer l'image et le style à l'API RunPod
            files = {"file": ("image.png", img_bytes, "image/png")}
            data = {"style": style_choice}
            response = requests.post(API_URL, headers=headers, files=files, data=data)


            if response.status_code == 200:
                # Charger l'image générée
                output_image = Image.open(io.BytesIO(response.content))
                st.image(output_image, caption=f"Style : {style_choice}", use_container_width=True)

                # Ajouter un bouton de téléchargement
                st.download_button(
                    label="📥 Télécharger l'image stylisée",
                    data=response.content,
                    file_name=f"styled_{style_choice.lower()}.png",
                    mime="image/png"
                )
            else:
                st.error("Erreur lors de la génération. Vérifiez votre API ! 🚨")
