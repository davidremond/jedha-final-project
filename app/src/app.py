import os
import requests
import plotly.express as px
import streamlit as st
from PIL import Image

API_BASE_URL = os.getenv("API_BASE_URL")
GREEN_COLOR = "#4CAF50"
RED_COLOR = "#FF6347"

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