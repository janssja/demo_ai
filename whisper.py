import os
import io
import openai
from pydub import AudioSegment
from pydub.utils import make_chunks
import streamlit as st

OPENAI_API_KEY = st.secrets["openai_api_key"]
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def split_and_process_audio(audio_file_path, chunk_length_ms):
    print("Splitting audio file into chunks")
    print("Audio file path: ", audio_file_path)
    print("Chunk length: ", chunk_length_ms)
    # Load the large audio file
    try:
        large_audio = AudioSegment.from_file(audio_file_path, format="mp3")  # Adjust the format if necessary
    except Exception as e:
        print(f"Failed to load audio file: {e}")
        print(f"Attempting to load file: {audio_file_path}")
        return None

    print("Total audio length (in ms): ", len(large_audio))
    
    if len(large_audio) < chunk_length_ms:
        print(f"Audio file is shorter than the chunk length. Consider reducing the chunk length or processing the entire file as a single chunk.")
    
    # Split audio file into chunks of the specified length
    chunks = make_chunks(large_audio, chunk_length_ms)
    progress_bar = st.progress(0)

    transcriptions = []
    print("Processing audio file ")
    print("Number of chunks: ", len(chunks))
    total_chunks = len(chunks)

    for i, chunk in enumerate(chunks):
        progress = int(100 * (i / total_chunks))
        progress_bar.progress(progress)

        print(f"Length of chunk {i}: {len(chunk)} ms")
        progress = int(100 * ((i + 1) / total_chunks))
        progress_bar.progress(progress)

        if len(chunk) < 100:  # pydub uses milliseconds
            print(f"Skipping chunk {i} because it is too short")
            continue
        # Create a temporary file for the chunk
        chunk_file_path = f"temp_chunk{i}.wav"
        chunk.export(chunk_file_path, format="wav")
        
        # Process the chunk
        print("Processing chunk", i)
        transcription = process_audio_file_txt(chunk_file_path, client)
        transcriptions.append(transcription)
        
        # Delete the temporary file
        os.remove(chunk_file_path)
    
    progress_bar.progress(100)
    # Combine transcriptions
    combined_transcription = ' '.join(transcriptions)
    return combined_transcription


def process_audio_file(audio_file, client):
    audio_file = open(audio_file, "rb")

    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="vtt",
    )

    return transcription

def translate_audio_english(audio_file, client):
    audio_file = open(audio_file, "rb")

    transcription = client.audio.translations.create(
        model="whisper-1",
        file=audio_file,
        response_format="vtt",
    )

    return transcription.text

def translate_to_any_language(text, target_language, client):
    target_language = target_language
    text = text
    messages = [
        {"role": "system", 
         "content": f"""
            I want you to act as an algorithm for translation to language {target_language}. 
            System will provide you with a text, and your only task is to translate it to {target_language}. 
            Never break character. Keep the WebVTT layout intact."""}
    ]
    messages.append({"role":"user","content": text })

    translation_res = client.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=messages,
        temperature=0.9,
    )

    return translation_res.choices[0].message.content

def create_audio_file(speech_file_path, text, client):
    text = text
    speech_file_path = speech_file_path

    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text,
    )
    response.stream_to_file(speech_file_path)

def process_audio_file_txt(audio_file, client):
    audio_file = open(audio_file, "rb")
    try: 
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text",
        )
    except Exception as e:
        print(f"An error occurred: {e}")
        print(f"Full response: {e.response.text}")  # Log the full API response
        raise

    return transcription

def make_summary(text, target_language):
    target_language = target_language
    text = text
    messages = [
        {"role": "system", 
         "content": f"""
            I want you to make a summary of {text} in {target_language}. 
            System will provide you with a text, and your only task is to make an extensive summarize it in {target_language}. 
            Never break character."""}
    ]
    messages.append({"role":"user","content": text })

    response = client.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=messages,
        temperature=0.3,
    )

    summary = response.choices[0].message.content

    return summary