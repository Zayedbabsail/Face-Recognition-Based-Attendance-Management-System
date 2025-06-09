# FaceNetAttendanceSystem/pages/admin.py
import streamlit as st
import pandas as pd
import os
from utils.database import init_db, get_student_details, get_all_attendance

# Ensure database is initialized
init_db()

# Hard-coded admin credentials
ADMIN_USERNAME = "Zayed"
ADMIN_PASSWORD = "Zayed123"

def admin_panel():
    st.title("Admin Panel")
    st.write("Welcome to the admin panel. Use the options below to view system data.")

    tab1, tab2 = st.tabs(["Student Details", "Attendance Records"])

    with tab1:
        st.subheader("Registered Student Details")
        df_students = get_student_details()
        if df_students is not None and not df_students.empty:
            st.dataframe(df_students)
        else:
            st.info("No student details found.")

    with tab2:
        st.subheader("All Attendance Records")
        df_attendance = get_all_attendance()
        if df_attendance is not None and not df_attendance.empty:
            st.dataframe(df_attendance)
        else:
            st.info("No attendance records found.")
    if st.button('logout'):
        st.session_state.admin_logged_in = False

def app():
    st.title("Admin Login")
    
    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False

    if not st.session_state.admin_logged_in:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Log In"):
            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                st.session_state.admin_logged_in = True
                st.success("Logged in successfully!")
                st.experimental_rerun()
            else:
                st.error("Incorrect username or password.")
    else:
        admin_panel()
