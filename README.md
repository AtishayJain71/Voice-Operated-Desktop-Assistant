# 🗣️ Voice Assistant Desktop Application

A Python-based voice-controlled desktop assistant that can perform a variety of tasks through simple voice commands. This assistant utilizes `speech_recognition`, `pyttsx3`, and other essential Python libraries to create an interactive and responsive voice assistant for Windows systems.

---

## 🚀 Features

- 🕒 Announces current time
- 🌦️ Fetches real-time weather information
- 🌐 Opens websites and performs Google searches
- 📂 Opens system applications
- 💻 Shuts down the system
- 🎤 Listens for voice commands and responds via speech
- 🔁 Continuous listening loop with graceful exit

---

## 🧰 Technologies & Libraries Used

- `speech_recognition` – To capture and recognize speech input.
- `pyttsx3` – For text-to-speech conversion.
- `datetime` – To fetch current date and time.
- `os` – To run system-level commands.
- `requests` – To fetch weather data via HTTP API.
- `pyautogui` – To automate GUI interactions.
- `time` – To introduce execution delays.
- `webbrowser` – To open web URLs.

---

## 🧠 Functional Overview

| Command | Functionality |
|--------|---------------|
| “What's the time?” | Announces current time. |
| “Open Chrome” | Opens Google Chrome using system commands. |
| “Shutdown system” | Executes Windows shutdown command. |
| “What's the weather in [city]?” | Fetches weather using OpenWeatherMap API. |
| “Search for [query]” | Performs Google search in browser. |
| “Open [application]” | Opens apps using simulated keystrokes. |
| “Exit” / “Stop” | Exits the assistant gracefully. |

---
