def test_index(app, client):
    res = client.get('/')
    assert res.status_code == 200


def test_home(app, client):
    res = client.get('/home')
    assert res.status_code == 200


def test_joke(app, client):
    res = client.get('/Joke')
    assert res.status_code == 200


def test_anime(app, client):
    res = client.get('/RandomAnime')
    assert res.status_code == 200


def test_read(app, client):
    res = client.get('/read')
    assert res.status_code == 200


def test_facts(app, client):
    res = client.get('/funfact')
    assert res.status_code == 200


def test_menu(app, client):
    res = client.get('/menu')
    assert res.status_code == 200
