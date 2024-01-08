#!/bin/bash

set -x

source ~/.bashrc
source activate $CONDA_ENV_NAME

echo "PWD: $PWD"

cd ..

echo "PWD: $PWD"

# Instructions for user
# echo "================================================================================================================================================"
# echo "After seeing the messages 'Application startup complete' for the FASTAPI UvicornWorkers,
# pls proceed to use FASTAPI Swagger UI to test the Upload json file feature /api/v1/model/upload/ endpoint at http://localhost:8080/docs"
# echo "You may also use the CURL command to use the FAST API /api/v1/model/predict endpoint for batch inference"
# echo "================================================================================================================================================"

# gunicorn vits_fastapi.main:APP -b 0.0.0.0:8080 -w $NUM_WORKERS -k uvicorn.workers.UvicornWorker --timeout $TIMEOUT_DURATION
# gunicorn lightspeed_fastapi.main:APP -b 0.0.0.0:8080 -w 4 -k uvicorn.workers.UvicornWorker --timeout 90
gunicorn -w 4 -k uvicorn.workers.UvicornWorker asr.asr_api:app --bind 0.0.0.0:8001 --timeout=300

## Alternatively:
# bash vits_fastapi.sh $INPUT_FILE $OUTPUT_FILE $PRED_MODEL_UUID $PRED_MODEL_PATH


# bash vits_fastapi.sh $INPUT_FILE $OUTPUT_BASE_DIR $PRED_MODEL_UUID $PRED_MODEL_PATH
# bash vits_fastapi.sh /home/aisg/lightspeed/src/vits/10_test.txt /home/aisg/lightspeed/src/outputs/vits_fastapi_output.json 7251ac3655934299aad4cfebf5ffddbe /home/aisg/lightspeed/conf/base/pipelines_test_fastapi_docker.yaml
