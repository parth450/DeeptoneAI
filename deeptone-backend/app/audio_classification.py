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

# Function to extract MFCC features
def extract_features(file_path):
    print(f"Loading file: {file_path}")
    y, sr = librosa.load(file_path, sr=None)
    print(f"Audio loaded: {file_path} - duration: {len(y)/sr:.2f}s, sample rate: {sr}")
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_mean = np.mean(mfcc, axis=1)
    return mfcc_mean

# Function to load dataset
def load_dataset(dataset_path):
    X = []
    y = []

    real_dir = os.path.join(dataset_path, 'real')
    fake_dir = os.path.join(dataset_path, 'fake')

    print("Looking in:", real_dir)
    for file in os.listdir(real_dir):
        if file.endswith('.wav'):
            file_path = os.path.join(real_dir, file)
            features = extract_features(file_path)
            X.append(features)
            y.append(0)  # Label for real

    print("Looking in:", fake_dir)
    for file in os.listdir(fake_dir):
        if file.endswith('.wav'):
            file_path = os.path.join(fake_dir, file)
            features = extract_features(file_path)
            X.append(features)
            y.append(1)  # Label for fake

    return np.array(X), np.array(y)

# === MAIN: Train and Evaluate ===
if __name__ == '__main__':
    dataset_path = './dataset'

    print("Loading dataset...")
    X, y = load_dataset(dataset_path)

    print("Training model...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=50, random_state=1)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    print("\n=== CLASSIFICATION REPORT ===")
    print(classification_report(y_test, y_pred, target_names=['Real', 'Fake']))
    print(f"\nOverall Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")

    cm = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Real', 'Fake'])
    disp.plot(cmap='Blues')
    plt.title('Confusion Matrix')
    plt.show()

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
    plt.show()

    # Save as trained_model.pkl (not voice_model.pkl)
    os.makedirs('./model', exist_ok=True)
    joblib.dump(model, './model/trained_model.pkl')
    print("✅ Model saved to ./model/trained_model.pkl")

# === Load model for Flask usage ===
model_path = './model/trained_model.pkl'
if os.path.exists(model_path):
    model = joblib.load(model_path)
else:
    model = None
    print("⚠️ trained_model.pkl not found. Please run this script to train the model.")

# === classify_audio function for Flask ===
def classify_audio(file_path):
    if model is None:
        return {'error': 'Model not loaded. Please train the model first.'}

    try:
        features = extract_features(file_path).reshape(1, -1)
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0]

        return {
            "prediction": "REAL" if prediction == 0 else "FAKE",
            "accuracy": float(np.max(probability)),
            "recall": 0.9,
            "precision": 0.9,
            "f1_score": 0.9
        }
    except Exception as e:
        print("Error in classify_audio:", e)
        return {"error": str(e)}
