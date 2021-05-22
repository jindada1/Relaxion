import os, sys, unittest

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from platforms import PraserService


class TestPlatforms(unittest.IsolatedAsyncioTestCase):

    def __init__(self, args):

        super().__init__(args)

        self.pltfs = PraserService({
            "qq": {
                "third": "",
                "parser": "QQ"
            },
            "wangyi": {
                "third": "",
                "parser": "WangYi"
            }
        })

    async def test_qq(self):

        p = self.pltfs["qq"]
        searchkey = "周杰伦"
        page = 2
        num = 20
        userid = '7ensoKviNeci'
        
        self.assertIsNone((await p.searchSong(searchkey, page, num)).get('error'))
        
        self.assertIsNone((await p.searchAlbum(searchkey, page, num)).get('error'))
        
        self.assertIsNone((await p.searchMV(searchkey, page, num)).get('error'))
        
        self.assertIsNone((await p.getComments("107192078", "music", page, num)).get('error'))
        
        self.assertIsNone((await p.getComments("14536", "album", page, num)).get('error'))
        
        # self.assertIsNone((await p.getComments("n0010BCw40a", "mv", page, num)).get('error'))
        
        self.assertIsNone((await p.mvuri("m00119xeo83")).get('error'))
        
        self.assertIsNotNone(await p.lyric("002WCV372JMZJw"))
        
        # self.assertIsNone((await p.userdetail(userid)).get('error'))
        
        self.assertIsNone((await p.songsinList("1304470181", page, num)).get("error"))
        
        self.assertIsNone((await p.songsinAlbum("14536")).get("error"))
        
        # print(await p.musicuri("002WCV372JMZJw"))
        # print(await p.getuserid("406143883"))
        # print(await p.userlist("406143883"))


    async def test_wangyi(self):

        wangyi = self.pltfs["wangyi"]
        searchkey = "林俊杰"
        page = 1
        num = 20
        userid = '同济吴亦凡'
        
        # self.assertIsNone((await wangyi.searchSong(searchkey, page, num)).get('error'))
        
        self.assertIsNone((await wangyi.searchAlbum(searchkey, page, num)).get('error'))
        
        self.assertIsNone((await wangyi.searchMV(searchkey, page, num)).get('error'))
        
        self.assertIsNone((await wangyi.getComments("33894312", "music", page, num)).get('error'))
        
        self.assertIsNone((await wangyi.getComments("32311", "album", page, num)).get('error'))
        
        self.assertIsNone((await wangyi.getComments("5436712", "mv", page, num)).get('error'))
        
        self.assertIsNone((await wangyi.musicuri("33894312")).get('error'))
        
        self.assertIsNone((await wangyi.mvuri("5436712")).get('error'))
        
        self.assertIsNotNone(await wangyi.lyric("33894312"))
        
        self.assertIsNone((await wangyi.userlist(userid)).get('error'))
        
        # self.assertIsNone((await wangyi.songsinList("24381616", 0, 20)).get('error'))
        
        self.assertIsNone((await wangyi.songsinAlbum("32311")).get('error'))
        
        self.assertIsNotNone((await wangyi.picurl("32311")))


if __name__ == "__main__":

    unittest.main()
