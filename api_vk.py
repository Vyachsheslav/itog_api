from calendar import c
import time
import pandas as pd
import requests
# импортируем pprint для более комфортного вывода информации
from pprint import pprint
import configparser
import json


# data=input()

# with open("token.json", "w") as write_file:
#     json.dump(data, write_file)

with open("token.json", "r") as read_file:
    token = json.load(read_file)

# print(token)




# URL = 'https://api.vk.com/method/users.get'
# params = {
#     'user_ids': '1,sex_love_rock_n_roll',
#     'fields': 'photo_max_orig, city,sex',
    
#     'access_token': token, # токен и версия api являются обязательными параметрами во всех запросах к vk
#     'v':'5.131'
# }
# res = requests.get(URL, params=params)
# pprint(res.json())


# def search_groups(q, sorting=0):
#     '''
#     Параметры sort
#     0 — сортировать по умолчанию (аналогично результатам поиска в полной версии сайта);
#     6 — сортировать по количеству пользователей.
#     '''
#     params = {
#         'q': q,
#         'access_token': token,
#         'v':'5.131',
#         'sort': sorting,
#         'count': 20
#     }
#     req = requests.get('https://api.vk.com/method/groups.search', params).json()
#     # pprint(req)
#     req = req['response']['items']
#     return req

# target_groups = search_groups('стопдолг')

# # pprint(target_groups)

# # преобразуем список всех id в строку (в таком виде принимает данные параметр fields)
# target_group_ids = ','.join([str(group['id']) for group in target_groups])
# # pprint(target_group_ids)

# params = {
#     'access_token': token,
#     'v':'5.131',
#     'group_ids': target_group_ids,
#     'fields':  'members_count,activity,description'

# }
# req = requests.get('https://api.vk.com/method/groups.getById', params)

# pprint(req.json()['response'])




# токен и версия могут быть разные в разных экзмеплярах
# базовый URL будет всегда один, в инициализации он не нужен
class VkUser:
    url = 'https://api.vk.com/method/'
    def __init__(self, token, version):
        self.params = {
            'access_token': token,
            'v': version    
        }


    def search_groups(self, q, sorting=0):
        '''
        Параметры sort
        0 — сортировать по умолчанию (аналогично результатам поиска в полной версии сайта);
        6 — сортировать по количеству пользователей.
        '''
        group_search_url = self.url + 'groups.search'
        group_search_params = {
            'q': q,
            'sort': sorting,
            'count': 3
        }
        req = requests.get(group_search_url, params={**self.params, **group_search_params}).json()
        
        return req['response']['items']
    
    def search_groups_ext(self, q, sorting=0):
        group_search_ext_url = self.url + 'groups.getById'
        target_groups = self.search_groups(q, sorting)
        target_group_ids = ','.join([str(group['id']) for group in target_groups])
        groups_info_params = {
            'group_ids': target_group_ids,
            'fields': 'members_count,activity,description'
        }
        req = requests.get(group_search_ext_url, params={**self.params, **groups_info_params}).json()
        return req['response']

    def get_followers(self, user_id=None):
        followers_url = self.url + 'users.getFollowers'
        followers_params = {
            'count': 1000,
            'user_id': user_id
        }
        res = requests.get(followers_url, params={**self.params, **followers_params}).json()
        return res['response']

    def get_groups(self, user_id=None):
        groups_url = self.url + 'groups.get'
        groups_params = {
            'count': 10,
            'user_id': user_id,
            'extended': 1,
            'fields': 'members_count',
        }
        res = requests.get(groups_url, params={**self.params, **groups_params})
        return res.json()

    def get_news(self, query):
        groups_url = self.url + 'newsfeed.search'
        groups_params = {
            'q': query,
            'count': 200
        }
        
        newsfeed_df = pd.DataFrame()

        while True:
            result = requests.get(groups_url, params={**self.params, **groups_params})
            time.sleep(0.33)
            newsfeed_df = pd.concat([newsfeed_df, pd.DataFrame(result.json()['response']['items'])])
            if 'next_from' in result.json()['response']:
                groups_params['start_from'] = result.json()['response']['next_from']
            else:
                break
        return newsfeed_df    

# vk_client = VkUser(token, '5.131')
# pprint(vk_client.search_groups('стопдолг'))
# pprint(vk_client.search_groups_ext('стопдолг'))


# data = pd.DataFrame(vk_client.search_groups_ext('python'))
# print(type(data))
# data.to_csv('test.csv')



# pprint(vk_client.get_followers())

# pprint(vk_client.get_groups())


# pprint(vk_client.get_news('попутчики усть-каменогорск'))