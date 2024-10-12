from base64 import b64decode
import speech_recognition as sr
from os import path
from gtts import gTTS
#import streamlit as st
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import time
from pydub import AudioSegment
from pydub.playback import play
from IPython.display import Audio, display
import pyttsx3
import ollama
import warnings

engine = pyttsx3.init()
# engine.stop()

# """ RATE"""
# rate = engine.getProperty('rate')   # getting details of current speaking rate
# print ("rate: ",rate)                        #printing old voice rate
# engine.setProperty('rate', 130)     # setting up new voice rate
# print ("rate: ",rate)                        #printing current voice rate

# engine.say("Hello World!")
# engine.say('My current speaking rate is ' + str(rate))

# """VOLUME"""
# volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
# print ("volume "+volume)                          #printing old volume level
# engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1
# print ("volume "+volume)                          #printing new volume level

# """VOICE"""
voices = engine.getProperty('voices')       #getting details of current voice
# #engine.setProperty('voice', voices[0].id)  #changing index, changes voices. 0 for male
engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female


template = """
You are a helpful AI assistant that provides the answer for the question asked in a short and concise way.

Here is the conversation history: {context}

Question: {question}

Answer:
"""
model = OllamaLLM(model="llama3.2:1b")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

def recordUser():

  print("Listening..")
  recognizer = sr.Recognizer()
  with sr.Microphone() as source:
    recognizer.adjust_for_ambient_noise(source, duration=0.15)
    recognizer.pause_threshold=1
    heardAudio = recognizer.listen(source)
    print("Done")
  return heardAudio

# jsRecordCode = """
# const sleep  = time => new Promise(resolve => setTimeout(resolve, time))
# const b2text = blob => new Promise(resolve => {
#   const reader = new FileReader()
#   reader.onloadend = e => resolve(e.srcElement.result)
#   reader.readAsDataURL(blob)
# })
# var record = time => new Promise(async resolve => {
#   stream = await navigator.mediaDevices.getUserMedia({ audio: true })
#   recorder = new MediaRecorder(stream)
#   chunks = []
#   recorder.ondataavailable = e => chunks.push(e.data)
#   recorder.start()
#   await sleep(time)
#   recorder.onstop = async ()=>{
#     blob = new Blob(chunks)
#     text = await b2text(blob)
#     resolve(text)
#   }
#   recorder.stop()
# })
# """

# def recordUser(seconds=3):
#   while True:
#     display(Javascript(jsRecordCode))
#     print("Started Recording")
#     s = output.eval_js('record(%d)' % (seconds*1000))
#     # print(s)
#     b = b64decode(s.split(',')[1])
#     # print(b)
#     with open('oldAudio.wav', 'wb') as f:
#       f.write(b)
#     x, _ = librosa.load('oldAudio.wav', sr=16000)
#     sf.write('audio.wav', x, 16000)
#     print("Stopped Recording")
#     return 'audio.wav created successfully'
#     # return 0
def convertSpeechToText(audioResponse):
  recognizer = sr.Recognizer()
  try:    
    print("You: " +recognizer.recognize_google(audioResponse))
  except sr.UnknownValueError:
    return "Google could not understand audio" 
  except sr.RequestError as e:
    print("Google error; {0}".format(e))
    return "Google made an oopsie"
  return recognizer.recognize_google(audioResponse)
  

# def estimateDuration(text):
#     words_per_minute = 130  # Typical speaking speed
#     word_count = len(text.split())  # Count the number of words
#     duration = word_count / words_per_minute * 60  # Convert minutes to seconds
#     return int(duration)

    
def convertTextToSpeech(text):
  engine.say(text)
  engine.runAndWait()
    
def llmResponse():
  context = ""
  
  audioResponse = recordUser()
  text = convertSpeechToText(audioResponse)
  result = text
  if text.lower() in ["stop", "exit", "quit"]:
    return text
  if text not in ["Google could not understand audio" ,"Google made an oopsie"]:
    result = chain.invoke({"context": context, "question": text})
    print("AI: "+result)
    context += f"\nUser: {text}\nAI: {result}"
  convertTextToSpeech(result)

  return result
  
def main():
  warnings.filterwarnings("ignore")
  while True:
    userInput = llmResponse()
    if userInput.lower() in ["stop", "exit", "quit"]:
      break

if __name__ == "__main__":
  main()