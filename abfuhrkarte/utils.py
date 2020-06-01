from json import load, dump
from os import makedirs
from pathlib import Path


def dict_to_jsonfile(data_dict, path_with_filename):
    path = Path(path_with_filename)
    makedirs(path.parent, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as outfile:
        dump(data_dict, outfile,
             ensure_ascii=False, sort_keys=True)


def dict_from_jsonfile(path_with_filename):
    with open(path_with_filename, 'r', encoding='utf-8') as infile:
        return load(infile)
