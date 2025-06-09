# pages/train.py
import streamlit as st
from utils.face_recognition import train_model

def app():
    st.title("Train Model")
    st.write("Train the FaceNet-based model using captured images from individual person folders.")

    if st.button("Train Model"):
        with st.spinner("Training in progress..."):
            result = train_model()
        st.success("Model trained successfully!")
        st.write(result)
