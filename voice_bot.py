import time
import requests
import speech_recognition as sr
from time import ctime
import playsound
import os
import random
from gtts import gTTS
import subprocess
from os import path
from pydub import AudioSegment

r = sr.Recognizer()

def record_audio():

    with sr.Microphone() as source:
        audio = r.listen(source)
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)
            print(voice_data)
        except sr.UnknownValueError:
            print('Sorry I didnt get that')
        
        return voice_data


def speak(audio_string):

    tts = gTTS(text=audio_string, lang='en')
    r = random.randint(1,20000000)
    s = str(r)
    audio_file = 'Audio' '.mp3'
    tts.save(audio_file)
    print(audio_file)
    

    #subprocess.call(['mpg321', 'Audio.mp3', '--play-and-exit'])
    #audio19091855s   Audio8664496.mp3
    
    playsound.playsound('Audio.mp3')   

    time.sleep(1)

    #os.remove(audio_file)


print('how can I help you ?')



bot_message = " "

while bot_message != "Bye":

    message = input(' ')
    #message = record_audio()

    r = requests.post('http://localhost:5002/webhooks/rest/webhook', json={"message": message})

    for i in r.json():
        bot_message = i['text']
    print(f"{bot_message}")
    speak(bot_message)