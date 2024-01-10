FROM docker.elastic.co/elasticsearch/elasticsearch:7.15.2

# Copy custom elasticsearch.yml to the container
COPY elasticsearch.yml /usr/share/elasticsearch/config/elasticsearch.yml
