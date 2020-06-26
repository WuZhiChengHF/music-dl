#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: wzc
@file: test_dl_mlist.py
@time: 2020-06-26
"""

import re, os, sys
import requests as req
from music_dl.source import MusicSource
from music_dl import config


class dlist(object):
    def __init__(self, src_list=["migu", "kugou"]):
        config.init()
        self.ms = MusicSource()
        self._src_list = src_list

    def get_mlist(self, url):
        #https://www.kugou.com/yy/special/single/2440703.html
        resp = req.get(url)
        if resp and resp.status_code != 200:
            raise Exception("get music list failed")
        slist = re.findall(r"\"[^\"\<\>]* \- [^\"\<\>]*\"", resp.text)

        rlist = list()
        for s in slist:
            tmp = s.split("-")
            author = tmp[0].replace("\"", "").replace(" ", "")
            song = tmp[1].replace("\"", "").replace(" ", "")
            rlist.append((author, song))

        return rlist

    def __get_max_size_item(self, rlist):
        max_size = 0
        for i in rlist:
            if i.size > max_size:
                r = i
                max_size = i.size
        return r

    def search_song(self, author, sname):
        rest_list = self.ms.search(sname, self._src_list)
        if not rest_list:
            print("{}-{} search faild".format(author, sname))
            return None

        rest_list = [i for i in rest_list if i.name.find("DJ") < 0]

        spare_list = list()
        for rest in rest_list:
            if rest.name.find(author) >= 0 and rest.name.find(sname) >=0:
                spare_list.append(rest)

        if len(spare_list) == 1: return spare_list[0]
        else:
            return self.__get_max_size_item(
                rest_list if not spare_list else spare_list)

    def down_mlist(self, url):
        rlist = self.get_mlist(url)
        for s in rlist:
            sobj = self.search_song(s[0], s[1])
            if not sobj: continue
            print(sobj.name)
            sobj.download()


def test_search():
    config.init()
    ms = MusicSource()
    songs_list = ms.search("五月天", ["baidu"])
    assert songs_list is not None


if '__main__' == __name__:
    #dl = dlist(["migu"])
    dl = dlist()
    #rlist = dl.get_mlist("https://www.kugou.com/yy/special/single/2440703.html")
    #print(rlist)
    uid = "2688007"
    dl.down_mlist("https://www.kugou.com/yy/special/single/{}.html".format(str(uid)))
    #test_search()

# def test_single():
#     ms = MusicSource()
#     song = ms.single("https://music.163.com/#/song?id=26427663")
#     assert song is not None
#
#
# def test_playlist():
#     ms = MusicSource()
#     songs_list = ms.playlist("https://music.163.com/#/playlist?id=2602222983")
#     assert songs_list is not None
