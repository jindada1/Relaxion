
from flask import Flask,make_response,request
import requests
import json

app = Flask(__name__)

headers={
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}


kg_cook = {
    "kg_mid": 'af7c2445064307fc9ef998eff735b0d1',
    "Hm_lvt_aedee6983d4cfc62f509129360d6bb3d": '1565879171,1566012408,1566137661,1566286143',
    "kg_dfid": '10P9yI2EfXk70MCKMa4TFGjg'
}

kugoucache = {}

@app.route('/kugou/playres', methods = ['GET'])
def kugou():
    _hash = request.args.get('hash')
    _key = request.args.get('key')

    validkeys = ["play_url", "lyrics", "img"]

    params = {
        "r": 'play/getdata',
        "hash": _hash
    }
    # this api is from kugou
    api = "https://wwwapi.kugou.com/yy/index.php"

    
    if not _key:

        result = requests.get(api, headers=headers, cookies = kg_cook, params=params).text
        return result

    if not _key in validkeys:

        return "invalid key %s" % _key

    if _hash in kugoucache.keys():
        print('hit cache')
        return kugoucache[_hash][_key]

    # store cache here
    result = requests.get(api, headers=headers, cookies = kg_cook, params=params).text

    data = json.loads(result)['data']

    new = {}
    for k in validkeys:
        new[k] = data[k]

    kugoucache[_hash] = new

    return new[_key]
    


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8081, debug=True)