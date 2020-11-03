#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/hex/lake.html

from auth import get_img_url
from auth import read_url
from itertools import chain
from PIL import Image

import io
import wave


def read_waves(url):
    """Reads all the WAVE files there are available under similar URLs"""
    i, waves = 1, []
    while True:
        try:
            payload = read_url(url.replace("1", str(i)))
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


url = get_img_url("http://www.pythonchallenge.com/pc/hex/lake.html")
image_name = "25-lake.png"
create_image(read_waves(url.replace("jpg", "wav"))).save(image_name)
print("Check", image_name)
