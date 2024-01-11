#!/bin/bash

set -x

source ~/.bashrc
source activate $CONDA_ENV_NAME

echo "PWD: $PWD"

cd ..

echo "PWD: $PWD"

# Instructions for user
echo "============================================================================================="
echo "After seeing the messages 'Application startup complete' for the FASTAPI UvicornWorkers,
pls proceed to test the server is running with 'curl http://localhost:8001/ping'
You should receive a pong response"
echo "You may also use the CURL command for inference: 
'curl -F file=@path/to/sample-000000.mp3 http://localhost:8001/asr'"
echo "============================================================================================="

gunicorn -w 2 -k uvicorn.workers.UvicornWorker asr.asr_api:app --bind 0.0.0.0:8001 --timeout=300
