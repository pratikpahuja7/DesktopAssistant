import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import random
import requests

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)


def speak(audio):
    """Speaks out provided parameter"""
    engine.say(audio)
    engine.runAndWait()


def greet():
    """Greets user according to time"""
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good morning sir")
    elif 12 < hour < 18:
        speak("Good afternoon sir")
    else:
        speak("Good evening sir")
    speak("How can I assist you?")


def takeCommand():
    """Takes microphone input and provides string output"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening..")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing..")
        query = r.recognize_google(audio, language="en-in")
        print("Command : {}".format(query))
    except Exception:
        print("I am not yet programmed for that function")
        return "none"
    return query


def weather():
    """Provides weather of specified city using API"""
    API_KEY = "27c3ead25b65bb2befc32ac977ebdc4x"  # enter your API key
    BASEURL = "https://api.openweathermap.org/data/2.5/weather"
    city = "Ambarnath"  # enter your city name
    requestURL = f"{BASEURL}?appid={API_KEY}&q={city}"
    response = requests.get(requestURL)
    if response.status_code == 200:
        data = response.json()
        weather = data["weather"][0]["main"] + " , " + data["weather"][0]["description"]
        temperature = round(data["main"]["temp"] - 273.15, 2)
        print(f"Weather : {weather}")
        print(f"Temperature : {temperature}°C")
        speak(f"Weather : {weather}")
        speak(f"Temperature : {temperature}°C")
    else:
        speak("An error occurred")


if __name__ == '__main__':
    greet()
    while True:
        query = takeCommand().lower()

        # Wikipedia search
        if "wikipedia" in query:
            speak("Searching wikipedia")
            query = query.replace("wikipedia", "")
            result = wikipedia.summary(query, sentences=1)
            print(result)
            speak("According to wikipedia")
            speak(result)
            break
        # Opens YouTube in browser
        elif "open youtube" in query:
            webbrowser.open("youtube.com")
            break
        # Opens Google in browser
        elif "open google" in query:
            webbrowser.open("google.com")
            break
        # Plays random music from specified folder
        elif "play music" in query:
            music_dir = "D:\\Songs\\English"
            songs = os.listdir(music_dir)
            total_number = len(songs)
            speak("")
            os.startfile(os.path.join(music_dir, songs[random.randint(0, total_number)]))
            break
        # Speaks out time right now
        elif "time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Time now is {strTime}")
            break
        elif "weather" in query:
            weather()
            break
        elif "who are you" in query:
            speak("My name is Jarvis, your desktop assistant")
        # Quits
        elif "quit" in query:
            speak("Thank you sir")
            break
        else:
            speak("I am not yet programmed for that function")
