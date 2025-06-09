# FaceNetAttendanceSystem/app.py
import streamlit as st

def main():
    # Set the page configuration
    st.set_page_config(page_title="FaceNet Attendance System", layout="wide")
    
    # Sidebar for custom navigation
    st.sidebar.title("Navigation")
    options = ["Home", "Registration", "Train", "Automatic Attendance", "Manual Attendance", "Admin"]
    choice = st.sidebar.radio("Go to", options)
    

    # Routing to different pages from the "screens" folder
    if choice == "Home":
        from screens import home
        home.app()
    elif choice == "Registration":
        from screens import registration
        registration.app()
    elif choice == "Train":
        from screens import train
        train.app()
    elif choice == "Automatic Attendance":
        from screens import auto_attendance
        auto_attendance.app()
    elif choice == "Manual Attendance":
        from screens import manual_attendance
        manual_attendance.app()
    elif choice == "Admin":
        from screens import admin
        admin.app()

if __name__ == "__main__":
    main()
