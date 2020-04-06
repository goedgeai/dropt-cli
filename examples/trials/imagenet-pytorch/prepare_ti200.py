"""prepare_ti200.py downloads and prepares dataset tiny-imagenet-200."""

from pathlib import Path
from tempfile import TemporaryFile
from zipfile import ZipFile
import csv
from tqdm import tqdm
import requests


# define url of dataset tiny-imagenet-200
URL = "http://cs231n.stanford.edu/tiny-imagenet-200.zip"

# define paths
ROOT = Path(".")
DATA_PATH = ROOT.joinpath("tiny-imagenet-200")
TRAIN_PATH = DATA_PATH.joinpath("train")
VAL_PATH = DATA_PATH.joinpath("val")
TEST_PATH = DATA_PATH.joinpath("test")


# download and unzip dataset
with TemporaryFile() as fp, requests.get(URL, stream=True) as rp:
    TOTAL_SIZE = int(rp.headers.get("content-length", 0))
    BLOCK_SIZE = 1024
    print("Downloading dataset tiny-imagenet-200...")
    with tqdm(total=TOTAL_SIZE, unit="iB", unit_scale=True) as t:
        for data in rp.iter_content(BLOCK_SIZE):
            t.update(BLOCK_SIZE)
            fp.write(data)

    print("Unzipping dataset...", end=" ")
    with ZipFile(fp) as zf:
        zf.extractall(ROOT)
    print("done.")


# prepare training data
print("Prepare training data...", end=" ")
for im_path in TRAIN_PATH.rglob("*.JPEG"):
    im_path.rename(im_path.parents[1].joinpath(im_path.name))
print("done.")


# prepare validating data
print("Prepare validating data...", end=" ")
CSV_PATH = next(VAL_PATH.glob("*.txt"))
with open(CSV_PATH) as csv_file:
    READER = csv.reader(csv_file, dialect="excel-tab")
    for im_info in READER:
        im_path = VAL_PATH.joinpath("images", im_info[0])
        class_path = VAL_PATH.joinpath(im_info[1])
        if not class_path.is_dir():
            class_path.mkdir()
        im_path.rename(class_path.joinpath(im_info[0]))
print("done.")


# remove extra files
print("Removing extra files...", end=" ")
for im_path in TEST_PATH.rglob("*.JPEG"):
    im_path.unlink()

for txt_path in DATA_PATH.rglob("*.txt"):
    txt_path.unlink()

for dir_path in DATA_PATH.rglob("images"):
    dir_path.rmdir()

TEST_PATH.rmdir()
print("done.\n")
