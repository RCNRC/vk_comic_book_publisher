from urllib.parse import urlparse
import os
from random import randint
import requests


def download_random_image():
    response = requests.get(url="https://xkcd.com/info.0.json")
    comics_count = response.json()["num"]
    random_comics_num = randint(1, comics_count)
    return download_image(resource_url=f"https://xkcd.com/{random_comics_num}/info.0.json")


def get_image_type(image_url):
    parsed_url = urlparse(image_url)
    _, ext = os.path.splitext(parsed_url.path)
    return ext


def download_image(resource_url, image_name=None, resource_params=None, image_params=None):
    resource_response = requests.get(url=resource_url, params=resource_params)
    resource_response.raise_for_status()
    response = requests.get(url=resource_response.json()["img"], params=image_params)
    response.raise_for_status()
    if not image_name:
        image_name = resource_response.json()["safe_title"]
    image_type = get_image_type(resource_response.json()['img'])
    image_full_name = f"{image_name}{image_type}"
    file_name = f"{image_full_name}"
    
    with open(file_name, 'wb') as fd:
        fd.write(response.content)
    message = resource_response.json()['alt']
    return message, file_name


def main():
    download_random_image()


if __name__ == '__main__':
    main()
