import os
import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechSynthesizer
from LLM_source import llm
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

class AzureTextToSpeech:
    def __init__(self):
        load_dotenv()  # Load variables from .env
        self.speech_key = os.getenv("AZURE_SPEECH_KEY")
        self.service_region = os.getenv("AZURE_SERVICE_REGION", "eastus2")
        
        if not self.speech_key:
            raise ValueError("AZURE_SPEECH_KEY not set in environment variables")
        
        self.speech_config = SpeechConfig(
            subscription=self.speech_key, 
            region=self.service_region
        )
        self.speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"

    def create_audio(self, text, output_path="output.wav", use_ssml=False):
        synthesizer = SpeechSynthesizer(
            speech_config=self.speech_config, 
            audio_config=None
        )
        
        # Generate speech using either SSML or plain text
        if use_ssml:
            result = synthesizer.speak_ssml_async(text).get()
        else:
            result = synthesizer.speak_text_async(text).get()
        
        stream = AudioDataStream(result)
        stream.save_to_wav_file(output_path)
        
        return output_path

    def change_voice(self, voice_name):
        self.speech_config.speech_synthesis_voice_name = voice_name





