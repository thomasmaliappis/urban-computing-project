# urban-computing-project

<!-- TODO
add google create key link
add dataset source
add dataset analysis (class pie chart)
add plot image
network description
-->

# Dataset
The dataset used is [Urban Atlas dataset](https://land.copernicus.eu/local/urban-atlas/urban-atlas-2018?tab=download). The processed-data used were provided in this [GitHub project](https://github.com/adrianalbert/urban-environments).

A simple analysis of the dataset can be found in [dataset_analysis.ipynb](./download_images.py)
# Process
Google Static Maps API is used to download satellite images for the given locations. ([download_images.py](./download_images.py))

In order to use this API you need to create a google api key using these [instructions](https://developers.google.com/maps/documentation/javascript/get-api-key).

After downloading the satellite images we resample each image. ([read_and_resample.ipynb](./read_and_resample.ipynb))

The resampled images are used to train our neural network. ([download_images.py](./network.ipynb))