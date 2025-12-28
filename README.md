<h1 align="center"> AI Waifu </h1>


## Features

- 🎤 **Voice Interaction:** Speak to your AI waifu and get instant (almost) responses.
    - Whisper - openai's paid speech recognition.
    - Google sr - free speech recognition alternative.
    - Console - if you don't want use microphone just type prompts with your keyboard.

## Installation

To run this project, you need:
 1. Install Python 3.10.5 if you don't already have it installed.
 2. Clone the repository by running `git clone https://github.com/JarikDem-Bot/ai-waifu.git`
 3. Install the required Python packages by running `pip install -r requirements.txt` in the project directory.
 4. Create `.env` file inside the project directory and enter your API keys
    <details>
      <summary> .env template</summary>
      
      ```shell
      OPENAI_API_KEY=lm-studio
      OPENAI_API_BASE=http://localhost:1234/v1
      ELEVENLABS_API_KEY=YOUR_ELEVENLABS_KEY
      VOICEVOX_URL=http://localhost:50021
      ```
    </details>
    
 5. Install [VB-Cable](https://vb-audio.com/Cable/)
 7. Install and set [VTube Studio](https://store.steampowered.com/app/1325860/VTube_Studio/)
    <details>
      <summary>Settings: </summary>
      
      - Select `CABLE Output` as microphone. Select `Preview microphone audio` to hear waifu's answers

        <img src='https://github.com/JarikDem-Bot/ai-waifu/assets/73791422/a38f8b45-44f3-4b4d-9626-2f3c812b8ba2' width='50%'>
        
      - Select input and output for `Mouth Open`. Optionally you can set "breathing" to get idle movents.

        <img src='https://github.com/JarikDem-Bot/ai-waifu/assets/73791422/4e7341b1-91a8-48f9-94e4-b5669163c89b' width='50%'>

    </details>


 9. Select your required settings in `main.py` in `waifu.initialize`
     <details>
      <summary>Arguments: </summary>
      
      - `user_input_service` (str) - the way to interact with Waifu
          - `"whisper"` - OpenAI's whisper speech to text service; paid, requires OpanAi API key.
          - `"google"` - free google speech to text service.
          - `"console"` - type your promt in console with text (absoulutely free).
          - `None` or unspecified - default value is `"whisper"`.
      - `stt_duration` (float) - the maximum number of seconds that it will dynamically adjust the threshold for before returning. This value should be at least 0.5 in order to get a representative sample of the ambient noise. Default value is `0.5`.
      - `mic_index` (int) - index of the device to use for audio input. If `None` or unspecified will use default microphone.

      - `chatbot_service` (str) - service that will generate responses
          - `"openai"` - OpenAI text generation servise; paid, requires OpanAi API key.
          - `"test"` - returns prewritten message; used as dummy text for developement to reduce time and cost of testings.
          - `None` or unspecified - default value is `"openai"`.
      - `chatbot_model` (str) - model used for text generation. List of available models you can find [here](https://platform.openai.com/docs/models/overview). Default value is `"gpt-3.5-turbo"`.
      - `chatbot_temperature` (float) - determines creativity of the generated text. A higher value leads to more creative result. A lower value leads to less creative and more similar results. Default value is `0.5`.
      - `personality_file` (str) - relative path to txt file with waifu's description. Default value is `"personality.txt"`.
        
      - `tts_service` (str) - service that "reads" Waifu's responses
          - `"google"` - free Google's tts, voice feels very "robotic".
          - `"elevenlabs"` - ElevenLabs tts with good quality; paid, requires ElevenLabs API key.
          - `"console"` - output will be printed in console (free).
          - `"voicevox"` - download voicevox engine [here](https://github.com/VOICEVOX/voicevox_engine/releases) for japanese voice
          - `None` or unspecified - default value is `"google"`.
      - `output_device` - (int) output device ID or (str) output device name substring. If VB-Cable is used, you need to find device, that will start with `CABLE Input (VB-Audio Virtual` using `sd.query_devices()` command. 
      - `tts_voice` (str) - ElevenLabs voice name. Default value is `"Elli"`.
      - `tts_model` (str) - ElevenLabs model. Recommended values are `"eleven_monolingual_v1"` and `"eleven_multilingual_v1"`. Default value is `"eleven_monolingual_v1"`.

    </details>

    
 10. Run the project by executing `python main.py` in the project directory.

<br>

> <picture>
>   <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Mqxx/GitHub-Markdown/main/blockquotes/badge/light-theme/warning.svg">
>   <img alt="Warning" src="https://raw.githubusercontent.com/Mqxx/GitHub-Markdown/main/blockquotes/badge/dark-theme/warning.svg">
> </picture><br>
>
> Depending on the selected input mode, program may send all recorded sounds or other data to the 3-rd parties such as: Google (stt, tts), OpenAI (stt, text generation), ElevenLabs (tts).
