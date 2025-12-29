import openai
import speech_recognition as sr
from gtts import gTTS
from elevenlabs import generate, save, set_api_key, voices
import sounddevice as sd
import soundfile as sf
import requests
import re

from dotenv import load_dotenv
from os import getenv, path
from json import load, dump, dumps, JSONDecodeError

class Waifu:
    def __init__(self) -> None:
        self.mic = None
        self.recogniser = None

        self.user_input_service = None
        self.stt_duration = None

        self.chatbot_service = None
        self.chatbot_model = None
        self.chatbot_temperature = None
        self.chatbot_personality_file = None

        self.message_history = []
        self.context = []

        self.tts_service = None
        self.tts_voice = None
        self.tts_model = None


    def initialize(self, user_input_service:str = None, stt_duration:float = None, mic_index:int = None,
                    chatbot_service:str = None, chatbot_model:str = None, chatbot_temperature:float = None, personality_file:str = None,
                    tts_service:str = None, output_device = None, tts_voice:str = None, tts_model:str = None) -> None:
        load_dotenv()

        self.update_user_input(user_input_service=user_input_service, stt_duration=stt_duration)
        self.mic = sr.Microphone(device_index=mic_index)
        self.recogniser = sr.Recognizer()
        
        openai.api_key = getenv("OPENAI_API_KEY")
        openai.api_base = getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
        self.update_chatbot(service = chatbot_service, model = chatbot_model, temperature = chatbot_temperature, personality_file = personality_file)
        self.__load_chatbot_data()

        self.update_tts(service=tts_service, output_device=output_device, voice=tts_voice, model=tts_model)

    def update_user_input(self, user_input_service:str = 'whisper', stt_duration:float = 0.5) -> None:
        if user_input_service:
            self.user_input_service = user_input_service
        elif self.user_input_service is None:
            self.user_input_service = 'whisper'

        if stt_duration:
            self.stt_duration = stt_duration
        elif self.stt_duration is None:
            self.stt_duration = 0.5

    def update_chatbot(self, service:str = 'openai', model:str = 'gpt-3.5-turbo', temperature:float = 0.5, personality_file:str = 'personality.txt') -> None:
        if service:
            self.chatbot_service = service
        elif self.chatbot_service is None:
            self.chatbot_service = 'openai'

        if model:
            self.chatbot_model = model
        elif self.chatbot_model is None:
            self.chatbot_model = 'gpt-3.5-turbo'

        if temperature:
            self.chatbot_temperature = temperature
        elif self.chatbot_temperature is None:
            self.chatbot_temperature = 0.5

        if personality_file:
            self.chatbot_personality_file = personality_file
        elif self.chatbot_personality_file is None:
            self.chatbot_personality_file = 'personality.txt'

    def update_tts(self, service:str = 'google', output_device = None, voice = None, model:str = None) -> None:
        if service:
            self.tts_service = service
        elif self.tts_service is None:
            self.tts_service = 'google'

        set_api_key(getenv('ELEVENLABS_API_KEY'))

        if voice is not None:  # Changed from 'if voice:' to handle voice=0 correctly
            self.tts_voice = voice
        elif self.tts_voice is None:
            self.tts_voice = 'Elli'

        if model:
            self.tts_model = model
        elif self.tts_model is None:
            self.tts_model = 'eleven_monolingual_v1'

        if output_device is not None:
            try:
                sd.check_output_settings(output_device)
                sd.default.samplerate = 44100
                sd.default.device = output_device
            except sd.PortAudioError:
                print("Invalid output device! Make sure you've launched VB-Cable.\n",
                       "Check that you've choosed the correct output_device in initialize method.\n", 
                       "From the list below, select device that starts with 'CABLE Input' and set output_device to it's id in list.\n",
                       "If you still have this error try every device that starts with 'CABLE Input'. If it doesn't help please create GitHub issue.")
                print(sd.query_devices())
                raise

    def get_audio_devices(self):
        return sd.query_devices()

    def get_user_input(self, service:str = None, stt_duration:float = None) -> str:
        service = self.user_input_service if service is None else service
        stt_duration = self.stt_duration if stt_duration is None else stt_duration

        supported_stt_services = ['whisper', 'google']
        supported_text_services = ['console']

        result = ""
        if service in supported_stt_services:
            result = self.__recognise_speech(service, duration=stt_duration)
        elif service in supported_text_services:
            result = self.__get_text_input(service)
        else:
            raise ValueError(f"{service} servise doesn't supported. Please, use one of the following services: {supported_stt_services + supported_text_services}")
        
        return result

    def get_chatbot_response(self, prompt:str, service:str = None, model:str = None, temperature:float = None) -> str:
        service = self.chatbot_service if service is None else service
        model = self.chatbot_model if model is None else model
        temperature = self.chatbot_temperature if temperature is None else temperature

        supported_chatbot_services = ['openai', 'test']

        result = ""
        if service == 'openai':
            result = self.__get_openai_response(prompt, model=model, temperature=temperature)
        elif service == 'test':
            result = "This is test answer from Waifu. Nya kawaii, senpai!"
        else:
            raise ValueError(f"{service} servise doesn't supported. Please, use one of the following services: {supported_chatbot_services}")
        
        return result

    def tts_say(self, text:str, service:str = None, voice:str = None, model:str = None) -> None:
        service = self.tts_service if service is None else service
        voice = self.tts_voice if voice is None else voice
        model = self.tts_model if model is None else model

        supported_tts_services = ['google', 'elevenlabs', 'voicevox', 'console']

        if service not  in supported_tts_services:
            raise ValueError(f"{service} servise doesn't supported. Please, use one of the following services: {supported_tts_services}")



        if service == 'google':
            gTTS(text=text, lang='en', slow=False, lang_check=False).save('output.mp3')
        elif service == 'elevenlabs':
            self.__elevenlabs_generate(text=text, voice=voice, model=model)
        elif service == 'voicevox':
            self.__voicevox_generate(text=text, speaker_id=voice)
            data, fs = sf.read('output.wav')
            sd.play(data, fs)
            sd.wait()
            return
        elif service == 'console':
            print('\n\33[7m' + "Waifu:" + '\33[0m' + f' {text}')
            return

        data, fs = sf.read('output.mp3')
        sd.play(data, fs)
        sd.wait()

    def conversation_cycle(self) -> dict:
        input = self.get_user_input()

        response = self.get_chatbot_response(input)

        self.tts_say(response)
        
        return dict(user = input, assistant = response)

    def __get_openai_response(self, prompt:str, model:str, temperature:float) -> str:
        self.__add_message('user', prompt)
        messages = self.context + self.message_history

        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature, 
        )
        response = response.choices[0].message["content"]
        response = re.sub(r'\([^)]*\)', '', response).strip()

        self.__add_message('assistant', response)

        self.__add_message('assistant', response)
        self.__update_message_history()

        return response

    def __add_message(self, role:str, content:str) -> None:
        self.message_history.append({'role': role, 'content': content})

    def __load_chatbot_data(self, file_name:str = None) -> None:
        file_name = self.chatbot_personality_file if file_name is None else file_name

        with open(file_name, 'r', encoding='utf-8') as f:
            personality = f.read()
        self.context = [{'role': 'system', 'content': personality}]

        if path.isfile('./message_history.txt'):
            with open('message_history.txt', 'r') as f:
                try:
                    self.message_history = load(f)
                except JSONDecodeError:
                    pass

    def __update_message_history(self) -> None:
        with open('message_history.txt', 'w') as f:
                dump(self.message_history, f)

    def __get_text_input(self, service:str) -> str:
        user_input = ""
        if service == 'console':
            user_input = input('\n\33[42m' + "User:" + '\33[0m' + " ")
        return user_input

    def __elevenlabs_generate(self, text:str, voice:str, model:str, filename:str='output.mp3'):
        audio = generate(
                 text=text,
                 voice=voice,
                 model=model
                )
        save(audio, filename)

    def __voicevox_generate(self, text:str, speaker_id:int=1, filename:str='output.wav'):
        voicevox_url = getenv("VOICEVOX_URL", "http://localhost:50021")

        # COEIROINK uses /v1/predict endpoint instead of /audio_query and /synthesis
        # Check if we're using COEIROINK (port 50032) or VOICEVOX (port 50021)
        if ':50032' in voicevox_url:
            # COEIROINK API - uses JSON body, not query params
            payload = {
                'text': text,
                'speakerUuid': '3c37646f-3881-5374-2a83-149267990abc',  # Tsukuyomi-chan UUID
                'styleId': speaker_id,
                'prosodyDetail': [],
                'speedScale': 1.0,
                'volumeScale': 1.0,
                'pitchScale': 0.0,
                'intonationScale': 1.0,
                'prePhonemeLength': 0.1,
                'postPhonemeLength': 0.1,
                'outputSamplingRate': 24000
            }
            response = requests.post(
                f"{voicevox_url}/v1/predict",
                json=payload,
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()
            with open(filename, 'wb') as f:
                f.write(response.content)
        else:
            # VOICEVOX API (original)
            params = {'text': text, 'speaker': speaker_id}
            query = requests.post(f"{voicevox_url}/audio_query", params=params)
            query.raise_for_status()
            synthesis = requests.post(f"{voicevox_url}/synthesis", params={'speaker': speaker_id}, json=query.json())
            synthesis.raise_for_status()
            with open(filename, 'wb') as f:
                f.write(synthesis.content)

    def __recognise_speech(self, service:str, duration:float) -> str:
        with self.mic as source:
            print('(Start listening)')
            self.recogniser.adjust_for_ambient_noise(source, duration=duration)
            audio = self.recogniser.listen(source)
            print('(Stop listening)')

            result = ""
            try:
                if service == 'whisper':
                    result = self.__whisper_sr(audio)
                elif service == 'google':
                    result = self.recogniser.recognize_google(audio)
            except Exception as e:
                print(f"Exeption: {e}")
        return result

    def __whisper_sr(self, audio) -> str:
        with open('speech.wav', 'wb') as f:
            f.write(audio.get_wav_data())
            audio_file = open('speech.wav', 'rb')
            transcript = openai.Audio.transcribe(model="whisper-1", file=audio_file)
        return transcript['text']



def main():
    w = Waifu()
    w.initialize(user_input_service='console', 
                 chatbot_service='test', 
                 tts_service='google', output_device=8)

    w.conversation_cycle()

    #while True:
    #    w.conversation_cycle()

if __name__ == "__main__":
    main()