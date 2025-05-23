def test_feed_redirects_when_not_logged_in(client):
    response = client.get('/feed')
    assert response.status_code == 302
    assert '/login' in response.headers['Location']

def test_feed_access_when_logged_in(client, test_user_id):
    with client.session_transaction() as sess:
        sess['user_id'] = str(test_user_id)

    response = client.get('/feed')
    assert response.status_code == 200
    assert b'Posts' in response.data or b'Game Reviews Feed' in response.data
