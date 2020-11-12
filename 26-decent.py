#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/hex/decent.html

from auth import read_riddle
from image import image_to_text
from importlib import import_module
from io import BytesIO
from PIL import Image
from wand.exceptions import BaseError as WandBaseError
from wand.image import Image as WandImage

import inspect
import zipfile


def get_ambiguity_data():
    ambiguity = import_module("24-ambiguity")
    return ambiguity.data


def extract_source(func):
    """Extracts source of func"""
    source = inspect.getsource(func).splitlines()
    indentation = len(source[0]) - len(source[0].lstrip())
    return "\n".join(line[indentation:] for line in source)


def patch_update_crc():
    """Monkey-patches `ZipExtFile._update_crc` to bypass any bad CRC"""
    update_crc_src = extract_source(zipfile.ZipExtFile._update_crc).replace(
        "raise", "return  #"
    )
    exec_globals = {"crc32": zipfile.crc32}
    exec(compile(update_crc_src, "<string>", "exec"), exec_globals)
    zipfile.ZipExtFile._update_crc = exec_globals["_update_crc"]


def extract_image(zip_data):
    """Extracts an image from a corrupt zip file inside `zip_data`"""
    patch_update_crc()
    with zipfile.ZipFile(BytesIO(zip_data)) as outer:
        for name in outer.namelist():
            try:
                with zipfile.ZipFile(outer.open(name)) as inner, inner.open(
                    inner.namelist()[0]
                ) as img_file:
                    # Pillow couldn't read the corrupt gif, even with
                    # PIL.ImageFile.LOAD_TRUNCATED_IMAGES set to True
                    return WandImage(file=img_file)
            except (zipfile.BadZipFile, WandBaseError):
                pass


ambiguity_data = get_ambiguity_data()
image = extract_image(ambiguity_data)
image_data = image.export_pixels()
pil_image = Image.frombytes("RGBA", image.size, bytes(image_data))
print(image_to_text(pil_image, skip=3))

for line in read_riddle(
    "http://www.pythonchallenge.com/pc/hex/decent.html"
).splitlines():
    if not line:
        break
    if "<" in line:
        continue
    print(line.rsplit(maxsplit=1)[-1])
