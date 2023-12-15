import sys
import os

import pytest

# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now you should be able to import the app module
from app import app
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_app_creation(client):
    response = client.get('/')
    assert response.status_code == 404