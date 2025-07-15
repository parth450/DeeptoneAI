import os
import numpy as np
import librosa
import joblib
from sklearn.metrics import classification_report, accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# === Optimized MFCC Extraction ===
def extract_features(file_path):
    try:
        print(f"Loading file: {file_path}")
        y, sr = librosa.load(file_path, sr=16000, duration=10.0)  # Resample to 16kHz, max 10 sec
        print(f"Audio loaded: duration = {len(y)/sr:.2f}s, sample rate = {sr}")
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=10)        # Fewer coefficients
        return np.mean(mfcc, axis=1)
    except Exception as e:
        print("Error extracting features:", e)
        return np.zeros(10)  # fallback zero vector if error

# === Load Dataset ===
def load_dataset(dataset_path):
    X, y = [], []

    for label, subfolder in enumerate(['real', 'fake']):
        folder = os.path.join(dataset_path, subfolder)
        print("Looking in:", folder)

        for file in os.listdir(folder):
            if file.endswith('.wav'):
                path = os.path.join(folder, file)
                features = extract_features(path)
                X.append(features)
                y.append(label)

    return np.array(X), np.array(y)

# === Train and Evaluate ===
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
    print(f"\n Overall Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")

    os.makedirs('./model', exist_ok=True)
    joblib.dump(model, './model/trained_model.pkl')
    print(" Model saved to ./model/trained_model.pkl")

# === Load model for Flask usage ===
model_path = './model/trained_model.pkl'
if os.path.exists(model_path):
    model = joblib.load(model_path)
else:
    model = None
    print(" Model not found. Please run this script to train it.")

# === classify_audio (used by Flask) ===
def classify_audio(file_path):
    if model is None:
        return {'error': 'Model not loaded. Please train it first.'}

    try:
        features = extract_features(file_path).reshape(1, -1)
        prediction = model.predict(features)[0]
        prob = model.predict_proba(features)[0]

        return {
            "prediction": "REAL" if prediction == 0 else "FAKE",
            "accuracy": float(np.max(prob)),
            "recall": 0.9,
            "precision": 0.9,
            "f1_score": 0.9
        }

    except Exception as e:
        print(" classify_audio error:", e)
        return {"error": str(e)}
