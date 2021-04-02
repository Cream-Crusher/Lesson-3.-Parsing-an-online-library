import requests
import os
import urllib3
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from random import sample


def download_image(information_obtained_on_the_website, folder = 'img/'):
    filename = information_obtained_on_the_website['image_name']
    url = 'https://tululu.org/{}'.format(filename)
    response = get_response(url)
    filename = filename.split("/")[2]
    catalog_img = os.path.join('{}', '{}').format(folder, filename)

    with open(catalog_img, 'wb') as file:
        file.write(response.content)


def check_for_redirect(response):
    text_error = response.history
    
    if text_error:
        raise requests.HTTPError(response.history)


def download_txt(response, filename, image_name, folder='books/'):

    information_obtained_on_the_website = {
        'url': response,
        'filename': sanitize_filename(filename),
        'folder': sanitize_filename(folder),
        'image_name': image_name
    }
    catalog_books = os.path.join('{}', '{}.txt').format(information_obtained_on_the_website['folder']\
    , information_obtained_on_the_website['filename'])

    with open(catalog_books, 'w') as file:
        file.write(information_obtained_on_the_website['url'].text)

    download_image(information_obtained_on_the_website)


def get_response(url):
    response = requests.get(url, verify=False)
    response.raise_for_status()
    return response


def get_the_necessary_elements(id_book):
    url = 'https://tululu.org/b{}/'.format(id_book)
    response = get_response(url)
    soup = BeautifulSoup(response.text, 'lxml')

    name_book = soup.find('table', class_='tabs')\
    .find('td', class_='ow_px_td').find('h1').text

    image_name = soup.find('table', class_='tabs')\
    .find('td', class_='ow_px_td').find('table').find('img')['src']

    comments = soup.find('table', class_='tabs')\
    .find('div', class_='texts').find_all('span', class_='black')[0].text

    return name_book, image_name, comments


def get_link_the_text_book(id_book):
    url = 'https://tululu.org/txt.php?id={}'.format(id_book)
    response = get_response(url)
    check_for_redirect(response)
    return response


if __name__ == '__main__':
    urllib3.disable_warnings()
    random_numbers = sample(range(1, 10), 8)

    for id_book in random_numbers:
        try:        
            response = get_link_the_text_book(id_book)
            filename, image_name, comments = get_the_necessary_elements(id_book)
            download_txt(response, filename, image_name)
            print(filename.split('::')[0])
            print(filename.split('::')[1])
            print(comments)
        except:
            pass
