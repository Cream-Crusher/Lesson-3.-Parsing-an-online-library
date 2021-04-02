import requests
from bs4 import BeautifulSoup


def get_the_post_page():
    url = 'https://www.franksonnenbergonline.com/blog/are-you-grateful/'
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_site_text(soup):
    title_tag = soup.find('main').find('header').find('h1')
    title_text = title_tag.text
    return title_text


def get_the_link_images(soup):
    title_link = soup.find('img', class_='attachment-post-image')['src']
    return title_link


def get_the_text_the_post(soup):
    entrance = 0
    post_text = soup.find('main').find('article').find('div', class_='entry-content')\
    .find('p').text.split('::')[entrance]
    return post_text


if __name__ == '__main__':
    soup = get_the_post_page()
    print(get_site_text(soup))
    print(get_the_link_images(soup))
    print(get_the_text_the_post(soup))
