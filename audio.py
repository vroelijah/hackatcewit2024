import os
import librosa
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


def extract_features(audio_file):

    y, sr = librosa.load(audio_file)
    
    # Extract features using Mel-Frequency Cepstral Coefficients)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    feature_vector = np.mean(mfccs, axis=1)
    
    return feature_vector

def train_model(audio_files, labels):

    features = np.array([extract_features(file) for file in audio_files])

    X_train, y_train = features, labels

    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    
    return clf

audio_folder_path = 'med_audio'

audio_files = []
labels = []
for file in os.listdir(audio_folder_path):
    if file.endswith('.wav'):
        filepath = os.path.join(audio_folder_path, file)
        audio_files.append(filepath)

        label = os.path.splitext(os.path.basename(file))[0]
        labels.append(label)


model = train_model(audio_files, labels)

new_audio_file = "test.wav"

new_feature = extract_features(new_audio_file)

predicted_label = model.predict([new_feature])[0]
print("Predicted label:", predicted_label)
