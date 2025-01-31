import os
import requests
import plotly.express as px
import streamlit as st
import base64
from PIL import Image


API_BASE_URL = os.getenv("API_BASE_URL")
GREEN_COLOR = "#4CAF50"
RED_COLOR = "#FF6347"


# Fonction pour convertir une image locale en base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

# Chemins des images
SPLASH_IMAGE = "images/image_splash_screen.jpg"
IMAGE_1 = "images/image_1.jpg"
IMAGE_2 = "images/image_2.jpg"
IMAGE_3 = "images/image_3.jpg"
IMAGE_4 = "images/image_4.jpg"
IMAGE_5 = "images/image_5.jpg"
IMAGE_6 = "images/image_6.jpg"
IMAGE_7 = "images/image_7.jpg"

# Convertir les images nécessaires en base64
splash_image_base64 = get_base64_image(SPLASH_IMAGE)

# Définir et lire les paramètres d'URL
query_params = st.query_params
current_step = query_params.get("step", "splash")

# Simuler un rafraîchissement automatique avec JavaScript
def auto_refresh(step, delay=3000):
    st.markdown(
        f"""
        <meta http-equiv="refresh" content="{delay / 1000}; url=/?step={step}">
        """,
        unsafe_allow_html=True,
    )

# Étape 1 : Splash Screen
if current_step == "splash":
    st.markdown(
        f"""
        <style>
        .splash-container {{
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: black;
        }}
        .splash-image {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}
        .text-overlay {{
            position: absolute;
            bottom: 7%;
            color: white;
            font-size: 6rem;
            font-weight: bold;
            text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.8);
            text-align: center;
            width: 100%;
        }}
        </style>
        <div class="splash-container">
            <img src="data:image/png;base64,{splash_image_base64}" class="splash-image">
            <div class="text-overlay">PulmoAId</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    auto_refresh("transition", delay=3000)

# Étape 2 : Page de Transition
elif current_step == "transition":
    # Ajouter une version centrée et réduite du texte
    st.markdown(
        """
        <style>
        .title-container {
            text-align: center;
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .subtitle {
            font-size: 2rem; 
            display: block;
            margin-top: 5px;
        }
        .caption {
            text-align: center;
            font-size: 1rem;
            color: white;
            margin-top: 5px;
        }
        .image-container {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 10px;
        }
        .image-item {
            width: 200px;
            height: 200px;
            position: relative;
        }
        .image-item img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        .image-caption {
            position: absolute;
            bottom: 0;
            width: 100%;
            background: rgba(0, 0, 0, 0.5);
            color: white;
            text-align: center;
            padding: 5px;
        }
        </style>
        <div class="title-container">
            <span>The app that will help you diagnose these</span>
            <br>
            <span class="subtitle">7 lung diseases:</span>
        </div>
        """,
        unsafe_allow_html=True
    )

# Disposition des images en lignes
    st.markdown(
        f"""
        <div class="image-container">
            <div class="image-item">
                <img src="data:image/jpeg;base64,{get_base64_image(IMAGE_1)}" alt="Image 1">
                <div class="image-caption">Higher density</div>
            </div>
            <div class="image-item">
                <img src="data:image/jpeg;base64,{get_base64_image(IMAGE_2)}" alt="Image 2">
                <div class="image-caption">Lower density</div>
            </div>
            <div class="image-item">
                <img src="data:image/jpeg;base64,{get_base64_image(IMAGE_3)}" alt="Image 3">
                <div class="image-caption">Chest changes</div>
            </div>
            <div class="image-item">
                <img src="data:image/jpeg;base64,{get_base64_image(IMAGE_4)}" alt="Image 4">
                <div class="image-caption">Encapsulated Lesions</div>
            </div>
            <div class="image-item">
                <img src="data:image/jpeg;base64,{get_base64_image(IMAGE_5)}" alt="Image 5">
                <div class="image-caption">Obstructive Pulmonary Diseases</div>
            </div>
            <div class="image-item">
                <img src="data:image/jpeg;base64,{get_base64_image(IMAGE_6)}" alt="Image 6">
                <div class="image-caption">Mediastinal Changes</div>
            </div>
            <div class="image-item">
                <img src="data:image/jpeg;base64,{get_base64_image(IMAGE_7)}" alt="Image 7">
                <div class="image-caption">Degenerative Infectious Diseases</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Liste des créateurs
    st.markdown(
    """
    <style>
    .creator-list {
        text-align: center;
        font-size: 1.15rem;
        font-weight: bold;
        color: white;
        margin-top: 40px;
    }
    </style>
    <div class="creator-list">
        Made by: Sophie Laussel, Eugénie Modolo, Juliette Rodrigues, David Remond
    </div>
    """,
        unsafe_allow_html=True
)
    auto_refresh("main", delay=6000)
    
# Étape 3 : Page principale
elif current_step == "main":
    st.set_page_config(
        page_title="PulmoAId",
        layout='wide',
        page_icon='🫁')

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stMainBlockContainer {padding-top: 0rem; padding-bottom: 0rem;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title("Pulmonary Diagnosis Aid", anchor=False)

col1, col2, col3 = st.columns(3, gap="small", vertical_alignment="top", border=True)

with col1:
   
    st.subheader("Patient", anchor=False)
    st.html('<hr style="border: none; height: 1px; background-color: #444444;"/>')

    uploaded_file = st.file_uploader("Choose a chest x-ray image :", type=["png", "jpg"], accept_multiple_files=False)

    if uploaded_file is not None:
        # Display image
        st.html('<hr style="border: none; height: 1px; background-color: #444444;"/>')
        col11, col12 = st.columns(2, gap="small", vertical_alignment="top", border=False)
        with col11:
            st.markdown("Original image")
            image = Image.open(uploaded_file)
            st.image(image, use_container_width=False )
        with col12:
            st.markdown("Detection image")
            if uploaded_file is not None:
                bytes_data = uploaded_file.getvalue()
                api_url = f"{API_BASE_URL}/detected_zones"
                files = {'file': (uploaded_file.name, bytes_data, uploaded_file.type)}
                with st.spinner('Pending analysis...'):
                    response = requests.post(api_url, files=files)
                detected_zones_result = response.json()
                st.image(f"data:image/png;base64,{detected_zones_result['image_with_detected_zones']}", use_container_width=True)

with col2:

    st.subheader("Results", anchor=False)
    st.html('<hr style="border: none; height: 1px; background-color: #444444;"/>')

    if uploaded_file is not None:
        # Run prediction
        bytes_data = uploaded_file.getvalue()
        api_url = f"{API_BASE_URL}/predict"
        files = {'file': (uploaded_file.name, bytes_data, uploaded_file.type)}
        with st.spinner('Pending analysis...'):
            response = requests.post(api_url, files=files)
        result = response.json()

        # Display results
        col21, col22 = st.columns([2, 1], gap="small", vertical_alignment="top", border=False)
        primary_color = RED_COLOR if result['has_pathology'] else GREEN_COLOR
        with col21:
            st.html(f'''
                <div style="
                    border: 1px solid {primary_color};
                    padding: 10px;
                    border-radius: 5px;
                    margin: 10px 0;
                ">
                    {'<div>Pathology Detected</div>' if result['has_pathology'] else '<div>No Pathology Detected</div>'}
                    <div style="font-size:24px;color:{primary_color};">{result['prediction']['name']}</div>
                </div>
        ''')
        with col22:
            st.html(f'''
                <div style="
                    border: 1px solid {primary_color};
                    padding: 10px;
                    border-radius: 5px;
                    margin: 10px 0;
                    text-align: right;
                ">
                    <div>Confidence Ratio</div>
                    <div style="font-size:24px;color:{primary_color};">{f'{round(result['prediction']['ratio'], 1)} %'}</div>
                </div>
        ''')
    
        st.subheader("Ranking", anchor=False)
        st.html('<hr style="border: none; height: 1px; background-color: #444444;"/>')

        fig = px.bar(result['ranking'], x='name', y='ratio', color_discrete_sequence=[primary_color], text="displayed_ratio")
        fig.update_layout(xaxis_title='Pathology', yaxis_title='Ratio (%)')
        st.plotly_chart(fig, border=True)
    else:
        st.write("Please upload a chest x-ray image.")

with col3:
    
    st.subheader("Similar X-rays", anchor=False)
    st.html('<hr style="border: none; height: 1px; background-color: #444444;"/>')

    if uploaded_file is not None:
        st.markdown("Here are some samples of chest x-ray images :")
        
        # Get similar xrays
        api_url = f"{API_BASE_URL}/similar_xrays"
        class_names = [f"class_names={item['name'].lower()}" for item in result['ranking'] if item['ratio'] > 0.1]
        class_names = str.join("&", class_names)
        with st.spinner('Pending analysis...'):
            print(f'{api_url}?{class_names}')
            response = requests.get(f'{api_url}?{class_names}')
        xrays_result = response.json()
        
        # Display similar xrays
        for class_name, images in xrays_result['samples'].items():
            st.markdown(f"**{class_name.title()}**")
            cols = st.columns(len(images), gap="small", vertical_alignment="top", border=False)
            for i, image in enumerate(images):
                with cols[i]:
                    st.image(f"data:image/png;base64,{image}")
        
        
    else:
        st.write("Please upload a chest x-ray image.")