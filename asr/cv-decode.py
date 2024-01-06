import os
import requests
import pandas as pd

# ASR API URL
asr_api_url = "http://localhost:8001/asr"

# Function to transcribe audio using ASR API
def transcribe_audio(file_path):
    with open(file_path, "rb") as file:
        files = {"file": (os.path.basename(file_path), file)}
        response = requests.post(asr_api_url, files=files)
        result = response.json()
        return result.get("transcription", ""), result.get("duration", 0)

# Function to process Common Voice dataset and update CSV
def process_common_voice(dataset_path, output_csv_path):
    # Initialize an empty DataFrame
    df = pd.DataFrame(columns=["filename", "generated_text", "duration"])

    # Iterate through audio files in the dataset folder
    for filename in os.listdir(dataset_path):
        if filename.endswith(".mp3"):
            audio_file_path = os.path.join(dataset_path, filename)
            transcription, duration = transcribe_audio(audio_file_path)

            # Append information to the DataFrame
            df = df.append({"filename": filename, "generated_text": transcription, "duration": duration}, ignore_index=True)

            print(f"Processed {filename} - Duration: {duration}s - Transcription: {transcription}")

    # Save the DataFrame to CSV
    df.to_csv(output_csv_path, index=False)

if __name__ == "__main__":
    # Specify the path to the Common Voice dataset and the output CSV file
    common_voice_path = "/path/to/common_voice/cv-valid-dev"
    output_csv_path = "/path/to/output/generated_text.csv"

    # Process Common Voice dataset
    process_common_voice(common_voice_path, output_csv_path)
