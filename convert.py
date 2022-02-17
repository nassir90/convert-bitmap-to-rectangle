import zlib
import getopt
import base64
import json
import numpy as np
import cv2
import os
import sys
import glob
import re

options, remainder = getopt.getopt(sys.argv[1:], "hd:m:D:", ["--help", "root-dir=", "mappings=","dataset="])

root_dir = "."
project_meta_path = root_dir + "/meta.json"
dataset = ""
output_basename = "new_ann"
name_mappings = {}

for option, argument in options:
    if option in ("-h", "--help"):
        print(open("help").read())
        quit()
    elif option in ("-d", "--root-dir"):
        root_dir = argument
        project_meta_path = os.path.join(root_dir, "meta.json")
    elif option in ("-D", "--dataset"):
        dataset = argument
    elif option in ("-m", "--mappings"):
        name_map_file = open(argument)
        for mapping in name_map_file:
            source, destination = mapping.split("=")
            destination = re.sub("#.*$", "", destination).strip()
            name_mappings[source] = destination

project_meta = json.load(open(project_meta_path))

mappings = {}

for source in name_mappings:
    source_id = ""
    destination_id = ""
    for klass in project_meta["classes"]:
        if klass["title"] == source:
            source_id = klass["id"]
            break
    for klass in project_meta["classes"]:
        if klass["title"] == destination:
            destination_id = klass["id"]
            break
    mappings[source_id] = (destination_id, destination)
            
if not dataset: dataset = os.path.dirname(glob.glob(os.path.join(root_dir, "*/ann"))[0])
ann_dir = os.path.join(dataset, "ann")
output_dir = os.path.join(dataset, output_basename)
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

image_meta_paths = glob.glob(os.path.join(ann_dir, "*"))
image_metas = [(image_meta_path, json.load(open(image_meta_path))) for image_meta_path in image_meta_paths]

# See: https://legacy.docs.supervise.ly/ann_format/#bitmap
def base64_2_mask(s):
    z = zlib.decompress(base64.b64decode(s))
    n = np.fromstring(z, np.uint8)
    mask = cv2.imdecode(n, cv2.IMREAD_UNCHANGED)[:, :, 3].astype(bool)
    return mask

for image_meta_path, image_meta in image_metas:
    image_meta_basename = os.path.basename(image_meta_path)
    for obj in image_meta["objects"]:
        if obj["geometryType"] == "bitmap":
            bitmap = obj["bitmap"]
            height, width = base64_2_mask(bitmap["data"]).shape
            rectangle = {
                "classId" : mappings[obj["classId"]][0],
                "geometryType" : "rectangle",
                "labelerLogin" : obj["labelerLogin"],
                "tags" : obj["tags"],
                "classTitle" : mappings[obj["classId"]][1],
                "points" : {
                    "exterior" : [
                        bitmap["origin"],
                        [
                            bitmap["origin"][0] + width,
                            bitmap["origin"][1] + height,
                        ]
                    ],
                    "interior" : []
                },
                "sourceBitmap" : obj["id"] 
            }
            image_meta["objects"].append(rectangle)
    output_file = open(os.path.join(output_dir, image_meta_basename), "w")
    json.dump
    quit()(image_meta, output_file, indent=4)
