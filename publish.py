from comics_download import get_random_comics_resource_url, download_image
from dotenv import dotenv_values
import requests
import os


BASE_URL = "https://api.vk.com/method/"


class HTTPError(Exception):
    def __init__(self, text=None):
        self.text = text


def try_response(response, error_massage):
    try:
        if "error" in response.json():
            raise HTTPError(error_massage)
    finally:
        pass


def publish_comics(access_token, api_version, user_id, post_id, message, vk_group_id):
    method = "wall.post"
    params = {
        "access_token": access_token,
        "v": api_version,
        "attachments": f"photo{user_id}_{post_id}",
        "message": f"{message}",
        "owner_id": f"-{vk_group_id}",
    }
    response = requests.post(url=f"{BASE_URL}{method}", params=params)
    response.raise_for_status()
    try_response(response=response, error_massage="publish_comics response raised exception.")


def save_comics(access_token, api_version, server, photo, wall_hash):
    method = "photos.saveWallPhoto"
    params = {
        "access_token": access_token,
        "v": api_version,
        "server": server,
        "photo": photo,
        "hash": wall_hash,
    }
    response = requests.post(url=f"{BASE_URL}{method}", params=params)
    response.raise_for_status()
    try_response(response=response, error_massage="save_comics response raised exception.")
    return response.json()["response"][0]["owner_id"], response.json()["response"][0]["id"]


def upload_image(post_image_url, file_name):
    with open(f"{file_name}", 'rb') as fd:
        files = {'photo': fd}
        response = requests.post(url=f"{post_image_url}", files=files)
    response.raise_for_status()
    try_response(response=response, error_massage="upload_image response raised exception.")
    return response.json()["server"], response.json()["photo"], response.json()["hash"]


def get_upload_server_url(access_token, api_version):
    method = "photos.getWallUploadServer"
    params = {
        "access_token": access_token,
        "v": api_version,
    }
    response = requests.get(url=f"{BASE_URL}{method}", params=params)
    response.raise_for_status()
    try_response(response=response, error_massage="get_upload_server_url response raised exception.")
    return response.json()["response"]["upload_url"]


def main():
    vk_group_id = dotenv_values(".env")["VK_GROUP_ID"]
    access_token = dotenv_values(".env")["VK_APP_API_ACCESS_TOKEN"]
    api_version = "5.131"
    post_image_url = get_upload_server_url(access_token=access_token, api_version=api_version)
    comics_url = get_random_comics_resource_url()
    message, file_name = download_image(resource_url=comics_url)
    try:
        server, photo, wall_hash = upload_image(post_image_url=post_image_url, file_name=file_name)
        user_id, post_id = save_comics(access_token=access_token, api_version=api_version, server=server, photo=photo, wall_hash=wall_hash)
        publish_comics(access_token=access_token, api_version=api_version, user_id=user_id, post_id=post_id, message=message, vk_group_id=vk_group_id)
    finally:
        os.remove(file_name)


if __name__ == '__main__':
    main()
