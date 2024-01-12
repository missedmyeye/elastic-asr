# ASR Dataset Inference and Search Pipeline
## Table of Contents
- Overview
- Pre-requisites
- ASR Inference API
- Dataset Information/Analysis
- Dataset Processing
- Elasticsearch Backend (Dataset Indexing)
- Search UI Frontend
- Cloud Deployment (AWS)
- Future Improvements/Considerations

## Overview
This repository is a step by step process to set up an API for Speech-To-Text inference (and dockerize it), then run an audio dataset through it to obtain the generated transcriptions and durations of the files and update the dataset's manifest. Subsequently, there are scripts provided to index the manifest into an Elasticsearch backend, set up a Search UI frontend to access this information, and also to deploy this service onto cloud.
## Prerequisites
This repository is run and tested on MacOS Sonoma 14.2.1 with Apple M2 Chip (ARM64/Aarch64 architecture).<br>
Min. 8GB RAM<br>
Other requirements:<br>
- Docker engine ([Rancher Desktop](https://rancherdesktop.io/) was used)<br>
- [Miniconda](https://docs.conda.io/projects/miniconda/en/latest/)
- [Homebrew (For MacOS/Linux)](https://brew.sh/)
- Node.js (v18.19.0)
    ```bash
    brew install node@18
    ```
    Run `node -v` to check on your version. If you get a response `node: command not found`, run the command provided when you install node@18:<br>
    ```
    If you need to have node@18 first in your PATH, run:
    echo 'export PATH="/opt/homebrew/opt/node@18/bin:$PATH"' >> ~/.zshrc
    ```
- yarn (Install after Node.js)
    ```
    npm install --global yarn
    ```
## ASR Inference API
### Environment Setup (For running locally)
Navigate to `/asr` and install via Miniconda or PIP. Uncomment the tensorflow packages in `requirements.txt` if using MacOS
```bash
$ conda env create -f environment.yml
OR
$ conda env create -n asr_api_env python=3.10
$ pip install -r requirements.txt

$ conda activate asr_api_env
```
Install `ffmpeg`
```bash
brew install ffmpeg
```
### Download dataset
Go back to the repository folder and create a folder `data`
```bash
cd ..
# You should be in /htx-asr
mkdir data
```
Download the dataset into this folder `data`. It should have the following folder structure:<br>
The key things to have are `cv-valid-dev` folder and `cv-valid-dev.csv`
```
/data
└── common_voice
    ├── cv-invalid
    │   └── cv-invalid
    ├── cv-other-dev
    │   └── cv-other-dev
    ├── cv-other-test
    │   └── cv-other-test
    ├── cv-other-train
    │   └── cv-other-train
    ├── cv-testing
    ├── cv-valid-dev
    │   └── cv-valid-dev
    ├── cv-valid-test
    │   └── cv-valid-test
    ├── cv-valid-train
    │   └── cv-valid-train
    ├── LICENSE.txt
    ├── README.txt
    ├── cv-valid-dev-backup.csv
    ├── cv-valid-test.csv
    ├── cv-other-dev.csv
    ├── cv-other-train.csv
    ├── cv-valid-dev-test.csv
    ├── cv-valid-dev.csv
    ├── cv-valid-train.csv
    ├── cv-invalid.csv
    └── cv-other-test.csv
```
### Running locally
Make sure you are in `/htx-asr` folder before running the API. Otherwise, adjust your paths accordingly. (e.g. if in `asr` folder, then change `asr.asr_api:app` to `asr_api:app`)<br>
If you have a larger RAM feel free to adjust `-w 2` to a higher value.
```bash
gunicorn -w 2 -k uvicorn.workers.UvicornWorker asr_api:app --bind 0.0.0.0:8001 --timeout=300
```
### Running docker image
Build and run the Docker image, update version numbers as you see fit:
```bash
docker build --platform=linux/arm64 -t asrapi:1.0.12 ./asr
docker run -p 8001:8001 asrapi:1.0.12
```
### Testing API and running inference
Open another terminal and ping to check if the server is up:
```bash
curl http://localhost:8001/ping
>>> {"response":"pong"}
```
To run inference on a single file, here is an example:
```bash
curl -F file=@data/common_voice/cv-valid-dev/cv-valid-dev/sample-000000.mp3 http://localhost:8001/asr
>>> {"transcription":"BE CAREFUL WITH YOUR PROGNOSTICATIONS SAID THE STRANGER","duration":5.064}
```
To run inference on a dataset:<br>
    Before running, please take note of the following:
    1. Make sure the filepaths `audio_data_path`, `input_csv_path` and `output_csv_path` in `cv-decode.py` are accurate.<br>
    2. If running locally, please comment out line 37 of `asr_api.py`, if not your audio file will be deleted. (`os.remove(temp_wav_path)`)
```bash
python -m asr.cv-decode
```
You should receive an output `cv-valid-dev.csv` in folder `/asr`, which should appear while the process is running as it is updating at regular intervals. **Should the process be interrupted halfway, just run it again without removing any files as there are measures implemented to resume from where it left off.**
## Dataset Information/Analysis

## Dataset Processing

## Elasticsearch Backend (Dataset Indexing)

## Search UI Frontend

## Cloud Deployment (AWS)

## Future Improvements/Considerations
### Config files
The file paths and directory paths in the scripts provided, as well as other values such as index name, host addresses are mostly written directly into the code. For more accessible modification and configuration, I would have preferred to use config files to input these values.
### Catering to Multiple Chip Architectures
I wanted to test my code locally as well as via Docker images, hence in the interest of time I had to replicate them as closely as possible. As a result some of the details in the code are specified to cater to the Aarch64 chip architecture, for Macbooks with M1/M2/M3 chips. If you encounter any issues with regards to Docker image building you may need to adjust some of the code before using it, especially if your setup is using x86-64 (Windows) chip. Some installations are also named differently (aarch64 instead of arm64 and vice versa) so do take note as well.
### Exploratory Data Analysis
The Common Voice dataset that was used in this repository, although open-source, was found to have some issues during implementation, such as null values in features like age/accent/gender. A better EDA conducted would have allowed for better handling of the data and fewer issues to debug.
### Authentication for API connections
Currently the connections to the APIs and containers are not authenticated for ease of testing and debugging, however this poses as a security risk if running in production, as they are currently easily accessible to public. Hence set up of authentication via API keys or restricting access to specific IP addresses would be good.