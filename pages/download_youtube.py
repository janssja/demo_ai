import streamlit as st
from pytube import YouTube
import os
from tempfile import TemporaryDirectory
import subprocess  # Import subprocess for calling ffmpeg
from whisper import split_and_process_audio, make_summary
import time

def app():
    st.title("YouTube Video's downloaden en samenvatten")

    video_url = st.text_input("Voer de URL van de YouTube-video in:")

    if st.button("Video downloaden en samenvatten"):
        if not video_url:
            st.error("Voer een geldige YouTube-video-URL in.")
        else:
            with st.spinner("Downloaden..."):
                try:
                    yt = YouTube(video_url)
                    stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
                    audio_stream = yt.streams.filter(only_audio=True).order_by('bitrate').desc().first()
                    video_duration = yt.length
                    if stream:
                        with TemporaryDirectory() as tmpdirname:
                            # Download de video in de tijdelijke directory
                            stream.download(output_path=tmpdirname)
                            video_path = os.path.join(tmpdirname, stream.default_filename)
                            st.success("Download voltooid!")
                            st.video(video_path)
                            if not audio_stream:
                                logging.error("Geen audio stream gevonden.")
                            else:
                                st.info("Downloading audio stream...")
                                # Generate a unique filename without specifying .mp3 extension
                                filename = f"downloaded_audio_{yt.video_id}.{audio_stream.mime_type.split('/')[1]}"  # e.g., "downloaded_audio_video123.webm"
                                # Download the audio stream
                                audio_stream.download(filename=filename)
                                
                                # Define the output filename with .mp3 extension
                                output_filename = f"downloaded_audio_{yt.video_id}.mp3"

                                # Convert the audio to MP3 using ffmpeg
                                # Placeholder for progress
                                progress_placeholder = st.empty()
                                progress_placeholder.progress(0)

                                start_time = time.time()

                                process = subprocess.Popen([
                                    'ffmpeg', '-y', '-i', filename, '-vn', '-ar', '44100', '-ac', '2', '-b:a', '192k',
                                    '-f', 'mp3', output_filename
                                ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

                                while True:
                                    output = process.stdout.readline()
                                    if output == '' and process.poll() is not None:
                                        break
                                    if output:
                                        current_time = time.time()
                                        elapsed_time = current_time - start_time
                                        progress = min(int((elapsed_time / video_duration) * 100), 100)
                                        progress_placeholder.progress(progress)
                                
                                # Ensure progress reaches 100% at the end
                                progress_placeholder.progress(100)

                                # Remove the original downloaded file
                                os.remove(filename)
                                st.success(f"Audio downloaded and converted to {output_filename}")  # Display a success message
                                if output_filename:
                                    with st.spinner('Video bekijken en samenvatten ...'):
                                        transcription = split_and_process_audio(output_filename, 120000)
                                        if transcription:  # Check if transcription is not None or empty
                                            st.title("Transcriptie")
                                            st.write(transcription)
                                            summary = make_summary(transcription, "Nederlands")
                                            if summary:
                                                st.title("Samenvatting")
                                                st.write(summary)
                                        else:
                                            st.error("Transcription failed, cannot create summary.")
                    else:
                        st.error("Kon geen downloadbare video vinden.")
                except Exception as e:
                    st.error(f"Er is een fout opgetreden: {e}")