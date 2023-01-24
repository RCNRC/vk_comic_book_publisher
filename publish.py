from comics_download import get_random_comics_resource_url, download_image
from dotenv import dotenv_values
import requests
import os


BASE_URL = "https://api.vk.com/method/"


def post_vk_wall(base_params, user_id, post_id, message, vk_group_id):
    method = "wall.post"
    params = base_params
    params["attachments"] = f"photo{user_id}_{post_id}"
    params["message"] = f"{message}"
    params["owner_id"] = f"-{vk_group_id}"
    response = requests.post(url=f"{BASE_URL}{method}", params=params)
    response.raise_for_status()
    return response


def safe_vk_wall(base_params, server, photo, hash):
    method = "photos.saveWallPhoto"
    params = base_params
    params["server"] = server
    params["photo"] = photo
    params["hash"] = hash
    response = requests.post(url=f"{BASE_URL}{method}", params=params)
    response.raise_for_status()
    return response


def post_vk_image(post_image_url, file_name):
    with open(f"{file_name}", 'rb') as fd:
        files = {'photo': fd}
        response = requests.post(url=f"{post_image_url}", files=files)
    response.raise_for_status()
    return response


def get_vk_wall(base_params):
    method = "photos.getWallUploadServer"
    params = base_params
    response = requests.get(url=f"{BASE_URL}{method}", params=params)
    response.raise_for_status()
    return response


def main():
    vk_group_id = dotenv_values(".env")["VK_GROUP_ID"]
    vk_app_api_access_token = dotenv_values(".env")["VK_APP_API_ACCESS_TOKEN"]
    base_params = {
        "access_token": f"{vk_app_api_access_token}",
        "v": "5.131",
    }
    response = get_vk_wall(base_params=base_params)
    comics_url = get_random_comics_resource_url()
    message, file_name = download_image(resource_url=comics_url)
    try:
        post_image_url=response.json()["response"]["upload_url"]
        response = post_vk_image(post_image_url=post_image_url, file_name=file_name)
        response_server = response.json()["server"]
        response_photo = response.json()["photo"]
        response_hash = response.json()["hash"]
        response = safe_vk_wall(base_params=base_params, server=response_server, photo=response_photo, hash=response_hash)
        user_id = response.json()["response"][0]["owner_id"]
        post_id = response.json()["response"][0]["id"]
        response = post_vk_wall(base_params=base_params, user_id=user_id, post_id=post_id, message=message, vk_group_id=vk_group_id)
    finally:
        os.remove(file_name)


if __name__ == '__main__':
    main()
