import math
import pprint
import time
import os
import urllib2

def fetch_tile(tile):
    target_filepattern = "static/images/%s"
    filename = "%d/%d/%d.png" % (tile[0], tile[1], tile[2])
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

tiles = set()

# 39.836 to 40.213
# -119.272 to -118.601
min_latitude = 39.836
max_latitude = 40.213
latitude = min_latitude

min_longitude = -119.272
max_longitude = -118.601

while latitude <= max_latitude:
    longitude = min_longitude
    while longitude <= max_longitude:
        for zoom in range(5, 15, 1):
            n = pow(2, zoom)
            latitude_rad = math.radians(latitude)
            x = n * ((longitude + 180) / 360)
            y = n * (1 - (math.log(math.tan(latitude_rad) +
                    (1 / math.cos(latitude_rad))) / math.pi)) / 2
            tile = (zoom, int(x), int(y))
            if tile not in tiles:
                fetch_tile(tile)
                tiles.add(tile)
        longitude += .001
    latitude += .001

pprint.pprint(tiles)
print("%d tiles" % len(tiles))

