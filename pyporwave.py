# DONE: Allow users to search songs, rather than paste URLs.
# DONE: Add mp3 conversion.
# TODO: Add bpm analysis for song 'chopping'.

import hashlib
import os
import sys
import uuid

import youtube_dl

from pysndfx import AudioEffectsChain
from pydub import AudioSegment

vw_fx_chain = (
    AudioEffectsChain()
    .speed(0.87)  # 0.87 for Floral Shoppe
    # .chorus(0.4, 0.6, [[55, 0.4, 0.55, .5, 't']])
    .reverb(
       reverberance=30,
       hf_damping=50,
       room_scale=100,
       stereo_depth=100,
       pre_delay=20,
       wet_gain=0,
       wet_only=False
    )
)

output_dir = 'output'

ydl_config = {
    'quiet': True,
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
        'preferredquality': '192', # Originally 192
    }],
}


def download(query):
    print(f' ．．．ｓｅａｒｃｈｉｎｇ  ｆｏｒ  "{query}" ．．．')

    wav_path = f'{output_dir}/{random_filename()}.wav'
    outtmpl = wav_path.replace('.wav', '.%(ext)s')
    ydl_config['outtmpl'] = outtmpl
    with youtube_dl.YoutubeDL(ydl_config) as ydl:
        info = ydl.extract_info(f'ytsearch:{query}')

    title = info["entries"][0]["title"]
    print(f' ．．．fｏｕｎｄ  "{title}"， ｄｏｗｎｌｏａｄｅｄ  ｔｏ  ./{wav_path} ．．．')

    return title, wav_path


def random_filename():
    return hashlib.md5(uuid.uuid4().bytes).hexdigest()[:12]


def apply_fx(in_wav_path):
    print(f' ．．．ａｐｐｌｙｉｎｇ  ｖａｐｏｒｗａｖｅ  ｅｆｆｅｃｔｓ  ｔｏ  ./{in_wav_path} ．．．')

    out_wav_path = in_wav_path.replace('.wav', '.vw.wav')
    vw_fx_chain(in_wav_path, out_wav_path)

    print(f' ．．．ｖｗ  ｒｅｓｕｌｔ  ｓｔｏｒｅｄ  ｉｎ  ./{out_wav_path} ．．．')

    return out_wav_path


def wav_to_mp3(wav_path):
    print(f' ．．． ｃｏｎｖｅｒｔｉｎｇ  ./{wav_path}  ｉｎｔｏ  ｍｐ３ ．．．')

    mp3_path = wav_path.replace('.wav', '.mp3')
    with open(wav_path, 'rb') as wav_file:
        wav = AudioSegment.from_file(wav_file, format='wav')
    wav.export(mp3_path, format='mp3')

    return mp3_path


def remove_all(*paths):
    print(' ．．．ｔｉｄｙｉｎｇ　ｕｐ ．．．')
    for path in paths:
        print(f' ．．． ｒｅｍｏｖｉｎｇ  {path} ．．．')
        os.remove(path)


def main(query):
    print('Ｓｔａｒｔｉｎｇ  ｐｒｏｃｅｓｓ ．．．')

    title, in_wav_path = download(query)
    out_wav_path = apply_fx(in_wav_path)
    in_mp3_path = wav_to_mp3(in_wav_path)
    out_mp3_path = wav_to_mp3(out_wav_path)
    os.rename(in_mp3_path, f'{output_dir}/{title}.mp3')
    os.rename(out_mp3_path, f'{output_dir}/{title} - ｖａｐｏｒｗａｖｅ.mp3')
    remove_all(in_wav_path, out_wav_path)

    print('．．． ｆｉｎｉｓｈｅｄ．')


if __name__ == '__main__':
    query = sys.argv[1]
    main(query)
