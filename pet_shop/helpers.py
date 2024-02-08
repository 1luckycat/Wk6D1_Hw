import requests
import requests_cache
import json


requests_cache.install_cache('image_cache', backend='sqlite')

def get_image(search):
    url = "https://google-search72.p.rapidapi.com/imagesearch"

    querystring = {"q": search,"gl":"us","lr":"lang_en","num":"10","start":"0"}

    headers = {
	    "X-RapidAPI-Key": "dd03695a23msh3f0275a27580377p1bec69jsn1a5632f1e109",
	    "X-RapidAPI-Host": "google-search72.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    data = response.json()

    img_url = ""

    if 'items' in data.keys():
        img_url = data['items'][0]['originalImageUrl']

    return img_url


# tried to add a second API for animal descriptions
def get_info(search):
    url = "https://animals-by-api-ninjas.p.rapidapi.com/v1/animals"

    querystring = {"animal_type": search}

    headers = {
	    "X-RapidAPI-Key": "dd03695a23msh3f0275a27580377p1bec69jsn1a5632f1e109",
	    "X-RapidAPI-Host": "animals-by-api-ninjas.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    data = response.json()

    info_url = ""

    if 'items' in data.keys():
        info_url = data['items'][0]['characteristics']
    return info_url


# I could not figure out how to display it in the description portion.  The website is saying I have made 
# API calls, but I couldnt get it to display on the shop.  