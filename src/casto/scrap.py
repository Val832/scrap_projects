import pandas as pd 
import requests 
import json 


cat = pd.read_csv('id.csv')
cat = cat.drop('Unnamed: 0' ,axis = 1 )

base = 'https://www.castorama.fr'

print(len(cat))
e = 0
query_list = []




while e != len(cat) : 

    cat_id = cat['id'][e]
    content_loc = cat['path'][e]
    r = base + content_loc

    url = "https://api.kingfisher.com/prod/v1/product-search-bff/products/CAFR"

    querystring = {"channelApiVersion":"v2","filter[category]": cat_id  ,"include":"content","page[number]":"1","page[size]":"200","supportMerchTiles":"true"}

    headers = {
        "cookie": "TS013aa2d6=011543659ba2f180aea3ed106a302f1177feaae80664b510fa08066096b8a6e9edb39cb9bc49da26709b5751a09e0ccbb7c368e320; TSce5a380a027=08016f2e84ab20007f3441d17e1ec166d17880b09688c8d79947b5133c07d36fc64a59724a589171087092cc8a11300066c97d9a8a320061bfef6350baf5a906fa5cb6be47f585bec634bdbec859dffabbd7b5eabc9121a128f8026a58a11da5",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://www.castorama.fr",
        "Authorization": "Atmosphere atmosphere_app_id=kingfisher-o4ITR0sWAyCVQBraQf4Es61jHV3dN4oO9UwJQMrS",
        "Referer": "https://www.castorama.fr/",
        "Accept-Language": "fr-FR,fr;q=0.9",
        "Host": "api.kingfisher.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "X-Context-Location": f"{content_loc}",
        "x-dtc": f'sn="v_4_srv_-2D64_sn_DT6PV4C3187S2UCTP5RUK787IAUHIMNI", pc="-64$471313258_896h15vHGQIWCKVDUTMAQDCTATKMDWCORMFABRW-0e0", v="16748137103710K7F1MT3VILA0RAK43A6TIH7G93PT88T", app="7fad07df8aa3fcc7", r= {r}'
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()
    print(data)

    i  = 0 

    while i != len(data['data']) : 

        query = data['data'][i]['attributes']
        del query["mediaObjects"]
        query_list.append(query)
        
        i = i+1

    e = e + 1 
    print(e)
            

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(query_list, f, ensure_ascii=False, indent=4)


