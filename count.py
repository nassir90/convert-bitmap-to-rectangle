import json
from os import listdir
import os.path.join

def count(ann_dir):
    paths = [ join(ann_dir, ann_file) for ann_file in listdir(ann_dir) ]
    for path in paths:
        with open(ann_path) as ann_file:
            ann = json.load(ann_file)
            if ann["geometryType"] == "rectangle" and (not ann.get("createdAt") or ann.get("robotAuthor")):
                count += 1
    return count
    
