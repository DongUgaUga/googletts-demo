import google.cloud.texttospeech as tts
import google.cloud.texttospeech as tts
import sounddevice as sd
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLETTS_API_KEY")
if not api_key:
    raise ValueError("환경변수 'GOOGLETTS_API_KEY'가 설정되지 않았습니다.")

PROJECT_ID = "winection-project"

# TTS type 리스트 확인
def list_voices(language_code=None):
    client = tts.TextToSpeechClient(client_options={"api_key": api_key, "quota_project_id": PROJECT_ID})
    response = client.list_voices(language_code=language_code)
    voices = sorted(response.voices, key=lambda voice: voice.name)

    print(f" Voices: {len(voices)} ".center(60, "-"))
    for voice in voices:
        languages = ", ".join(voice.language_codes)
        name = voice.name
        gender = tts.SsmlVoiceGender(voice.ssml_gender).name
        rate = voice.natural_sample_rate_hertz
        print(f"{languages:<8} | {name:<24} | {gender:<8} | {rate:,} Hz")

list_voices("ko")

# TTS 생성값 설정
def text_to_speech_with_api_key(voice_name, text):
    try:
        # Google TTS 클라이언트를 생성하며, API 키와 프로젝트 ID를 전달합니다.
        client = tts.TextToSpeechClient(client_options={"api_key": api_key, "quota_project_id": PROJECT_ID})

        # 입력된 음성 이름(voice_name)을 기반으로 언어 코드를 추출합니다.
        language_code = "-".join(voice_name.split("-")[:2])

        # TTS 입력 텍스트를 설정합니다.
        text_input = tts.SynthesisInput(text=text)

        # 음성 선택 파라미터를 설정합니다 (언어 코드 및 음성 이름).
        voice_params = tts.VoiceSelectionParams(
            language_code=language_code, name=voice_name
        )

        # 오디오 생성 설정을 LINEAR16 형식으로 설정합니다.
        audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16)

        # TTS API를 호출하여 음성을 생성합니다.
        response = client.synthesize_speech(
            input=text_input,
            voice=voice_params,
            audio_config=audio_config,
        )

        # 생성된 오디오 데이터를 가져옵니다.
        audio_content = response.audio_content

        # 오디오 데이터를 NumPy 배열로 변환합니다.
        audio_array = np.frombuffer(audio_content, dtype=np.int16)

        # 오디오를 재생합니다.
        sd.play(audio_array, samplerate=24000)
        sd.wait()

    except Exception as e:
        # 오류 발생 시 에러 메시지를 출력합니다.
        print("Google TTS Error: ", e)

# 함수 호출 예제: TTS로 음성을 생성하고 출력합니다.
text_to_speech_with_api_key("ko-KR-Wavenet-D", "안녕하세요! 구글 티티에스 입니다!")