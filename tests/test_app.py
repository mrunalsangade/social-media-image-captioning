import os
import io
import pytest
from app import app

# Define a pytest fixture to create a test client
@pytest.fixture
def client():
    app.config['TESTING'] = True  # Enable testing mode
    return app.test_client()

def test_home_get(client):
    """
    Test the home route with a GET request.
    Verifies that the home page loads and contains the expected HTML form.
    """
    response = client.get('/')
    assert response.status_code == 200
    # Check if the response contains a form tag (assuming your index.html includes one)
    assert b"<form" in response.data

def test_home_post(client, monkeypatch):
    """
    Test the home route with a POST request.
    Uses monkeypatch to override the captioning function so it returns a test caption.
    Also verifies that the file is saved to the static folder and the correct caption is rendered.
    """

    # Override the caption_this_image function in Caption_it.py to return a fixed caption.
    monkeypatch.setattr("Caption_it.caption_this_image", lambda path: "Test Caption")

    # Create a dummy file to simulate an image upload
    dummy_image_data = b"fake image data"
    data = {
        'userfile': (io.BytesIO(dummy_image_data), 'test_image.jpg')
    }

    # Send POST request with multipart/form-data content type
    response = client.post('/', data=data, content_type='multipart/form-data')
    assert response.status_code == 200

    # Verify that the dummy caption ("Test Caption") is rendered in the response
    assert b"Test Caption" in response.data

    # Verify that the file was saved in the static folder
    file_path = os.path.join("static", "test_image.jpg")
    assert os.path.isfile(file_path)

    # Cleanup: Remove the test file from the static folder after testing
    os.remove(file_path)
