# Face-Recognition-Based-Attendance-Management-System

An intelligent, face-recognition-based attendance management system built using **Streamlit**, **FaceNet**, and **SQLite**. This project automates student attendance by identifying faces via webcam input and maintaining secure records.

---

## 🔧 Features

- 📷 **Automatic Image Capture**: Captures 50 images per student for accurate face embedding.
- 🤖 **Face Recognition**: Uses FaceNet + MTCNN to extract high-quality facial embeddings.
- 🧠 **Model Training**: Trains an SVM classifier on the captured embeddings.
- 📋 **Automatic Attendance**: Recognizes faces from webcam and marks attendance with timestamp and subject.
- ✍️ **Manual Attendance**: Allows manual entry of attendance.
- 🔐 **Admin Panel**: Protected access to student details and full attendance logs.

---
## 🧪 Usage Flow

### 📌 Register Student
- Navigate to **Registration**.
- Enter **Enrollment Number** & **Name**.
- Click **"Capture 50 Images Automatically"**.

### 🧠 Train Model
- Go to the **Train** section.
- Click **"Train Model"** to update the FaceNet classifier.

### 📷 Mark Attendance
- Go to **Automatic Attendance**.
- Enter the **Subject**, capture a **webcam image**, and click **"Mark Attendance"**.

### ✍️ Manual Attendance
- Used for **fallback entry or corrections**.

### 🔐 Admin Panel
- **Username**: ``  
- **Password**: ``  
- View **registered students** and **attendance logs**.

---

## 🧠 Model Details

- **Face Detection**: MTCNN  
- **Face Embedding**: FaceNet (`InceptionResnetV1`)  
- **Classifier**: Linear SVM trained on face embeddings  
- **Threshold**: Confidence score ≥ `0.6` to accept a prediction

---

## 💡 Future Improvements

- 🧾 Export attendance to **CSV/Excel**
- 🔄 Real-time attendance stream with **continuous video feed**
- ☁️ Cloud-based storage (**Firebase** or **AWS**)
- 🧬 Enhanced face preprocessing (**augmentation**, **lighting normalization**)
- 🔒 Encrypted login for **multiple admin roles**


