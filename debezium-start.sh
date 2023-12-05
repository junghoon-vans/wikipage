#!/usr/bin/env bash

# Create Mapping
curl -i -X PUT -H "Accept:application/json" -H  "Content-Type:application/json" http://localhost:9200/posts -d @debezium/config/posts.json

# Start Elasticsearch connector
curl -i -X POST -H "Accept:application/json" -H  "Content-Type:application/json" http://localhost:8083/connectors/ -d @debezium/config/es-sink.json

# Start PostgreSQL connector
curl -i -X POST -H "Accept:application/json" -H  "Content-Type:application/json" http://localhost:8083/connectors/ -d @debezium/config/source.json
