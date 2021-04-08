import os
import re
import json

from glob import glob
from collections import OrderedDict
from tqdm import tqdm

for file_name in tqdm(glob('AIhub/*.trn')):

    json_list = []
    with open(file_name, 'r', encoding='utf-8') as f:
        for x in f.read().splitlines():
            wav, text = x.split('/', 2)[-1].split(" :: ")
            wav = wav.replace('pcm', 'wav')
            text = re.sub("b/|l/|o/|n/|/|\+", "", text)

            json_data = OrderedDict()
            json_data["wav"] = wav
            json_data["text"] = text.strip()
            json_data["speaker_id"] = "0"
            json_list.append(json_data)

    with open(file_name.replace('trn', 'json'), 'w', encoding='utf-8') as make_file:
        json.dump(json_list, make_file, ensure_ascii=False, indent='\t')

    os.remove(file_name)
