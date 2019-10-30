import pytest

import app

@pytest.fixture
def apptest():
    apptest = app.create_app()
    apptest.debug = True
    return apptest.test_client()

def test_hello_world(apptest):
    res = apptest.get("/")
    # print(dir(res), res.status_code)
    assert res.status_code == 200
    assert b"Hello, World!" in res.data

def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

def test_registration(apptest):
    res = apptest.get("/register")
    # print(dir(res), res.status_code)
    assert res.status_code == 200
    assert b"Registration" in res.data
    
def test_registration_no2fa(apptest):
    response = apptest.post('/register',
                                data=dict(uname='user1', pword='FlaskIsAwesome'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"Success. Your username is user1" in response.data

def test_registration_2fa(apptest):
    response = apptest.post('/register',
                                data=dict(uname='user2', pword='FlaskIsAwesome2', twofa='1234567890'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"Success. Your username is user2" in response.data
    
def test_login(apptest):
    res = apptest.get("/login")
    # print(dir(res), res.status_code)
    assert res.status_code == 200
    assert b"Login" in res.data
    
def test_login_user(apptest):
    response = apptest.post('/register',
                                data=dict(uname='user1', pword='FlaskIsAwesome'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"Success" in response.data
    
def test_login_user2fa(apptest):
    response = apptest.post('/register',
                                data=dict(uname='user2', pword='FlaskIsAwesome2', twofa='1234567890'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"Success" in response.data
    
def test_spellcheck(apptest):
    res = apptest.get("/spell_check")
    # print(dir(res), res.status_code)
    assert res.status_code == 200
    assert b"Spell Check Tool" in res.data
