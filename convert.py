#!/usr/bin/python3

import zlib
import getopt
import cv2
import base64
from matplotlib import pyplot as plt
import json
import numpy as np
import os
import sys
import re

options, remainder = getopt.getopt(sys.argv[1:], "d:m:C:", ["ann-dir=", "class-map-file="])

ann_dir = "ann"
class_map = {}

for option, argument in options:
    if option in ("-d", "--ann-dir"):
        ann_dir = argument
    elif option == "-m":
        source, destination = argument.split("=")
        class_map[source] = destination
    elif option in ("-C", "--class-map-file"):
        class_map_file = open(argument)
        for mapping in class_map_file:
            source, destination = mapping.split("=")
            destination = re.sub("#.*$", "", destination)
            class_map[source] = destination.strip()

print(class_map)

image_metas = [json.load(open(os.path.join(ann_dir, path))) for path in os.listdir(ann_dir)]

def base64_2_mask(s):
    z = zlib.decompress(base64.b64decode(s))
    n = np.fromstring(z, np.uint8)
    mask = cv2.imdecode(n, cv2.IMREAD_UNCHANGED)[:, :, 3].astype(bool)
    return mask

for image_meta in image_metas:
    for obj in image_meta["objects"]:
        if obj["geometryType"] == "bitmap":
            bitmap = obj["bitmap"]
            mask = base64_2_mask(bitmap["data"])
            print(mask.shape)
