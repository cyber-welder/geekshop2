from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse
from django.utils import timezone
from social_core.exceptions import AuthForbidden
import requests
from re import sub

from authapp.models import ShopUserProfile
from geekshop import settings


def save_user_profile(backend, user, response, *args, **kwargs):

    if backend.name == 'vk-oauth2':
        api_url = urlunparse(('https',
                              'api.vk.com',
                              '/method/users.get',
                              None,
                              urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about')),
                                                    access_token=response['access_token'],
                                                    v='5.131')),
                              None
                              ))

        resp = requests.get(api_url)
        if resp.status_code != 200:
            return

        data = resp.json()['response'][0]
        if data['sex']:
            user.shopuserprofile.gender = ShopUserProfile.MALE if data['sex'] == 2 else ShopUserProfile.FEMALE

        if data['about']:
            user.shopuserprofile.about_me = data['about']

        if data['bdate']:
            bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()

            age = timezone.now().date().year - bdate.year
            if age < 18:
                user.delete()
                raise AuthForbidden('social_core.backend.vk.VKOAuth2')
            else:
                user.age = age

        if response['email']:
            user.email = response['email']

        if response['photo']:
            avatar_name = response['photo'].split('/')[-1]
            avatar_name = sub("[:*?=|<>]", "", avatar_name)  # безопасное имя файла (для windows)
            avatar_path = 'users_avatars/' + avatar_name
            with open(settings.MEDIA_URL[1:] + avatar_path, 'wb') as f:
                f.write(requests.get(response['photo']).content)

            user.avatar = avatar_path

        user.save()

    elif backend.name == 'github':

        if response['name']:
            user.first_name = response['name']

        if response['email']:
            user.email = response['email']

        if response['avatar_url']:
            avatar_name = response['avatar_url'].split('/')[-1]
            avatar_name = sub("[:*?=|<>]", "", avatar_name)  # безопасное имя файла (для windows)
            avatar_path = 'users_avatars/' + avatar_name
            with open(settings.MEDIA_URL[1:] + avatar_path, 'wb') as f:
                f.write(requests.get(response['avatar_url']).content)

            user.avatar = avatar_path

        user.save()

    else:
        return
