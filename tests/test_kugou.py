import unittest
from music import Fetchers

searchkey = "周杰伦"
page = 2
num = 10
songhash = "382DC60D2879205633FBB7F2685D9840"
gbqq = "5FCE4CBCB96D6025033BCE2025FC3943"
mvhash = "1b43baaf79c20489c85def55e2ba7af0"


class TestPlatforms(unittest.IsolatedAsyncioTestCase):

    def __init__(self, args):

        super().__init__(args)

        fetchers = Fetchers({
            "kugou": {
                "fetcher": "KuGou"
            }
        })

        self.fetcher = fetchers["kugou"]

    async def test_search(self):

        self.assertIsNone((await self.fetcher.searchSong(searchkey, page, num)).get('error'))

        self.assertIsNone((await self.fetcher.searchAlbum(searchkey, page, num)).get('error'))

        self.assertIsNone((await self.fetcher.searchMV(searchkey, page, num)).get('error'))

    # async def test_comments(self):

    #     self.assertIsNone((await self.fetcher.getComments(songhash, "music", page, num)).get('error'))

    #     self.assertIsNone((await self.fetcher.getComments("23509815", "album", page, num)).get('error'))

    #     self.assertIsNone((await self.fetcher.getComments("0c28d3658d3ec86e9d033c80d9d8e9da", "mv", page, num)).get('error'))

    async def test_musicuri(self):

        self.assertIsNone((await self.fetcher.musicuri(songhash)).get('error'))

    async def test_mvuri(self):

        self.assertIsNone((await self.fetcher.mvuri(mvhash)).get('error'))

    async def test_lyric(self):

        self.assertIsNotNone(await self.fetcher.lyric(gbqq))

    # async def test_account(self):

    #     self.assertIsNone((await self.fetcher.userlist(userid)).get('error'))

    async def test_songlist(self):

        self.assertIsNone((await self.fetcher.songsinList("547134", page, num)).get('error'))

    async def test_albumlist(self):

        self.assertIsNone((await self.fetcher.songsinAlbum("23509815")).get('error'))

    async def test_picurl(self):

        self.assertIsNotNone((await self.fetcher.picurl("32311")))


if __name__ == "__main__":

    unittest.main()
