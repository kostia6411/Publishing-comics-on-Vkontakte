import logging
import os
import random

import requests
from dotenv import load_dotenv


def get_upload_link(vk_access_token, vk_group_id, vk_user_id):
    url = "https://api.vk.com/method/photos.getWallUploadServer"
    payload = {
        "access_token": vk_access_token,
        "v": '5.131',
        "group_id": vk_group_id,
        "user_id": vk_user_id
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    check_vk_response(response)
    return response.json()["response"]["upload_url"]


def publication_comic_wall(vk_access_token, media_id, vk_group_id, owner_id):
    url = "https://api.vk.com/method/wall.post"
    payload = {
        "access_token": vk_access_token,
        "v": '5.131',
        "owner_id": f"-{vk_group_id}",
        "attachments": f"photo{owner_id}_{media_id}"
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    check_vk_response(response)
    return response.json()


def save_comic(vk_access_token, photo_hash, photo_photo, photo_server, vk_group_id):
    url = "https://api.vk.com/method/photos.saveWallPhoto"
    payload = {
        "access_token": vk_access_token,
        "v": '5.131',
        "group_id": vk_group_id,
        "hash": photo_hash,
        "photo": photo_photo,
        "server": photo_server,
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    check_vk_response(response)
    return response.json()["response"][0]["id"], response.json()["response"][0]["owner_id"]


def upload_server_photos(upload_link, comic_path):
    with open(comic_path, 'rb') as file:
        payload = {
            "photo": file
        }
        response = requests.post(upload_link, files=payload)
    response.raise_for_status()
    check_vk_response(response)
    response_payload = response.json()
    return response_payload['hash'], response_payload['photo'], response_payload['server']


def download_random_comic(images_path):
    url = "https://xkcd.com/info.0.json"
    response = requests.get(url)
    response.raise_for_status()
    comic_num = response.json()["num"]
    random_comic_num = random.randint(0, comic_num)
    random_comic_url = f"https://xkcd.com/{random_comic_num}/info.0.json"
    response = requests.get(random_comic_url)
    response.raise_for_status()
    random_comic = requests.get(response.json()["img"])
    random_comic.raise_for_status()
    picture_path= os.path.join(images_path, 'comic.jpg')
    with open(picture_path, 'wb') as file:
        file.write(random_comic.content)
    return response.json()["alt"]


def check_vk_response(response):
    if response.json().get('error'):
        logging.warning(response.json())
        raise requests.exceptions.HTTPError


if __name__ == "__main__":
    load_dotenv()
    vk_group_id = os.environ["VK_GROUP_ID"]
    vk_user_id = os.environ["VK_USER_ID"]
    vk_access_token = os.environ["VK_ACCESS_TOKEN"]
    comic_path = os.path.join('images', 'comic.jpg')
    images_path = os.getenv("IMAGES_DIR", "images")
    os.makedirs(images_path, exist_ok=True)
    try:
        download_random_comic(images_path)
        upload_link = get_upload_link(vk_access_token, vk_group_id, vk_user_id)
        photo_hash, photo_photo, photo_server = upload_server_photos(upload_link, comic_path)
        media_id, owner_id = save_comic(vk_access_token, photo_hash, photo_photo, photo_server, vk_group_id)
        publication_comic_wall(vk_access_token, media_id, vk_group_id, owner_id)
    except requests.exceptions.HTTPError:
        print("Ошибка при запросе к ВК")
    finally:
        files_in_dir = os.listdir("images")
        for filename in files_in_dir:
            os.remove(os.path.join("images", filename))
        os.rmdir("images")
