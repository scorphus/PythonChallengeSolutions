#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/return/disproportional.html

from xmlrpc.client import ServerProxy

url = 'http://www.pythonchallenge.com/pc/phonebook.php'

with ServerProxy(url) as proxy:
    print("system.listMethods(): {}".format(proxy.system.listMethods()))
    print("phone('Bert'): {}".format(proxy.phone('Bert')))
