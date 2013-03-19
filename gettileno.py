import math
import pprint
import time
import os
import urllib2
from collections import defaultdict

def fetch_tile(zoom, tile):
    target_filepattern = "static/images/tiles/%s"
    filename = "%d/%d/%d.png" % (zoom, tile[0], tile[1])
    folder = os.path.dirname(target_filepattern % filename)
    try:
        os.makedirs(folder)
    except OSError:
        pass

    if not os.path.exists(target_filepattern % filename):
        print "Fetching %s" % filename
        d = urllib2.urlopen('http://a.tile.osm.org/%s' % filename)
        with open(target_filepattern % filename, 'w') as output_file:
            output_file.write(d.read())
        time.sleep(.1)
    else:
        print "Already have %s" % filename

tiles = defaultdict(set)

# original
# 39.836 to 40.213
# -119.272 to -118.601

#new
# 39.934 to 40.685
# -117.459 to -116.116

# relaly new
# 39.6995 to  39.5099
# -117.0425 to -116.7067
min_latitude = 39.5099
max_latitude = 39.6995
latitude = min_latitude

min_longitude = -117.0425
max_longitude = -116.7067

while latitude <= max_latitude:
    longitude = min_longitude
    while longitude <= max_longitude:
        for zoom in range(9, 16, 1):
            n = pow(2, zoom)
            latitude_rad = math.radians(latitude)
            x = n * ((longitude + 180) / 360)
            y = n * (1 - (math.log(math.tan(latitude_rad) +
                    (1 / math.cos(latitude_rad))) / math.pi)) / 2
            tile = (int(x), int(y))
            if tile not in tiles[zoom]:
                fetch_tile(zoom, tile)
                tiles[zoom].add(tile)
        longitude += .001
    latitude += .001

pprint.pprint(tiles)
print("%d tiles" % len(tiles))

