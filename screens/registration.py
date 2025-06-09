# FaceNetAttendanceSystem/pages/registration.py
import streamlit as st
import cv2
import os
import datetime
import time
import pandas as pd
from utils.database import init_db, insert_student_detail

# Ensure the database and tables are initialized
init_db()

def capture_50_images(enrollment, name, num_images=50):
    # Create a folder for the specific person under data/training_images
    training_dir = os.path.join("data", "training_images", f"{name}_{enrollment}")
    os.makedirs(training_dir, exist_ok=True)
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        st.error("Error: Could not open webcam.")
        return False

    live_feed = st.empty()
    st.info("Live camera feed is active. Capturing images, please wait...")

    for i in range(num_images):
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to capture image from webcam.")
            break
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        live_feed.image(frame_rgb, channels="RGB")
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        filename = f"{name}_{enrollment}_{timestamp}_{i}.jpg"
        filepath = os.path.join(training_dir, filename)
        cv2.imwrite(filepath, frame)
        time.sleep(0.1)

    cap.release()
    live_feed.empty()
    return True

def app():
    st.title("Student Registration with Automatic Image Capture")
    st.write("Enter your enrollment number and name, then click the button below to capture 50 images automatically for robust training.")
    
    # ← Add these two lines (they may already exist)
    enrollment = st.text_input("Enter Enrollment Number")
    name       = st.text_input("Enter Student Name")
    
    if enrollment and name:
        if st.button("Capture 50 Images Automatically"):
            with st.spinner("Capturing images..."):
                success = capture_50_images(enrollment, name)
            if success:
                st.success(f"Successfully captured 50 images for {name} (Enrollment: {enrollment}).")
                
                # Write student details to the database after successful capture
                now = datetime.datetime.now()
                insert_student_detail(
                    enrollment,
                    name,                         # ← now passing the real name
                    now.strftime("%Y-%m-%d"),
                    now.strftime("%H:%M:%S"),
                    50
                )
            else:
                st.error("Image capture failed. Please check your webcam and try again.")
    else:
        st.warning("Please enter both Enrollment Number and Student Name.")
