
import requests
import json
from urllib.parse import urlencode
from tqdm import tqdm

class vk_client:

    API_BASE_URL = "https://api.vk.com/method/"
    def __init__(self, token, user_id, v='5.199'):
        self.token = token
        self.user_id = user_id
        self.v = v
        self.photo_info = {}
        self.photo_json_list = []
        self.photo_json_dict = {}
    def get_common_params(self):
        return {
            'access_token': self.token,
            'v': self.v,
            'owner_id': self.user_id,
            'album_id': 'profile',
            'rev': '1',
            'extended': '1',
            'photo_sizes': '1',
            'count': '5',
        }

    def get_photo(self):

        response = requests.get(
            f'{self.API_BASE_URL}/photos.get?{urlencode(self.get_common_params())}')
        items = response.json()['response']['items']
        for elements in items:
            image_url = elements.get("orig_photo")['url']
            name = elements.get('likes')['count']
            self.photo_info.update({name: image_url})
            self.photo_json_dict = {'file_name': f'{name}.jpg', 'size': 'orig_photo', 'height': elements.get("orig_photo")['height'], 'width': elements.get("orig_photo")['width']}
            self.photo_json_list.append(self.photo_json_dict)


        with open('photo_data.json', 'w') as file:
            json.dump(self.photo_json_list, file)

class ya_client:
    url_create_folder = 'https://cloud-api.yandex.net/v1/disk/resources'


    def save_photo(self):
        params = {
            'path': 'Vk_Photos',
        }
        headers = {
            "Authorization": "y0_AgAAAAAjFoM9AADLWwAAAAETMnwZAABRhYGydXVH25_nPpHIopIZvF1xvw"
        }
        response_create = requests.put(self.url_create_folder, params=params, headers=headers)
        for key in tqdm(vk.photo_info, desc="Saving photos", leave=True):
            params.update({'url': vk.photo_info.get(key),
                           'path': f'Vk_Photos/{key}'
                           })
            response_save = requests.post(f'{self.url_create_folder}/upload', params=params, headers=headers)

token = input("Введите токен с полигона яндекс-диска:")
user_id = input("Введите ID пользователя vk:")
vk = vk_client(token, user_id)
ya = ya_client()

print(vk.get_photo())
print(ya.save_photo())






