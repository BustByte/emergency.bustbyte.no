import requests

class Fetcher:

    user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:15.0) ' \
               + 'Gecko/20100101 Firefox/15.0.1'

    headers = {
        'accept-language': 'nb-NO,nb;q=0.8,no;q=0.6,nn;'
    }

    @classmethod
    def request(cls, url):
        response = requests.get(url, headers=Fetcher.headers)
        return response.text
