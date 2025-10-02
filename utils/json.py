import json

type VALID_JSON_TYPES = str | int | float | bool | None | dict[
    str, VALID_JSON_TYPES
] | list[VALID_JSON_TYPES]


def read_json(file: str) -> dict[str, VALID_JSON_TYPES]:

    print(f"Reading json file {file}")

    with open(file, "r") as json_file:
        ret = json.load(json_file)

    return ret


def to_json(to_filepath: str, data: str | dict[str, VALID_JSON_TYPES]):
    with open(to_filepath, "w") as file:
        json.dump(data, file, indent=4)
