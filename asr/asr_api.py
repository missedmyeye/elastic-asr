from fastapi import FastAPI, File, UploadFile
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
from fastapi.responses import JSONResponse
import librosa
import torch
import io
import os
from pydub import AudioSegment
import logging

app = FastAPI()

# Load pre-trained model and processor
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h")
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-960h")

@app.get("/ping")
def ping():
    return {"response": "pong"}

@app.post("/asr")
async def transcribe_audio(file: UploadFile = File(...)):
    try:
        # Use pydub to load and convert the audio to WAV format
        audio_data = AudioSegment.from_file(io.BytesIO(file.file.read()), format="mp3")

        # Save the converted audio to a temporary WAV file
        temp_wav_path = "/tmp/temp_audio.wav"
        audio_data.export(temp_wav_path, format="wav")

        # Load the converted WAV audio using librosa
        audio_input, rate = librosa.load(temp_wav_path, sr=16000, mono=True)
        print(audio_input)
        print(rate)

        # Remove the temporary WAV file
        os.remove(temp_wav_path)

        # Close uploaded file
        await file.close()
        current_directory = os.getcwd()
        result = search_file(current_directory, file.filename)

        if result:
            logging.info(f"File found at: {result}")
            # Confirm file exists
            if os.path.exists(result):
                logging.info("Delete uploaded file.")
                os.remove(result)
            else:
                logging.info("File does not exist, check filepath.")
            if os.path.exists(result):
                logging.info("File failed to delete.")
            else:
                logging.info("File deleted successfully.")
        else:
            logging.info("File not found in the specified directory.")

    except Exception as e:
        return JSONResponse(content={"error": f"Failed to load audio: {e}"}, status_code=500)


    # Model inference
    input_values = processor(audio_input, return_tensors="pt", sampling_rate=16000).input_values
    logits = model(input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.batch_decode(predicted_ids)[0]
    logging.info(transcription)

    # Duration calculation
    duration = len(audio_input) / rate

    return {"transcription": transcription, "duration": duration}

def search_file(directory, filename):
    # Walk through the directory and its subdirectories
    for root, dirs, files in os.walk(directory):
        # Check if the filename is in the list of files
        if filename in files:
            # Return the full path to the file
            return os.path.join(root, filename)

    # If the file is not found, return None
    return None