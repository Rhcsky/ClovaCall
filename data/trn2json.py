import os
import re
import json

from glob import glob
from collections import OrderedDict
from tqdm import tqdm

kspon_1 = (0, 124000)
kspon_2 = (124001, 248000)
kspon_3 = (248001, 372000)
kspon_4 = (372001, 496000)
kspon_5 = (496001, 622545)
kspon_list = [kspon_1, kspon_2, kspon_3, kspon_4, kspon_5]


def where_is_wav(num_file):
    num_file = int(num_file)
    for i, kspon in enumerate(kspon_list):
        if i > 0:
            return 'NO'
        if num_file <= kspon[1] and num_file >= kspon[0]:
            return f'KsponSpeech_0{i + 1}'


for file_name in tqdm(glob('AIhub/*.trn')):

    json_list = []
    with open(file_name, 'r', encoding='utf-8') as f:
        for x in f.read().splitlines():
            wav, text = x.split('/', 2)[-1].split(" :: ")
            wav = wav.replace('pcm', 'wav')
            text = re.sub("b/|l/|o/|n/|/|\+", "", text)

            try:
                num_file = wav.split('_')[1].split('.')[0]

                base_dir = where_is_wav(num_file)
                if base_dir == 'NO':
                    continue

            except:
                num_file = wav.split('E')[1].split('.')[0]

                base_dir = 'KsponSpeech_Eval'

            json_data = OrderedDict()
            json_data["wav"] = os.path.join(base_dir, wav)
            json_data["text"] = text.strip()
            json_data["speaker_id"] = "0"
            json_list.append(json_data)

    with open(file_name.replace('trn', 'json'), 'w', encoding='utf-8') as make_file:
        json.dump(json_list, make_file, ensure_ascii=False, indent='\t')

    # os.remove(file_name)
