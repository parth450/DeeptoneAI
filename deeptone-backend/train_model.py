import os
import numpy as np
import librosa
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import joblib
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report, accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# === CONFIG ===
DATASET_PATH = './dataset'
MODEL_PATH = './model/trained_model.pkl'
GRAPH_DIR = './app/static/images'
os.makedirs(GRAPH_DIR, exist_ok=True)

# === Feature Extraction ===
def extract_features(file_path):
    print(f"Loading file: {file_path}")
    y, sr = librosa.load(file_path, sr=None)
    print(f"Audio loaded: {file_path} - duration: {len(y)/sr:.2f}s, sample rate: {sr}")
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_mean = np.mean(mfcc, axis=1)
    return mfcc_mean

# === Load Dataset ===
def load_dataset(dataset_path):
    X, y = [], []


    real_dir = os.path.join(dataset_path, 'real')
    fake_dir = os.path.join(dataset_path, 'fake')

    print("Looking in:", real_dir)
    for file in os.listdir(real_dir):
        if file.endswith('.wav'):
            features = extract_features(os.path.join(real_dir, file))
            X.append(features)
            y.append(0)  # Real

    print("Looking in:", fake_dir)
    for file in os.listdir(fake_dir):
        if file.endswith('.wav'):
            features = extract_features(os.path.join(fake_dir, file))
            X.append(features)
            y.append(1)  # Fake

    return np.array(X), np.array(y)

# === Train Model and Save ===
def train_and_save_model():
    print("Loading dataset...")
    X, y = load_dataset(DATASET_PATH)

    print("Training model...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=50, random_state=1)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # === Save Model ===
    joblib.dump(model, MODEL_PATH)
    print(f"Model saved at: {MODEL_PATH}")

    # === Metrics ===
    print("\n=== CLASSIFICATION REPORT ===")
    print(classification_report(y_test, y_pred, target_names=['Real', 'Fake']))

    acc = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {acc * 100:.2f}%")

    # === Confusion Matrix Graph ===
    cm = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Real', 'Fake'])
    disp.plot(cmap='Blues')
    plt.title('Confusion Matrix')
    plt.savefig(os.path.join(GRAPH_DIR, 'confusion_matrix.png'))
    plt.close()

    # === Per-Class Bar Graph ===
    report = classification_report(y_test, y_pred, target_names=['Real', 'Fake'], output_dict=True)
    df = pd.DataFrame(report).transpose()
    df_metrics = df.loc[['Real', 'Fake'], ['precision', 'recall', 'f1-score']]
    df_metrics.plot(kind='bar', figsize=(8, 6), colormap='viridis')
    plt.title('Per-Class Metrics (Precision, Recall, F1-score)')
    plt.ylabel('Score')
    plt.ylim(0, 1)
    plt.xticks(rotation=0)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(GRAPH_DIR, 'per_class_metrics.png'))
    plt.close()

    print("Graphs saved in:", GRAPH_DIR)

# === Run ===
if __name__ == '__main__':
    train_and_save_model()
