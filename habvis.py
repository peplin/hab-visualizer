#!/usr/bin/env python
"""Visualize live GPS track"""

import sys
from threading import Thread
import time
from socketio import socketio_manage
from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin, BroadcastMixin
from werkzeug.exceptions import NotFound
from gevent import monkey

from flask import Flask, Response, request, render_template, url_for, redirect

monkey.patch_all()

app = Flask(__name__)
app.debug = True

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


class HABNamespace(BaseNamespace, BroadcastMixin):
    listeners = []

    def recv_disconnect(self):
        self.disconnect(silent=True)

    # TODO recv_connect doesn't seem to work, so I defined a user event
    def on_connect(self):
        self.listeners.append(self)

def read_stdin(callback):
    while True:
        with open("test.log", 'r') as log:
            where = log.tell()
            line = log.readline()
            if not line:
                time.sleep(1)
                log.seek(where)
            else:
                callback(line)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create', methods=['POST'])
def create():
    name = request.form.get("name")
    if len(HABNamespace.listeners) > 0:
        # is there a better way to broadcast? we seem to need a reference to
        # just any old client
        HABNamespace.listeners[0].broadcast_event('position',
                request.form['data'])
    return Response()


@app.route('/socket.io/<path:remaining>')
def socketio(remaining):
    try:
        socketio_manage(request.environ, {'/track': HABNamespace}, request)
    except:
        app.logger.error("Exception while handling socketio connection",
                         exc_info=True)
    return Response()


if __name__ == '__main__':
    app.run()
