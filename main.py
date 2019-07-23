import requests
import urls
from config import base_request_params, GROUP_ID
import json
import random

#Получить список id всех участников группы
def get_member_id_list(group_id):
    extra_params = {'group_id': group_id}
    response = requests.get(urls.get_members, params=dict(base_request_params, **extra_params))
    member_id_list = json.loads(response.text)['response']['items']
    return member_id_list

class Member:
    first_name = None
    last_name = None
    is_subscribe = None

    def __init__(self, id):
        self.id = id

    def get_name(self):
        extra_params = {'user_id': self.id}
        response = requests.get(urls.get_user_info, params=dict(base_request_params, **extra_params))
        json_data = json.loads(response.text)['response'][0]
        self.first_name = json_data.get('first_name')
        self.last_name = json_data.get('last_name')

    def get_subscribe_status(self):
        extra_params = {'user_id': self.id, 'group_id': GROUP_ID}
        response = requests.get(urls.is_messages_allow, params=dict(base_request_params, **extra_params))
        self.is_subscribe = True if json.loads(response.text)['response']['is_allowed'] is 1 else False

    def get_full_info(self):
        self.get_name()
        self.get_subscribe_status()

    def send_msg(self, msg):
        if self.is_subscribe:
            random_id = random.randint(1, 2147483647)
            extra_params = {'user_id': self.id, 'group_id': GROUP_ID, 'message': msg, 'random_id': random_id}
            r = requests.get(urls.send_message, params=dict(base_request_params, **extra_params))

    def __repr__(self):
        return str(self.id)

if __name__ == '__main__':

    msg_template = """
Добрый вечер, {}! Мы настроили автоматическую рассылку сообщений из группы и теперь будем иногда \
присылать важную информацию в личные сообщения. Это будет происходить нечасто, но если Вы вообще не хотите получать \
такие сообщения, от них можно отписаться в настройках группы. 
    
А пока наше первое важное сообщение: 

25 июля (в этот четверг) в 21:00 мы хотим провести встречу жителей дома и обсудить планы по дальнейшему \
взаимодействию с управляющей компанией. 
    
Собираемся во дворе. Приходите! :) 
"""

    member_id_list = get_member_id_list(GROUP_ID)
    members = [Member(id) for id in member_id_list]

    """Продакшн так сказать :)"""
    # for member in members:
    #     member.get_full_info()
    #     person_name = member.first_name
    #     msg = {msg_template.format(person_name)}
    #     member.send_msg(msg)


    """Тест на мне"""
    # iam = Member(21205528)
    # iam.get_full_info()
    # person_name = iam.first_name
    # msg = {msg_template.format(person_name)}
    # iam.send_msg(msg)

