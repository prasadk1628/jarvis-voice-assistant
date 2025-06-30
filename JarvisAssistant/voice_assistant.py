import speech_recognition as sr
import pyttsx3
import datetime
import os
import webbrowser
import requests

# === SETUP ===
engine = pyttsx3.init()
recognizer = sr.Recognizer()

# === SPEAK ===
def speak(text):
    engine.say(text)
    engine.runAndWait()

# === LISTEN ===
def listen_command():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio)
            print("You said:", command)
            return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
    except sr.RequestError:
        speak("Network error.")
    return ""

# === TIME FUNCTION ===
def tell_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%I:%M %p")
    speak("The time is " + current_time)

# === OPEN APPLICATIONS ===
def open_app(command):
    if "notepad" in command:
        os.system("notepad")
    elif "chrome" in command:
        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        os.startfile(chrome_path)
    elif "calculator" in command:
        os.system("calc")
    else:
        speak("Application not found")

# === WEATHER ===
def get_weather(city):
    API_KEY = "your_openweather_api_key_here"  # Replace with your API key
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if data["cod"] != "404":
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            speak(f"The temperature in {city} is {temp} degrees Celsius with {desc}.")
        else:
            speak("City not found.")
    except:
        speak("Unable to fetch weather right now.")

# === MAIN LOOP ===
speak("Hello! I am your assistant. How can I help you?")

while True:
    command = listen_command()

    if "time" in command:
        tell_time()
    elif "open" in command:
        open_app(command)
    elif "weather" in command:
        speak("Which city?")
        city = listen_command()
        if city:
            get_weather(city)
    elif "exit" in command or "stop" in command or "quit" in command:
        speak("Goodbye!")
        break
    elif command != "":
        speak("Sorry, I didn't understand that.")
