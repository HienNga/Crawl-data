import pandas as pd
import requests
import time
import random
from tqdm import tqdm

cookies = {
'TIKI_RECOMMENDATION':	'6ff7407f5e0377e374458ea6935ab60a',
'TKSESSID':	'f97caf587f7f85985ffe973dde1042b8',
'_trackity':	'61dec858-ad5a-b5d3-a041-7162594cf5f4',
'_gcl_au':	'1.1.910516200.1683687384',
'__uidac':	'4501de22001e23a8c3f6fb694a37cfd1',
'__iid':	'749',
'__iid':	'749',
'__su':	'0',
'__su':	'0',
'TOKENS':	'{%22access_token%22:%22GASLhqtdFo936Dv2OkKfJB0nXI7pwgsj%22}',
'delivery_zone':	'Vk4wMzkwMDYwMDE=',
'_gid':	'GA1.2.1193196888.1684136122',
'tiki_client_id':	'7.496.131.101.683.680.000',
'_hjSessionUser_522327':	'eyJpZCI6IjQ5OTQ2MmI2LTIyNDUtNTRmMy1hZTI5LTEwYjBhY2MzZmYwOSIsImNyZWF0ZWQiOjE2ODM2ODczODY1MDEsImV4aXN0aW5nIjp0cnVlfQ==',
'_gaexp':	'GAX1.2.C-c7Bj3wRv6XIWSxxHvkgQ.19558.0',
'_hjIncludedInSessionSample_522327':	'0',
'_hjSession_522327':	'eyJpZCI6ImQ0NmMxMzkzLTY0ZDktNDU2MC05ZWE2LWUzOGRhNTcxYmMzOSIsImNyZWF0ZWQiOjE2ODQxNDc4OTg4NzUsImluU2FtcGxlIjpmYWxzZX0=',
'_hjAbsoluteSessionInProgress':	'0',
'amp_99d374':	'UsxqFr01eoaKi0EXD6qQNy...1h0fgiqit.1h0fgq799.1f.29.3o',
'_ga':	'GA1.1.749613110.1683687240',
'cto_bundle':	'NmT-gF85cDNXajBZTGpHQlVTbkRJT051MWVoaUs0b050NkVrVkNmYXVIUjZkSW9PRU5xdUpmVSUyRmpJJTJGQUdkeTJtWW5oUGF3Y0hDeVA0V2NuOUxWa3ZBTmhZcGs2SWNBZCUyQlNmNGJDVmc5Q1BmTHAzY2wzMnhDWlBuWnBvSyUyQmJsV05McmNN',
'_ga_GSD4ETCY1D':	'GS1.1.1684147898.3.1.1684148408.60.0.0',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'vi-VN,vi;q=0.8,en-US;q=0.5,en;q=0.3',
    'Referer': 'https://tiki.vn/nen-thom-tinh-dau-cao-cap-khong-khoi-an-toan-candle-cup-white-tea-s-100g-kg-nap-p118896584.html?itm_campaign=tiki-reco_UNK_DT_UNK_UNK_tiki-listing_UNK_p-category-mpid-listing-v1_202305140600_MD_batched_PID.118896585&itm_medium=CPC&itm_source=tiki-reco&spid=118896585',
    'x-guest-token': 'GASLhqtdFo936Dv2OkKfJB0nXI7pwgsj',
    'Connection': 'keep-alive',
    'TE': 'Trailers',
}

params = (
    ('platform', 'web'),
    ('spid', '118896585')
    #('include', 'tag,images,gallery,promotions,badges,stock_item,variants,product_links,discount_tag,ranks,breadcrumbs,top_features,cta_desktop'),
)

def parser_product(json):
    d = dict()
    #d['id'] = json.get('id')
    d['name'] = json.get('name')
   
    d['short_description'] = json.get('short_description')
    d['price'] = json.get('price')

    #d['discount'] = json.get('discount')
    #d['discount_rate'] = json.get('discount_rate')

    d['order_count'] = json.get('order_count')
    d['inventory_status'] = json.get('inventory_status')
    d['is_visible'] = json.get('is_visible')
    d['stock_item_qty'] = json.get('stock_item').get('qty')
    d['stock_item_max_sale_qty'] = json.get('stock_item').get('max_sale_qty')
    d['product_name'] = json.get('meta_title')
    #d['brand_id'] = json.get('brand').get('id')
    d['brand_name'] = json.get('brand').get('name')
    d['thumbnail_url']= json.get('thumbnail_url')
    return d


df_id = pd.read_csv('product_id_ncds.csv')
p_ids = df_id.id.to_list()
print(p_ids)
result = []
for pid in tqdm(p_ids, total=len(p_ids)):
    response = requests.get('https://tiki.vn/api/v2/products/{}'.format(pid), headers=headers, params=params, cookies=cookies)
    if response.status_code == 200:
        print('Crawl data {} success !!!'.format(pid))
        result.append(parser_product(response.json()))
    time.sleep(0.3)  
    # time.sleep(random.randrange(3, 5))
#print(result)
df_product = pd.DataFrame(result)
df_product.to_csv('crawled_data_ncds.csv', index=False)
