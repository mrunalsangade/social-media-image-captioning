# test_app.py
import os
import tempfile
import pytest
from app import app

@pytest.fixture
def client():
    # Create a test client using Flask's test_client
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

def test_home_get(client):
    """Test the home page returns a 200 status code on a GET request."""
    response = client.get('/')
    assert response.status_code == 200

def test_home_post(client):
    """Test the home page with a dummy file upload."""
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp:
        temp.write(b'\xff\xd8\xff\xe0' + b'\x00' * 1024)  # Minimal JPEG
        temp_filename = temp.name

    with open(temp_filename, 'rb') as img:
        data = {'userfile': (img, 'test.jpg')}
        response = client.post('/', data=data, content_type='multipart/form-data')

    os.remove(temp_filename)
    assert response.status_code == 200
