import keras
import librosa
import numpy as np
#import os

def prediction(file):
    path = 'E:/priya_backup/Priya/PythonProjects/Speech_Emotion_Recognition/Emotion_Voice_Detection_Model.h5'
    loaded_model = keras.models.load_model(path)
    data, sampling_rate = librosa.load(file)
    mfccs = np.mean(librosa.feature.mfcc(y=data, sr=sampling_rate, n_mfcc=40).T, axis=0)
    x = np.expand_dims(mfccs, axis=1)
    x = np.expand_dims(x, axis=0)
    predictions = loaded_model.predict_classes(x)
    print(predictions)
    pred = predictions[0]
    print(pred)
    label_conversion = {'0': 'neutral','1': 'calm','2': 'happy','3': 'sad','4': 'angry','5': 'fearful','6': 'disgust','7': 'surprised'}
    for key, value in label_conversion.items():
        if int(key) == pred:
            label = value
            print(label)
    return label

if __name__ == "__main__":
    file = "E:/priya_backup/Priya/PythonProjects/Speech_Emotion_Recognition/Audio1.wav"
    prediction(file)