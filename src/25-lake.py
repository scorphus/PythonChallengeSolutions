#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/hex/lake.html

from auth import get_last_src_url
from auth import read_url
from cache import autocached
from etc import image_to_text
from itertools import product
from PIL import Image
from urllib.error import HTTPError

import io
import wave


@autocached
def read_waves(url):
    """Reads all the WAVE files there are available under similar URLs"""
    i, waves = 1, []
    while True:
        try:
            payload = read_url(url.replace("1", str(i)))
            with wave.open(io.BytesIO(payload)) as wave_read:
                waves.append(wave_read.readframes(wave_read.getnframes()))
            i += 1
        except HTTPError:
            return waves


def create_image(waves):
    """Creates an image out of the WAVE frames"""
    wav_size = int((len(waves[0]) / 3) ** 0.5)  # a square with len(waves[0]) RGB pixels
    size = int(len(waves) ** 0.5) * wav_size  # a square with len(waves) subsquares
    ratio = size // wav_size
    new_image = Image.new("RGB", (size, size))
    for i, wav in enumerate(waves):
        new_image.paste(
            Image.frombytes("RGB", (wav_size, wav_size), wav),
            (i % ratio * wav_size, i // ratio * wav_size),
        )
    return new_image


@autocached
def highlight_blue(image):
    """Highlights the bluest pixels of image"""
    for xy in product(range(image.width), range(image.height)):
        r, g, b = image.getpixel(xy)
        if b > 1.2 * r and b > 1.2 * g:
            image.putpixel(xy, (255,) * 3)
        else:
            image.putpixel(xy, (0,) * 3)
    return image


url = get_last_src_url("http://www.pythonchallenge.com/pc/hex/lake.html")
image = create_image(read_waves(url.replace("jpg", "wav")))
print(image_to_text(highlight_blue(image)))
