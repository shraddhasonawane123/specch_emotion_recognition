
"""
This file can be used to try a live prediction. 
"""

import keras
import librosa
import numpy as np
import os
#from config import EXAMPLES_PATH
#from config import MODEL_DIR_PATH


class LivePredictions:
    """
    Main class of the application.
    """
    #Files = 'E:/priya_backup/Priya/PythonProjects/Speech_Emotion_Recognition/Audio1.wav'
    def __init__(self, file):
        """
        Init method is used to initialize the main parameters.
        """
        #print(Files)
        self.file = file
        self.path = 'E:/priya_backup/Priya/PythonProjects/Speech_Emotion_Recognition/Emotion_Voice_Detection_Model.h5'
        self.loaded_model = keras.models.load_model(self.path)

    def make_predictions(self):
        """
        Method to process the files and create your features.
        """
        data, sampling_rate = librosa.load(self.file)
        mfccs = np.mean(librosa.feature.mfcc(y=data, sr=sampling_rate, n_mfcc=40).T, axis=0)
        x = np.expand_dims(mfccs, axis=1)
        x = np.expand_dims(x, axis=0)
        predictions = self.loaded_model.predict_classes(x)
        predicted_emotion = self.convert_class_to_emotion(predictions)
        print(predicted_emotion)
        filename = 'EmotionRecognized' + '.txt'
        filepath = 'E:/priya_backup/Priya/PythonProjects/Speech_Emotion_Recognition/media/'
        complete_name = os.path.join(filepath, filename)
        f= open(complete_name,"w+")
        f.write("\n Prediction Recognized " + predicted_emotion)
        #f.write("\n [+] Detected " " " + str(len_form) +" " "forms on " +url)
        #f.write("\n [*] Form details:" + str(form_details))
        f.close()
        print( "Prediction is", " ", self.convert_class_to_emotion(predictions))

    @staticmethod
    def convert_class_to_emotion(pred):
        """
        Method to convert the predictions (int) into human readable strings.
        """
        
        label_conversion = {'0': 'neutral',
                            '1': 'calm',
                            '2': 'happy',
                            '3': 'sad',
                            '4': 'angry',
                            '5': 'fearful',
                            '6': 'disgust',
                            '7': 'surprised'}

        for key, value in label_conversion.items():
            if int(key) == pred:
                label = value
        return label


if __name__ == '__main__':
    files = 'E:/priya_backup/Priya/PythonProjects/Speech_Emotion_Recognition/Audio1.wav'
    live_prediction = LivePredictions(files)
    #live_prediction = LivePredictions(file)
    live_prediction.loaded_model.summary()
    live_prediction.make_predictions()
    