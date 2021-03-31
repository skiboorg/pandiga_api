from random import choices
import string
import settings
import requests


def create_random_string(digits=False, num=4):
    if not digits:
        random_string = ''.join(choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=num))
    else:
        random_string = ''.join(choices(string.digits, k=num))
    return random_string

def set_user_rating(id,value):
    """Обновление рейтинга техники при создании отзыва"""
    from .models import User

    user = User.objects.get(id=id)
    user.rate_times += 1
    user.rate_value += value
    user.rating = round(user.rate_value / user.rate_times)
    user.save()
    return


def send_sms(phone, msg, text=None):
    print(phone)
    result = {'result': False, 'code': None}
    code = ''.join(choices(string.digits, k=4))
    if text:
        text = text
    else:
        text = code
    url = f'https://smsc.ru/sys/send.php?login={settings.SMS_LOGIN}&psw={settings.SMS_PASSWORD}' \
          f'&phones={phone}&mes=PANDIGA. {msg}: {text}'
    response = requests.post(url)
    if 'ERROR' not in response.text:
        result = {'result': True, 'code': text}
    return result
