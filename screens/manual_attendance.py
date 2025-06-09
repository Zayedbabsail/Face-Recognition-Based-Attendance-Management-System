# FaceNetAttendanceSystem/screens/manual_attendance.py
import streamlit as st
import datetime
from utils.database import init_db, insert_attendance, get_all_attendance

# Ensure the database is initialized
init_db()

def app():
    st.title("Manual Attendance")
    st.write("Enter attendance details manually below.")
    
    enrollment = st.text_input("Enrollment Number")
    name = st.text_input("Student Name")
    subject = st.text_input("Subject")
    
    if st.button("Mark Attendance"):
        if not (enrollment and name and subject):
            st.error("Please fill in all fields.")
        else:
            now = datetime.datetime.now()
            date_str = now.strftime("%Y-%m-%d")
            time_str = now.strftime("%H:%M:%S")
            
            # Insert the attendance record into the database
            insert_attendance(enrollment, name, subject, date_str, time_str)
            
            st.success(f"Attendance marked for {name} (Enrollment: {enrollment}).")
    
    st.subheader("All Attendance Records")
    df_attendance = get_all_attendance()
    if df_attendance is not None and not df_attendance.empty:
        st.dataframe(df_attendance)
    else:
        st.info("No attendance records found.")
