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

## Alternatively:
# bash vits_fastapi.sh $INPUT_FILE $OUTPUT_FILE $PRED_MODEL_UUID $PRED_MODEL_PATH


# bash vits_fastapi.sh $INPUT_FILE $OUTPUT_BASE_DIR $PRED_MODEL_UUID $PRED_MODEL_PATH
# bash vits_fastapi.sh /home/aisg/lightspeed/src/vits/10_test.txt /home/aisg/lightspeed/src/outputs/vits_fastapi_output.json 7251ac3655934299aad4cfebf5ffddbe /home/aisg/lightspeed/conf/base/pipelines_test_fastapi_docker.yaml
