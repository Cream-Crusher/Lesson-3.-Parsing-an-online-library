import requests
import os
import urllib3
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from random import sample


def check_for_redirect(response):
    text_error = response.history
    
    if text_error:
        raise requests.HTTPError(response.history)


def download_txt(response, filename, folder='books/'):

    information_for_saving_text = {
        'url': response,
        'filename': sanitize_filename(filename),
        'folder': sanitize_filename(folder)
    }
    directory = os.path.join('{}', '{}.txt').format(information_for_saving_text['folder']\
    , information_for_saving_text['filename'])

    with open(directory, 'w') as file:
        file.write(information_for_saving_text['url'].text)


def get_response(url):
    response = requests.get(url, verify=False)
    response.raise_for_status()
    return response


def get_name_book(id_book):
    url = 'https://tululu.org/b{}/'.format(id_book)
    response = get_response(url)
    soup = BeautifulSoup(response.text, 'lxml')
    name_book = soup.find('table', class_='tabs')\
    .find('td', class_='ow_px_td').find('h1').text
    return name_book


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
            filename = get_name_book(id_book)
            download_txt(response, filename)
        except:
            pass
