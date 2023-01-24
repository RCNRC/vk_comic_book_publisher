from comics_download import download_random_image
from dotenv import dotenv_values
import requests
import os


BASE_URL = "https://api.vk.com/method/"
VK_APP_API_ACCESS_TOKEN = dotenv_values(".env")["VK_APP_API_ACCESS_TOKEN"]


def base_parametres():
    params = {
        "access_token": f"{VK_APP_API_ACCESS_TOKEN}",
        "v": "5.131",
    }
    return params


def vk_post_wall(user_id, post_id, message, vk_group_id):
    method = "wall.post"
    params = base_parametres()
    params["attachments"] = f"photo{user_id}_{post_id}"
    params["message"] = f"{message}"
    params["owner_id"] = f"-{vk_group_id}"
    response = requests.post(url=f"{BASE_URL}{method}", params=params)
    response.raise_for_status()
    return response.json()


def vk_safe_wall(server, photo, hash):
    method = "photos.saveWallPhoto"
    params = base_parametres()
    params["server"] = server
    params["photo"] = photo
    params["hash"] = hash
    response = requests.post(url=f"{BASE_URL}{method}", params=params)
    response.raise_for_status()
    return response.json()


def vk_post_image(post_image_url, file_name):
    with open(f"{file_name}", 'rb') as fd:
        files = {'photo': fd}
        response = requests.post(url=f"{post_image_url}", files=files)
        response.raise_for_status()
    return response.json()


def vk_get_wall():
    method = "photos.getWallUploadServer"
    params = base_parametres()
    response = requests.get(url=f"{BASE_URL}{method}", params=params)
    response.raise_for_status()
    return response.json()


def main():
    vk_group_id = dotenv_values(".env")["VK_GROUP_ID"]
    json_response = vk_get_wall()
    message, file_name = download_random_image()  # скачивать рандомную
    post_image_url=json_response["response"]["upload_url"]
    json_response = vk_post_image(post_image_url=post_image_url, file_name=file_name)
    response_server = json_response["server"]
    response_photo = json_response["photo"]
    response_hash = json_response["hash"]
    json_response = vk_safe_wall(server=response_server, photo=response_photo, hash=response_hash)
    user_id = json_response["response"][0]["owner_id"]
    post_id = json_response["response"][0]["id"]
    json_response = vk_post_wall(user_id=user_id, post_id=post_id, message=message, vk_group_id=vk_group_id)
    os.remove(file_name)


if __name__ == '__main__':
    main()
