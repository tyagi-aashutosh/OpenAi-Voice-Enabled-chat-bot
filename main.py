
import speech_recognition as sr
import openai
import pyttsx3

# OpenAI API key set up

openai.api_key = "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"
# initialize the text-to-speech engine
engine = pyttsx3.init()

# seting the speech rate
rate = engine.getProperty('rate')
engine.setProperty('rate', 180)

# initialize the conversation history
history = ""

# function that captures user speech input and converts it to text
def get_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
    try:
        query = recognizer.recognize_google(audio)
        print("You: " + query)
        return query
    except:
        print("Sorry, I didn't understand. Could you please repeat?")
        return ""

# function that generate a response to the user query from Openai
def get_response(query, history):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=history + "\nUser: " + query + "\nAI:",
        temperature=0.7,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].text.strip()

# Text to speech so it read's the response back to the user in speech format
def speak(text):
    engine.say(text)
    engine.runAndWait()

#start the conversation
speak("Hello, how can I help you?")

# openai response, and the response getting back to the user
while True:
    query = get_input()
    if query:
        try:
            response = get_response(query, history)
            print(response)
            speak(response)
            history += "\nUser: " + query + "\nAI: " + response
        except:
            speak("Sorry, I couldn't process your request. Please try again later.")