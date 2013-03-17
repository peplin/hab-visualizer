#!/usr/bin/env python
"""Visualize live GPS track"""

import sys

class InvalidMessage(Exception): pass

class HABMessage(object):
    KEYS = ["callsign", "message_count", "latitude", "longitude",
            "altitude", "crc"]

    def __init__(self, data):
        self._fields = data.split(",")
        if len(self._fields) != 6:
            raise InvalidMessage()
        # TODO check crc

    def __getattr__(self, name):
        return self._fields[self.KEYS.index(name)]

def visualize(input_stream, **kwargs):
    for line in input_stream:
        if not line.startswith("$$"):
            continue

        message = HABMessage(line)
        print("%f, %f @ %fm" % (float(message.latitude),
                float(message.longitude),
                float(message.altitude)))


if __name__ == '__main__':
    visualize(sys.stdin)
