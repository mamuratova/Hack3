import requests
from bs4 import BeautifulSoup

data_list = []


def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.1) Gecko/2008070208 Firefox/3.0.1'
    }
    response = requests.get(url, headers=headers)
    return response.text


def parsing_neman(html):
    soup = BeautifulSoup(html, 'lxml')
    news = soup.find('div', class_="ty-compact-list").find_all('div', class_="ty-compact-list__item")
    for new in news:
        try:
            title = new.find('div', class_='ty-compact-list__title').find('bdi').text.strip()
        except:
            title = 'no title'

        try:
            photo = new.find('div', class_='ty-compact-list__image').find('a').find('img').get('src')
        except Exception as e:
            print(e)

        try:
            price = new.find('div', class_='ty-compact-list__price').find('span', class_="ty-price").find('bdi').text
        except:
            price = 'no price'

        try:
            link = new.find('div', class_='ty-compact-list__title').find('bdi').find('a').get('href')
        except:
            link = 'no link'

        data = {'title': title, 'link': link, 'photo': photo, 'price': price}
        data_list.append(data)

    return data_list


def pars():
    url = 'https://neman.kg/lekarstvennye-sredstva'
    data_list.clear()
    return parsing_neman(get_html(url))