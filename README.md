# Bitmap to rectangle converter

```
py convert.py -m [mappings-file] -d [root-dir]
py convert.py --mappings [mappings-file] --root-dir [root-dir]
```

See help for more info on the command line arguments available.

The new json files will be exported to a folder called `new_ann`.
First, verify that the exported json files look correct, then delete the original `ann` folder and rename `new_ann` as `ann`.
