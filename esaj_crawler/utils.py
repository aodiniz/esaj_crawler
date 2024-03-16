import json

def json_load(json_file_path):
    with open(json_file_path, "r", encoding="utf-8") as fp:
        json_obj = json.load(fp)

    return json_obj


def json_dump(json_file_path, json_content):
    with open(json_file_path, "w", encoding="utf-8") as fp:
        json.dump(json_content, fp, indent=4, separators=(",", ": "), ensure_ascii=False)
