from count import count
from convert import convert
from purify import purify

CONVERT = 0;
COUNT = 1;
PURIFY = 2;

options, remainder = getopt.getopt(
    sys.argv[1:],
    "phd:m:D:",
    ["purify", "help", "root-dir=", "mappings=","dataset="]
)

options = {
    "project_dir" : ".",
    "dataset" : "",
    "map_file" : "",
    "output_dir" : "new_ann"
}

mode = CONVERT;

for option, argument in options:
    if option in ("-h", "--help"):
        print(open("help").read())
        quit()
    elif option in ("-d", "--root-dir"):
        options["project_dir"] = argument
    elif option in ("-D", "--dataset"):
        options["dataset"] = argument
    elif option in ("-m", "--mappings"):
        options["map_path"] = argument
    elif option in ("-c", "--convert"):
        mode = COUNT
    elif option in ("-p", "--purify"):
        mode = PURIFY

if mode == CONVERT:
    convert(options)
elif mode == COUNT:
    number_of_autogenerated_masks = count(options)
    print(number_of_autogenerated_masks)
elif mode == PURIFY:
    purify(options)
