import requests
from dotenv import load_dotenv
from os import getenv
import sys

# Fix encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

load_dotenv()

voicevox_url = getenv("VOICEVOX_URL", "http://localhost:50032")

print(f"Connecting to COEIROINK at {voicevox_url}\n")

# Try different endpoints
endpoints_to_try = ['/speakers', '/speaker_info', '/v1/speakers']

for endpoint in endpoints_to_try:
    try:
        print(f"Trying endpoint: {endpoint}")
        response = requests.get(f"{voicevox_url}{endpoint}")

        if response.status_code == 200:
            speakers = response.json()
            print(f"\n✓ Success! Found speakers using {endpoint}\n")

            # Debug: print raw data structure
            print("Raw data:", speakers[:1] if speakers else speakers)
            print()

            print("Available COEIROINK Voices:\n")
            print("=" * 60)

            # Handle both list and dict responses
            if isinstance(speakers, list):
                for speaker in speakers:
                    # Try different possible key names
                    name = speaker.get('speakerName', speaker.get('name', 'Unknown'))
                    speaker_uuid = speaker.get('speakerUuid', speaker.get('uuid', ''))
                    styles = speaker.get('styles', [])

                    print(f"\nSpeaker: {name}")
                    if speaker_uuid:
                        print(f"UUID: {speaker_uuid}")
                    print("-" * 60)

                    for style in styles:
                        style_name = style.get('styleName', style.get('name', 'Unknown'))
                        style_id = style.get('styleId', style.get('id', 'N/A'))
                        print(f"  Style: {style_name}")
                        print(f"  ID: {style_id}")
                        print()
            break
        else:
            print(f"  Status: {response.status_code}")
    except Exception as e:
        print(f"  Error: {e}")

print("\n" + "=" * 60)
print("\nTo test if COEIROINK is running, try accessing:")
print(f"{voicevox_url}/docs in your browser")
