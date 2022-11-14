# numeric packages
import glob
import os
import time
from io import BytesIO
from pathlib import Path

import abbreviate
import numpy as np
import pandas as pd
import requests
import seaborn as sns
from IPython.display import clear_output
from matplotlib import pyplot as plt
from PIL import Image
from skimage import io

sns.set_style("whitegrid", {'axes.grid': False})

GOOGLE_API_KEY = 'AIzaSyD5xV6b4K0oKs5VChZQSj2temmOeg-oCIE'
abbr = abbreviate.Abbreviate()


def load_locations(path):
    '''
    This function loads csv files for which each line is contains information on the 
    location of an image to be acquired from Google Maps.
    '''
    grid_locations_df = pd.read_csv(path + "/sample_locations_raster_25km.csv")
    print("Grid samples: %d." % (len(grid_locations_df)))
    columns = ["lon", "lat", "grid-i", "grid-j", "class"]

    locations = grid_locations_df[columns]

    return locations


# def construct_static_url(latlon, zoom=17, imgsize=(500, 500),
#                          maptype="roadmap", imgformat="jpeg"):
#     center = "%2.5f,%2.5f" % latlon if type(latlon) == tuple else latlon
#     return construct_googlemaps_url_request(
#         center=center,
#         zoom=zoom,
#         imgsize=imgsize,
#         maptype=maptype,
#         imgformat=imgformat,
#         apiKey=GOOGLE_API_KEY)
# def construct_googlemaps_url_request(center=None, zoom=None, imgsize=(500, 500),
#                                      maptype="roadmap", apiKey="", imgformat="jpeg"):
#     # base URL, append query params, separated by &
#     request = "http://maps.google.com/maps/api/staticmap?"
#     if center is not None:
#         request += "center=%s&" % center.replace(" ", "+")
#     if zoom is not None:
#         # zoom 0 (all of the world scale ) to 22 (single buildings scale)
#         request += "zoom=%d&" % zoom
#     if apiKey is not None:
#         request += "key=%s&" % apiKey
#     request += "size=%dx%d&" % imgsize  # tuple of ints, up to 640 by 640
#     request += "format=%s&" % imgformat
#     # roadmap, satellite, hybrid, terrain
#     request += "maptype=%s&sensor=false" % maptype
#     return request


def get_static_google_map(response, filename=None, crop=False):

    # check for an error (no image at requested location)
    if 'x-staticmap-api-warning' in response.headers.keys():
        return None

    try:
        img = Image.open(BytesIO(response.content))
    except IOError:
        # print error (or it may return a image showing the error"
        print("IOError:")
        return None
    else:
        img = np.asarray(img.convert("RGB"))

    # there seems not to be any simple way to check for the gray error image
    # that Google throws when going above the API limit -- so here's a hack.
    if (img == 224).sum() / float(img.size) > 0.95:
        return None

    # remove the Google watermark at the bottom of the image
    if crop:
        img_shape = img.shape
        img = img[:int(img_shape[0]*0.85), :int(img_shape[1]*0.85)]

    if filename is not None:
        basedir = os.path.dirname(filename)
        if not os.path.exists(basedir) and basedir not in ["", "./"]:
            os.makedirs(basedir)
        io.imsave(filename, img)
    return img


def get_static_map_image(center=None, zoom=17, imgsize=(500, 500), maptype="satellite", imgformat="jpeg", max_tries=2,
                         filename=None, crop=False):
    numTries = 0
    while numTries < max_tries:
        numTries += 1
        size = '{}x{}'.format(imgsize[0], imgsize[1])
        center = '{},{}'.format(center[0], center[1])
        url = "https://maps.googleapis.com/maps/api/staticmap?center={}&maptype={}&zoom={}&size={}&format={}&key={}".format(
            center, maptype, zoom, size, imgformat, GOOGLE_API_KEY)
        response = requests.request("GET", url, headers={}, data={})
    # try:
        img = get_static_google_map(response, filename=filename, crop=crop)
        if img is not None:
            return img
    # except:
            # print("Error! Trying again (%d/%d) in 5 sec"%(numTries, max_tries))
            # time.sleep(5)
    return None


def download_images(locations, prefix="", out_path="./"):
    if not out_path.exists():
        out_path.mkdir()

    global n_requests

    for i, r in locations.iterrows():
        clear_output(wait=True)
        print("Pulling image %d/%d... (# API requests = %d)" %
              (i, len(locations), n_requests))
        label, lat, lon, grid_i, grid_j = r['class'], r['lat'], r['lon'], r['grid-i'], r['grid-j']

        basename = "%s/%s/%s_z%d_%2.5f_%2.5f" % (
            str(out_path), label, prefix, ZOOM, lat, lon)
        if not np.isnan(grid_i) and not np.isnan(grid_j):
            cur_filename = "%s_grid-i%d_grid-j%d.jpg" % (
                basename, grid_i, grid_j)
        else:
            cur_filename = "%s.jpg" % basename
        print(cur_filename)

        if os.path.exists(cur_filename):
            continue

        # req = construct_static_url((lat, lon), maptype="satellite", zoom=ZOOM, imgsize=(
        #     int(img_size*1.18), int(img_size*1.18)))
        img = get_static_map_image((lat, lon), maptype="satellite", zoom=ZOOM, imgsize=(int(
            img_size*1.18), int(img_size*1.18)), filename=cur_filename, max_tries=MAX_TRIES, crop=True)

        if img is None or n_requests >= MAX_REQUESTS:
            print("API requests quota exceeded!")
            break
        n_requests += 1

        # display samples every now and then
        if i % 100 == 0:
            plt.imshow(img)
            plt.title("image %d (label = %s)" % (i, label))
            plt.show()
            time.sleep(5)


if __name__ == "__main__":
    outPath = Path("./extracted-data")
    if not outPath.exists():
        outPath.mkdir()
    locations_path = Path("./processed-data")

    # grid_location_path = str(locations_path / "*/sample_locations_raster_25km.csv")
    # grid_location_files = glob.glob(grid_location_path)
    # print(grid_location_files)
    # more_location_path = str(locations_path / "*/additional_sample_locations.csv")
    # more_location_files = glob.glob(more_location_path)
    # print(more_location_files)

    locations = {}
    for path in locations_path.iterdir():
        locations[path.name] = load_locations(str(path))

    print(locations.keys())

    MAX_REQUESTS = 1
    MAX_TRIES = 2
    img_size = 224
    ZOOM = 17

    n_requests = 0

    # path to save data
    extraction_path = Path("./extracted-data/imagery/")
    if not extraction_path.exists():
        extraction_path.mkdir()

    # download data for all cities from data
    for city, city_locations in locations.items():
        out_path = extraction_path / city
        download_images(city_locations, prefix=city.split(',')[0], out_path=out_path)
    # print(n_requests)

    # get_static_map_image test
    # get_static_map_image(center=(37.8891505835, 23.4384444463), filename='./test.jpg')
    # get_static_map_image(center=(37.8891505835, 23.4384444463), filename='./test_cropped.jpg', crop=True)