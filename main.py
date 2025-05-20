import os
import speech_recognition as sr
import webbrowser
import pygame
import requests
from gtts import gTTS
from openai import OpenAI

pygame.mixer.init()

musicLibrary = {
    "wol": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "amplify": "https://www.youtube.com/watch?v=7wtfhZwyrcc",
    "faded": "https://www.youtube.com/watch?v=60ItHLz5WEA"
}

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

if not OPENAI_API_KEY or not NEWS_API_KEY:
    print("API keys not found. Please set OPENAI_API_KEY and NEWS_API_KEY in your environment.")
    exit(1)

client = OpenAI(api_key=OPENAI_API_KEY)

def speak(text):
    print(f"Jarvis says: {text}")
    tts = gTTS(text=text, lang='en')
    filename = "temp.mp3"
    tts.save(filename)
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.stop()
    os.remove(filename)

def aiProcess(command):
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful virtual assistant named Jarvis."},
                {"role": "user", "content": command}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print("Error talking to OpenAI:", e)
        return "Sorry, I couldn't reach OpenAI."

def get_news():
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            headlines = [article['title'] for article in articles[:5]]
            return headlines
    except Exception as e:
        print("Error fetching news:", e)
    return []

def processCommand(command):
    c = command.lower()
    if "open google" in c:
        webbrowser.open("https://google.com")
    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c:
        webbrowser.open("https://linkedin.com")
    elif c.startswith("play "):
        song = c.split("play ")[1].strip()
        if song in musicLibrary:
            webbrowser.open(musicLibrary[song])
            speak(f"Playing {song}")
        else:
            speak("Song not found in your library.")
    elif "news" in c:
        headlines = get_news()
        if headlines:
            speak("Here are the top news headlines:")
            for headline in headlines:
                speak(headline)
        else:
            speak("Sorry, I couldn't fetch news right now.")
    else:
        response = aiProcess(command)
        speak(response)

if __name__ == "__main__":
    recognizer = sr.Recognizer()
    speak("Initializing Jarvis. Say 'Jarvis' to wake me up.")
    while True:
        try:
            with sr.Microphone() as source:
                print("Waiting for wake word...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                wake_word = recognizer.recognize_google(audio)
                print(f"Heard wake word attempt: {wake_word}")
                if wake_word.lower() == "jarvis":
                    speak("Yes?")
                    print("Listening for command...")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=7)
                    command = recognizer.recognize_google(audio)
                    print(f"Heard command: {command}")
                    processCommand(command)
        except sr.WaitTimeoutError:
            pass
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
        except Exception as e:
            print(f"Error: {e}")

