import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import os
import requests
import json
from openai import OpenAI
import random  # For joke feature

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Set voice (0 for male, 1 for female if available)

# Initialize speech recognizer
recognizer = sr.Recognizer()

# Initialize OpenAI client with hardcoded API key
client = OpenAI(api_key="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")

# OpenWeatherMap API key (hardcoded as provided)
weather_api_key = "cd0ef82d72645c018b32d07be1f6744d"

# Simple reminder storage (in-memory; for persistence, use a file or database)
reminders = []

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen for audio input and convert to text."""
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that.")
            return ""
        except sr.RequestError:
            speak("Sorry, there was an error with the speech recognition service.")
            return ""

def get_ai_response(prompt):
    """Get response from OpenAI API."""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error with AI response: {str(e)}"

def get_weather(city):
    """Fetch weather data for a city using OpenWeatherMap API."""
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": weather_api_key, "units": "metric"}
    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        if data["cod"] == 200:
            weather_desc = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            return f"The weather in {city} is {weather_desc} with a temperature of {temp}°C."
        else:
            return "Sorry, I couldn't fetch the weather data. Please check the city name."
    except Exception as e:
        return f"Error fetching weather: {str(e)}"

def set_reminder(reminder_text):
    """Set a simple reminder."""
    reminders.append(reminder_text)
    return f"Reminder set: {reminder_text}"

def get_reminders():
    """Get list of reminders."""
    if reminders:
        return "Your reminders are: " + "; ".join(reminders)
    else:
        return "You have no reminders set."

def tell_joke():
    """Tell a random joke using OpenAI."""
    prompt = "Tell me a short, funny joke."
    return get_ai_response(prompt)

def execute_command(command):
    """Process and execute commands."""
    if "hello" in command:
        speak("Hello! How can I assist you today?")
    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%H:%M")
        speak(f"The current time is {current_time}.")
    elif "open google" in command:
        webbrowser.open("https://www.google.com")
        speak("Opening Google.")
    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube.")
    elif "weather" in command:
        # Simple parsing: assume "weather in [city]"
        city = command.split("in")[-1].strip() if "in" in command else "London"  # Default city
        weather_info = get_weather(city)
        speak(weather_info)
    elif "set reminder" in command:
        reminder_text = command.replace("set reminder", "").strip()
        response = set_reminder(reminder_text)
        speak(response)
    elif "get reminders" in command or "what are my reminders" in command:
        response = get_reminders()
        speak(response)
    elif "tell a joke" in command:
        joke = tell_joke()
        speak(joke)
    elif "exit" in command or "stop" in command:
        speak("Goodbye!")
        return False
    else:
        # Use OpenAI for general queries
        response = get_ai_response(command)
        speak(response)
    return True

def main():
    """Main function to run JARVIS."""
    speak("JARVIS online. How can I help you?")
    while True:
        command = listen()
        if command:
            if not execute_command(command):
                break

if __name__ == "__main__":
    main()
