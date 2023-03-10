from comics_download import get_random_comics_resource_url, download_image
from dotenv import load_dotenv
import requests
import os


BASE_URL = "https://api.vk.com/method/"


class VKResponseError(Exception):
    def __init__(self, text=None):
        self.text = text


def check_response(response, error_massage):
    if "error" in response.json():
        raise VKResponseError(error_massage)


def publish_comic(access_token, api_version, user_id, post_id, message, vk_group_id):
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
    check_response(
        response,
        error_massage="publish_comics response raised exception.",
    )


def save_comic(access_token, api_version, server, photo, wall_hash):
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
    check_response(
        response,
        error_massage="save_comics response raised exception.",
    )
    response_content = response.json()
    return response_content["response"][0]["owner_id"], response_content["response"][0]["id"]


def upload_image(post_image_url, file_name):
    with open(f"{file_name}", 'rb') as fd:
        files = {'photo': fd}
        response = requests.post(url=f"{post_image_url}", files=files)
    response.raise_for_status()
    check_response(
        response,
        error_massage="upload_image response raised exception.",
    )
    response_content = response.json()
    return response_content["server"], response_content["photo"], response_content["hash"]


def get_upload_server_url(access_token, api_version):
    method = "photos.getWallUploadServer"
    params = {
        "access_token": access_token,
        "v": api_version,
    }
    response = requests.get(url=f"{BASE_URL}{method}", params=params)
    response.raise_for_status()
    check_response(
        response,
        error_massage="get_upload_server_url response raised exception.",
    )
    return response.json()["response"]["upload_url"]


def main():
    load_dotenv()
    vk_group_id = os.environ["VK_GROUP_ID"]
    access_token = os.environ["VK_APP_API_ACCESS_TOKEN"]
    api_version = "5.131"
    post_image_url = get_upload_server_url(
        access_token,
        api_version,
    )
    comics_url = get_random_comics_resource_url()
    message, file_name = download_image(resource_url=comics_url)
    try:
        server, photo, wall_hash = upload_image(
            post_image_url,
            file_name,
        )
        user_id, post_id = save_comic(
            access_token,
            api_version,
            server,
            photo,
            wall_hash,
        )
        publish_comic(
            access_token,
            api_version,
            user_id,
            post_id,
            message,
            vk_group_id,
        )
    finally:
        os.remove(file_name)


if __name__ == '__main__':
    main()
