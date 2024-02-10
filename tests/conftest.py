
from fastapi.testclient import TestClient 
from app.main import app
from app import schemas
from app.config import settings
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker 
from sqlalchemy import create_engine 
from app.database import get_db
from app.database import Base 
import pytest
from app.auth2 import create_access_token
from app import models
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'
#SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Universe.Inc@localhost:5432/fastapi_test
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

#Base.metadata.create_all(bind = engine)

#def override_get_db():
    #db = TestingSessionLocal()
    #try:
     #   yield db
    #finally:
     #   db.close()

#app.dependency_overrides[get_db]= override_get_db 

@pytest.fixture(scope = "function")
def session():
    Base.metadata.drop_all(bind = engine)
    Base.metadata.create_all(bind = engine)
    db = TestingSessionLocal()
    try:
        yield db 
    finally:
        db.close()
@pytest.fixture(scope = "function")
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db 
    yield TestClient(app)

@pytest.fixture
def test_user(client):
    user_data = {'email': 'omayaoratiwe@gmail.com', 'password': 'omaya5'}
    res = client.post("/users/", json = user_data)
    assert res.status_code == 201 
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email": "thabz@gmail.com", "password": "12345"}
    res = client.post("/users/", json = user_data)
    new_users = res.json()
    new_users['password'] = user_data['password']
    return new_users
 

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f'Bearer {token}'
    }
    return client 

@pytest.fixture
def test_posts(test_user, session, test_user2):
    post_data = [{"title": "Chief Executive Officer", "content": "Thabang Mbhele", "user_id": test_user['id']}, 
                 {"title": "Researcher", "content": "Sunita Govender", "user_id": test_user['id']}, 
                 {"title": "Chief of Staff", "content": "Luvuyo Makhanya", "user_id": test_user['id']}, {"title": "Chief Risk Officer", "content": "Mr Sui Lao", "user_id": test_user2['id']}]
    def create_posts_model(posts):
        return models.Post(**posts)
    post_map = map(create_posts_model, post_data) 
    post = list(post_map)

    session.add_all(post)
    session.commit()
    posts = session.query(models.Post).all()
    return posts 