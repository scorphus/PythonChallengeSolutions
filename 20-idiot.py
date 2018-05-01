#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/hex/bin.html

from base64 import encodebytes
from io import BytesIO
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from zipfile import ZipFile

url = 'http://www.pythonchallenge.com/pc/hex/unreal.jpg'
auth = encodebytes(b'butter:fly').decode().rstrip()
headers = {'Authorization': f'Basic {auth}'}

range_start, range_end = None, None
while True:
    if range_start or range_end:
        headers['Range'] = f'bytes={range_start}-{range_end}'
    try:
        req = urlopen(Request(url=url, headers=headers))
        if range_start or range_end:
            print(req.read().decode().strip())
        content_range = req.headers.get('Content-Range').replace('bytes ', '')
        range_start_end = content_range.split('/')[0]
        range_start, range_end = (int(x) for x in range_start_end.split('-'))
        range_start, range_end = range_end + 1, 2 * range_end - range_start + 2
    except HTTPError:
        break

content_max = int(content_range.split('/')[1])

headers['Range'] = f'bytes={content_max}-{content_max}'
req = urlopen(Request(url=url, headers=headers))
msg = req.read().decode().strip()
print(f'{msg} ({msg[::-1]})')

headers['Range'] = f'bytes={content_max - 3*len(msg)//2}-{content_max}'
req = urlopen(Request(url=url, headers=headers))
msg = req.read().decode().strip()
print(msg)

range_start = int(msg.rstrip('.').split()[-1])
headers['Range'] = f'bytes={range_start}-{content_max}'
req = urlopen(Request(url=url, headers=headers))
zip_content = req.read()
with ZipFile(BytesIO(zip_content), 'r') as zip:
    print(f'Open {" and ".join(zip.namelist())}')
    zip.extractall(pwd=b'invader'[::-1])
