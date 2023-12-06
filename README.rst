========
Wikipage
========

Wikipage is a simple wiki page built with FastAPI and Svelte.

How to run
==========

1. Run docker-compose to start containers

.. code:: bash

    export DEBEZIUM_VERSION=1.8.1.Final
    docker-compose up

2. Check the debezium and elasticsearch containers are up

This project uses debezium to capture changes in the database and elasticsearch to index the changes.
So, It is required to check the containers are up and configure the debezium connector.

.. code:: bash

    ❯ curl -H "Accept:application/json" localhost:8083/
    {"version":"3.0.0","commit":"8cb0a5e9d3441962","kafka_cluster_id":"1andHvG1Qy-3FVz8lWJYZA"}%

.. code:: bash

    ❯ curl http://localhost:9200

    {
      "name" : "50fd72fdb6ff",
      "cluster_name" : "docker-cluster",
      "cluster_uuid" : "JnRmQtcUSMahO_4j3nw-7Q",
      "version" : {
        "number" : "7.0.0",
        "build_flavor" : "default",
        "build_type" : "docker",
        "build_hash" : "b7e28a7",
        "build_date" : "2019-04-05T22:55:32.697037Z",
        "build_snapshot" : false,
        "lucene_version" : "8.0.0",
        "minimum_wire_compatibility_version" : "6.7.0",
        "minimum_index_compatibility_version" : "6.0.0-beta1"
      },
      "tagline" : "You Know, for Search"
    }

3. Run debezium-start.sh to configure debezium connector

.. code:: bash

    ./debezium-start.sh

4. Launch the web

Open ``http://localhost`` in your browser.
