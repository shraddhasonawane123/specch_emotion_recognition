from django.shortcuts import render,redirect
from .models import *
from tensorflow import keras
from django.contrib import messages
from django.contrib.sessions.models import Session
from tensorflow.keras.models import model_from_json
from os import path
import os
import keras
import librosa
from django.views import View
import numpy as np
from .live_predictions  import *
from django.http import JsonResponse
from pydub import AudioSegment
import wave
import keras
import pyaudio
import pandas as pd
import numpy as np
from os import path
from pydub import AudioSegment
import IPython.display as ipd

def home(request):
	return render(request,'home.html',{})

def base(request):
	return render(request,'base.html',{})

def SignIn(request):
	if request.method == "POST":
		C_name = request.POST['uname']
		C_password = request.POST['pwds']
		if UserDetails.objects.filter(Username=C_name, Password=C_password).exists():
			user = UserDetails.objects.all().filter(Username=C_name, Password=C_password)
			messages.info(request, 'logged in')
			request.session['UserId'] = user[0].id
			request.session['type_id'] = 'User'
			request.session['UserType'] = C_name
			request.session['login'] = "Yes"
			return redirect("/")
		else:
			messages.info(request, 'Please Register')
			return redirect("/SignUp")
	else:
		return render(request,'SignIn.html',{})
	return render(request,'SignIn.html',{})

def SignUp(request):
	if request.method == "POST":
		username = request.POST['uname']
		password = request.POST['pwds']
		email = request.POST['eid']
		if  UserDetails.objects.filter(Username=username,EmailID=email).exists():
			myObjects = UserDetails.objects.all().filter(Username=username,EmailID=email)
			name = myObjects[0].Username
			messages.error(request,'Already Registered Please Login')
			return render(request,'SignIn.html',{})
		else:
			user = UserDetails(Username=username,Password=password,EmailID=email)
			user.save()
			messages.error(request,'Registered Sucessfully')
			return redirect('/SignIn')
	else:
		return render(request,'SignUp.html',{})

def ChangePassword(request):
	if request.method == 'POST':
		CurrentPassword = request.POST['CurrentPassword']
		NewPassword = request.POST['NewPassword']
		ConfirmPassword = request.POST['ConfirmPassword']
		userId = request.session['UserId']
		CurrUser =UserDetails .objects.all().filter(id=userId)
		if CurrUser[0].Password == CurrentPassword:
			if NewPassword == ConfirmPassword:
				UserDetails.objects.filter(id=userId).update(Password=NewPassword)
				messages.info(request,'Passwords Changed Successfully')
				return render(request, 'ChangePassword.html', {})
			else:
				messages.info(request,'New Passwords doesnt match')
				return render(request, 'ChangePassword.html', {})
		else:
			messages.info(request,'Current Password doesnt match')
			return render(request, 'ChangePassword.html', {})
	else:
		userId = request.session['UserId']
		return render(request,'ChangePassword.html',{'userId':userId})
	return render(request,'ChangePassword.html',{})

def Logout(request):
	Session.objects.all().delete()
	return redirect('/')
	
def Services(request):
	return render(request,'Services.html',{})

def RecordVoice(request):
	CHUNK = 1024 
	FORMAT = pyaudio.paInt16 #paInt8
	CHANNELS = 2 
	RATE = 44100 #sample rate
	RECORD_SECONDS = 20
	WAVE_OUTPUT_FILENAME = "audio1.wav"
	#emotions=["Anger","disgust","fear","happy","Neutral", "sad", "surprise"]
	p = pyaudio.PyAudio()
	stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK) #buffer
	print("* recording")
	frames = []
	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
		data = stream.read(CHUNK)
		frames.append(data) # 2 bytes(16 bits) per channel
	print("* done recording")
	stream.stop_stream()
	stream.close()
	p.terminate()
	wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(p.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	wf.close()
	file = 'C:/PythonProjects/Speech_Emotion_Recognition/' + WAVE_OUTPUT_FILENAME
	print(file)
	path = 'C:/PythonProjects/Speech_Emotion_Recognition/Emotion_Voice_Detection_Model.h5'
	loaded_model = keras.models.load_model(path)
	data, sampling_rate = librosa.load(file)
	mfccs = np.mean(librosa.feature.mfcc(y=data, sr=sampling_rate, n_mfcc=40).T, axis=0)
	x = np.expand_dims(mfccs, axis=1)
	x = np.expand_dims(x, axis=0)
	predictions = loaded_model.predict(x)
	classes=np.argmax(predictions,axis=1)
	print(classes)
	pred = classes[0]
	print(pred)
	label_conversion = {'0': 'Neutral','1': 'Calm','2': 'Happy','3': 'Sad','4': 'Angry','5': 'Fearful','6': 'Disgust','7': 'Surprised'}
	for key, value in label_conversion.items():
		if int(key) == pred:
			label = value
			print(label)
	if label == "Neutral":
		emoji =" &#128528;"
	if label == "Calm":
		emoji =" &#128524;"
	if label == "Happy":
		emoji =" &#128512;"
	if label == "Sad":
		emoji =" &#128546;"
	if label == "Angry":
		emoji =" &#128544;"
	if label == "Fearful":
		emoji =" &#128552;"
	if label == "Disgust":
		emoji =" &#129314;"
	if label == "Surprised":
		emoji =" &#128562;"
	label = label + ' ' + 'mood'
	data = {
			'respond': label,
			}
	return JsonResponse(data)


def pred1(request):
	file = request.POST.get('text')
	print(file)
	filename = file.split('.')
	print(filename)
	file_name = filename[0]
	print(file_name)
	mp3File = file_name + '.wav'
	print(mp3File)
	sound = AudioSegment.from_mp3(file)
	sound.export(mp3File, format="wav")
	file = 'C:/Python Projects/Speech_Emotion_Recognition/'+ mp3File
	print(file)
	path = 'C:/Python Projects/Speech_Emotion_Recognition/Emotion_Voice_Detection_Model.h5'
	loaded_model = keras.models.load_model(path)
	data, sampling_rate = librosa.load(file)
	mfccs = np.mean(librosa.feature.mfcc(y=data, sr=sampling_rate, n_mfcc=40).T, axis=0)
	x = np.expand_dims(mfccs, axis=1)
	x = np.expand_dims(x, axis=0)
	predictions = loaded_model.predict(x)
	classes=np.argmax(predictions,axis=1)
	print(classes)
	pred = classes[0]
	print(pred)
	label_conversion = {'0': 'Neutral','1': 'Calm','2': 'Happy','3': 'Sad','4': 'Angry','5': 'Fearful','6': 'Disgust','7': 'Surprised'}
	for key, value in label_conversion.items():
		if int(key) == pred:
			label = value
			print(label)
	if label == "Neutral":
		emoji =" &#128528;"
	if label == "Calm":
		emoji =" &#128524;"
	if label == "Happy":
		emoji =" &#128512;"
	if label == "Sad":
		emoji =" &#128546;"
	if label == "Angry":
		emoji =" &#128544;"
	if label == "Fearful":
		emoji =" &#128552;"
	if label == "Disgust":
		emoji =" &#129314;"
	if label == "Surprised":
		emoji =" &#128562;"
	label = label + ' ' + 'mood'
	data = {
	'respond': label,
	'emo':emoji,
	}
	return JsonResponse(data)

class LivePredictions(View):


	def __init__(self, file):
		self.file = file
		self.path = 'C:/PythonProjects/Speech_Emotion_Recognition/Emotion_Voice_Detection_Model.h5'
		self.loaded_model = keras.models.load_model(self.path)

	def make_predictions(self):
		data, sampling_rate = librosa.load(self.file)
		mfccs = np.mean(librosa.feature.mfcc(y=data, sr=sampling_rate, n_mfcc=40).T, axis=0)
		x = np.expand_dims(mfccs, axis=1)
		x = np.expand_dims(x, axis=0)
		predictions = self.loaded_model.predict_classes(x)
		print( "Prediction is", " ", self.convert_class_to_emotion(predictions))

	@staticmethod
	def convert_class_to_emotion(pred):
		label_conversion = {'0': 'neutral','1': 'calm','2': 'happy','3': 'sad','4': 'angry','5': 'fearful','6': 'disgust','7': 'surprised'}
		for key, value in label_conversion.items():
			if int(key) == pred:
				label = value
				return label


if __name__ == '__main__':
	live_prediction = LivePredictions(file='C:/PythonProjects/Speech_Emotion_Recognition/Audio1.wav')
	live_prediction.loaded_model.summary()
	live_prediction.make_predictions()
    