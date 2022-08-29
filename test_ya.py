from urllib import response
import requests
from pprint import pprint
import yadisk



TOKEN = "AQAEA7qj0SyLAADLWxJK0PtrYUrqkqZl0aVPcxY"


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

        response = requests.post(href)
        response.raise_for_status()
        if response.status_code == 201:
            print('Загружено')

    

ya = YandexDisk(token=TOKEN)
# ya = yadisk.YaDisk(token=TOKEN)
# ya.upload_url('https://sun4-17.userapi.com/impf/byTiuiCzlcw-7HQqNI8VeOhaKVPrGm-Sdt9wsQ/banGDBotKVM.jpg?size=731x1000&quality=96&sign=432b2466a268e6e51f46eb47c80ce26a&c_uniq_tag=IraiqwN4-ugqtJPjK4lTRIFF5_YM2KEiJGJmVi9HjtY&type=album', '56')
# pprint(ya.get_files_list())
pprint(ya.upload_file_to_disk('https://sun4-17.userapi.com/impf/byTiuiCzlcw-7HQqNI8VeOhaKVPrGm-Sdt9wsQ/banGDBotKVM.jpg?size=731x1000&quality=96&sign=432b2466a268e6e51f46eb47c80ce26a&c_uniq_tag=IraiqwN4-ugqtJPjK4lTRIFF5_YM2KEiJGJmVi9HjtY&type=album'))