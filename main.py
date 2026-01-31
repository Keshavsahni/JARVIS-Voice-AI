import speech_recognition as sr
import google.generativeai as genai
import os
import webbrowser
import datetime
import random
from key import keys

chatStr=""
def chat(text):
    global chatStr
    api_key = keys[4]
    genai.configure(api_key=api_key)
    chatStr+=f"Keshav: {text}. Dont pronounce the word 'Jarvis' in your response\n Jarvis: "
    prompt=chatStr
    # Configure generation parameters
    generation_config = genai.GenerationConfig(
        temperature=0.7,
        max_output_tokens=100
    )

    model = genai.GenerativeModel("gemini-2.5-flash-lite", generation_config=generation_config)
    response = model.generate_content(prompt)
    print(response.text)
    chatStr+=f"{response.text}\n"
    sayCommand(response.text)
    return response.text


def ai(prompt):
    text=f"GenAI response for prompt:{prompt} \n\n\n"
    api_key = keys[4]
    genai.configure(api_key=api_key)
    # Configure generation parameters
    generation_config = genai.GenerationConfig(
        temperature=0.7,
        max_output_tokens=100
    )

    model = genai.GenerativeModel("gemini-2.5-flash-lite", generation_config=generation_config)
    # Use the correct method to generate content
    # prompt assigned from argument directly
    response = model.generate_content(prompt)
    print(response.text)
    text+=response.text
    if not os.path.exists("Openai"):
        os.mkdir("Openai")
    
    
    with open(f"Openai/prompt-{random.randint(1,1000)}","w") as f:
        f.write(text)

    
def sayCommand(talk):
    os.system(f"say {talk}")

def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold=1
        audio=r.listen(source)
        try:
            query=r.recognize_google(audio,language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            print("Sorry, I didn't understand that")
            return "Some error occured"

if __name__ == "__main__":
    sayCommand("hello i am Jarvis")
    while True:
        text=takeCommand()
        sites=[["youtube","https://www.youtube.com/"],["google","https://www.google.com/"],["instagram","https://www.instagram.com/"],["linkedin","https://www.linkedin.com/"],["github","https://www.github.com/"]]
        for site in sites:
            if f"open {site[0]}" in text.lower():
                sayCommand(f"opening {site[0]}")
                webbrowser.open(site[1])
        if "time" in text.lower():
            current_time=datetime.datetime.now().strftime("%H:%M:%S")
            sayCommand(f"the current time is {current_time}")

        if "using AI".lower() in text.lower():
            ai(text)
        
        if "quit".lower() in text.lower():
            exit()
        
        else:
            chat(text)