#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: HJK
@file: test_addon_migu2.py
@time: 2019-06-10
"""
import sys
sys.path.append("..")
from music_dl import config
config.init()
from music_dl.addons import migu2


def test_migu2():
    songs_list = migu2.search("丢了你","井胧")
    print(songs_list)
    assert songs_list is not None

if __name__ == '__main__':
    test_migu2()
