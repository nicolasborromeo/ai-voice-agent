import os
import logging
from deepgram.utils import verboselogs
from dotenv import load_dotenv
from deepgram import (
    DeepgramClient,
    SpeakOptions
)

load_dotenv()

SPEAK_TEXT = {"text": "Hi, I’m reaching out because my flight was unexpectedly canceled, and I need some help sorting it out. I didn’t receive any notification about the cancellation, and I’m not sure what the next steps are. I need to know if I can get rebooked on another flight or if there’s a way to request a refund. Also, I had paid for extra baggage and seat selection—could you let me know if those charges will be refunded as well? I’d appreciate any information you can provide to help me resolve this quickly. Thanks so much!"}
filename = "sample.mp3"

def main():
    API_KEY = os.getenv("DG_API_KEY")

    if not API_KEY:
        raise ValueError("Please set the DG_API_KEY environment variables")

    try:
        deepgram = DeepgramClient(API_KEY)

        options = SpeakOptions(
            model="aura-asteria-en",
        )

        response = deepgram.speak.rest.v("1").save(filename, SPEAK_TEXT, options)
        print(response.to_json(indent=4))

    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    main()
