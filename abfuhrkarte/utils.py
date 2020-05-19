import json


def dict_to_jsonfile(data_dict, path_with_filename):
    with open(path_with_filename, 'w', encoding='utf-8') as outfile:
        json.dump(data_dict, outfile,
                  ensure_ascii=False, sort_keys=True)

def dict_from_jsonfile(path_with_filename):
    with open(path_with_filename, 'r', encoding='utf-8') as infile:
        return json.load(infile)
        # json.dump(data_dict, outfile,
        #           ensure_ascii=False, sort_keys=True)
