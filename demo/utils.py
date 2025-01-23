import os
import json
import openai
from dotenv import load_dotenv
from deepgram import DeepgramClient, PrerecordedOptions, SpeakOptions, DeepgramClientOptions
from deepgram.utils import verboselogs

load_dotenv()

DG_API_KEY = os.getenv("DG_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


if not DG_API_KEY or not OPENAI_API_KEY:
    raise ValueError("Please set the DG_API_KEY and/or OPENAI_API_KEY environment variable.")



deepgram = DeepgramClient(DG_API_KEY)
config: DeepgramClientOptions = DeepgramClientOptions(
    verbose=verboselogs.DEBUG
)

openai_client = openai.OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

system_prompt = """
You are a helpful and friendly customer service assistant for a cell phone provider.
Your goal is to help customers with issues like:
- Billing questions
- Troubleshooting their mobile devices
- Explaining data plans and features
- Activating or deactivating services
- Transferring them to appropriate departments for further assistance

Maintain a polite and professional tone in your responses. Always make the customer feel valued and heard.
"""

text_options = PrerecordedOptions(
    model="nova-2",
    language="en",
    summarize="v2",
    topics=True,
    intents=True,
    smart_format=True,
    sentiment=True
)

speak_options = SpeakOptions(
    model="aura-asteria-en",
    encoding="linear16",
    container="wav"
)

def ask_openai(prompt):
    """
    Send OpenAI a prompt, returns a response back.
    """
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except openai.OpenAIError as e:
        return f"An error ocurred: {e}"

# query deepgrams voice APIs

def get_transcript(payload, options=text_options):
    """
    Returns a JSON of Deepgram's transcription given an audio file.
    """
    response = deepgram.listen.rest.v("1").transcribe_file(payload, options).to_json()
    return json.loads(response) #parse the json string into a dictionary


def get_topics(transcript):
    """
    Returns back a list of all unique topics in a transcript.
    """
    topics = set() #emtpy set to store unique topics
    for segment in transcript['results']['topics']['segments']:
        for topic in segment['topics']:
            topics.add(topic['topic'])
    return topics

def get_summary(transcript):
    # """
    # returns the summary of the transcript as a string.
    # """
    return transcript['results']['summary']['short']

def save_speech_summary(transcript, options=speak_options):
    """
    Writes an audio summary of the transcript to disk.
    """
    s = {"text": transcript}
    filename = "output.wav"
    response = deepgram.speak.rest.v("1").save(filename, s, options)
