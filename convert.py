import zlib
import getopt
import base64
import json
import numpy as np
import cv2
import os
from os.path import join
import sys
import glob
import re

def convert(options):
    root_dir = options["project_dir"]
    dataset = options["dataset"]
    project_meta_path = join(root_dir, "/meta.json")
    output_basename = options["output_dir"]

    title_map = {}

    if options["map_file"]:
        title_map = parse_title_map(options["map_fie"])

    with open(meta_path) as meta_file:
        meta_json = json.load(meta_file)

    id_map = generate_id_map(title_map, meta_json)
                
    if not dataset:
        dataset = os.path.dirname(glob.glob(join(root_dir, "*/ann"))[0])

    ann_dir = join(dataset, "ann")
    output_dir = join(dataset, output_basename)
    
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    image_meta_paths = glob.glob(join(ann_dir, "*"))
    image_metas = [(image_meta_path, json.load(open(image_meta_path))) for image_meta_path in image_meta_paths]

    with open("filter") as images_filter:
        valid_pahts = json.load(images_filter)

    for image_meta_path, image_meta in image_metas:
        image_meta_basename = os.path.basename(image_meta_path)
        for obj in image_meta["objects"]:
            if obj["geometryType"] == image_meta_path in valid_paths:
                bitmap = obj["bitmap"]
                height, width = base64_2_mask(bitmap["data"]).shape
                rectangle = {
                    "classId" : id_map[obj["classId"]][0],
                    "geometryType" : "rectangle",
                    "labelerLogin" : obj["labelerLogin"],
                    "tags" : obj["tags"],
                    "classTitle" : id_map[obj["classId"]][1],
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
        output_file = open(join(output_dir, image_meta_basename), "w")
        json.dump(image_meta, output_file, indent=4)

def parse_title_map(title_map_path: str):
    title_map = {}
    with open(title_map_path) as id_map:
        for mapping in id_map:
            source_title, destination_title = mapping.split("=")
            destination_title = re.sub("#.*$", "", destination_title).strip()
            title_map[source_title] = destination_title
    return title_map

def generate_id_map(title_map: dict, meta: dict):
    id_map = {}
    for source in title_map:
        destination = title_map[source]
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
        id_map[source_id] = (destination_id, destination)

# See: https://legacy.docs.supervise.ly/ann_format/#bitmap
def base64_2_mask(s):
    z = zlib.decompress(base64.b64decode(s))
    n = np.fromstring(z, np.uint8)
    mask = cv2.imdecode(n, cv2.IMREAD_UNCHANGED)[:, :, 3].astype(bool)
    return mask

