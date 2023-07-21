import requests
import time
import random
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.35',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8',
    'Referer': 'https://tiki.vn/nen-thom/c8224',
    'x-guest-token': 'GASLhqtdFo936Dv2OkKfJB0nXI7pwgsj',
    'Connection': 'keep-alive',
    'TE': 'Trailers',
}

params = { 
    'limit': '40',
    'include': 'advertisement',
    'aggregations': '2',
    'trackity_id': '61dec858-ad5a-b5d3-a041-7162594cf5f4',
    'category': '8224',
    'page': '1',  
    'urlKey':  'nen-thom',
}

product_id = []
imgURL= []
for i in range(1, 13):
    params['page'] = i
    response = requests.get('https://tiki.vn/api/personalish/v1/blocks/listings', headers=headers, params=params)#, cookies=cookies)
    if response.status_code == 200:
        print('request success!!!')
        for record in response.json().get('data'):
            (product_id.append({'id': record.get('id')}))
            print(product_id)
           
    #time.sleep(random.randrange(3, 10))

df = pd.DataFrame(product_id)

df.to_csv('product_id_ncds.csv', index=False)