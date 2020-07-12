#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: ZC
@file: migu2
@time: 2020-07-12
"""

import copy
import requests as req
from .. import config
from ..api import MusicApi
from ..song import BasicSong


class Migu2Api(MusicApi):
    session = copy.deepcopy(MusicApi.session)
    session.headers.update(
        {"referer": "http://music.migu.cn/", "User-Agent": config.get("ios_useragent")}
    )


class Migu2Song(BasicSong):
    def __init__(self):
        super(Migu2Song, self).__init__()
        self.content_id = ""

def get_url_by_id(sid):
    if not sid: return ""
    params = {
        "id": sid,
    }
    url = "http://api.migu.jsososo.com/song"
    for ty in ["320"]:
        params["type"] = ty
        res_data = (
            Migu2Api.request(
                url,
                method="GET",
                data=params,
            )
            .get("data", {})
            .get("url", "")
        )
        if res_data: return res_data
    return ""

def migu2_search(keyword) -> list:
    """ 搜索音乐 """
    params = {
        "keyword": keyword,
        "pageNo": 1,
    }

    songs_list = []
    Migu2Api.session.headers.update(
            {"referer": "http://api.migu.jsososo.com", "User-Agent": config.get("ios_useragent")}
    )

    res_data = (
        Migu2Api.request(
            "http://api.migu.jsososo.com/search",
            method="GET",
            data=params,
        )
        .get("data", {})
        .get("list", [])
    )

    for item in res_data:
        # 获得歌手名字
        singers = [s.get("name", "") for s in item.get("artists", [])]
        song = Migu2Song()
        song.source = "MIGU2"
        song.id = item.get("id", "")
        song.title = item.get("name", "")
        song.singer = "、".join(singers)
        song.album = item.get("album", {}).get("name", "")
        song.cover_url = item.get("imgItems", [{}])[0].get("img", "")
        song.lyrics_url = item.get("lyricUrl", item.get("trcUrl", ""))
        # song.duration = item.get("interval", 0)
        # 特有字段
        song.content_id = item.get("contentId", "")
        song.song_url = get_url_by_id(song.id)
        song.size = "--"
        ext = "mp3" if song.song_url and song.song_url.find("mp3") >=0 else "flac"
        song.ext = ext
        songs_list.append(song)

    return songs_list

search = migu2_search
