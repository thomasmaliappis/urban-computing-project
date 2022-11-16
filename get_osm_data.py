# TODO get OpenStreetMap data for each image
# https://stackoverflow.com/questions/69174361/how-to-extract-street-graph-or-network-from-openstreetmap/69377396
import osmnx as ox

# get graph frome center and distance
G = ox.graph_from_point((37.88915, 23.43844), dist=500, network_type='all')
ox.plot_graph(G, save=True, filepath='test.jpg')

# get graph from bounding box
G = ox.graph_from_bbox(37.79, 37.78, -122.41, -122.43, network_type='drive')
G_projected = ox.project_graph(G)
ox.plot_graph(G_projected)


# TODO check what the below code does
# if we can use it to get the coordinates of the corners of the image
# and then ask for the network data using the bounding box they represent
import math
OFFSET = 268435456 # half of the earth circumference's in pixels at zoom level 21
RADIUS = OFFSET / math.pi

def get_pixel(x, y, x_center, y_center, zoom_level):
    """
    x, y - location in degrees
    x_center, y_center - center of the map in degrees (same value as in the google static maps URL)
    zoom_level - same value as in the google static maps URL
    x_ret, y_ret - position of x, y in pixels relative to the center of the bitmap
    """
    x_ret = (l_to_x(x) - l_to_x(x_center)) >> (21 - zoom_level)
    y_ret = (l_to_y(y) - l_to_y(y_center)) >> (21 - zoom_level)
    return x_ret, y_ret

def l_to_x(x):
    return int(round(OFFSET + RADIUS * x * math.pi / 180))

def l_to_y(y):
    return int(round(OFFSET - RADIUS * math.log((1 + math.sin(y * math.pi / 180)) / (1 - math.sin(y * math.pi / 180))) / 2))