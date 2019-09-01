
from flask import Flask,make_response,request

app = Flask(__name__)

headers={
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}


kg_cook = {
    "kg_mid": 'af7c2445064307fc9ef998eff735b0d1',
    "Hm_lvt_aedee6983d4cfc62f509129360d6bb3d": '1565879171,1566012408,1566137661,1566286143',
    "kg_dfid": '10P9yI2EfXk70MCKMa4TFGjg'
}


def CORS_response_json(data):
    response = make_response(data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return response

@app.route('/kugou/info', methods = ['GET'])
def kugou(_hash):
    _hash = request.args.get('hash')

    params = {
        "r": 'play/getdata',
        "hash": _hash
    }
    # this api is from kugou
    api = "https://wwwapi.kugou.com/yy/index.php"

    result = requests.get(api, headers=headers, cookies = kg_cook, params=params).text
    
    return CORS_response_json(result)


if __name__ == '__main__':
    app.run(host='127.0.0.1',port=8081)