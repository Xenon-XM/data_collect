import requests
from bs4 import BeautifulSoup

ATTRIBUTES = ['description', 'keywords', 'Description', 'Keywords']

collected_data = []

def keyword_search(url):
    url = "http://"+url
    #entry = {'url': url}
    entry={}
    try:
        r = requests.get(url)
    except Exception as e:
        print('Could not load page {}. Reason: {}'.format(url, str(e)))
        return 0
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        meta_list = soup.find_all("meta")
        for meta in meta_list:
            if 'name' in meta.attrs:
                name = meta.attrs['name']
                if name in ATTRIBUTES:
                    try:
                        entry[name.lower()] = meta.attrs['content']
                    except:
                        entry[name.lower()] = None
        if len(entry) == 3:
            collected_data.append(entry)
        else:
           # print('Could not find all required attributes for URL {}'.format(url))
            collected_data.append(entry)
    else:
        print('Could not load page {}.Reason: {}'.format(url, r.status_code))
    return collected_data
