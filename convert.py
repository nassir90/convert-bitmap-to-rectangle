#!/usr/bin/python3

import zlib
import cv2
import base64
from matplotlib import pyplot as plt
import json
import numpy as np

ann_dir = "ann"
class_map = {} # Bitmap ID : Rectangle ID
image_metas = [json.load(path) for path in os.listdir(ann_dir)]

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
