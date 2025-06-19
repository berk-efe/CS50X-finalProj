import os

import json
import requests

from typing import Union

DEFAULT_SHOPS = [61, 16, 35, 48]  # Steam, Epic Games, GOG, Microsoft Store

def get_deals(sort:str="-trending", limit:int=6, shops:list[int]=DEFAULT_SHOPS) -> Union[dict, None]:
    """Get deals, you can get deals **sorting** and **limiting**<br>There are several sorting **options** such as:<br>
    **trending:** get the most trending deals
    <br>
    **price:** get the cheapest deals
    <br>
    **cut:** get deals with the highest sale rate
    <br>
    ...
    <br>
    you can reverse sort them with minus(-)
    
    Args:
        sort (str, optional): sorting option. Defaults to "-trending".
        limit (int, optional): limit. Defaults to 6.
        shops (list[int], optional): list of shop IDs to filter deals. Defaults to DEFAULT_SHOPS.
    
    Returns:
        Union[dict, None]: Returns a dictionary with game data or None if an error occurs.
    
    """

    """
    id
    slug
    
    title
    assets['boxart']
    assets['banner300']
    
    deal['shop'] {id, name}
    
    deal['price'] {amount, currency}
    deal['regular'] {amount, currency}
    
    deal['cut']
    deal['url']
    """
    
    shop_str = ','.join(map(str, shops))

    url = f"https://api.isthereanydeal.com/deals/v2?country=TR&limit={limit}&sort={sort}&shops={shop_str}&key={os.environ.get('ITAD_API_KEY')}"

    payload = {}
    headers = {
    'Cookie': 'PHPSESSID=sv6vbd83btan3s8ipoootf0b57'
    }

    response = json.loads(requests.request("GET", url, headers=headers, data=payload).text)

    data=[]
    
    # There is an important error with deal['url']
    # i got timed out
    
    # further tests shows that it works okay with steam and epicgames

    list_of_games = response['list']
    for game in list_of_games:
        if game:    
            info={}
            
            info['id'] = game['id']
            info['slug'] = game['slug']
            
            info['title'] = game['title']
            info['boxart'] = game['assets']['boxart']
            info['banner'] = game['assets']['banner145']
            
            info['shop'] = game['deal']['shop'] # {id, name}
            
            info['price'] = game['deal']['price'] # {amount, currency}
            info['regular'] = game['deal']['regular'] # {amount, currency}
            
            info['cut'] = game['deal']['cut']
            info['url'] = game['deal']['url']
            
            data.append(info)

    return data if data else None

