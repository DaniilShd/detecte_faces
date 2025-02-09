import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture(scope="function", autouse=True)
def test_index_redirect():
    response = client.get("/")
    assert response.status_code in [200, 302]
    print(response.url)
    assert "/login" in response.url