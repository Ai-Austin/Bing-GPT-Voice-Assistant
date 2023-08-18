from os import system
from EdgeGPT.EdgeUtils import Query
import speech_recognition as sr
import sys, whisper, warnings, time, openai

# Wake word variables
BING_WAKE_WORD = "bing"
GPT_WAKE_WORD = "gpt"

# Initialize the OpenAI API
openai.api_key = "[paste your OpenAI API key here]"

r = sr.Recognizer()
tiny_model = whisper.load_model('tiny')
base_model = whisper.load_model('base')
listening_for_wake_word = True
bing_engine = True
source = sr.Microphone() 
warnings.filterwarnings("ignore", category=UserWarning, module='whisper.transcribe', lineno=114)

if sys.platform != 'darwin':
    import pyttsx3
    engine = pyttsx3.init()

def speak(text):
    if sys.platform == 'darwin':
        ALLOWED_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,?!-_$:+-/ ")
        clean_text = ''.join(c for c in text if c in ALLOWED_CHARS)
        system(f"say '{clean_text}'")
    else:
        engine.say(text)
        engine.runAndWait()

def listen_for_wake_word(audio):
    global listening_for_wake_word
    global bing_engine
    with open("wake_detect.wav", "wb") as f:
        f.write(audio.get_wav_data())
    result = tiny_model.transcribe('wake_detect.wav')
    text_input = result['text']
    if BING_WAKE_WORD in text_input.lower().strip():
        print("Speak your prompt to Bing.")
        speak('Listening')
        listening_for_wake_word = False
    elif GPT_WAKE_WORD in text_input.lower().strip():
        print("Speak your prompt to GPT 3.5 Turbo.")
        speak('Listening')
        bing_engine = False
        listening_for_wake_word = False

def prompt_bing(audio):
    global listening_for_wake_word
    global bing_engine
    try:
        with open("prompt.wav", "wb") as f:
            f.write(audio.get_wav_data())
        result = base_model.transcribe('prompt.wav')
        prompt_text = result['text']
        if len(prompt_text.strip()) == 0:
            print("Empty prompt. Please speak again.")
            speak("Empty prompt. Please speak again.")
            listening_for_wake_word = True
        else:
            print('User: ' + prompt_text)
            output = Query(prompt_text)
            print('Bing: ' + str(output))
            speak(str(output))
            print('\nSay Ok Bing or Ok GPT to wake me up. \n')
            bing_engine = True
            listening_for_wake_word = True
    
    except Exception as e:
        print("Prompt error: ", e)
    

def prompt_gpt(audio):
    global listening_for_wake_word
    global bing_engine
    try:
        with open("prompt.wav", "wb") as f:
            f.write(audio.get_wav_data())
        result = base_model.transcribe('prompt.wav')
        prompt_text = result['text']
        if len(prompt_text.strip()) == 0:
            print("Empty prompt. Please speak again.")
            speak("Empty prompt. Please speak again.")
            listening_for_wake_word = True
        else:
            response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content":
                        "You are a helpful assistant."},
                        {"role": "user", "content": prompt_text},
                    ],
                    temperature=0.5,
                    max_tokens=150,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0,
                    n=1,
                    stop=["\nUser:"],
                )
            bot_response = response["choices"][0]["message"]["content"]
            listening_for_wake_word = True
            bing_engine = True

    except Exception as e:
        print("Prompt error: ", e)

def callback(recognizer, audio):
    global listening_for_wake_word
    global bing_engine
    if listening_for_wake_word:
        listen_for_wake_word(audio)
    elif bing_engine == True:
        prompt_bing(audio)
    elif bing_engine == False:
        prompt_gpt(audio)

def start_listening():
    with source as s:
        r.adjust_for_ambient_noise(s, duration=2)
    print('\nSay Ok Bing or Ok GPT to wake me up. \n')
    r.listen_in_background(source, callback)
    while True:
        time.sleep(1) 

if __name__ == '__main__':
    start_listening() 
