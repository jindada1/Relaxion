import unittest
from music import Fetchers

searchkey = "周杰伦"
page = 2
num = 20
userid = '7ensoKviNeci'


class TestPlatforms(unittest.IsolatedAsyncioTestCase):

    def __init__(self, args):

        super().__init__(args)

        fetchers = Fetchers({
            "qq": {
                "fetcher": "QQ"
            }
        })

        self.fetcher = fetchers["qq"]

    async def test_search(self):

        self.assertIsNone((await self.fetcher.searchSong(searchkey, page, num)).get('error'))

        self.assertIsNone((await self.fetcher.searchAlbum(searchkey, page, num)).get('error'))

        self.assertIsNone((await self.fetcher.searchMV(searchkey, page, num)).get('error'))

    async def test_comments(self):

        self.assertIsNone((await self.fetcher.getComments("107192078", "music", page, num)).get('error'))

        self.assertIsNone((await self.fetcher.getComments("14536", "album", page, num)).get('error'))

        self.assertIsNone((await self.fetcher.getComments("n0010BCw40a", "mv", page, num)).get('error'))

    async def test_mvuri(self):

        self.assertIsNone((await self.fetcher.mvuri("m00119xeo83")).get('error'))

    async def test_lyric(self):

        self.assertIsNotNone(await self.fetcher.lyric("002WCV372JMZJw"))

    # async def test_account(self):
        # print(await self.fetcher.getuserid("406143883"))
        # print(await self.fetcher.userlist("406143883"))
        # self.assertIsNone((await self.fetcher.userdetail(userid)).get('error'))

    async def test_songlist(self):

        self.assertIsNone((await self.fetcher.songsinList("1304470181", page, num)).get("error"))

    async def test_albumlist(self):

        self.assertIsNone((await self.fetcher.songsinAlbum("14536")).get("error"))

    async def test_musicuri(self):

        print(await self.fetcher.musicuri("002WCV372JMZJw"))


if __name__ == "__main__":

    unittest.main()
