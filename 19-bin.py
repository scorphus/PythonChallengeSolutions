#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/hex/bin.html

import email
import io
import wave

from base64 import encodebytes
from urllib.request import Request, urlopen

url = "http://www.pythonchallenge.com/pc/hex/bin.html"
auth = encodebytes(b"butter:fly").decode().rstrip()
headers = {"Authorization": f"Basic {auth}"}

page_source = urlopen(Request(url=url, headers=headers)).read().decode()
page_data = page_source.split("<!--")[1].split("-->")[0].strip()

email_message = email.message_from_string(page_data)
wave_payload = email_message.get_payload()[0].get_payload(decode=True)

with wave.open(io.BytesIO(wave_payload)) as wave_read:
    frames = wave_read.readframes(wave_read.getnframes())
    with wave.open("19-bin.wav", "wb") as wave_write:
        wave_write.setnchannels(wave_read.getnchannels())
        wave_write.setsampwidth(wave_read.getsampwidth())
        wave_write.setframerate(wave_read.getframerate())
        wave_write.writeframesraw(b"@" + frames)

print("Open 19-bin.wav")
