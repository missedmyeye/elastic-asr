import os
import requests
import pandas as pd
from tqdm import tqdm
import logging
import signal

# Configure logging to write to a file
logging.basicConfig(filename='transcription_log-testing.txt', level=logging.INFO)

# ASR API URL
asr_api_url = "http://localhost:8001/asr"

# Global variables for tracking progress and storing DataFrames
dfs = []
processed_files = 0
checkpoint_interval = 100  # Save checkpoint every 100 files

# Function to transcribe audio using ASR API
def transcribe_audio(file_path):
    try:
        with open(file_path, "rb") as file:
            files = {"file": (os.path.basename(file_path), file)}
            response = requests.post(asr_api_url, files=files)
            result = response.json()
            return result.get("transcription", ""), result.get("duration", 0)
    except requests.RequestException as e:
        logging.error(f"Failed to transcribe audio {file_path}. Error: {str(e)}")
        save_checkpoint(remove_last_entry=True)  # Trigger save_checkpoint on API request failure
        pass
    except Exception as e:
        logging.error(f"An unexpected error occurred while transcribing audio {file_path}. Error: {str(e)}")
        pass

# Function to handle signal interruption (e.g., connection loss)
def signal_handler(signum, frame):
    logging.warning("Received signal: Saving checkpoint and exiting.")
    save_checkpoint()
    exit(1)

# Save checkpoint and clear dfs
def save_checkpoint(remove_last_entry=False):
    global processed_files
    global dfs

    # Save the DataFrame to CSV
    if dfs:
        if remove_last_entry:
            # Remove the last entry in dfs
            dfs.pop()
        if os.path.isfile(output_csv_path):
            df = pd.concat(dfs, ignore_index=True)
            df.to_csv(output_csv_path, mode='a', header=False, index=False)
        else:
            df = pd.concat(dfs, ignore_index=True)
            df.to_csv(output_csv_path, index=False)
            # df.to_csv(output_csv_path, index=False)

    # Clear the list of DataFrames
    dfs = []

# Function to process audio dataset and update CSV
def process_audio_dataset(dataset_path, output_csv_path):
    global processed_files
    global dfs

    # Set up signal handler
    signal.signal(signal.SIGINT, signal_handler)

    # Check if CSV file exists, and if so, load it
    if os.path.isfile(output_csv_path):
        logging.info(f"CSV file '{output_csv_path}' found. Resuming from the last checkpoint.")
        df = pd.read_csv(output_csv_path)
        processed_files = list(df["filename"])
        # tqdm_init = len(processed_files)
    else:
        logging.info(f"CSV file '{output_csv_path}' not found. Starting from scratch.")
        processed_files = []
        # tqdm_init = 0

    # Iterate through audio files in the dataset folder
    # for filename in tqdm(os.listdir(dataset_path), desc="Processing files", unit="file", initial=tqdm_init):
    for filename in tqdm(os.listdir(dataset_path), desc="Processing files", unit="file"):
        if filename.endswith(".mp3") and filename not in processed_files:
            audio_file_path = os.path.join(dataset_path, filename)
            transcription, duration = transcribe_audio(audio_file_path)

            # Create a DataFrame for the current row
            df_row = pd.DataFrame([[dataset_path,filename, transcription, duration]], columns=["directory","filename", "generated_text", "duration"])

            # Append the DataFrame to the list
            dfs.append(df_row)

            # Increment the processed files counter
            processed_files.append(filename)

            # Log the processed file
            logging.info(f"Processed {filename} - Duration: {duration}s - Transcription: {transcription}")

            # Save checkpoint every checkpoint_interval files
            if len(processed_files) % checkpoint_interval == 0:
                save_checkpoint()
        else:
            logging.info(f"{filename} exists in current dataset and will not be processed.")

    # Save the final checkpoint
    save_checkpoint()

if __name__ == "__main__":
    logging.info("Job Start")
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
    logging.info("Job Complete")
