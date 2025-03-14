from pydub import AudioSegment
import os

def split_audio(file_path, outputFolder,chunk_length_ms=1000):  # 300000ms = 5 minutes
    audio = AudioSegment.from_file(file_path)
    chunks = [audio[i:i+chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]

    # Save chunks
    output_files = []
    for i, chunk in enumerate(chunks):
        chunk_name = f"{outputFolder}/chunk_{i}.mp3"
        print(f"Exporting {chunk_name}...")
        chunk.export(chunk_name, format="mp3")
        output_files.append(chunk_name)

    return output_files



ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

audiofile = f"{ROOT_DIR}/data/voice.mp3"
outputFolder = f"{ROOT_DIR}/data/tmp"

audioTrunks = split_audio(audiofile,outputFolder,5*60*1000)
print(audioTrunks)