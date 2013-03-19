#!/usr/bin/bash

# minimodem --rx 300 --ascii --stopbits 2 -a -q

while read LINE; do
    echo $LINE
    curl -X POST "http://localhost:5000/create" --data-urlencode "data=$LINE";
    sleep 1;
done
