from calendar import c
import time
import pandas as pd
import requests
# импортируем pprint для более комфортного вывода информации
from pprint import pprint
import configparser
import json




with open("token.json", "r") as read_file:
    token = json.load(read_file)


class VkUser:
    url = 'https://api.vk.com/method/'
    def __init__(self, token, version):
        self.params = {
            'access_token': token,
            'v': version    
        }

      

    def photos_get(self, owner_id=None, count=5):
        get_photo = self.url + 'photos.get'
        get_photo_params = {
            'owner_id': owner_id,
            'count': count,
            'album_id': 'profile',
            'extended': 'likes',
            'photo_sizes': 1,
            'type': 'z',
            'rev': '1'
        }
        
        list_photo = []
        dict_photo = {}
        req = requests.get(get_photo, params={**self.params, **get_photo_params}).json()
        req = req['response']['items']
        for z in req:
            req = z['sizes']
            for size in req:
                if size['type'] == 'z':
                    list_photo.append(size['url'])
                    dict_photo[z['likes']['count']] = size['url']
        return dict_photo


vk_client = VkUser(token, '5.131')
pprint(vk_client.photos_get('1'))


class YandexDisk:

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

   
    
    def _get_upload_link(self, disk_file_path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": disk_file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        pprint(response.json())
        return response.json()


    def upload_file_to_disk(self, disk_file_path):
        href = self._get_upload_link(disk_file_path=disk_file_path).get("href", "")
        response = requests.post(href, 'https://sun4-17.userapi.com/impf/byTiuiCzlcw-7HQqNI8VeOhaKVPrGm-Sdt9wsQ/banGDBotKVM.jpg?size=731x1000&quality=96&sign=432b2466a268e6e51f46eb47c80ce26a&c_uniq_tag=IraiqwN4-ugqtJPjK4lTRIFF5_YM2KEiJGJmVi9HjtY&type=album')
        response.raise_for_status()
        if response.status_code == 201:
            print('Загружено')

ya = YandexDisk(token=TOKEN)
# # pprint(ya.get_files_list())
pprint(ya.upload_file_to_disk('test'))



