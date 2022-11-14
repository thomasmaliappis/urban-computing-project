# TODO get OpenStreetMap data for each image
# https://stackoverflow.com/questions/69174361/how-to-extract-street-graph-or-network-from-openstreetmap/69377396
import osmnx as ox

G = ox.graph_from_point((37.88915, 23.43844), dist=750, network_type='all')
ox.plot_graph(G, save=True, filepath='test.jpg')