import io
import os
import json
import time
from pathlib import Path

import matplotlib.image as mpimg
import pandas as pandas
import tqdm as tqdm
from matplotlib.backends.backend_pdf import PdfPages
import requests
from typing import Optional, List

import numpy as np
import matplotlib.pyplot as plt

time_before = 0
card_size_inch = np.array([2.5, 3.5])
page_size_inch = np.array([210, 297]) / 25.4
page_margin_prop = ((page_size_inch % card_size_inch) / 2) / page_size_inch
card_size_prop = card_size_inch / page_size_inch
dpi = 600


def get_front_image_url_from_id(card_id: str) -> Optional[str]:
    global time_before
    time.sleep(max(0., 0.1 - time.time() + time_before))
    r = requests.get(f"https://api.scryfall.com/cards/{card_id}")
    if r.status_code != 200: return None
    request_text_json = json.loads(r.content.decode())
    time_before = time.time()
    return request_text_json['image_uris']['png']


def get_back_image_url_from_back_id(card_id: str) -> Optional[str]:
    return f"https://c1.scryfall.com/file/scryfall-card-backs/png/{card_id[:2]}/{card_id}.png"




def gen_pngs_from_urls(image_url_list: List[str]) -> List[Optional[bytes]]:
    for url in image_url_list:
        with requests.get(url) as r:
            assert r.headers.get('content-type') == 'image/png', "not an image something terribly wrong"
            with io.BytesIO(r.content) as image_byte_buffer:
                yield mpimg.imread(image_byte_buffer, format='png')


def get_urls_from_ids_file(card_id_file_path: str) -> List[str]:
    with open(card_id_file_path, 'r') as card_ids_file:
        return [get_front_image_url_from_id(card_id.strip()) for card_id in card_ids_file.readlines()]


def pngs_as_bytes_to_pdf(pngs: list, out_pdf_path: str):
    with PdfPages(out_pdf_path) as pdf_saver:
        for page_number in tqdm.tqdm(range(1, len(pngs) // 9 + 2)):
            fig = plt.figure(figsize=page_size_inch)
            ax = fig.add_axes([0, 0, 1, 1])
            plt.xlim(0, 1)  # page goes from
            plt.ylim(0, 1)  # vertically and horizontally
            pngs_on_page = pngs[(page_number - 1) * 9:min(page_number * 9, len(pngs))]
            for png, i in tqdm.tqdm(zip(pngs_on_page, range(len(pngs_on_page)))):
                plt.imshow(png,
                           extent=[page_margin_prop[0] + int(i % 3) * card_size_prop[0],
                                   page_margin_prop[0] + card_size_prop[0] + int(i % 3) * card_size_prop[0],
                                   page_margin_prop[1] + (i // 3) * card_size_prop[1],
                                   page_margin_prop[1] + card_size_prop[1] + (i // 3) * card_size_prop[1]],
                           aspect=page_size_inch[1] / page_size_inch[0]
                           )
            plt.xlim(0, 1)
            plt.ylim(0, 1)

            ax.axis("off")
            pdf_saver.savefig(dpi=dpi)
            plt.close()


def get_pdf_from_id_list(ids_list: List[str], out_file_path: str, side="fronts"):
    url_getter_func = get_front_image_url_from_id if side == "fronts" else \
        (get_back_image_url_from_back_id if side == "backs" else None)
    pngs_as_bytes_to_pdf(
        list(gen_pngs_from_urls(
            [url_getter_func(id) for id in ids_list]))
        , out_file_path)



if __name__ == "__main__":
    panda_frame = pandas.read_csv('set.csv')
    #get_pdf_from_id_list(panda_frame['card_id'][:22], 'fronts.pdf')
    get_pdf_from_id_list(panda_frame['back_id'][:22], 'backs.pdf', "backs")

