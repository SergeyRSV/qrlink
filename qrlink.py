import os
import json
import random
from base64 import b64encode

import hashlib
import requests
import pyqrcode



def handle(data):
    url = 'https://api.imgbb.com/1/upload'
    key = ''

    indata = json.loads(data)

    string = ''

    for keys in indata.keys():
        string += str(keys) + ': ' + str(indata[keys]) + '\n'

    h = hashlib.sha1(string.encode('utf-8'))
    hashstring = str(h.hexdigest())
    hashdec = int(hashstring, 16)
    gen_code = str(hashdec)[:10]

    code = pyqrcode.create(gen_code, encoding='utf-8')
    x = random.random()
    name = (str(x)[14:]) + '.png'
    codesvg = code.png(name, scale=8)

    res = requests.post(
        url,
        data={
            'key': key,
            'image': b64encode(open(name, 'rb').read()),
        }
    )

    os.remove(name)

    indata = json.loads(res.text)
    url = indata['data']
    link = url['url']

    data = {}
    data["data"] = link
    data["code"] = gen_code

    djey = json.dumps(data)

    return djey