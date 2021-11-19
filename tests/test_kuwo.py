import unittest
from music import Fetchers

searchkey = "周杰伦"
page = 2
num = 20


class TestPlatforms(unittest.IsolatedAsyncioTestCase):

    def __init__(self, args):

        super().__init__(args)

        fetchers = Fetchers({
            "kuwo": {
                "fetcher": "KuWo"
            }
        })

        self.fetcher = fetchers["kuwo"]

    async def test_search(self):

        self.assertIsNone((await self.fetcher.searchSong(searchkey, page, num)).get('error'))

        self.assertIsNone((await self.fetcher.searchAlbum(searchkey, page, num)).get('error'))

        self.assertIsNone((await self.fetcher.searchMV(searchkey, page, num)).get('error'))

    # async def test_comments(self):

    #     self.assertIsNone((await self.fetcher.getComments("33894312", "music", page, num)).get('error'))

    #     self.assertIsNone((await self.fetcher.getComments("32311", "album", page, num)).get('error'))

    #     self.assertIsNone((await self.fetcher.getComments("5436712", "mv", page, num)).get('error'))

    async def test_musicuri(self):

        self.assertIsNone((await self.fetcher.musicuri("728668")).get('error'))

    async def test_mvuri(self):

        self.assertIsNone((await self.fetcher.mvuri("728668")).get('error'))

    async def test_lyric(self):

        self.assertIsNotNone(await self.fetcher.lyric("728668"))

    # async def test_account(self):

    #     self.assertIsNone((await self.fetcher.userlist(userid)).get('error'))

    # async def test_songlist(self):

    #     self.assertIsNone((await self.fetcher.songsinList("24381616", 0, 20)).get('error'))

    # async def test_albumlist(self):

    #     self.assertIsNone((await self.fetcher.songsinAlbum("32311")).get('error'))

    # async def test_picurl(self):

    #     self.assertIsNotNone((await self.fetcher.picurl("32311")))


if __name__ == "__main__":

    unittest.main()
