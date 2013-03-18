import math
import pprint
import time

tiles = set()

# 39.836 to 40.213
# -119.272 to -118.601
min_latitude = 38.836
max_latitude = 41.213
latitude = min_latitude

min_longitude = -120.272
max_longitude = -117.601
longitude = min_longitude

while latitude <= max_latitude:
    while longitude <= max_longitude:
        for zoom in range(5, 18, 1):
            n = pow(zoom, 2)
            latitude_rad = math.radians(latitude)
            x = n * ((longitude + 180) / 360)
            y = n * (1 - (math.log(math.tan(latitude_rad) +
                    (1 / math.cos(latitude_rad))) / math.pi)) / 2
            tiles.add((zoom, int(x), int(y)))
        longitude += .1
    latitude += .1

pprint.pprint(tiles)
print("%d tiles" % len(tiles))

for tile in tiles:
    print('http://a.tile.osm.org/%d/%d/%d.png' % tile)
    time.sleep(1)
