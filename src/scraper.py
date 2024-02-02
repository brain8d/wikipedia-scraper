# Script for wikipedia scraper
import requests, json, re
from bs4 import BeautifulSoup

class WikipediaScraper:
    '''
    base_url: str containing the base url of the API (https://country-leaders.onrender.com)
    country_endpoint: str → /countries endpoint to get the list of supported countries
    leaders_endpoint: str → /leaders endpoint to get the list of leaders for a specific country
    cookies_endpoint: str → /cookie endpoint to get a valid cookie to query the API
    leaders_data: dict is a dictionary where you store the data you retrieve before saving it into the JSON file
    cookie: object is the cookie object used for the API calls
    ):
    '''
    def __init__(self, base_url: str, country_endpoint: str, leaders_endpoint: str, cookies_endpoint: str, status_endpoint: str, cookie = None):
        self.base_url = base_url
        self.country_endpoint = country_endpoint
        self.leaders_endpoint = leaders_endpoint
        self.cookies_endpoint = cookies_endpoint
        self.leaders_data = ""
        self.status_endpoint = status_endpoint

    def check_status(self):
        status = requests.get(self.base_url+self.status_endpoint)
        if status.status_code == 200:
            return status.text
        else:
            return status.status_code

    def get_cookie(self):
        ''' gets cookie for the API '''
        cookie = requests.get(self.base_url+self.cookies_endpoint)
        return cookie.cookies

    def check_cookie(self):
        ''' checks cookie status'''
        cookie_check = requests.get(self.base_url+"/check", cookies=self.get_cookie())
        return cookie_check

    def get_countries(self):
        ''' gets a list of countries supported by the API '''
        countries = requests.get(self.base_url+self.country_endpoint, cookies=self.get_cookie())
        return countries


    def get_leaders(self,  country: str):
        '''get leaders of specified country, does not return anything but populates self.leaders_data '''
        leaders = {'country': country}
        leader = requests.get(self.base_url+self.leaders_endpoint, cookies=self.get_cookie(), params=leaders)
        self.leaders_data = json.loads(leader.text)


    def get_first_paragraph(self, wikipedia_url: str) -> str:
        ''' gets the first paragraph on leaders' wikipedia URL, uses the BOLD letters to identify first paragraph '''
        r = requests.get(wikipedia_url)
        soup = BeautifulSoup(r.text, "html.parser")
        for tag in soup.find_all("p"):
            if re.search(r'<p><b>(.*)<\/b>', str(tag)):
                return tag.text   #re.sub(r"<[^>]*>", r"", self.paragraph)


    def to_json_file(self, filepath: str) -> None:
        ''' Saves data structure into JSON file in filepath '''
        with open(filepath, "w") as output:
            json.dump(self.leaders_data, output)  # put the created file here
        



