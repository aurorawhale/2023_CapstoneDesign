from fmb.settings import API_KEY
import requests

client_id = API_KEY['naver_id']
client_secret = API_KEY['naver_secret']
header = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret,
          'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}


def papago_trans(st, text):
    url = "https://openapi.naver.com/v1/papago/n2mt"
    params = {'source': st, 'target': 'ko', 'text': text}
    result = requests.post(url, headers=header, params=params).json()
    if 'errorCode' in result:
        return -1
    return result['message']['result']['translatedText']


def is_korean(text):
    url = "https://openapi.naver.com/v1/papago/detectLangs"
    params = {'query': text}
    result = requests.post(url, headers=header, params=params).json()
    if 'errorCode' in result:
        return -1
    return result['langCode']
