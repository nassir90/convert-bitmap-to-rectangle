#!/usr/bin/python3

import zlib
import copy
import getopt
import cv2
import base64
from matplotlib import pyplot as plt
import json
import numpy as np
import os
import sys
import glob
import re

options, remainder = getopt.getopt(sys.argv[1:], "d:m:C:", ["root-dir=", "meta-file=", "class-map-file="])

root_dir = "."
meta_path = root_dir + "/meta.json"
ann_dir = ""
class_map = {}

for option, argument in options:
    if option in ("-d", "--root-dir"):
        root_dir = argument
        meta_path = os.path.join(root_dir, "meta.json")
    elif option in ("-C", "--class-map-file"):
        class_map_file = open(argument)
        for mapping in class_map_file:
            source, destination = mapping.split("=")
            destination = re.sub("#.*$", "", destination).strip()
            class_map[source] = destination

meta = json.load(open(meta_path))

mappings = {}

for source in class_map:
    source_id = ""
    destination_id = ""
    for klass in meta["classes"]:
        if klass["title"] == source:
            source_id = klass["id"]
            break
    for klass in meta["classes"]:
        if klass["title"] == destination:
            destination_id = klass["id"]
            break
    mappings[source_id] = (destination_id, destination)
            
l = os.path.join(root_dir, "*/ann")
if not ann_dir: ann_dir = glob.glob(l)[0]

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
            height, width = mask.shape
            rectangle = {}
            rectangle["classId"] = mappings[obj["classId"]][0]
            rectangle["geometryType"] = "rectangle"
            rectangle["labelerLogin"] = obj["labelerLogin"]
            rectangle["tags"] = obj["tags"]
            rectangle["classTitle"] = mappings[obj["classId"]][1]
            rectangle["points"] = {
                "exterior" : [
                    bitmap["origin"],
                    [
                        bitmap["origin"][0] + width,
                        bitmap["origin"][1] + height,
                    ]
                ],
                "interior" : []
            }
            print(rectangle)
