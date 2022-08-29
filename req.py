from urllib import response
import requests
from pprint import pprint




TOKEN = "AQAEA7qj0SyLAADLWxJK0PtrYUrqkqZl0aVPcxY"


class YandexDisk:

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def get_files_list(self):
        files_url = 'https://cloud-api.yandex.net/v1/disk/resources/files'
        headers = self.get_headers()
        response = requests.get(files_url, headers=headers)
        return response.json()
    
    def _get_upload_link(self, disk_file_path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": disk_file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        pprint(response.json())
        return response.json()


    def upload_file_to_disk(self, disk_file_path, filename):
        href = self._get_upload_link(disk_file_path=disk_file_path).get("href", "")
        response = requests.post(href, data=open(filename, 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            print('Загружено')

    def upload_url(self):
        files_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        response = requests.get(files_url, headers=headers)
        return response.json()

ya = YandexDisk(token=TOKEN)
# # pprint(ya.get_files_list())
pprint(ya.upload_file_to_disk("Netology/test.txt", "1.txt"))

# reddit = Reddit()
# pprint(reddit.get_popular_videos())