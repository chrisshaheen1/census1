import requests
from bs4 import BeautifulSoup
import lxml
import json

url='https://api.census.gov/data.html'

def refresh_census_datasets():
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    table=soup.find('table')
    headers = [th.text.rstrip() for th in table.find('tr').find_all('th')]
    rows=table.find_all('tr')[1:]
    dataset=[]
    for row in rows:
        tds=row.find_all('td')
        if len(tds) != len(headers):
            continue

        tmp={}
        tmp['title']=row.find_all('td')[0].text
        tmp['description']=row.find_all('td')[1].text
        tmp['link']=row.find_all('td')[-1].find('a')['href']
        dataset.append(tmp)
    with open('census.json', 'w') as f:
        json.dump(dataset, f, indent=4)
    return dataset

def get_census_datasets():
    with open('census.json', 'r') as f:
        ds=json.load(f)
        ns=[{'title':d['title'], 'link':d['link']} for d in ds]
        # return ds # Uncomment this if you want the full dataset
        return ns
if __name__ == '__main__':
    refresh_census_datasets()
