import datetime
from bs4 import BeautifulSoup

def test_login_success(client):
    """
    test login
    """
    response = client.post(
        '/login',
        data={'username': 'johndoe', 'password': 'secret'},
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b'Home' in response.data

def test_signup_page(client):
    response = client.get('/signup')
    assert response.status_code == 200
    assert b'Sign Up' in response.data

def test_successful_signup(client):
    test_username = "signup_test"
    test_password = "secret"

    response = client.post('/signup', data={
        'username': test_username,
        'password': test_password
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Account created successfully!' in response.data

    # Delete newly registered user
    mongo = client.application.mongo
    mongo.db.user.delete_one({"username": test_username})


def test_signup_fail_existing_user(client):
    response = client.post(
        '/signup',
        data={'username': 'johndoe', 'password': 'secret'},
        follow_redirects=True
    )
    assert b'Username is already in use' in response.data

def test_home_access_when_logged_in(client, test_user_id):
    with client.session_transaction() as sess:
        sess['user_id'] = str(test_user_id)

    response = client.get('/home')
    assert response.status_code == 200
    assert b'Home' in response.data

def test_logout(client, test_user_id):
    with client.session_transaction() as sess:
        sess['user_id'] = str(test_user_id)

    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Thanks for using GameLog' in response.data

def test_create_post_get(client, test_user_id):
    with client.session_transaction() as sess:
        sess['user_id'] = str(test_user_id)

    response = client.get('/post')
    assert response.status_code == 200
    assert b'Make a Post' in response.data

def test_create_post_submit(client, test_user_id): 
    with client.session_transaction() as sess:
        sess['user_id'] = str(test_user_id)

    response = client.post('/post', data={
        'game_title': 'Test Game',
        'rating': '9',
        'description': 'Awesome game, awesome test, awesome life.',
        'hours_played': '5',
        'recommends': 'true'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Your review has been posted' in response.data

    # Delete newly made post
    mongo = client.application.mongo
    mongo.db.post.delete_one({"game": "Test Game", "user_id": test_user_id})

def test_react_to_post(client, test_user_id):
    with client.session_transaction() as sess:
        sess['user_id'] = str(test_user_id)

    # Existing post id
    post_id = "68105b3a4404847de9b361cf"

    # Like the post
    response = client.post('/react', data={
        'post_id': post_id,
        'reaction_type': 'like'
    })
    
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data['success'] is True

    # Unlike it
    response = client.post('/react', data={
        'post_id': post_id,
        'reaction_type': 'like'
    })
    
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data['success'] is True

def test_full_happiness(client, test_happiness_user_id):
    with client.session_transaction() as sess:
        sess['user_id'] = str(test_happiness_user_id)

    mongo = client.application.mongo
    mongo.db.user.update_one(
        {"_id": test_happiness_user_id},
        {"$set": {"last_post_time": datetime.datetime.now(datetime.timezone.utc)}}
    )

    response = client.get('/home')

    soup = BeautifulSoup(response.data, 'html.parser')
    happiness = int(soup.find('span', {'id': 'happiness'}).text.strip())
    assert happiness == 100
    
def test_half_happiness(client, test_happiness_user_id):
    with client.session_transaction() as sess:
        sess['user_id'] = str(test_happiness_user_id)

    mongo = client.application.mongo
    mongo.db.user.update_one(
        {"_id": test_happiness_user_id},
        {"$set": {"last_post_time": datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=3)}}
    )

    response = client.get('/home')
    soup = BeautifulSoup(response.data, 'html.parser')
    happiness = int(soup.find('span', {'id': 'happiness'}).text.strip())

    # Expected happiness: hours_since = 3 * 24 = 72, happiness = 1 - (72 / 120) = 0.4
    # 0.4 * 100 = 40
    assert happiness == 40

def test_no_happiness(client, test_happiness_user_id):
    with client.session_transaction() as sess:
        sess['user_id'] = str(test_happiness_user_id)

    mongo = client.application.mongo
    mongo.db.user.update_one(
        {"_id": test_happiness_user_id},
        {"$set": {"last_post_time": datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=7)}}
    )

    response = client.get('/home')
    soup = BeautifulSoup(response.data, 'html.parser')
    happiness = int(soup.find('span', {'id': 'happiness'}).text.strip())

    # Expected happiness: hours_since = 7 * 24 = 168, happiness = 1 - (168 / 120) < 0
    # 0
    assert happiness == 0