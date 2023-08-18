import openai
import asyncio
import re
import whisper
import boto3
import pydub
from pydub import playback
import speech_recognition as sr
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle

# Initialize the OpenAI API
openai.api_key = "[paste your OpenAI API key here]"

# Create a recognizer object and wake word variables
recognizer = sr.Recognizer()
BING_WAKE_WORD = "bing"
GPT_WAKE_WORD = "gpt"

def get_wake_word(phrase):
    if BING_WAKE_WORD in phrase.lower():
        return BING_WAKE_WORD
    elif GPT_WAKE_WORD in phrase.lower():
        return GPT_WAKE_WORD
    else:
        return None
    
def synthesize_speech(text, output_filename):
    polly = boto3.client('polly', region_name='us-west-2')
    response = polly.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId='Salli',
        Engine='neural'
    )

    with open(output_filename, 'wb') as f:
        f.write(response['AudioStream'].read())

def play_audio(file):
    sound = pydub.AudioSegment.from_file(file, format="mp3")
    playback.play(sound)

#function to handle cookies
def getCookies(url):
    import browser_cookie3
    browsers = [
        # browser_cookie3.chrome,
        # browser_cookie3.chromium,
        # browser_cookie3.opera,
        # browser_cookie3.opera_gx,
        # browser_cookie3.brave,
        browser_cookie3.edge,
        # browser_cookie3.vivaldi,
        # browser_cookie3.firefox,
        # browser_cookie3.librewolf,
        # browser_cookie3.safari,
    ]
    for browser_fn in browsers:
        # if browser isn't installed browser_cookie3 raises exception
        # hence we need to ignore it and try to find the right one
        try:
            cookies = []
            cj = browser_fn(domain_name=url)
            for cookie in cj:
                cookies.append(cookie.__dict__)
            return cookies
        except:
            continue

async def main():
    cookies = getCookies('.bing.com') #handling cookies of edge
    # Use the preloaded tiny_model
    model = whisper.load_model("tiny")
    while True:

        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            print(f"Waiting for wake words 'ok bing' or 'ok chat'...")
            while True:
                audio = recognizer.listen(source)
                try:
                    with open("audio.wav", "wb") as f:
                        f.write(audio.get_wav_data())
                    result = model.transcribe("audio.wav")
                    phrase = result["text"]
                    print(f"You said: {phrase}")

                    wake_word = get_wake_word(phrase)
                    if wake_word is not None:
                        break
                    else:
                        print("Not a wake word. Try again.")
                except Exception as e:
                    print("Error transcribing audio: {0}".format(e))
                    continue

            print("Speak a prompt...")
            synthesize_speech('What can I help you with?', 'response.mp3')
            play_audio('response.mp3')
            audio = recognizer.listen(source)

            try:
                with open("audio_prompt.wav", "wb") as f:
                    f.write(audio.get_wav_data())
                result = model.transcribe("audio_prompt.wav")
                user_input = result["text"]
                print(f"You said: {user_input}")
            except Exception as e:
                print("Error transcribing audio: {0}".format(e))
                continue

            if wake_word == BING_WAKE_WORD:
                bot = Chatbot(cookies=cookies)
                response = await bot.ask(prompt=user_input, conversation_style=ConversationStyle.precise)
                # Select only the bot response from the response dictionary
                for message in response["item"]["messages"]:
                    if message["author"] == "bot":
                        bot_response = message["text"]
                # Remove [^#^] citations in response
                bot_response = re.sub('\[\^\d+\^\]', '', bot_response)

            else:
                # Send prompt to GPT-3.5-turbo API
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content":
                        "You are a helpful assistant."},
                        {"role": "user", "content": user_input},
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
                
        print("Bot's response:", bot_response)
        synthesize_speech(bot_response, 'response.mp3')
        play_audio('response.mp3')
        await bot.close()

if __name__ == "__main__":
    asyncio.run(main())
