from urllib.parse import urlparse
import os
import requests


def get_image_type(image_url):
    parsed_url = urlparse(image_url)
    (_, ext) = os.path.splitext(parsed_url.path)
    return ext


def download_image(resource_url, image_name=None, image_directory="./images", resource_params=None, image_params=None):
    resource_response = requests.get(url=resource_url, params=resource_params)
    resource_response.raise_for_status()
    response = requests.get(url=resource_response.json()["img"], params=image_params)
    response.raise_for_status()
    if(not image_name):
        image_name = resource_response.json()["safe_title"]
    image_type = get_image_type(resource_response.json()['img'])
    os.makedirs(image_directory, exist_ok=True)
    with open(f"{image_directory}/{image_name}{image_type}", 'wb') as fh:
        fh.write(response.content)


def main():
    download_image(resource_url="https://xkcd.com/info.0.json")


if __name__ == '__main__':
    main()
