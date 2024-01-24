from elasticsearch import Elasticsearch
import pandas as pd
from tqdm import tqdm

# Function to wait for Elasticsearch to start
def wait_for_elasticsearch():
    while True:
        # Elasticsearch configuration
        es = Elasticsearch(['http://es01:9200'])
        status = es.ping()
        if status:
            print("Connected to Elasticsearch.")
            return es
        else:
            print("Connection failed.")
            raise Exception("Connection failed.")

# Wait for Elasticsearch to start before proceeding
es = wait_for_elasticsearch()

# Read CSV file
csv_file = 'cv-valid-dev.csv'
print(f'Reading CSV...{csv_file}')
df = pd.read_csv(csv_file)
# Replace null values with an empty string
# Elasticsearch is unable to parse null values
df = df.fillna('')
print(df.head())

# Set up mapping for index
index_name = 'cv-transcriptions'
mapping = {
    "mappings": {
        "properties": {
            "filename": {"type": "keyword"},
            "text": {
                "type": "text",
                "analyzer": "standard",
            },
            "up_votes": {"type": "integer"},
            "down_votes": {"type": "integer"},
            "age": {
                "type": "text",
                "analyzer": "standard",  # Age provided in text in dataset
            },
            "gender": {"type": "keyword"},
            "accent": {"type": "keyword"},
            "duration": {"type": "float"},
            "generated_text": {
                "type": "text",
                "analyzer": "standard",
                "fields": {
                    "keyword": {
                    "type": "keyword",
                    "ignore_above": 256
                    }
                    },
                # "suggest": {
                #     "type": "completion"
                #     }
                }
            }
        }
    }

# Delete the index if it exists
if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)

# Create the index with mapping
es.indices.create(index=index_name, body=mapping, ignore=400)

# Indexing function
def index_data(index_name, data_frame, es):
    for _, row in tqdm(
        data_frame.iterrows(), desc="Processing rows", total=len(data_frame), unit="row"
        ):
        document = row.to_dict()
        # print(document)
        es.index(index=index_name, body=document)
    print("Indexing complete.")

# Index data into Elasticsearch
index_data(index_name, df, es)
