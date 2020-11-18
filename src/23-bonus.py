#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/hex/bonus.html

from auth import get_nth_comment
from contextlib import redirect_stdout
from difflib import get_close_matches
from difflib import ndiff
from importlib import import_module


def import_this():
    """Imports the "this" module without printing the Zen of Python"""
    with redirect_stdout(None):
        this = import_module("this")
        return this


def find_sentence(this, search):
    """Finds the first sentence of the Zen with the similar start as `search`"""
    sentences = this.s.splitlines()
    for cutoff in range(6, 0, -1):
        matches = get_close_matches(search, sentences, cutoff=cutoff / 10)
        if matches:
            return matches[0].lower()


def find_word(search, sentence):
    """Finds the first word of `sentence` that is not in `search`"""
    return next(
        word[2:]
        for word in ndiff(
            [s.rstrip(",?") for s in search.split()],
            [s.rstrip(",.") for s in sentence.split()],
        )
        if word.startswith("+ ")
    )


def translate(this, word):
    return "".join(this.d.get(c, c) for c in word)


url = "http://www.pythonchallenge.com/pc/hex/bonus.html"
search = get_nth_comment(url, 3).strip("\n'")
this = import_this()
sentence = find_sentence(this, search)
word = find_word(search, sentence)
print(translate(this, word))
