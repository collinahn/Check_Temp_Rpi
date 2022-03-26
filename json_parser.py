# json 에서 값을 읽어온다

import os
import json


class JsonParser(object):

    def __init__(self, key_name: str, file_name: str='./settings.json') -> None:
        with open(file_name, 'r', encoding='utf-8') as f:
            json_data: dict = json.loads(f.read())

        self.value = json_data.get(key_name)
