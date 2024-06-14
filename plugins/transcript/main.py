import os
import tempfile
import multiprocessing
import requests
import speech_recognition as sr
from pydub import AudioSegment
from concurrent.futures import ThreadPoolExecutor
from nara.extra import TimeIt
from dotenv import get_key

def download_audio(url, temp_dir):
    response = requests.get(url)
    if response.status_code == 200:
        file_path = os.path.join(temp_dir, "audio_file")
        with open(file_path, "wb") as f:
            f.write(response.content)
        return file_path
    else:
        raise Exception(f"Failed to download audio file from URL: {url}")

def transcribe_segment(audio_segment_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_segment_path) as source:
        recognizer.adjust_for_ambient_noise(source)
        audio_data = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.RequestError as e:
        return f"API request error: {e}"
    except sr.UnknownValueError:
        return "*"

def transcribe_audio(file_path, segment_duration=30):
    audio = AudioSegment.from_file(file_path)


    with tempfile.TemporaryDirectory() as temp_dir:
        segments = []
        for i in range(0, len(audio), segment_duration * 1000):
            segment = audio[i:i + segment_duration * 1000]
            segment_path = os.path.join(temp_dir, f"segment_{i//1000}.wav")
            segment.export(segment_path, format='wav')
            segments.append(segment_path)

        def get_thread_cnt():
            cpu = multiprocessing.cpu_count()
            cpu = max(1, int(get_key(".env", "MAX_THREADS")))
            return cpu

        max_workers = get_thread_cnt()

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            transcriptions = list(executor.map(transcribe_segment, segments))

    transcription = " ".join(transcriptions)
    return transcription



def transcriptAudio(audio_source:str, is_url=False) -> str:
    """
    Parameters
    ----------
    audio_source : str
        The audio source to transcribe.
    is_url : bool, optional
        Whether the audio source is a URL, by default False

    Returns
    -------
    str
        The transcription of the audio source.
    """
    if is_url:
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = download_audio(audio_source, temp_dir)
            transcription = transcribe_audio(file_path)
    else:
        transcription = transcribe_audio(audio_source)

    return transcription




@TimeIt
def main(audio_source, is_url=False):
    if is_url:
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = download_audio(audio_source, temp_dir)
            transcription = transcribe_audio(file_path)
    else:
        transcription = transcribe_audio(audio_source)
    
    print(transcription)

if __name__ == "__main__":
    # Example usage:
    # audio_url = "https://github.com/AssemblyAI-Examples/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3"

    local_file_path = r"C:\Users\Divyansh\Desktop\YT\Ai\plugins\transcript\ttsMP3.com_VoiceText_2024-6-14_16-30-38.mp3"

    # For URL
    # main(audio_url, is_url=True)

    # print("-"*100)

    # # For local file
    main(local_file_path, is_url=False)

