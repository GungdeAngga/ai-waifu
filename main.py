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
                    output_device=17, #5, 17 for pc 10 for handheld
                    tts_voice=3,
                    tts_model = None
                    )

    while True:
        waifu.conversation_cycle()

if __name__ == "__main__":
    main()