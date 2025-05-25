import speech_recognition as sr
import pyttsx3
import datetime
import os
import requests

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen_command():
    """
    Listen to user voice input and convert it to text.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return ""
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service.")
            return ""

def get_current_time():
    """
    Get the current time.
    """
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    return current_time

def get_weather(city):
    """
    Fetch weather information for a specified city.
    """
    api_key = "783909bc65d6cb3117bc5e8eff889071"  # Replace with your actual OpenWeatherMap API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    weather_data = response.json()
    if weather_data["cod"] == 200:
        main = weather_data["main"]
        temperature = main["temp"]
        weather_desc = weather_data["weather"][0]["description"]
        return f"The current temperature in {city} is {temperature} degrees Celsius with {weather_desc}."
    else:
        return "Sorry, I couldn't fetch the weather data."

def process_command(command):
    if "time" in command:
        current_time = get_current_time()
        speak(f"The current time is {current_time}")
    elif "open browser" in command:
        speak("Opening the browser.")
        os.system("start chrome")  # For Windows

    elif "shutdown" in command:
        speak("Shutting down the system.")
        os.system("shutdown /s /t 1")  # For Windows

    elif "weather" in command:
        city = command.split("in")[-1].strip()
        weather_info = get_weather(city)
        speak(weather_info)
    elif "exit" in command or "stop" in command:
        speak("Goodbye!")
        return True
    else:
        speak("Sorry, I don't understand that command.")
    return False

if __name__ == "__main__":
    speak("Hello, how can I assist you today?")
    while True:
        command = listen_command()
        if command:
            should_exit = process_command(command)
            if should_exit:
                break
