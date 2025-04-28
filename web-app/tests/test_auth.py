# Testing authentication/login
def test_redirect_index(client):
    response = client.get('/')
    assert response.status_code == 302
    assert '/login' in response.headers['Location']

def test_login_fail(client):
    response = client.post(
        '/login',
        data={'username': 'wrong', 'password': 'wrong'},
        follow_redirects=True
    )
    assert b'Invalid username' in response.data or b'Invalid' in response.data
