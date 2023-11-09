from fmb.settings import API_KEY
import requests

rest_api_key = API_KEY['kakao_rest_key']
header = {'Authorization': 'KakaoAK ' + rest_api_key}


def get_books(params):
    url = "https://dapi.kakao.com/v3/search/book"
    result = requests.get(url, headers=header, params=params).json()
    if 'errorType' in result:
        return -1
    else:
        return result
