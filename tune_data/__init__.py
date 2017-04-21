import json
import os
import pathlib
from collections import namedtuple


def load_tune(tune_name):
    if not tune_name.endswith('.json'):
        tune_name = tune_name + '.json'
    file_dir = (os.path.dirname(os.path.realpath(__file__)))

    for p in pathlib.Path(file_dir).iterdir():
        if p.is_file() and p.name == tune_name:
            with open(p, encoding='utf-8') as f:
                tune_dict = json.loads(f.read())
                return namedtuple('Tune', tune_dict.keys())(**tune_dict)
