#!/usr/bin/env bash

for LINE in `cat test.log`; do
    echo $LINE
    curl -X POST "http://localhost:5000/create" -d "data=$LINE";
    sleep 1;
done
