import subprocess
import speech_recognition as sr
import time
import pyautogui

# --- OPEN COMMANDS ---
def open_chrome():
    subprocess.Popen("start chrome", shell=True)

def open_workspace():
    apps = [
        "start code",
        "start cursor",
        "start https://chat.openai.com",
        "start https://gemini.google.com",
        "start https://youtube.com"
    ]
    for app in apps:
        subprocess.Popen(app, shell=True)

def open_youtube():
    subprocess.Popen("start https://youtube.com", shell=True)

def open_chatgpt():
    subprocess.Popen("start https://chat.openai.com", shell=True)

def open_gemini():
    subprocess.Popen("start https://gemini.google.com", shell=True)


# --- CLOSE COMMANDS ---
def close_chrome():
    subprocess.Popen("taskkill /f /im chrome.exe", shell=True)

def close_notepad():
    subprocess.Popen("taskkill /f /im notepad.exe", shell=True)

def close_vscode():
    subprocess.Popen("taskkill /f /im Code.exe", shell=True)

def close_cursor():
    subprocess.Popen("taskkill /f /im Cursor.exe", shell=True)

def close_workspace():
    apps = ["chrome.exe", "Code.exe", "Cursor.exe", "notepad.exe"]
    for app in apps:
        subprocess.Popen(f"taskkill /f /im {app}", shell=True)


# --- DICTATION MODE ---
def dictation_mode(recognizer):
    print("Dictation started... say 'stop writing' to end.")

    while True:
        with sr.Microphone() as source:
            audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio).lower()
            print("You said:", text)

            if "stop writing" in text:
                print("Stopping dictation...")
                break

            pyautogui.write(text + " ", interval=0.05)

        except:
            print("Could not understand...")


def open_notepad_and_dictate(recognizer):
    subprocess.Popen("notepad", shell=True)
    time.sleep(1.5)
    dictation_mode(recognizer)


# --- COMMAND LOGIC ---
def handle_command(text, recognizer):

    # OPEN
    if "open chrome" in text:
        print("Opening Chrome...")
        open_chrome()

    elif "open workspace" in text:
        print("Opening your workspace...")
        open_workspace()

    elif "open youtube" in text:
        print("Opening YouTube...")
        open_youtube()

    elif "open chatgpt" in text:
        print("Opening ChatGPT...")
        open_chatgpt()

    elif "open gemini" in text:
        print("Opening Gemini...")
        open_gemini()

    elif "open notepad" in text:
        print("Opening Notepad and starting dictation...")
        open_notepad_and_dictate(recognizer)

    # CLOSE
    elif "close chrome" in text:
        print("Closing Chrome...")
        close_chrome()

    elif "close notepad" in text:
        print("Closing Notepad...")
        close_notepad()

    elif "close code" in text or "close vscode" in text:
        print("Closing VS Code...")
        close_vscode()

    elif "close cursor" in text:
        print("Closing Cursor...")
        close_cursor()

    elif "close workspace" in text:
        print("Closing your workspace...")
        close_workspace()

    # EXIT PROGRAM
    elif "exit" in text or "stop program" in text:
        print("Exiting assistant...")
        return False

    else:
        print("I don't understand that yet.")

    return True

# --- VOICE SYSTEM ---
recognizer = sr.Recognizer()

while True:
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("\nListening...")
        audio = recognizer.listen(source)

    try:
        user_input = recognizer.recognize_google(audio).lower()
        print("You said:", user_input)

        if not handle_command(user_input, recognizer):
            break

    except sr.UnknownValueError:
        print("Sorry, I didn’t catch that.")
    except sr.RequestError:
        print("Network issue.")