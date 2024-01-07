import os
import requests
import pandas as pd
from tqdm import tqdm
import logging

# Configure logging to write to a file
logging.basicConfig(filename='transcription_log.txt', level=logging.INFO)

# ASR API URL
asr_api_url = "http://localhost:8001/asr"

# Function to transcribe audio using ASR API
def transcribe_audio(file_path):
    with open(file_path, "rb") as file:
        files = {"file": (os.path.basename(file_path), file)}
        response = requests.post(asr_api_url, files=files)
        result = response.json()
        return result.get("transcription", ""), result.get("duration", 0)

# Function to process audio dataset and update CSV
def process_audio_dataset(dataset_path, output_csv_path):
     # Initialize an empty list to store DataFrames
    dfs = []

    # Iterate through audio files in the dataset folder
    for filename in tqdm(os.listdir(dataset_path), desc="Processing files", unit="file"):
        if filename.endswith(".mp3"):
            audio_file_path = os.path.join(dataset_path, filename)
            transcription, duration = transcribe_audio(audio_file_path)

            # Create a DataFrame for the current row
            df_row = pd.DataFrame([[dataset_path,filename, transcription, duration]], columns=["directory","filename", "generated_text", "duration"])

            # Append the DataFrame to the list
            dfs.append(df_row)

            logging.info(f"Processed {filename} - Duration: {duration}s - Transcription: {transcription}")

    # Concatenate all DataFrames in the list
    # Note: pd.DataFrame.append has been deprecated, docs suggested pd.concat is more efficient.
    df = pd.concat(dfs, ignore_index=True)

    # Save the DataFrame to CSV
    df.to_csv(output_csv_path, index=False)

if __name__ == "__main__":
    # Specify the path to the audio dataset and the output CSV file
    # Setting relative path, assuming that code is run from repo parent folder htx-asr
    #TODO Pend transfer to configs if time allows
    audio_data_path = "data/common_voice/cv-valid-dev/cv-valid-dev"
    output_csv_path = "asr/cv-valid-dev.csv"

    # Testing
    # audio_data_path = "data/common_voice/cv-testing"
    # output_csv_path = "asr/cv-testing.csv"

    # Process audio dataset
    process_audio_dataset(audio_data_path, output_csv_path)
