from typing import List
from app import schemas 
import pytest 

def test_all_posts(test_posts, authorized_client):
    res = authorized_client.get("/posts/")

    def validate(posts):
        return schemas.Post_Out(**posts)
    post_map = map(validate, res.json())
    posts = list(post_map)

    #assert len(res.json()) == len(test_posts)
    assert res.status_code == 200
    #assert post_list[0].Post.id == test_posts[0].id 

def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401 

def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_get_one_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/9999")
    assert res.status_code == 404 

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.Post_Out(**res.json())
    #assert res.status_code == 201
    assert post.Post.id == test_posts[0].id 
    assert post.Post.content == test_posts[0].content 
    assert post.Post.title == test_posts[0].title 


@pytest.mark.parametrize("title,content,published", [("Chief Executive Officer", "Thabang Mbhele", True), ("Researcher", "Luvuyo Makhanya", True), ("Researcher", "Anita Govender", True), ("Chief of Staff", "N/A", False)])
def test_create_one_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post("/posts/", json = {"title": title, "content": content , "published": published})
    posts = schemas.Post(**res.json())
    assert res.status_code == 201
    assert posts.title == title
    assert posts.content == content 
    assert posts.published == published 
    assert posts.user_id == test_user['id']

def test_default_published_post(authorized_client, test_user, test_posts):
    res = authorized_client.post("/posts/", json = {"title": "Chairman of the Board", "content": "Thabang Mbhele"})
    posts = schemas.Post(**res.json())
    assert posts.title == "Chairman of the Board"
    assert posts.content == "Thabang Mbhele"
    assert posts.published == True
    assert posts.user_id == test_user['id']

def test_create_unauthorized_client_post(client, test_posts, test_user):
    res = client.post("/posts/", json = {"title": "Vice President of Legal Affairs", "content": "Miss Jenice Reeves Phd"})
    assert res.status_code == 401 

def test_unauthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_delete_posts_non_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/9000")
    assert res.status_code == 404 

def test_delete_post_wrong_user(authorized_client, test_posts, test_user):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403 

def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "Employee 1",
        "content": "Thabang Mbhele",
        "id": test_posts[0].id
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json = data)
    post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert post.title == data['title']
    assert post.content == data['content']
    
def test_update_post_wrong_user(authorized_client, test_user, test_posts, test_user2):
    data = {
        "title": 'Personal Assistant to the Chief Executive',
        "content": "Miss Sunesh Ahir",
        "id": test_posts[3].id 
    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json = data)
    assert res.status_code == 403 

def test_update_post_not_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "Researcher- Legal Affairs",
        "content": "Jenny Washington",
        "id": test_posts[0].id
    }
    res= authorized_client.put(f"/posts/9000", json = data)
    assert res.status_code == 404 

def test_unathorized_user_update_post(client, test_user, test_posts):
    data = {
        "title": "Reaearcher- Marketing",
        "content": "Mr Sumbane Xhilisa",
        "id": test_posts[0].id 
    }
    res = client.put(f"/posts/{test_posts[0].id}", json = data)
    assert res.status_code == 401

























