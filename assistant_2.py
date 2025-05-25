import speech_recognition as sr
import pyttsx3
import datetime
import os
import requests
import pyautogui
import time
import webbrowser

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """
    Convert text to speech and print it to the terminal.
    """
    print(f"Assistant: {text}") 
    engine.say(text)
    engine.runAndWait()

def listen_command():
    """
    Listen to user voice input and convert it to text.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
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
    speak(f"The current time is {current_time}")

def open_browser():
    """
    Open the default web browser.
    """
    speak("Opening the browser.")
    os.system("start chrome") 

def shutdown_system():
    """
    Shut down the system.
    """
    speak("Shutting down the system.")
    os.system("shutdown /s /t 1") 

def get_weather(command):
    """
    Fetch weather information for a specified city.
    """
    city = command.split("in")[-1].strip() if "in" in command else "default city"
    api_key = "783909bc65d6cb3117bc5e8eff889071"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    weather_data = response.json()
    if weather_data["cod"] == 200:
        main = weather_data["main"]
        temperature = main["temp"]
        weather_desc = weather_data["weather"][0]["description"]
        weather_info = f"The current temperature in {city} is {temperature} degrees Celsius with {weather_desc}."
        speak(weather_info)
    else:
        speak("Sorry, I couldn't fetch the weather data.")

def open_application(command):
    """
    Open an application using the search functionality in the taskbar.
    """
    app_name = command.replace("open ", "").strip()
    if app_name:
        speak(f"Opening {app_name}.")
        try:
            pyautogui.press('win')
            time.sleep(1) 

            pyautogui.write(app_name)
            time.sleep(1)

            pyautogui.press('enter')
        except Exception as e:
            speak(f"Sorry, I couldn't open {app_name}.")
            print(f"Error: {e}")
    else:
        speak("Please specify the application you want to open.")

def search_web(command):
    """
    Perform a web search using the default browser.
    """
    query = command.replace("search for ", "").strip()
    if query:
        speak(f"Searching for {query}.")
        search_url = f"https://www.google.com/search?q={query}"
        webbrowser.open(search_url) 
    else:
        speak("Please specify what you want to search for.")

def exit_program():
    """
    Exit the program.
    """
    speak("Goodbye!")
    return True

command_map = {
    "time": get_current_time,
    "open browser": open_browser,
    "shutdown": shutdown_system,
    "weather": get_weather,
    "open": open_application,
    "search for": search_web,
    "exit": exit_program,
    "stop": exit_program,
}

def process_command(command):
    """
    Process the user's command using a command map.
    """
    command_handled = False

    for key in command_map:
        if key in command:
            command_handled = True
            if key in ["weather", "open", "search for"]:
                command_map[key](command)  
            else:
                should_exit = command_map[key]() 
                if should_exit:
                    return True
            break  

    if not command_handled:
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
