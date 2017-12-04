import concurrent.futures
import random
import time
from collections import namedtuple
from os import path
from urlib import parse
import requests
from mylogging import get_my_logger

logger = get_my_logger

Image = namedtuple('image', 'file_name', 'content')

RANDOM_SLEEP_TIMES = [x * 0.1 for x in range(10, 40, 5)]

IMAGE_URLS = []

def download(url, timeout=180):
    parsed_url = parse.urlparse(url)
    file_name = path.basename(parsed_url.path)

    sleep_time = random.choice(RANDOM_SLEEP_TIMES)

    time.sleep(sleep_time)

    r = requests.get(url, timeout=timeout)

    return Image(file_name=file_name, file_content=r.content)


if __name__ == '__main__':
    # 同時に2つの処理を並行実行するための executor を作成
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        logger.info("[main start]")

        # executor.submit() によりdownload()関数を並行実行する. download()関数の引数に music_url を与えている
        # 並行実行処理のまとまりを futures 変数に入れておく
        futures = [executor.submit(download, image_url) for image_url in IMAGE_URLS]

        # download()関数の処理が完了したものから future 変数に格納する
        for future in concurrent.futures.as_completed(futures):
            # download()関数の実行結果を result() メソッドで取り出す
            music = future.result()

            # music.filename にはmp3ファイルのファイル名が入っている.
            # このファイル名を使い、music.file_content に格納されている mp3 のデータをファイルに書き出す
            with open(image.file_name, 'wb') as fw:
                fw.write(music.file_content)
        logger.info("[main finished]")
