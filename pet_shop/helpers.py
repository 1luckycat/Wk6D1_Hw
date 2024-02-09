import requests
import requests_cache
import json
import os   # added this for the api key
import decimal


requests_cache.install_cache('image_cache', backend='sqlite')

def get_image(search):
    url = "https://google-search72.p.rapidapi.com/imagesearch"

    querystring = {"q": search,"gl":"us","lr":"lang_en","num":"10","start":"0"}

    headers = {
	    "X-RapidAPI-Key": os.environ.get('api_key'),   # !!! paste key given to .env and type os.environ.get('key') - a security measure !!!
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

    querystring = {"name": search}   # dont change the key, is required from the site to get the information

    headers = {
	    "X-RapidAPI-Key": os.environ.get('api_key_animal'),    # !!! paste key given to .env and type os.environ.get('key') - a security measure !!!
	    "X-RapidAPI-Host": "animals-by-api-ninjas.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    data = response.json()

    info_url = ""
    
    if data:
        info_url = data[0]['characteristics']['slogan']
        print(info_url)
    return info_url


 
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return json.JSONEncoder(JSONEncoder, self).default(obj)