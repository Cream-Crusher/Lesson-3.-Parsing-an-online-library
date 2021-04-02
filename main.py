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


def download_txt(response, book_page_information, image_name, folder='books/'):

    information_obtained_on_the_website = {
        'url': response,
        'filename': sanitize_filename(book_page_information['filename']),
        'folder': sanitize_filename(folder),
        'image_name': book_page_information['image_name']
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


def parse_book_page(id_book):
    entrance = 0
    url = 'https://tululu.org/b{}/'.format(id_book)
    response = get_response(url)
    soup = BeautifulSoup(response.text, 'lxml')

    filename = soup.find('table', class_='tabs')\
    .find('td', class_='ow_px_td').find('h1').text

    image_name = soup.find('table', class_='tabs')\
    .find('td', class_='ow_px_td').find('table').find('img')['src']

    comments = soup.find('table', class_='tabs')\
    .find('div', class_='texts').find_all('span', class_='black')[entrance].text

    genre = soup.find('table', class_='tabs')\
    .find('span', class_='d_book').find_all('a')[entrance].text

    book_page_information = {
        'filename': filename,
        'name_book': filename.split('::')[0],
        'author': filename.split('::')[1],
        'image_name': image_name,
        'comments': comments,
        'genre': genre
    }
    return book_page_information


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
            book_page_information = parse_book_page(id_book)
            download_txt(response, book_page_information, book_page_information)
            print(book_page_information)
        except:
            pass
