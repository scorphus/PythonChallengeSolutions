#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/hex/lake.html

from base64 import encodebytes
from itertools import chain
from PIL import Image
from urllib.request import Request
from urllib.request import urlopen

import io
import wave


def open_url(url):
    auth = encodebytes(b"butter:fly").decode().rstrip()
    headers = {"Authorization": f"Basic {auth}"}
    return urlopen(Request(url=url, headers=headers)).read()


def read_url(url):
    """Reads URL of the only image in the mission"""
    riddle_source = open_url(url).decode()
    return url.replace("lake.html", riddle_source.split('src="')[-1].split('"')[0])


def read_waves(url):
    """Reads all the WAVE files there are available under similar URLs"""
    url, i, waves = url.replace("jpg", "wav"), 1, []
    while True:
        try:
            payload = open_url(url.replace("1", str(i)))
            with wave.open(io.BytesIO(payload)) as wave_read:
                waves.append(wave_read.readframes(wave_read.getnframes()))
            i += 1
        except Exception:
            return waves


def create_image(waves):
    """Creates an image out of the WAVE frames"""
    wav_size = int((len(waves[0]) / 3) ** 0.5)  # a square with len(waves[0]) RGB pixels
    size = int(len(waves) ** 0.5) * wav_size  # a square with len(waves) subsquares
    new_image = Image.new("RGB", (size, size))
    pad_x = pad_y = 0
    waves_it = chain.from_iterable(waves)
    for _ in range(len(waves)):
        if pad_x == size:  # once a row is complete, go to the next
            pad_x, pad_y = 0, pad_y + wav_size
        for y in range(wav_size):
            for x in range(wav_size):
                new_image.putpixel(
                    (pad_x + x, pad_y + y),
                    (next(waves_it), next(waves_it), next(waves_it)),
                )
        pad_x += wav_size
    return new_image


url = read_url("http://www.pythonchallenge.com/pc/hex/lake.html")
image_name = "25-lake.png"
create_image(read_waves(url)).save(image_name)
print("Check", image_name)
