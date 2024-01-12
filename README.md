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