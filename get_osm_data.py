import math
import osmnx as ox

# TODO get OpenStreetMap data for each image
# https://stackoverflow.com/questions/69174361/how-to-extract-street-graph-or-network-from-openstreetmap/69377396

# TODO check what the below code does
# if we can use it to get the coordinates of the corners of the image
# and then ask for the network data using the bounding box they represent

TileSize = 128
OriginX =  TileSize / 2
OriginY =  TileSize / 2
PixelsPerLonDegree = TileSize / 360.0
PixelsPerLonRadian = TileSize / (2 * math.pi)


def degrees_to_radians(deg):
    return deg * math.pi / 180.0

def radians_to_degrees(rads):
    return rads * 180.0 / math.pi

def bound(value, min_val, max_val):
    value = min([value, max_val])
    return max([value, min_val])

# From Lat, Lon to World Coordinate X, Y. I'm being explicit in assigning to
# X and Y properties.
def mercator(latitude, longitude):
    siny = bound(math.sin(degrees_to_radians(latitude)), -.9999, .9999)

    x = OriginX + longitude*PixelsPerLonDegree
    y = OriginY + .5 * math.log((1 + siny) / (1 - siny)) * -PixelsPerLonRadian

    return x, y

# //From World Coordinate X, Y to Lat, Lon. I'm being explicit in assigning to
# //Latitude and Longitude properties.
def inverse_mercator(x, y):

    lon = (x - OriginX) / PixelsPerLonDegree
    latRadians = (y - OriginY) / -PixelsPerLonRadian
    lat = radians_to_degrees(math.atan(math.sinh(latRadians)))

    return lat, lon


def get_bounds(center, zoom, mapWidth, mapHeight):
    scale = math.pow(2, zoom)

    centerWorld = mercator(center[0], center[1])
    centerPixel = (centerWorld[0] * scale, centerWorld[1] * scale)

    NEPixel = (centerPixel[0] + mapWidth / 2.0, centerPixel[1] - mapHeight / 2.0)
    SWPixel = (centerPixel[0] - mapWidth / 2.0, centerPixel[1] + mapHeight / 2.0)
    # NWPixel = (centerPixel[0] - mapWidth / 2.0, centerPixel[1] - mapHeight / 2.0)
    # SEPixel = (centerPixel[0] + mapWidth / 2.0, centerPixel[1] + mapHeight / 2.0)

    NEWorld = (NEPixel[0] / scale, NEPixel[1] / scale)
    SWWorld = (SWPixel[0] / scale, SWPixel[1] / scale)
    # NWWorld = (NWPixel[0] / scale, NWPixel[1] / scale)
    # SEWorld = (SEPixel[0] / scale, SEPixel[1] / scale)

    NELatLon = inverse_mercator(NEWorld[0], NEWorld[1])
    SWLatLon = inverse_mercator(SWWorld[0], SWWorld[1])
    # NWLatLon = inverse_mercator(NWWorld[0], NWWorld[1])
    # SELatLon = inverse_mercator(SEWorld[0], SEWorld[1])

    # return NWLatLon, NELatLon, SELatLon, SWLatLon
    return NELatLon, SWLatLon

if __name__ == "__main__":
    
    # # get graph frome center and distance
    # G = ox.graph_from_point((37.88915, 23.43844), dist=500, network_type='all')
    # ox.plot_graph(G, save=True, filepath='test.jpg')

    # result = get_bounds((37.88915, 23.43844), 17, 512, 512)
    # north = result[0][0]
    # south = result[1][0]
    # east = result[0][1]
    # west = result[1][1]

    # print(result)

    # # get graph from bounding box
    # G = ox.graph_from_bbox(north, south, east, west, network_type='all')
    # G_projected = ox.project_graph(G)
    # ox.plot_graph(G_projected)

    import srtm
    geo_elevation_data = srtm.get_data()
    image = geo_elevation_data.get_image((500, 500), (45, 46), (13, 14), 300)
    # the image s a standard PIL object, you can save or show it:
    image.show()