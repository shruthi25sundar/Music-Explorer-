from App import artistinfo as info
from App import albumdetails as teaminfo
import json


class MainFun:
    @staticmethod
    def SearchArtist(a):
        inst = info.ArtistInfo(a)
        result = json.loads(inst.result)
        # result2 = json.loads(inst.result2)
        return result

    @staticmethod
    def team_search(team):
        tm = teaminfo.AlbumDetail(team)
        tm_result = json.loads(tm.tm_result)
        return tm_result
