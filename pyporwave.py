# DONE: Allow users to search songs, rather than paste URLs.
# DONE: Add mp3 conversion.
# TODO: Add bpm analysis for song 'chopping'.

from pysndfx import AudioEffectsChain 
from pydub import AudioSegment
import youtube_dl
import os
import time

# # infile gets stored as a string.
infile = input('Ｓｅａｒｃｈ　ｆｏｒ　ａ　ｓｏｎｇ：　')
print('Ｓｅａｒｃｈｉｎｇ．．．')

ydl_opts = {
    'quiet': True,
    'format': 'bestaudio/best',
    'outtmpl': '%(title)s.%(ext)s', # Necessary parameter to import youtube-dl's naming scheme into this program.
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
        'preferredquality': '192', # Originally 192
    }],
}

# Search and download.
infile = 'ytsearch:' + infile
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(infile)
print('Ｄｏｗｎｌｏａｄｉｎｇ　' + info['entries'][0]['title'])
print('Ｐｌｅａｓｅ　ｗａｉｔ．．．')
downloaded = info['entries'][0]['title'] + '.wav'

# # vaporwave parameters
fx = (
        AudioEffectsChain()
        .speed(0.87) # 0.87 for Floral Shoppe
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

outfile = downloaded.replace('.wav', '') + ' - ｖａｐｏｒｗａｖｅ.mp3'

# # Take the downloaded file and remove spaces from the filename.
# # librosa will not work with spaces in the filename.
downloaded = downloaded.replace(' ', '')
os.rename(info['entries'][0]['title'] + '.wav', downloaded)

# # Or, apply the effects directly to a ndarray.
from librosa import load
y, sr = load(downloaded, sr=None)
y = fx(y)

# # Apply the effects and return the results as a ndarray.
y = fx(downloaded)

# # Apply the effects to a ndarray but store the resulting audio to disk.
fx(y, 'VAPOR.wav')

# # Convert VAPOR.wav to an .mp3.
AudioSegment.from_wav('VAPOR.wav').export(outfile, format='mp3')

# # Remove downloaded files and quit.
os.remove(downloaded)
os.remove('VAPOR.wav')
print('Ｔｉｄｙｉｎｇ　ｕｐ．．．')
