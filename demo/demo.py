import utils
from deepgram import FileSource

AUDIO_FILE = "sample.mp3"

def main():
    try:
         # STEP 1: Ingest the audio file
        with open(AUDIO_FILE, "rb") as file:
            buffer_data = file.read()

         # Use FileSource to provide audio data to Deepgram's servers
        payload: FileSource = {
             "buffer": buffer_data,
         }

         # STEP 2: Get the transcript of the voice file
        customer_inquiry = utils.get_transcript(payload)
        # STEP 3: Send this information to OpenAI to respond.
        # Extract the transcribed text from the Deepgram response
        transcribed_text = customer_inquiry["results"]["channels"][0]["alternatives"][0]["transcript"]
        agent_answer = utils.ask_openai(transcribed_text)
        print(agent_answer)

        # STEP 4: Print responses (optional) that can be used for integration with an app or stored in a customer database for analytics
        print('Topics:', utils.get_topics(customer_inquiry))
        print('Summary:', utils.get_summary(customer_inquiry))

        # STEP 5: Take the OpenAI response and write this out as an audio file to generate an audio response using Deepgram's TTS
        print("Agent Answer: ", agent_answer)
        utils.save_speech_summary(agent_answer)

    except Exception as e:
        print(f"Exception: {e}")


#This ensures that the code inside main() only runs when the script is executed directly, not when imported as a module.
if __name__ == "__main__":
    main()
