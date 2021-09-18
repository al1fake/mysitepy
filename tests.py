import pytest
from pytest import ExitCode
import requests
from django.contrib.auth import get_user_model

def test_get(client):
    url = 'http://127.0.0.1:8000/api/comments/'
    headers = {'Authorization': 'Token 7c9a12d5947f518ecf77c64ba171497296b2f5e9'}
    r = requests.get(url, headers=headers)

    if r is not None:
        return 'Success!'
    else:
        pytest.fail()


def test_post(client):
    url = 'http://127.0.0.1:8000/api/comments/'
    headers = {'Authorization': 'Token 7c9a12d5947f518ecf77c64ba171497296b2f5e9'}
    data = {
        'post': 1,
        'name': 'admin',
        'body': 'hello world'
    }
    r = requests.post(url, data=data, headers=headers)

    if r is not None:
        return 'Success!'
    else:
        pytest.fail()


def test_delete(client):
    url = 'http://127.0.0.1:8000/api/comments/'
    headers = {'Authorization': 'Token 7c9a12d5947f518ecf77c64ba171497296b2f5e9'}
    data = {
        'id': 44,
    }
    r = requests.delete(url, data=data, headers=headers)
    if r is not None:
        return 'Success!'
    else:
        pytest.fail()


# @pytest.mark.django_db
# def test_user(client):
#     user_model = get_user_model()
#     user = user_model.objects.all()
#     me = user.filter(username='admin')
#     assert me.is_superuser
