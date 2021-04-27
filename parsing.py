import requests
import os
import urllib3
import argparse
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def download_image(image_name, folder = 'img/'):
    filename = image_name['image_name']
    url = 'https://tululu.org/{}'.format(filename)
    response = get_response(url)
    filename = filename.split("/")[2]
    catalog_img = os.path.join('{}', '{}').format(folder, filename)

    with open(catalog_img, 'wb') as file:
        file.write(response.content)


def check_for_redirect(response):
    status_code = response.history

    if status_code:
        raise requests.HTTPError(status_code)


def download_txt(response, book_page_information, image_name, folder='books/'):
    catalog_books = os.path.join('{}', '{}.txt').format(sanitize_filename(folder)
    , sanitize_filename(book_page_information['filename']))

    with open(catalog_books, 'w') as file:
        file.write(response.text)

    download_image(image_name)


def get_response(url):
    response = requests.get(url, verify=False)
    response.raise_for_status()
    check_for_redirect(response)
    return response


def parse_book_page(id_book):
    url = 'https://tululu.org/b{}/'.format(id_book)
    response = get_response(url)
    soup = BeautifulSoup(response.text, "html.parser")
    filename = soup.find('table', class_='tabs').find('td', class_='ow_px_td').find('h1').text
    image_name = soup.find('table', class_='tabs').find('td', class_='ow_px_td').find('table').find('img')['src']
    all_comments = soup.find('table', class_='tabs').find('div', class_='texts')
    if all_comments:
        comments = all_comments.find_all('span', class_='black')[0].text
    else:
        comments = None

    genre = soup.find('table', class_='tabs').find('span', class_='d_book').find_all('a')[0].text
    book_page_information = {
        'filename': filename,
        'name_book': filename.split('::')[0],
        'author': filename.split('::')[1],
        'image_name': image_name,
        'comments': comments,
        'genre': genre
    }
    return book_page_information


def get_link_the_book(id_book):
    get_parameter = '?id={}'.format(id_book)
    url = 'https://tululu.org/txt.php{}'.format(get_parameter)
    response = get_response(url)
    check_for_redirect(response)
    return response


def get_a_numeric_argument():
    parser = argparse.ArgumentParser(description='Скачивание книг\картинки с сайта')
    parser.add_argument('start_id', help='id книг от', type=int)
    parser.add_argument('end_id', help='id книг до', type=int)
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = get_a_numeric_argument()
    urllib3.disable_warnings()

    for id_book in range(args.start_id, args.end_id):
        try:
            response = get_link_the_book(id_book) 
            book_page_information = parse_book_page(id_book)
            download_txt(response, book_page_information, book_page_information)
        except requests.HTTPError:
            continue 
