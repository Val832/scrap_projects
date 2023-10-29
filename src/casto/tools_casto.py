def fetch_casto_data (id , session ) : 

     # URL de base du site Castorama.
    BASE = 'https://www.castorama.fr'

    # URL de l'API utilisée pour extraire les données des produits.
    URL = "https://api.kingfisher.com/prod/v1/product-search-bff/products/CAFR"

    # Construction des paramètres 
    cat_id = id['id']
    content_loc = id['path']
    r = BASE + content_loc

    # Paramètres de la requête pour filtrer les résultats.
    querystring = {"channelApiVersion":"v2",
                "filter[category]": cat_id  ,
                "include":"content",
                "page[number]":"1",
                "page[size]":"200",
                "supportMerchTiles":"true"}

    # En-têtes de la requête pour s'authentifier et fournir des informations contextuelles.
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
        "x-dtc": f'sn="v_4_srv_-2D64_sn_DT6PV4C3187S2UCTP5RUK787IAUHIMNI", pc="-64$471313258_896h15vHGQIWCKVDUTMAQDCTATKMDWCORMFABRW-0e0", v="16748137103710K7F1MT3VILA0RAK43A6TIH7G93PT88T",  app="7fad07df8aa3fcc7", r= {r}'
    }

    # Envoie de la requête et conversion de la réponse en format json. 
    response = session.request("GET", URL, headers=headers, params=querystring)
    data = response.json()

    return data

