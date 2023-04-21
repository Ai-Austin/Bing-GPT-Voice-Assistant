# Bing-GPT-Voice-Assistant
This is a Python voice assistant that uses both OpenAI's 3.5 turbo model and bing's model with access to the internet for searchable results. All speech-to-text transcription is done locally using OpenAI's Whisper running on the local machine, and text-to-speech is done with AWS Polly.

NOTE: You will need to have access to the bing AI search function to utilize this feature.

# Setup
The setup for this project is relatively simple and has a detailed [youtube tutorial](https://youtu.be/aokn48vB0kc), which briefly explains how the program works as well as providing a detailed installation guide. 


## Quick Setup:
### Install and Setup
1. install ffmpeg from their [website](https://ffmpeg.org/download.html), or by running ```sudo apt update && sudo apt install ffmpeg``` on Linux

2. Click the green ```Code``` button then ```Download ZIP```. After downloading, unzip the file and copy the path to the folder that has the main.py file in it. Alternatively run ```git clone https://github.com/Ai-Austin/Bing-GPT-Voice-Assistant.git``` if you have installed git on your device, 

3. To set up the AI's for response generation, use the steps outlined from the [video](https://youtu.be/aokn48vB0kc?t=119) to setup the cookies.json file and follow the steps for creating an [OpenAI key](https://youtu.be/aokn48vB0kc?t=444) and putting it in the program where prompted.

4. Install [python](https://www.python.org/downloads/release/python-3100/) if it is not already on your system. Scroll down to **files** and download and install the version compatible for your computer. ```Windows x86-64 executable installer``` should work for most windows users (note: The link is to the 3.10.0 version, the latest release 3.11 is not compatible with Whisper)

5. Open a new terminal window and run the command ```cd path\you\copied``` using the path from step 1. Then run ```pip install -r requirements.txt``` to install the required packages

### Running the Assistant
Simply open a terminal and move to the folder with the code ```cd path\you\copied``` or use the terminal from step 5. Then run ```python main.py``` to start the assitant. To exit the assistant, press ```ctrl+c``` to stop the program.


