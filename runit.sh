#!/usr/bin/env bash

minimodem --rx 300 --ascii --stopbits 2 -a -q | ./readmodem.sh
