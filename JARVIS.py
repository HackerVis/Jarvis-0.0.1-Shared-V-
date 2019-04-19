from gtts import gTTS
import speech_recognition as sr
import os
import pipes
import sys
import subprocess
import re
# import webbrowser
import smtplib
import urllib.request
import pygame
# from geopy.geocoders import Nominatim
from datetime import date, timedelta
from datetime import datetime
# from weather import Weather
from random import randint
import pyttsx3
import vlc
# import forecastio
import json
# from voiceit2 import VoiceIt2
from time import gmtime, strftime
import pyaudio
import wave
import requests
# import hud.py
# import geocoder
# import alarmJ
#from blu import startServer
#from blu import startLoop
import serial
from bluetooth import *
moviePlaying = False
ser = serial.Serial('/dev/ttyACM0', 9600)
ser.write("255,0,0".encode())
ser.write("0,255,0".encode())
ser.write("0,0,255".encode())

serverStarted = False
# Used to mute jarvis
#os.system("amixer set 'PCM' 0%")
usingBluetooth = False
engine = pyttsx3.init()
loopCommand = True
now = datetime.now()
Currenthour=now.strftime('%I')
AmPm=now.strftime('%p')
paused = False
if(AmPm =='PM'):
	engine.say('Good evening sir, How can I help?')
	engine.runAndWait()
else:
	engine.say('Good morning sir, How can I help?')
	engine.runAndWait()

#engine.say('Please authenticate')
#engine.runAndWait()

#User authentication
# def authStart():
#         FORMAT = pyaudio.paInt16
#         CHANNELS = 2
#         RATE = 44100
#         CHUNK = 1024
#         RECORD_SECONDS = 9
#         WAVE_OUTPUT_FILENAME = "auth2.wav"
		 
#         audio = pyaudio.PyAudio()
		 
#         # start Recording
#         stream = audio.open(format=FORMAT, channels=CHANNELS,
#                         rate=RATE, input=True,
#                         frames_per_buffer=CHUNK)
#         print ("recording...")
#         frames = []
		 
#         for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#             data = stream.read(CHUNK)
#             frames.append(data)
#         print ("finished recording")
		 
		 
#         # stop Recording
#         stream.stop_stream()
#         stream.close()
#         audio.terminate()
		 
#         waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
#         waveFile.setnchannels(CHANNELS)
#         waveFile.setsampwidth(audio.get_sample_size(FORMAT))
#         waveFile.setframerate(RATE)
#         waveFile.writeframes(b''.join(frames))
#         waveFile.close()
#         responseAuth=my_voiceit.voice_verification("usr_b9c994a6bc4149968eab59c6c9ca085b", "en-US", "hey jarvis you up initiate boot sequence two user stark", "auth2.wav")
#         print(responseAuth)
#         if("Successfully verified" in responseAuth["message"]):
#             authenticated = True
#         else:
#             engine.say('try again')
#             engine.runAndWait()
#             authStart()

# authStart()
connected = False
bluetoothNotWanted = True
# os.system("sudo python3 /home/pi/Jarvis-0.0.1-Shared-V-/blu.py &")
os.system("mkfifo jarvis")
# geolocator = Nominatim(user_agent="JARVIS2")
def talkToMe(audio):
	"speaks audio passed as argument"
	engine.say(audio)
	engine.runAndWait()
	print(audio)
	#for line in audio.splitlines():
	#	os.system("say " + audio)

	#  use the system's inbuilt say command instead of mpg123
	#  text_to_speech = gTTS(text=audio, lang='en')
	#  text_to_speech.save('audio.mp3')
	#  os.system('mpg123 audio.mp3')


def myCommand():
	global usingBluetooth, bluetoothNotWanted, connected, serverStarted
	"listens for commands"
	#if(not verified):
	#   authStart()
	if(not usingBluetooth):

		r = sr.Recognizer()
		
		with sr.Microphone() as source:
			print('Yes Sir?')
			r.pause_threshold = 0.5
			r.non_speaking_threshold = 0.3
			r.adjust_for_ambient_noise(source, duration=1)
			audio = r.listen(source)
		try:
			command = r.recognize_google(audio).lower()
			print('You said: ' + command + '\n')
		except sr.UnknownValueError:
			print('Your last command couldn\'t be heard')
			command = myCommand();
		# Below is used for keyboard input
		# command = input ("command: ")
		print(command)
		usingBluetooth = False
	else:
		command = ""
		# server_sock=BluetoothSocket( RFCOMM )
		# server_sock.bind(("",PORT_ANY))
		# server_sock.listen(1)

		# port = server_sock.getsockname()[1]

		# uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"


		# advertise_service( server_sock, "SampleServer", service_id = uuid, service_classes = [ uuid, SERIAL_PORT_CLASS ], profiles = [ SERIAL_PORT_PROFILE ])

		# client_sock, client_info = server_sock.accept()
		# print("Accepted connection from ", client_info)
		print("BLUETOOTH")
		# server_sock=BluetoothSocket( RFCOMM )
		# server_sock.bind(("",PORT_ANY))
		# server_sock.listen(1)
		# port = server_sock.getsockname()[1]
		# uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
		# client_sock, client_info = server_sock.accept()
		try:
			data = client_sock.recv(1024)
			command = data.decode('utf-8')
			if("USER:DISCONNECT" in command):
				connected = False
				bluetoothNotWanted = True
				serverStarted = False
				usingBluetooth = False
			print(command)
		except IOError:
			pass

		# print("disconnected")

		# client_sock.close()
		# server_sock.close()
		# print("all done")
		# command = subprocess.check_output(["eval $(cat bluetooth)"])
		# command = os.popen("eval $(cat bluetooth)").read()
		# t = pipes.Template()
		# f = t.open('bluetooth', 'r')
		# print(f.read().strip())
		# command = str(f.read().strip())
		# usingBluetooth = True
	return command


# def alarmjarvis(endTime, ampm):
#     alarmGoing = True
#     print("confirm set alarm for " + endTime)
#     while True:
#         assistant(myCommand())
#         now = datetime.now()
#         if((now.strftime('%I:%M') + ampm) == endTime):
#             if(alarmGoing == True):
#                 if(ampm == "a.m."):
#                     engine.say('Good morning sir, this is you alarm for ' + now.strftime('%I:%M') + ampm)
#                     engine.runAndWait()
#                     alarmGoing = False
#                 else:
#                     engine.say('Good afternoon sir, this is you alarm for ' + now.strftime('%I:%M') + ampm)
#                     engine.runAndWait()
#                     alarmGoing = False


def assistant(command):
	global moviePlaying, player, paused, usingBluetooth, bluetoothNotWanted, serverStarted
	"if statements for executing commands"
	if 'jarvis' in command:
		#if 'open website' in command:
		#	reg_ex = re.search('open website (.+)', command)
		#	if reg_ex:
		#		domain = reg_ex.group(1)
		#		url = 'https://www.' + domain
		#		webbrowser.open(url)
		#		print('Done!')
		#		engine.say('Opening ' + url)
		#		engine.runAndWait()
		#	else:
		#		pass
		#Get time
		if 'time' in command:
			 now = datetime.now()
			 talkToMe("It is " + now.strftime('%I:%M %p'))

		#get date
		elif 'date' in command:
			month = "";
			now=datetime.now()
			if(strftime("%m") == "01"):
				month = "January"
			elif(strftime("%m") == "02"):
				month = "Febuary"
			elif(strftime("%m") == "03"):
				month = "March"
			elif(strftime("%m") == "04"):
				month = "April"
			elif(strftime("%m") == "05"):
				month = "May"
			elif(strftime("%m")== "06"):
				month = "June"
			elif(strftime("%m") == "07"):
				month = "July"
			elif(strftime("%m") == "08"):
				month = "August"
			elif(strftime("%m") == "09"):
				month = "September"
			elif(strftime("%m") == "10"):
				month = "October"
			elif(strftime("%m") == "11"):
				month = "November"
			else:
				month = "December"
			if(strftime("%d")=="1"):
				talkToMe("The date is "+ month + " 1st, " + strftime("%Y"))
			elif(strftime("%d")=="2"):
				talkToMe("The date is "+ month + " 2nd, " + strftime("%Y"))
			elif(strftime("%d")=="3"):
				talkToMe("The date is "+ month + " 3rd, " + strftime("%Y"))
			elif(strftime("%d")=="21"):
				talkToMe("The date is "+ month + " 21st, " + strftime("%Y"))
			elif(strftime("%d")=="22"):
				talkToMe("The date is "+ month + " 22nd, " + strftime("%Y"))
			elif(strftime("%d")=="23"):
				talkToMe("The date is "+ month + " 23rd, " + strftime("%Y"))
			else:
				talkToMe("The date is " + month + strftime("%d") + ", " + strftime("%Y"))
		elif 'what\'s up' in command:
			talkToMe('Just doing my thing')
		elif 'help' in command:
			talkToMe('I can inform you of the time, tell you the date, and play entertainment for you')
		#elif 'joke' in command:
			#res = requests.get(
			#		'https://icanhazdadjoke.com/',
			#		headers={"Accept":"application/json"}
			#		)
			#if res.status_code == requests.codes.ok:
				#talkToMe(str(res.json()['joke']))
				#engine.say(str(res.json()['joke']))
				#engine.runAndWait()
			#else:
				#talkToMe('oops! I ran out of jokes')

		# elif ' in' in command:
		#     reg_ex = re.search('weather in (.*)', command)
		#     if reg_ex:
		#         city = reg_ex.group(1)
		#         weather = Weather()
		#         location = geolocator.geocode(city)
		#         placeweather = location.latitude, location.longitude
		#         #Get weather
		#         observation = owm.weather_at_place(city)
		#         w = observation.get_weather()
		#         currentTemperature = w.get_temperature('celsius')
		#         tempCelsius = int(currentTemperature['temp']) * 1.8
		#         tempFahrenheit = tempCelsius + 32
		#         tempFahrenheit = str(tempFahrenheit)
		#         talkToMe("It is "+tempFahrenheit + " degrees Fahrenheit")
		#         print ("It is "+tempFahrenheit + " degrees Fahrenheit")

		#elif 'lockdown in command:

		elif 'dandy\'s favorite' in command:
			talkToMe('Dandy\'s favorite student is Jason. He also likes Aaron equally as much.')

		elif 'play' in command:
			movieInput = command.split("play")[1].replace(" ", "")
			directory = "/media/pi/8891-D645/"
			movies = {}
			moviesList = []
			filetypes = ["mp4","mp3", "m4v"]
			
			for movie in os.listdir(directory):
				if("." in movie):
					if(movie.split(".")[1] in filetypes):
						pathToMovie = directory+movie
						movies[movie.split(".")[0]] = pathToMovie
						moviesList.append(movie.split(".")[0].replace("_", " ").replace(" ", ""))

						print("Movie: " + movie.split(".")[0] + " Location: " + pathToMovie)

			print(movies)
			# FOR JARVIS: change movieToPlay to command.split("play")[1]
			movieToPlay = movieInput
			if(movieToPlay in moviesList):
				# os.system("vlc " + movies[movieToPlay] + " --fullscreen --play-and-exit")
				player = vlc.MediaPlayer(movies[movieToPlay])

				player.set_fullscreen(True)
				player.video_set_mouse_input(True)
				player.video_set_key_input(True)
				os.system("")
				player.play()
				moviePlaying = True

			else:
				talkToMe("That does not exist")
		elif 'pause' in command:
			if(not paused and moviePlaying):
				player.pause()
				paused = True
			else:
				talkToMe("Nothing is playing")
		elif 'quit' in command:
			if(moviePlaying):
				player.stop()
				moviePlaying = False
			else:
				talkToMe("Nothing is playing")
		elif 'resume' in command:
			if(moviePlaying and paused):
				player.play()
				paused = False
				moviePlaying = True
		elif 'volume to' in command:
			setToPercent = command.split("volume to")[1]
			os.system("amixer set 'PCM' " + setToPercent+"%")
		elif 'go to the middle' in command:
			if(moviePlaying):
				player.set_position(0.5)
			else:
				talkToMe("Nothing is playing")
		elif 'go to the start' in command or 'go the beginning' in command:
			if(moviePlaying):
				player.set_position(0.2)
			else:
				talkToMe("Nothing is playing")
		elif 'go to the end' in command:
			if(moviePlaying):
				player.set_position(0.9)
			else:
				talkToMe("Nothing is playing")
		elif 'go to' in command:
			if(moviePlaying):
				position = command.split("go to ")[1]
				player.set_position((int(position)/100))
			else:
				talkToMe("Nothing is playing")
		elif 'color to' in command:
			color = command.split("color to")[1]
			ser.write(color.encode())
		elif 'enable app' in command or 'start app' in command or 'initialize app' in command:
			# os.system("sudo python3 ~/Jarvis-0.0.1-Shared-V-/blu.py")
			talkToMe('Starting app compatability')
			serverStarted = True
			bluetoothNotWanted = False
			# assistant(myCommand())
		# elif 'start hud' in command:
		# 	starthud()
		# elif 'stop hud' in command:
		# 	stophud()

		
		# elif 'stop hud' in command:
		# 	stophud()
		# elif 'start hud' in command:
		# 	os.system("python3 hud.py")
		else:
			talkToMe('I don\'t know what you mean!')
		# elif 'alarm' in command:
		#     reg_ex = re.search('an alarm for (.*)', command)
		#     if reg_ex:
		#         time = reg_ex.group(1)
		#         now = datetime.now()
		#         completeAmPm = ""
		#         AmPmCommand=now.strftime('%p')
		#         talkToMe("Alarm set for " + time)
		#         alarmjarvis(time, completeAmPm)



#loop to continue executing multiple commands
while True:
	ser = serial.Serial('/dev/ttyACM0', 9600)
	server_sock=BluetoothSocket( RFCOMM )
	server_sock.bind(("",PORT_ANY))
	server_sock.listen(1)
	port = server_sock.getsockname()[1]
	uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
	#advertise_service( server_sock, "SampleServer", service_id = uuid, service_classes = [ uuid, SERIAL_PORT_CLASS ], profiles = [ SERIAL_PORT_PROFILE ])
	#client_sock, client_info = server_sock.accept()

#     if(authenticated):
	if(loopCommand):
		if(serverStarted and not bluetoothNotWanted):
			print("Server Ready!")
			ser = serial.Serial('/dev/ttyACM0', 9600)
			server_sock=BluetoothSocket( RFCOMM )
			server_sock.bind(("",PORT_ANY))
			server_sock.listen(1)
			port = server_sock.getsockname()[1]
			uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
			advertise_service( server_sock, "SampleServer", service_id = uuid, service_classes = [ uuid, SERIAL_PORT_CLASS ], profiles = [ SERIAL_PORT_PROFILE ])
			client_sock, client_info = server_sock.accept()
			print("Accepted connection from ", client_info)
			startedServer = True
			connected = True
			bluetoothNotWanted = False
			usingBluetooth = True
			while connected:
				assistant(myCommand())
		else:
			assistant(myCommand())

