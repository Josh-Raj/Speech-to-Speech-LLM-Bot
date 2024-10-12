# from base64 import b64decode
import speech_recognition as sr
# from os import path
# from gtts import gTTS
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
# import time
# from pydub import AudioSegment
# from pydub.playback import play
# from IPython.display import Audio, display
import pyttsx3
import ollama
# import warnings
import tkinter as tk
import threading

engine = pyttsx3.init()
voices = engine.getProperty('voices')       #getting details of current voice
engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female

template = """
You are Alex, a helpful AI assistant that provides the answer for the question asked in a short and concise way. Ignore * when talking

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

def convertSpeechToText(audioResponse):
  recognizer = sr.Recognizer()
  try:    
    print("You: " +recognizer.recognize_google(audioResponse))
  except sr.UnknownValueError:
    return "Google could not understand audio" 
  except sr.RequestError as e:
    print("Google error; {0}".format(e))
    return f"Google error: {e}"
  return recognizer.recognize_google(audioResponse)
  

def convertTextToSpeech(text):
  engine.say(text)
  engine.runAndWait()

def llmResponse(context = ""):
  audioResponse = recordUser()
  text = convertSpeechToText(audioResponse)
  result = text
  if text.lower() in ["stop", "exit", "quit"]:
    return text, 

  if text not in ["Google could not understand audio" ,"Google error"]:
    result = chain.invoke({"context": context, "question": text})
    print("AI: "+result)
    context += f"User: {text}\nAI: {result}"
    convertTextToSpeech(result)

  return result
  

def main():
  context = ""
  threading.Thread(target=llmResponse).start()

window = tk.Tk()
window.title("Speech to Speech LLM Bot")

label = tk.Label(window, text="Press the button to start speaking:")
label.pack(pady=10)

start_button = tk.Button(window, text="Start LLM", command=main)
start_button.pack(pady=10)

window.mainloop()

if __name__ == "__main__":
  main()