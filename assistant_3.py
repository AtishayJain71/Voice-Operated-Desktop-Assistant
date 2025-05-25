import os
import pyautogui
import time
import winreg
import speech_recognition as sr
import pyttsx3
import datetime
import requests

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """
    Convert text to speech and print it to the terminal.
    """
    print(f"Assistant: {text}")  # Print the output to the terminal
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
    speak(f"The current time is {current_time}")

def open_browser():
    """
    Open the default web browser.
    """
    speak("Opening the browser.")
    os.system("start chrome")  # For Windows

def shutdown_system():
    """
    Shut down the system.
    """
    speak("Shutting down the system.")
    os.system("shutdown /s /t 1")  # For Windows

def get_weather(command):
    """
    Fetch weather information for a specified city.
    """
    city = command.split("in")[-1].strip() if "in" in command else "dehradun" 
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

def find_application_path(app_name):
    """
    Find the installation path of an application from the Windows Registry.
    """
    try:
        registry_paths = [
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
        ]
        
        for path in registry_paths:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path) as key:
                for i in range(0, winreg.QueryInfoKey(key)[0]):
                    subkey_name = winreg.EnumKey(key, i)
                    with winreg.OpenKey(key, subkey_name) as subkey:
                        try:
                            display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                            if app_name.lower() in display_name.lower():
                                return winreg.QueryValueEx(subkey, "InstallLocation")[0]
                        except FileNotFoundError:
                            pass
    except Exception as e:
        print(f"Error querying registry: {e}")
    
    return None

def open_application(command):
    """
    Open an application using the search functionality in the taskbar if found in the registry.
    """
    app_name = command.replace("open ", "").strip()
    if app_name:
        speak(f"Attempting to open {app_name}.")
        
        # First, try to find the application path from the registry
        app_path = find_application_path(app_name)
        
        if app_path:
            # If found, open using Start Menu search
            speak(f"Opening {app_name} using the Start Menu search.")
            try:
                # Open Start Menu
                pyautogui.press('win')
                time.sleep(1)  # Wait for the Start Menu to open
                
                # Type the application name
                pyautogui.write(app_name)
                time.sleep(1)  # Wait for search results to appear
                
                # Press Enter to open the first search result
                pyautogui.press('enter')
                time.sleep(2)  # Wait for the application to launch
            except Exception as e:
                speak(f"Sorry, I couldn't open {app_name}.")
                print(f"Error: {e}")
        else:
            speak(f"Application {app_name} not found in the registry. Please ensure it is installed.")
    else:
        speak("Please specify the application you want to open.")

def exit_program():
    """
    Exit the program.
    """
    speak("Goodbye!")
    return True

# Command map: maps keywords to functions
command_map = {
    "time": get_current_time,
    "open browser": open_browser,
    "shutdown": shutdown_system,
    "weather": get_weather,
    "open": open_application,  # Added generic application opening command
    "exit": exit_program,
    "stop": exit_program,
}

def process_command(command):
    """
    Process the user's command using a command map.
    """
    command_handled = False  # Flag to track if the command was handled

    for key in command_map:
        if key in command:
            if key == "weather":
                command_map[key](command)  # Pass the command to get_weather to extract the city name
            elif key == "open":
                command_map[key](command)  # Pass the command to open_application to handle application names
            else:
                command_map[key]()  # Execute the corresponding function
            command_handled = True
            break  # Exit the loop once a command is handled

    if not command_handled:
        speak("Sorry, I don't understand that command.")
    return key == "exit" or key == "stop"  # Exit the program if the command is "exit" or "stop"

if __name__ == "__main__":
    speak("Hello, how can I assist you today?")
    while True:
        command = listen_command()
        if command:
            should_exit = process_command(command)
            if should_exit:
                break
