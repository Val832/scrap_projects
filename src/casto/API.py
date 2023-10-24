import requests
import pandas as pd 
"""
url = "https://api.kingfisher.com/v2/mobile/products/CAFR"

querystring = {"filter\\[category\\]":"cat_id_3","include":"content","page\\[number\\]":"1","page\\[size\\]":"200","supportMerchTiles":"true"}

headers = {
    "cookie": "TS013aa2d6=011543659b5b95a2e47e614ad11b7b63349130650f02236b21f3be8742730709c71a06afc94ac17c4b3ace84dab199744dba1b1cd9; TSce5a380a027=08016f2e84ab20009cd2b0da30e4e313a718dc7472e197e6c6566f50be083affd56abb6d72378cc2086c02a65f113000dc1d650faa9682e099ff3e0c97857373a41099b9e0a09b634606bc45671954285ec60ec1fd136b28bae00b38ee508dd1",
    "Accept": "application/json, text/plain, */*",
    "Authorization": "Atmosphere atmosphere_app_id=kingfisher-o4ITR0sWAyCVQBraQf4Es61jHV3dN4oO9UwJQMrS",
    "Origin": "https://www.castorama.fr",
    "Referer": "https://www.castorama.fr/",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15",
    "X-Context-Location": "/jardin-et-terrasse/abri-de-jardin-garage-carport-et-rangement/abri-de-jardin/cat_id_3.cat",
    "x-dtc": 'sn="v_4_srv_-2D56_sn_SIRLOMB8SQLUTVLBINRVL7SJJ8CSIBP8", pc="https://www.castorama.fr/jardin-et-terrasse/abri-de-jardin-garage-carport-et-rangement/abri-de-jardin/cat_id_3.cat',
    "Content-Type": "application/json"
}

response = requests.request("GET", url, headers=headers, params=querystring)

data = response.json()

print(data)"""

url = "https://api.kingfisher.com/prod/v1/product-search-bff/products/CAFR"

querystring = {"channelApiVersion":"v2","filter[category]": "cat_id_3","include":"content","page[number]":"1","page[size]":"200","supportMerchTiles":"true"}

payload = ""
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
    "X-Context-Location": "/jardin-et-terrasse/abri-de-jardin-garage-carport-et-rangement/abri-de-jardin/cat_id_3.cat",
    "x-dtc": 'sn="v_4_srv_-2D64_sn_DT6PV4C3187S2UCTP5RUK787IAUHIMNI", pc="-64$471313258_896h15vHGQIWCKVDUTMAQDCTATKMDWCORMFABRW-0e0", v="16748137103710K7F1MT3VILA0RAK43A6TIH7G93PT88T", app="7fad07df8aa3fcc7", r="https://www.castorama.fr/jardin-et-terrasse/abri-de-jardin-garage-carport-et-rangement/abri-de-jardin/cat_id_3.cat"'
}

response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
data = response.json()
print(data)