#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/hex/bin.html

from auth import get_nth_comment

import email
import io
import wave


url = "http://www.pythonchallenge.com/pc/hex/bin.html"
page_data = get_nth_comment(url, 1).strip()
email_message = email.message_from_string(page_data)
payload = email_message.get_payload()[0].get_payload(decode=True)

with wave.open(io.BytesIO(payload)) as in_wav, wave.open("19-bin.wav", "wb") as out_wav:
    out_wav.setnchannels(in_wav.getnchannels())
    out_wav.setsampwidth(in_wav.getsampwidth())
    out_wav.setframerate(in_wav.getframerate())
    out_wav.writeframesraw(b"@" + in_wav.readframes(in_wav.getnframes()))

print("Open 19-bin.wav only to listen the word “idiot”")
