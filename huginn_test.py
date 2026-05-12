import subprocess
import speech_recognition as sr
import time
import pyautogui
import os
import pyttsx3
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# --- TTS SYSTEM ---
engine = pyttsx3.init()
# Optional: Adjust voice properties
voices = engine.getProperty('voices')
if voices:
    engine.setProperty('voice', voices[0].id) # Index 0 is usually male, 1 is female
engine.setProperty('rate', 180) # Speed of speech

def speak(text):
    """Prints and speaks the given text."""
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

# --- TOOLS FOR GEMINI ---
def run_command(command: str):
    """
    Executes a shell command on the system.
    Use this to open applications (e.g., 'start notepad', 'start chrome', 'start https://google.com').
    
    Args:
        command: The shell command to execute.
    """
    print(f"Executing: {command}")
    try:
        subprocess.Popen(command, shell=True)
        return f"Successfully executed: {command}"
    except Exception as e:
        return f"Error executing command: {str(e)}"

def close_application(process_name: str):
    """
    Closes an application by its process name (e.g., 'notepad.exe', 'chrome.exe').
    
    Args:
        process_name: The name of the process to kill.
    """
    print(f"Closing: {process_name}")
    try:
        subprocess.Popen(f"taskkill /f /im {process_name}", shell=True)
        return f"Closed {process_name}"
    except Exception as e:
        return f"Error closing {process_name}: {str(e)}"

def type_text(text: str):
    """
    Types text at the current cursor position.
    
    Args:
        text: The text to type.
    """
    print(f"Typing: {text}")
    pyautogui.write(text, interval=0.05)
    return f"Typed: {text}"

def press_key(key: str):
    """
    Presses a specific key on the keyboard (e.g., 'enter', 'tab', 'win').
    
    Args:
        key: The key to press.
    """
    print(f"Pressing key: {key}")
    pyautogui.press(key)
    return f"Pressed key: {key}"

def wait(seconds: float):
    """
    Waits for a specified number of seconds.
    
    Args:
        seconds: Number of seconds to wait.
    """
    print(f"Waiting for {seconds} seconds...")
    time.sleep(seconds)
    return f"Waited {seconds} seconds"

# Define the tools for Gemini
tools = [run_command, close_application, type_text, press_key, wait]

# Initialize Gemini Client
if not GEMINI_API_KEY or GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
    print("WARNING: GEMINI_API_KEY not found in .env file. Please add your API key.")
    client = None
    chat = None
else:
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    # System instruction for the assistant
    system_instruction = (
        "You are Huginn, an intelligent Windows voice assistant. "
        "You can control the computer using tools or answer questions. "
        "Keep your spoken responses concise and helpful. "
        "When asked to perform a task, do it and confirm briefly."
    )
    
    # Start a chat session with automatic function calling enabled by default
    # Using 'gemini-2.0-flash-lite' as it might be more stable regarding quota/thought signatures
    chat = client.chats.create(
        model='gemini-2.0-flash-lite',
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            tools=tools,
        )
    )

# --- VOICE SYSTEM ---
recognizer = sr.Recognizer()

def main():
    speak("Huginn Intelligent Assistant is online.")
    
    if not chat:
        print("Assistant cannot start without a valid API key.")
        return

    while True:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("\nListening...")
            audio = recognizer.listen(source)

        try:
            user_input = recognizer.recognize_google(audio).lower()
            print("You said:", user_input)

            if "exit" in user_input or "stop program" in user_input:
                speak("Goodbye!")
                break

            # Send input to Gemini
            response = chat.send_message(user_input)
            
            # Print and speak Gemini's text response if any
            if response.text:
                speak(response.text)
            else:
                # If there's no text but tools were called, Gemini usually follows up with text 
                # after the tool results are processed. 
                # In automatic mode, send_message handles the tool loop.
                pass

        except sr.UnknownValueError:
            print("Sorry, I didn’t catch that.")
        except sr.RequestError:
            print("Network issue.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
