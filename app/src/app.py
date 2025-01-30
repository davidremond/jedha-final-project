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
            st.image(image, use_container_width=False, )
        with col12:
            st.markdown("Detection image")
            with st.spinner('Pending analysis...'):
                st.write("TODO : Call API")

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
        with st.spinner('Pending analysis...'):
            st.write("TODO : Call API")
    else:
        st.write("Please upload a chest x-ray image.")