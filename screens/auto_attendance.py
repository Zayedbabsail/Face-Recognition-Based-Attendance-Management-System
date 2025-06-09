# FaceNetAttendanceSystem/pages/auto_attendance.py
import streamlit as st
import datetime
from PIL import Image
from utils.face_recognition import recognize_face
from utils.database import init_db, insert_attendance, get_all_attendance

# Ensure the database is initialized
init_db()

def app():
    st.title("Automatic Attendance")
    subject = st.text_input("Enter Subject Name", "")
    
    st.write("Capture your face for attendance:")
    image_data = st.camera_input("Take your attendance photo")
    
    if st.button("Mark Attendance"):
        if subject == "" or image_data is None:
            st.error("Please provide a subject name and capture your photo!")
        else:
            # Get recognition result from the model
            folder_label, auto_name = recognize_face(image_data)
            if folder_label is None:
                st.error("Face not recognized. Please try again.")
            else:
                # Parse the recognized folder label assuming the format "Name_Enrollment"
                parts = folder_label.split("_", 1)
                if len(parts) == 2:
                    parsed_name, parsed_enrollment = parts
                else:
                    parsed_name = auto_name  # fallback to auto_name if parsing fails
                    parsed_enrollment = folder_label

                now = datetime.datetime.now()
                date_str = now.strftime("%Y-%m-%d")
                time_str = now.strftime("%H:%M:%S")
                
                # Insert the attendance record into the database with parsed values
                insert_attendance(parsed_enrollment, parsed_name, subject, date_str, time_str)
                
                st.success(f"Attendance marked for {parsed_name} (Enrollment: {parsed_enrollment})")
                
                # Retrieve and display all attendance records from the database
                df_attendance = get_all_attendance()
                if df_attendance is not None and not df_attendance.empty:
                    st.write("All Attendance Records:")
                    st.dataframe(df_attendance)
