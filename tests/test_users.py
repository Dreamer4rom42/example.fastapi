from app import schemas 
import pytest
from jose import jwt
from app.config import settings 

#def test_root(client):
#    res = client.get("/")
#    assert res.status_code == 200 

def test_create_user(client):
    res= client.post("/users/", json= {"email": "omayaoratiwe@gmail.com", "password": "omaya5"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "omayaoratiwe@gmail.com"
    assert res.status_code == 201

def test_user_login(client, test_user):
    res = client.post("/login/", data= {'username': test_user['email'], 'password': test_user['password']})
    login_res= schemas.Token(** res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms = settings.algorithm)
    id = payload.get('user_id')
    assert id == test_user['id']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200

@pytest.mark.parametrize("email,password,status_code", [("omayagunpat@gmail.com", "omaya5", 403), ("oamayaoratiwe@gmail.com", "oratiwe5", 403), ("paballogranger@gmail.com", "omaya5", 403), (None, "omaya5", 422), ("thabangmbhele44@gmail.com", None, 422)])
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post("/login/", data = {'username': email, 'password': password})
    assert res.status_code == status_code
    #assert res.json().get('detail') == "Invalid credentials"

