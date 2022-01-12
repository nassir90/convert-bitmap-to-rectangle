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

options, remainder = getopt.getopt(sys.argv[1:], "d:C:", ["root-dir=", "class-map-file="])

root_dir = "."
meta_path = root_dir + "/meta.json"
output_basename = "new_ann"
name_mappings = {}

for option, argument in options:
    if option in ("-d", "--root-dir"):
        root_dir = argument
        meta_path = os.path.join(root_dir, "meta.json")
    elif option in ("-C", "--class-map-file"):
        class_map_file = open(argument)
        for mapping in class_map_file:
            source, destination = mapping.split("=")
            destination = re.sub("#.*$", "", destination).strip()
            name_mappings[source] = destination

meta = json.load(open(meta_path))

mappings = {}

for source in name_mappings:
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
            
dataset = os.path.dirname(glob.glob(os.path.join(root_dir, "*/ann"))[0])
ann_dir = os.path.join(dataset, "ann")
output_dir = os.path.join(dataset, output_basename)
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

image_meta_paths = os.listdir(ann_dir)
image_metas = [(path, json.load(open(os.path.join(ann_dir, path)))) for path in image_meta_paths]

# See: https://legacy.docs.supervise.ly/ann_format/#bitmap
def base64_2_mask(s):
    z = zlib.decompress(base64.b64decode(s))
    n = np.fromstring(z, np.uint8)
    mask = cv2.imdecode(n, cv2.IMREAD_UNCHANGED)[:, :, 3].astype(bool)
    return mask

for path, image_meta in image_metas:
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
            image_meta["objects"].append(rectangle)
    output_file = open(os.path.join(output_dir, path), "w")
    json.dump(image_meta, output_file, indent=4)
