#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: HJK
@file: test_addon_migu2.py
@time: 2019-06-10
"""
import sys
sys.path.append("..")
from music_dl.addons import migu2


def test_migu2():
    songs_list = migu2.search("包容")
    assert songs_list is not None
