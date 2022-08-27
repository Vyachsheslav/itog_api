import requests
from pprint import pprint
import json
import yadisk
from datetime import datetime as dt
from tqdm import tqdm


with open("token.json", "r", encoding='utf-8') as read_file:
    token = json.load(read_file)


class VkUser:
    url = 'https://api.vk.com/method/'

    def __init__(self, token, version):
        self.params = {
            'access_token': token,
            'v': version
        }

    def photos_get(self, owner_id=input('Введите id пользователя '), count=5):
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

        photos = {}
        data = []
        names = []
        req = requests.get(get_photo, params={**self.params, **get_photo_params}).json()
        items = req['response']['items']
        counter = 0
        for item in items:
            sizes = item['sizes']            
            for size in sizes:
                if size['type'] == 'z':
                    photos[counter] = {}
                    photos[counter]['name'] = str(item['likes']['count'])
                    names.append(photos[counter]['name'])
                    photos[counter]['url'] = size['url']
                    photos[counter]['date'] = dt.utcfromtimestamp(item['date']).strftime('%Y-%m-%d')
                    photos[counter]['size'] = 'z'
                    counter += 1

        for name in set(names):
            if names.count(name) >= 2:
                for photo in photos.values():
                    if photo['name'] == name:
                        photo['name'] = f"{photo['name']} {photo['date']}"

        for photo in photos.values():
            data.append({"file_name": f"{photo['name']}.jpg",
                        "size": photo['size']})

        with open('data.json', 'w', encoding='utf-8') as file:
            json.dump(f'{data}', file)

        return photos


vk_client = VkUser(token, '5.131')
photo_vk = vk_client.photos_get()

ya = yadisk.YaDisk(token=input('Вставьте токен YaDisc '))
dirs = []
for i in ya.listdir('/'):
    if i['file'] is None:
        dirs.append(i['name'])

name_folder = input("Введите название папки, в которую хотите добавить фото: ")
if name_folder not in dirs:
    ya.mkdir(name_folder)    

for photo in tqdm(photo_vk.values()):
    ya.upload_url(f"{photo['url']}", f"{name_folder}/{photo['name']}")

print('Фото успешно загружены')
