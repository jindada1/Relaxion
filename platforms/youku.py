'''
on  :  2019-10-18
by  :  Kris Huang

for : get data from youku directly
'''

try:
    from .baseparser import Video
except:
    from baseparser import Video



class YouKu(Video):

    # from you-get: https://github.com/soimort/you-get
    # Last updated: 2017-10-13
    stream_types = [
        {'id': 'hd3',      'container': 'flv', 'video_profile': '1080P'},
        {'id': 'hd3v2',    'container': 'flv', 'video_profile': '1080P'},
        {'id': 'mp4hd3',   'container': 'mp4', 'video_profile': '1080P'},
        {'id': 'mp4hd3v2', 'container': 'mp4', 'video_profile': '1080P'},

        {'id': 'hd2',      'container': 'flv', 'video_profile': '超清'},
        {'id': 'hd2v2',    'container': 'flv', 'video_profile': '超清'},
        {'id': 'mp4hd2',   'container': 'mp4', 'video_profile': '超清'},
        {'id': 'mp4hd2v2', 'container': 'mp4', 'video_profile': '超清'},

        {'id': 'mp4hd',    'container': 'mp4', 'video_profile': '高清'},
        # not really equivalent to mp4hd
        {'id': 'flvhd',    'container': 'flv', 'video_profile': '渣清'},
        {'id': '3gphd',    'container': 'mp4', 'video_profile': '渣清'},

        {'id': 'mp4sd',    'container': 'mp4', 'video_profile': '标清'},
        # obsolete?
        {'id': 'flv',      'container': 'flv', 'video_profile': '标清'},
        {'id': 'mp4',      'container': 'mp4', 'video_profile': '标清'},
    ]

    def __init__(self, thirdparty = None):

        Video.__init__(self, name = "YouKu", third = thirdparty)

        self.page = None
        self.password = None

        self.dispatcher_url = 'vali.cp31.ott.cibntv.net'

        self.ccode = '0519'
        # Found in http://g.alicdn.com/player/ykplayer/0.5.64/youku-player.min.js
        # grep -oE '"[0-9a-zA-Z+/=]{256}"' youku-player.min.js
        self.ckey = 'DIl58SLFxFNndSV1GFNnMQVYkx1PP5tKe1siZu/86PR1u/Wh1Ptd+WOZsHHWxysSfAOhNJpdVWsdVJNsfJ8Sxd8WKVvNfAS8aS8fAOzYARzPyPc3JvtnPHjTdKfESTdnuTW6ZPvk2pNDh4uFzotgdMEFkzQ5wZVXl2Pf1/Y6hLK0OnCNxBj3+nb0v72gZ6b0td+WOZsHHWxysSo/0y9D2K42SaB8Y/+aD2K42SaB8Y/+ahU+WOZsHcrxysooUeND'
        self.utid = None

        self.headers = {
            "Referer": 'http://v.youku.com',
            "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
        }

    def change_cdn(self, url):
        # from you-get
        if self.dispatcher_url in url:
            return url

        elif 'k.youku.com' in url:
            return url

        else:
            url_seg_list = list(self.split_url(url))
            url_seg_list[1] = self.dispatcher_url
            return self.unsplit_url(url_seg_list)

    async def videouri(self, _id):

        if not self.utid:
            
            self.utid = await self.fetch_cna()
        
        params = {
            "vid": _id,
            "ccode": self.ccode,
            "client_ip": '192.168.1.1',
            "utid": self.utid,
            "client_ts": self.now_str,
            "ckey": self.quote_cna(self.ckey)
        }
        
        api = "https://ups.youku.com/ups/get.json"

        jsonresp = await self._asyncGetJsonHeaders(api, params=params)

        resp_data = jsonresp['data']

        data_error = resp_data.get('error')

        if data_error:
            return data_error

        stream_types = dict([(i['id'], i) for i in self.stream_types])
        audio_lang = resp_data['stream'][0]['audio_lang']

        results = {}

        for stream in resp_data['stream']:
            stream_id = stream['stream_type']
            is_preview = False
            if stream_id in stream_types and stream['audio_lang'] == audio_lang:
                if 'alias-of' in stream_types[stream_id]:
                    stream_id = stream_types[stream_id]['alias-of']

                if stream_id not in results:
                    results[stream_id] = {
                        'container': stream_types[stream_id]['container'],
                        'video_profile': stream_types[stream_id]['video_profile'],
                        'size': stream['size'],
                        'pieces': [{
                            'segs': stream['segs']
                        }],
                        'm3u8_url': stream['m3u8_url']
                    }
                    src = []
                    for seg in stream['segs']:
                        if seg.get('cdn_url'):
                            src.append(self.change_cdn(seg['cdn_url']))
                        else:
                            is_preview = True
                    results[stream_id]['src'] = src
                else:
                    results[stream_id]['size'] += stream['size']
                    results[stream_id]['pieces'].append({
                        'segs': stream['segs']
                    })
                    src = []
                    for seg in stream['segs']:
                        if seg.get('cdn_url'):
                            src.append(self.change_cdn(seg['cdn_url']))
                        else:
                            is_preview = True
                    results[stream_id]['src'].extend(src)

            if is_preview:
                print('{} is a preview'.format(stream_id))

        return results


    async def fetch_cna(self):

        url = 'http://log.mmstat.com/eg.js'

        headers = await self._asyncGetHeaders(url)

        for header in headers:
            if header.lower() == 'set-cookie':
                n_v = headers[header].split(';')[0]
                name, value = n_v.split('=')
                if name == 'cna':
                    return self.quote_cna(value)
        
        print('It seems that the client failed to fetch a cna cookie. Please load your own cookie if possible')
        return self.quote_cna('DOG4EdW4qzsCAbZyXbU+t7Jt')



async def __test():

    p = YouKu()
    searchkey = "火影"

    # https://v.youku.com/v_show/id_XNTQwMTgxMTE2.html?spm=a2h1n.8261147.0.0&s=cc001f06962411de83b1
    vid = "XNTQwMTgxMTE2"
    
    '''
    '''
    
    # print(await p.fetch_cna())
    print((await p.videouri(vid)).keys())


if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(__test())
    loop.close()
