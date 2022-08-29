import requests
from pprint import pprint
import json
import yadisk
import sys




with open("token.json", "r") as read_file:
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
        
        list_photo = []
        dict_photo = {}
        photos = [{}]
        req = requests.get(get_photo, params={**self.params, **get_photo_params}).json()
        req = req['response']['items']
        for z in req:
            req = z['sizes']
            for size in req:                
                if size['type'] == 'z':
                    list_photo.append(size['url'])
                    dict_photo[z['likes']['count']] = size['url']
                    photos[0]["file_name:"] = f"{z['likes']['count']}.jpg"
                    photos[0]["size"] = size['type']
                    with open('data.json', 'a') as f:
                        json.dump(f'{photos}', f)  

        
            # print(photos)
        
        return dict_photo


vk_client = VkUser(token, '5.131')
photo_vk = vk_client.photos_get()




# TOKEN = ""


ya = yadisk.YaDisk(token=input('Вставьте токен YaDisc '))
name_folder = input("Введите название папки которую хотите создать ")
folder = ya.mkdir(name_folder)


x = 0 
for key, send in photo_vk.items():
    ya.upload_url(f'{send}',f'{name_folder}/{key}')
    print(f'Загружено {x} фото из {len(photo_vk)-1}')
    x +=1

print('Фото успешно загружены')

