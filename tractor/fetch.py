import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_html(url):
    response = requests.get(url, verify=False)
    return response.text
