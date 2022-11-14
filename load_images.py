# numeric packages
import glob
import re
from pathlib import Path

import abbreviate
import numpy as np
import pandas as pd
import seaborn as sns
from IPython.display import clear_output, display
from matplotlib import pyplot as plt
from skimage.io import imread
from skimage.transform import resize

sns.set_style("whitegrid", {'axes.grid': False})

GOOGLE_API_KEY = 'AIzaSyD5xV6b4K0oKs5VChZQSj2temmOeg-oCIE'
abbr = abbreviate.Abbreviate()


def split_str(s, target_len=12):
    s = re.sub('[^A-Za-z0-9% ]+', '', s)
    words = s.split(" ")
    words = [abbr.abbreviate(w, target_len=target_len).capitalize()
             for w in words]
    if len(words) == 1:
        return s  # + "\n"
    if len(words) > 4:
        words = words[:3] + [words[-1]]
    else:
        words = words[:4]
    return " ".join(words[:(len(words)/2)]) + "\n" + " ".join(words[(len(words)/2):])


def plot_examples(images, labels, classes=None,
                  nExamples=10, thumbSize=(50, 50), title="example"):
    # build example canvas
    clustLabels = np.unique(labels)
    nClusters = clustLabels.size
    canvas = np.zeros((thumbSize[0]*nClusters, nExamples*thumbSize[1], 3))
    for i, c in enumerate(clustLabels):
        cur_class_samples = np.where(labels == c)[0]
        idx = np.random.choice(cur_class_samples, replace=False, size=min(
            [nExamples, len(cur_class_samples)]))
        for j in range(len(idx)):
            img = images[idx[j], :, :, :3]
            img = resize(img, thumbSize)
            canvas[i*thumbSize[0]:(i+1)*thumbSize[0],
                   j*thumbSize[1]:(j+1)*thumbSize[1]] = img

    # plot examples of each class
    fig, ax = plt.subplots(1, figsize=(12, 10))
    plt.tight_layout()
    print(canvas.shape)
    ax.imshow(canvas.swapaxes(0, 1))  # , aspect='auto')
    ax.set_title(title, fontsize=18)
    ax.set_ylabel("-- examples --", fontsize=16)
    ax.set_xlabel("-- land classes --", fontsize=16)
    # Turn off tick labels
    if classes is None:
        classes = clustLabels
    ax.set_xticks([thumbSize[0]*(0.5 + x) for x in range(nClusters)])
    ax.set_xticklabels(classes, fontsize=16, rotation=90)
    ax.set_yticklabels([])
    # plt.axis("off")
    plt.show()


def create_dataframe(path):
    files = np.array(glob.glob(str(path)))
    files = np.array([Path(file) for file in files])
    files_df = pd.DataFrame(files).rename(columns={0: "filename"})
    # get class name from filename
    files_df['class'] = files_df['filename'].apply(lambda x: x.parent.name)
    # get city name from filename
    files_df['city'] = files_df['filename'].apply(lambda x: x.parent.parent.name)

    return files_df

if __name__ == "__main__":

    # read image files to dataframe
    jpg_path = Path("./extracted-data/imagery/") / Path('*/*/*.jpg')

    files_df = create_dataframe(jpg_path)
    # print(files_df.head())

    # plot examples of each class
    n_samples = 5

    # sel_df = files_df.groupby("class").apply(lambda x: x.sample(n_samples))
    sel_df = files_df.head(5)

    # read image files
    files_df['image'] = files_df['filename'].apply(imread).values
    images = np.array(sel_df['filename'].apply(imread).values.tolist())
    # labels = sel_df['class'].apply(split_str)
    labels = sel_df['class']

    plot_examples(images, labels, nExamples=5, thumbSize=(
        50, 50), title="Urban Atlas Dataset: Examples")
