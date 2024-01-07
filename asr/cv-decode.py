import os
import requests
import pandas as pd
from tqdm import tqdm
import logging
import signal

# Configure logging to write to a file
logging.basicConfig(filename='output_log/transcription_log.txt', level=logging.INFO)

# ASR API URL
asr_api_url = "http://localhost:8001/asr"

# Global variables for tracking progress and storing DataFrames
dfs = []
processed_files = []
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
def process_audio_dataset(dataset_path, input_csv_path, output_csv_path):
    global processed_files
    global dfs

    # Set up signal handler
    signal.signal(signal.SIGINT, signal_handler)

    # Read input CSV to DataFrame
    input_df = pd.read_csv(input_csv_path)

    # Check if CSV file exists, and if so, load it
    if os.path.isfile(output_csv_path):
        logging.info(f"CSV file '{output_csv_path}' found. Resuming from the last checkpoint.")
        output_df = pd.read_csv(output_csv_path)
        if "generated_text" in output_df.columns:
            processed_files = list(output_df[output_df["generated_text"].notnull()]["filename"])
        else:
            processed_files = []
    else:
        logging.info(f"CSV file '{output_csv_path}' not found. Starting from scratch.")
        processed_files = []

    # Iterate through audio files in the dataset folder
    for _, row in tqdm(input_df.iterrows(), desc="Processing files", total=len(input_df),unit="file"):
        filename = row["filename"]
        if filename.endswith(".mp3") and filename not in processed_files:
            audio_file_path = f"{dataset_path}/{filename}"  # Update with the correct path

            transcription, duration = transcribe_audio(audio_file_path)

            # Create a DataFrame for the current row
            df_row = pd.DataFrame(
                [[
                    filename,
                    row.text,
                    row.up_votes,
                    row.down_votes,
                    row.age,
                    row.gender,
                    row.accent,
                    duration,
                    transcription,
                    ]],
                columns=[
                    "filename",
                    "text",
                    "up_votes",
                    "down_votes",
                    "age",
                    "gender",
                    "accent",
                    "duration",
                    "generated_text"
                    ]
                    )

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
    audio_data_path = "data/common_voice/cv-valid-dev"
    input_csv_path = "data/common_voice/cv-valid-dev.csv"
    output_csv_path = "asr/cv-valid-dev.csv"

    # Testing
    # audio_data_path = "data/common_voice/cv-valid-dev"
    # input_csv_path = "data/common_voice/cv-valid-dev-test.csv"
    # output_csv_path = "asr/cv-testing.csv"

    # Process audio dataset
    process_audio_dataset(audio_data_path,input_csv_path,output_csv_path)
    logging.info("Job Complete")
