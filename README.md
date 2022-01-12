# Bitmap to rectangle converter

```
py convert.py -m [mappings-file] -d [root-dir]
py convert.py --mappings [mappings-file] --root-dir [root-dir]
```

**mappings** - This file is to contain lines in the format `source-class-name=destination-class-name`. In our case, this will be `seg-blue-cone=blue-cone` .etc.

**root-dir** - This is the root directory of the exported project (the one containing meta.json)

The new json files will be exported to a folder called `new_ann`.
First, verify that the exported json files look correct, then delete the original `ann` folder and rename `new_ann` as `ann`.
