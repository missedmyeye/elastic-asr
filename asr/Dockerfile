# Use an official Python runtime as a parent image, with multi-architecture support
FROM python:3.10

SHELL ["/bin/bash", "-c"]
ARG REPO_DIR="."
# Set the working directory to /app
ARG HOME_DIR="/app"
WORKDIR $HOME_DIR/asr

# Conda Environment parameters
# ENV REQ_FILE="requirements.txt"
ENV CONDA_ENV_FILE="environment.yml"
ENV REQ_FILE="requirements.txt"
ENV CONDA_ENV_NAME="asr_api_env"
ENV CONDA_HOME="/miniconda3"
ENV CONDA_BIN="$CONDA_HOME/bin/conda"
# ENV MINI_CONDA_SH="Miniconda3-py39_4.12.0-Linux-x86_64.sh"
# ENV MINI_CONDA_SH="Miniconda3-py39_4.12.0-Linux-aarch64.sh"
ENV MINI_CONDA_SH="Miniconda3-py310_23.3.1-0-Linux-aarch64.sh"

RUN touch "$HOME_DIR/.bashrc"

RUN apt-get update && \
    apt-get -y install bzip2 curl wget gcc rsync git vim locales \
    apt-transport-https ca-certificates gnupg && \
    sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=en_US.UTF-8 && \
    apt-get clean

ENV PATH $CONDA_HOME/bin:$HOME_DIR/.local/bin:$PATH
ENV PYTHONIOENCODING utf8
ENV LANG "C.UTF-8"
ENV LC_ALL "C.UTF-8"


# Install Miniconda
RUN curl -O https://repo.anaconda.com/miniconda/$MINI_CONDA_SH && \
    chmod +x $MINI_CONDA_SH && \
    ./$MINI_CONDA_SH -u -b -p $CONDA_HOME && \
    rm $MINI_CONDA_SH
ENV PATH $CONDA_HOME/bin:$HOME_DIR/.local/bin:$PATH

# Install Development Tools
RUN apt-get install -y build-essential

# Install Python3 Development Libraries
RUN apt-get install -y python3-dev

# Install ffmpeg
# RUN apt-get install -y ffmpeg
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y ffmpeg

# Copy the environment yml and requirements file into the container at /app
COPY $REPO_DIR/$CONDA_ENV_FILE $HOME_DIR/asr/$CONDA_ENV_FILE
COPY $REPO_DIR/$REQ_FILE $HOME_DIR/asr/$REQ_FILE

RUN python -m pip install --upgrade pip

# Create Conda environment
RUN $CONDA_BIN create --name $CONDA_ENV_NAME python=3.10 && \
    $CONDA_BIN run -n $CONDA_ENV_NAME conda env update -f environment.yml && \
    echo "source activate $CONDA_ENV_NAME" >> "$HOME_DIR/.bashrc"

# Copy the contents of the local asr directory into the container at /app/asr
# RUN mkdir $HOME_DIR/asr
COPY $REPO_DIR $HOME_DIR/asr

# Make port 8001 available to the world outside this container
EXPOSE 8001

# Define environment variable
ENV NAME asr-api

# Run asr_api.py with gunicorn, 4 workers, and a timeout of 300 seconds
CMD [ "/bin/bash", "./api-entrypoint.sh" ]
