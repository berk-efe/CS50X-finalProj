import os


from cs50 import SQL

import json
import requests

from flask import redirect, render_template, session
from functools import wraps

from typing import Union


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///keepTrack.db")

DEFAULT_SHOPS = [61, 16, 35, 48]  # Steam, Epic Games, GOG, Microsoft Store

API_KEY = os.environ.get('ITAD_API_KEY')

def get_game_by_id(game_id: str) -> Union[dict, None]:

    url = f"https://api.isthereanydeal.com/games/info/v2?id={game_id}&key={API_KEY}"
    response = requests.request("GET", url)
    print(f"Requesting game info for ID: {game_id}, Status Code: {response.status_code}")

    return response.json() if response.status_code == 200 else None

def get_deals(sort:str="-trending", limit:int=6, shops:list[int]=DEFAULT_SHOPS, max_price:int=None, min_cut:int=None, user_id:str=None) -> Union[dict, None]:
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

    url = f"https://api.isthereanydeal.com/deals/v2?country=TR&limit={limit*2}&sort={sort}&shops={shop_str}&key={API_KEY}"

    payload = {}
    headers = {
    'Cookie': 'PHPSESSID=sv6vbd83btan3s8ipoootf0b57'
    }

    response = json.loads(requests.request("GET", url, headers=headers, data=payload).text)

    data=[]
    
    # There is an important error with deal['url']
    # i got timed out
    
    # further tests shows that it works okay with steam and epicgames

    _count = 0
    list_of_games = response['list']
    for game in list_of_games:
        if game and _count < limit:
            _count += 1
                
            info={}
            info['price'] = game['deal']['price'] # {amount, currency}
            info['cut'] = game['deal']['cut']
            
            if max_price and info['price']['amount'] > max_price:
                continue
            if min_cut and info['cut'] < min_cut:
                continue
            
            info['id'] = game['id']
            info['slug'] = game['slug']
            
            info['title'] = game['title']
            
            try:
                info['boxart'] = game['assets']['boxart']
            except KeyError:
                continue
            
            info['banner'] = game['assets']['banner145']
            
            info['shop'] = game['deal']['shop'] # {id, name}
            
            info['regular'] = game['deal']['regular'] # {amount, currency}
            
            info['url'] = game['deal']['url']
            
            if user_id:
                favs = db.execute("SELECT * FROM deals WHERE user_id = ? AND game_id = ?", user_id, info['id'])
                info['is_fav'] = len(favs) > 0
            else:
                info['is_fav'] = False
            
            data.append(info)

    return data if data else None

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function
