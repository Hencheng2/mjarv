import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import os
from openai import OpenAI

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Set voice (0 for male, 1 for female if available)

# Initialize speech recognizer
recognizer = sr.Recognizer()

# Initialize OpenAI client (replace with your API key)
client = OpenAI(api_key="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")

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
