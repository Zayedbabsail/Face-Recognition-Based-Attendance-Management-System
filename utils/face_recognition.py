# FaceNetAttendanceSystem/utils/face_recognition.py
import os
import time
import torch
import numpy as np
from PIL import Image
from facenet_pytorch import MTCNN, InceptionResnetV1
import pickle
from sklearn.svm import SVC

# Set up device and models
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
mtcnn = MTCNN(image_size=160, margin=0, device=device)
resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)

def extract_face_embedding(image_path):
    try:
        img = Image.open(image_path)
    except Exception as e:
        print(f"Error opening image {image_path}: {e}")
        return None

    face = mtcnn(img)
    if face is None:
        return None
    face = face.unsqueeze(0).to(device)
    embedding = resnet(face)
    return embedding.detach().cpu().numpy()[0]

def train_model():
    training_dir = os.path.join("data", "training_images")
    if not os.path.exists(training_dir):
        return "Training folder not found. Please register some students first."
    
    embeddings = []
    labels = []
    
    for person_folder in os.listdir(training_dir):
        person_path = os.path.join(training_dir, person_folder)
        if os.path.isdir(person_path):
            label = person_folder  # e.g., "Zayed_20"
            for file in os.listdir(person_path):
                if file.endswith(".jpg"):
                    img_path = os.path.join(person_path, file)
                    embedding = extract_face_embedding(img_path)
                    if embedding is not None:
                        embeddings.append(embedding)
                        labels.append(label)
    
    if len(embeddings) == 0:
        return "No valid faces detected in training images."
    
    unique_labels = set(labels)
    if len(unique_labels) < 2:
        return ("Training requires at least two different classes (students). "
                f"Currently, only {len(unique_labels)} class is found. Please register at least one more student.")
    
    embeddings = np.array(embeddings)
    classifier = SVC(kernel='linear', probability=True)
    classifier.fit(embeddings, labels)
    
    model_dir = os.path.join("data", "model")
    os.makedirs(model_dir, exist_ok=True)
    model_file = os.path.join(model_dir, "facenet_classifier.pkl")
    with open(model_file, "wb") as f:
        pickle.dump(classifier, f)
    
    num_persons = len(unique_labels)
    return f"Model trained with {len(embeddings)} images from {num_persons} persons. Classifier saved to {model_file}"

def recognize_face(image_data):
    """
    Recognize a face from the provided image_data.
    Returns (enrollment, name) if recognized, otherwise (None, None).
    """
    try:
        img = Image.open(image_data)
    except Exception as e:
        print("Error processing input image:", e)
        return None, None
    
    face = mtcnn(img)
    if face is None:
        return None, None
    face = face.unsqueeze(0).to(device)
    embedding = resnet(face)
    embedding_np = embedding.detach().cpu().numpy()[0]
    
    model_file = os.path.join("data", "model", "facenet_classifier.pkl")
    if not os.path.exists(model_file):
        return None, None
    with open(model_file, "rb") as f:
        classifier = pickle.load(f)
    
    prediction = classifier.predict([embedding_np])[0]  # e.g., "Zayed_20"
    probability = classifier.predict_proba([embedding_np]).max()
    if probability < 0.6:
        return None, None
    
    # Parse the folder name assuming format "Name_Enrollment"
    parts = prediction.split("_", 1)
    if len(parts) == 2:
        parsed_name = parts[0]
        parsed_enrollment = parts[1]
    else:
        parsed_name = prediction
        parsed_enrollment = "Unknown"
    
    return parsed_enrollment, parsed_name
