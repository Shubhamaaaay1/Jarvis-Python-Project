import os
import speech\_recognition as sr
import webbrowser
import pygame
import requests
from gtts import gTTS
from openai import OpenAI

pygame.mixer.init()

musicLibrary = {
"wol": "[https://www.youtube.com/watch?v=dQw4w9WgXcQ](https://www.youtube.com/watch?v=dQw4w9WgXcQ)",
"amplify": "[https://www.youtube.com/watch?v=7wtfhZwyrcc](https://www.youtube.com/watch?v=7wtfhZwyrcc)",
"faded": "[https://www.youtube.com/watch?v=60ItHLz5WEA](https://www.youtube.com/watch?v=60ItHLz5WEA)",
}

OPENAI\_API\_KEY = os.getenv("OPENAI\_API\_KEY")
NEWS\_API\_KEY = os.getenv("NEWS\_API\_KEY")

if not OPENAI\_API\_KEY or not NEWS\_API\_KEY:
print("API keys not found. Please set OPENAI\_API\_KEY and NEWS\_API\_KEY in your environment.")
exit(1)

client = OpenAI(api\_key=OPENAI\_API\_KEY)

def speak(text):
print(f"Jarvis says: {text}")
tts = gTTS(text=text, lang='en')
filename = "temp.mp3"
tts.save(filename)
pygame.mixer.music.load(filename)
pygame.mixer.music.play()
while pygame.mixer.music.get\_busy():
pygame.time.Clock().tick(10)
pygame.mixer.music.stop()
os.remove(filename)

def aiProcess(command):
try:
completion = client.chat.completions.create(
model="gpt-3.5-turbo",
messages=\[
{"role": "system", "content": "You are a helpful virtual assistant named Jarvis."},
{"role": "user", "content": command}
]
)
return completion.choices\[0].message.content
except Exception as e:
print("Error talking to OpenAI:", e)
return "Sorry, I couldn't reach OpenAI."

def get\_news():
try:
url = f"[https://newsapi.org/v2/top-headlines?country=in\&apiKey={NEWS\_API\_KEY}](https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY})"
response = requests.get(url)
if response.status\_code == 200:
data = response.json()
articles = data.get('articles', \[])
headlines = \[article\['title'] for article in articles\[:5]]
return headlines
except Exception as e:
print("Error fetching news:", e)
return \[]

def processCommand(command):
c = command.lower()
if "open google" in c:
webbrowser.open("[https://google.com](https://google.com)")
elif "open facebook" in c:
webbrowser.open("[https://facebook.com](https://facebook.com)")
elif "open youtube" in c:
webbrowser.open("[https://youtube.com](https://youtube.com)")
elif "open linkedin" in c:
webbrowser.open("[https://linkedin.com](https://linkedin.com)")
elif c.startswith("play "):
song = c.split("play ")\[1].strip()
if song in musicLibrary:
webbrowser.open(musicLibrary\[song])
speak(f"Playing {song}")
else:
speak("Song not found in your library.")
elif "news" in c:
headlines = get\_news()
if headlines:
speak("Here are the top news headlines:")
for headline in headlines:
speak(headline)
else:
speak("Sorry, I couldn't fetch news right now.")
else:
response = aiProcess(command)
speak(response)

if **name** == "**main**":
recognizer = sr.Recognizer()
speak("Initializing Jarvis. Say 'Jarvis' to wake me up.")
while True:
try:
with sr.Microphone() as source:
print("Waiting for wake word...")
audio = recognizer.listen(source, timeout=5, phrase\_time\_limit=5)
wake\_word = recognizer.recognize\_google(audio)
print(f"Heard wake word attempt: {wake\_word}")
if wake\_word.lower() == "jarvis":
speak("Yes?")
print("Listening for command...")
audio = recognizer.listen(source, timeout=5, phrase\_time\_limit=7)
command = recognizer.recognize\_google(audio)
print(f"Heard command: {command}")
processCommand(command)
except sr.WaitTimeoutError:
pass
except sr.UnknownValueError:
print("Sorry, I did not understand that.")
except Exception as e:
print(f"Error: {e}")
