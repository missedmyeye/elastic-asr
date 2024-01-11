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

## Pre-requisites

## ASR Inference API

## Dataset Information/Analysis

## Dataset Processing

## Elasticsearch Backend (Dataset Indexing)

## Search UI Frontend

## Cloud Deployment (AWS)

## Future Improvements/Considerations
### Config files
The file paths and directory paths in the scripts provided, as well as other values such as index name, host addresses are mostly written directly into the code. For more accessible modification and configuration, I would have preferred to use config files to input these values.
### Exploratory Data Analysis
The Common Voice dataset that was used in this repository, although open-source, was found to have some issues during implementation, such as null values in features like age/accent/gender. A better EDA conducted would have allowed for better handling of the data and fewer issues to debug.
### Authentication for API connections
Currently the connections to the APIs and containers are not authenticated for ease of testing and debugging, however this poses as a security risk if running in production, as they are currently easily accessible to public. Hence set up of authentication via API keys or restricting access to specific IP addresses would be good.