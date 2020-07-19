#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: wzc
@file: test_dl_mlist.py
@time: 2020-06-26
"""

import re, os, sys
import requests as req
import json

sys.path.append("..")
from music_dl.source import MusicSource
from music_dl import config
from functools import wraps

import importlib
importlib.reload(sys)


class dlist(object):
    def __init__(self, src_list=["migu2", "kugou"]):
        config.init()
        self.ms = MusicSource()
        self._src_list = src_list
        self.ex_bracket = lambda x: re.sub(r"[\(（].*[\)）]", "", x)
        self.musics = list()

    def mlist(self, url):
        resp = req.get(url, headers={'User-agent': 'Mozilla/5.0'})
        if resp and resp.status_code != 200:
            raise Exception("get music list failed")
        return resp.text

    def get_kg_list(self, url):
        """get list"""
        text = self.mlist(url)
        slist = re.findall(r"\"[^\"\<\>\\u]* \- [^\"\<\>#]*\"", text)

        rlist = list()
        for s in slist:
            tmp = s.split("-")
            author = tmp[0].replace("\"", "").replace(" ", "")
            song = tmp[1].replace("\"", "").replace(" ", "")
            rlist.append((author, song))

        self.musics.extend(slist)

        return rlist

    def get_mg_list(self, url, page=None):
        """get list"""
        text = self.mlist(url + (("?" + page) if page else ""))

        pages = list()
        if not page: pages = list(set(re.findall(r'page=\d', text) or []))

        slist = re.findall(r"data\-share=\'\{[^\{\}]*\}\'", text)

        slist = [json.loads(i.replace("\n", "")
                     .replace("data-share=", "")
                     .replace("\'", "")) for i in slist if i]

        slist = [(self.ex_bracket(i.get('title')), self.ex_bracket(i.get('singer')))
                    for i in (slist or [])
                    if i and i.get('title') and i.get('singer')]

        slist = [i for i in slist if not re.match(r"^[a-zA-Z].*", i[1])]

        self.musics.extend(slist)

        for p in pages: self.get_mg_list(url, p)

        return slist

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

        #list(filter(lambda x: if i.name.find("DJ") >= 0, rest_list))
        rest_list = [i for i in rest_list if i.name.lower().find("dj") < 0]

        spare_list = list()
        for rest in rest_list:
            if rest.name.find(author) >= 0 and rest.name.find(sname) >=0:
                spare_list.append(rest)

        if len(spare_list) == 1: return spare_list[0]
        else:
            return self.__get_max_size_item(
                rest_list if not spare_list else spare_list)

    def down_mlist(self, url):

        if url and url.find("kugou") >= 0:
            self.get_kg_list(url)
        elif url and url.find("migu") >= 0:
            self.get_mg_list(url)
            #print(self.musics)
        else: raise Exception("error: can not get %s" % url)

        for s in self.musics:
            sobj = self.search_song(s[0], s[1])
            if not sobj: continue
            print(sobj.name)
            sobj.download()

    def start_download(self, url, idlist):
        for i, sid in enumerate(idlist):
            if i == len(idlist)-1:
                dl.down_mlist(url % str(sid))


def test_search():
    config.init()
    ms = MusicSource()
    songs_list = ms.search("五月天", ["baidu"])
    assert songs_list is not None


if '__main__' == __name__:
    dl = dlist(["migu2"])

    kgs = "https://www.kugou.com/yy/special/single/%s.html"
    kuid = ["2688007", "2440703", "1071267"]

    mgs = "https://music.migu.cn/v3/music/playlist/%s"
    muid = ["177711366"]

    dl.start_download(mgs, muid)
