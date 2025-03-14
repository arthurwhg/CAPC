import whisper
import torch
import glob
import os

print(torch.backends.mps.is_available()) 

print(f"Transcribing audio files...")
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
#device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
model = whisper.load_model("base")  # "small", "medium", "large" available
#model.to(device).half()

audioFolder = f"{ROOT_DIR}/data/tmp"


def getFileList(audioFolder):
    
    files = sorted([f for f in glob.glob(f"{audioFolder}/*.mp3") if os.path.isfile(f)])
    return files

audio_chunks = getFileList(audioFolder)
print(f"total {len(audio_chunks)} audio files to be transcribed")
transcripts = []
for chunk in audio_chunks:
    print(f"Transcribing {chunk}...")
    result = model.transcribe(chunk)
    text = result["text"]
    #print(f"{chunk}:{text}: {len(text)}")
    transcripts.append(result["text"])

# Combine transcripts
#final_transcript = "\n".join(transcripts)
#print(final_transcript)
#print(f"total characters {len(final_transcript)}")

print(f"creating task file...")
taskfile=f"{ROOT_DIR}/data/tasks/task_correction.jsonl"
url= "/v1/chat/completions"
method = "POST"
model = "gpt-4o-mini"
system_content = """I got following transcript from audio but found some Homophones & Misheard errors. Would you please correct errors according to the Bible content and return the corrected transcript in the original format. Please ignore both header and footer part."""
id = 0
with open(taskfile, "w", encoding="utf-8") as f:
    for line in transcripts:
        f.write(f'{{"method":"POST","url":"/v1/chat/completions","body":{{"model":"gpt-4o-mini","messages":[{{"role":"system","content":"{system_content}"}},{{"role":"user","content":"{line}"}}]}},"custom_id":"cid-{id}"}}\n')
        id += 1

f.close()

