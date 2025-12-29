from waifu import Waifu

def main():
    waifu = Waifu()

    waifu.initialize(user_input_service='console',
                     stt_duration = None,
                     mic_index = None,

                    chatbot_service='openai',
                    chatbot_model = None,
                    chatbot_temperature = None,
                    personality_file = None,

                    tts_service='voicevox',
                    output_device=21, #CABLE Input (VB-Audio Virtual Cable), Windows DirectSound
                    tts_voice=0, # つくよみちゃん (Tsukuyomi-chan) - れいせい (Calm) - COEIROINK voice
                    tts_model = None
                    )

    while True:
        waifu.conversation_cycle()

if __name__ == "__main__":
    main()