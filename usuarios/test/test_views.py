# tests/test_permissions.py
import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User
from app.views import IsStaffAndCanOnlyReadOrCreate, UsuarioView  # ajusta el import según tu app

def test_is_staff_can_only_read_or_create_list():
    user = User(username='staff', is_staff=True)
    factory = APIRequestFactory()
    request = factory.get('/usuarios/')
    request.user = user
    view = UsuarioView()
    view.action = 'list'

    permission = IsStaffAndCanOnlyReadOrCreate()
    assert permission.has_permission(request, view) == True

def test_is_staff_cannot_update():
    user = User(username='staff', is_staff=True)
    factory = APIRequestFactory()
    request = factory.put('/usuarios/')
    request.user = user
    view = UsuarioView()
    view.action = 'update_user'

    permission = IsStaffAndCanOnlyReadOrCreate()
    assert permission.has_permission(request, view) == False

def test_superuser_has_access():
    user = User(username='admin', is_superuser=True)
    factory = APIRequestFactory()
    request = factory.put('/usuarios/')
    request.user = user
    view = UsuarioView()
    view.action = 'update_user'

    permission = IsStaffAndCanOnlyReadOrCreate()
    assert permission.has_permission(request, view) == True

@pytest.mark.django_db
def test_register_user_creates_user_and_token():
    client = APIClient()
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "securepassword"
    }
    response = client.post('/usuarios/register/', user_data, format='json')

    assert response.status_code == 201
    assert 'token' in response.data
    assert 'user' in response.data
    assert User.objects.filter(username='testuser').exists()

@pytest.mark.django_db
def test_search_users_by_username():
    user = User.objects.create_user(username='john', password='pass123')
    superuser = User.objects.create_superuser(username='admin', password='adminpass')
    token, _ = Token.objects.get_or_create(user=superuser)

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    response = client.get('/usuarios/search_users/?criteria=username&value=john')
    assert response.status_code == 200
    assert response.data['users'][0]['username'] == 'john'