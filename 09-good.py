#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/return/good.html

from PIL import Image, ImageDraw  # pip install pillow
from base64 import encodebytes
from urllib.request import Request, urlopen

url = 'http://www.pythonchallenge.com/pc/return/good.html'
auth = encodebytes(b'huge:file').decode().rstrip()
headers = {'Authorization': f'Basic {auth}'}
page_source = urlopen(Request(url=url, headers=headers)).read().decode()
page_data = page_source.split('<!--')[2].split('-->')[0]

first, second = [[int(n) for n in s.split(',')] for s in [
    p.split(':')[-1].rstrip()
    for p in page_data.split('\n\n') if ':' in p
]]

size = [max(first + second) + 1] * 2
image = Image.new('1', size)

draw = ImageDraw.Draw(image)
draw.line(list(zip(first[::2], first[1::2])), 1, 2)
draw.line(list(zip(second[::2], second[1::2])), 1, 2)

image.save('09-good.png', 'PNG')
print('Open 09-good.png')
