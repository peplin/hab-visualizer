#!/usr/bin/env python
"""Visualize live GPS track"""

import sys
import thread
import time
from socketio.server import SocketIOServer
from socketio import socketio_manage
from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin
from gevent import monkey

monkey.patch_all()

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
    def recv_disconnect(self):
        self.disconnect(silent=True)

    # TODO recv_connect doesn't seem to work, so I defined a user event
    def on_connect(self):
        self.request['listeners'].append(self)

def read_stdin(callback):
    while True:
        time.sleep(1);
        callback("$$KB3TLD,1,2,3,4,5,*CRC16")
    # for line in sys.stdin:
        # callback(line)

class Application(object):
    def __init__(self):
        self.request = {
            'listeners': []
        }

        self.input_handler = thread.start_new_thread(read_stdin,
                [self.new_message])

    def new_message(self, data):
        for listener in self.request['listeners']:
            listener.broadcast_event('position', data)
            # is there a better way to broadcast? we seem to need a reference to
            # just any old client
            break

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO'].strip('/')

        if not path:
            path = 'index.html'

        if path.startswith('static/') or path == 'index.html':
            try:
                data = open(path).read()
            except Exception:
                return not_found(start_response)

            if path.endswith(".js"):
                content_type = "text/javascript"
            elif path.endswith(".css"):
                content_type = "text/css"
            elif path.endswith(".swf"):
                content_type = "application/x-shockwave-flash"
            else:
                content_type = "text/html"

            start_response('200 OK', [('Content-Type', content_type)])
            return [data]

        if path.startswith("socket.io"):
            socketio_manage(environ, {'': HABNamespace}, self.request)
        else:
            return not_found(start_response)

def not_found(start_response):
    start_response('404 Not Found', [])
    return ['<h1>Not Found</h1>']

if __name__ == '__main__':
    print 'Listening on port 8080 and on port 843 (flash policy server)'
    SocketIOServer(('0.0.0.0', 8080), Application(),
        resource="socket.io", policy_server=True,
        policy_listener=('0.0.0.0', 10843)).serve_forever()
