import pytest
from main import app
from fastapi import  status
from fastapi.testclient import TestClient

client = TestClient(app)


@pytest.fixture(scope="module")
def test_client():
    return TestClient(app)

# Тест для проверки перенаправления
def test_index_redirect(test_client):
    # Выполняем GET-запрос к корневому URL
    response = test_client.get("/", follow_redirects=False)

    # Проверяем статус-код (200 или 302)
    assert response.status_code in [200, 302], f"Ожидался статус-код 200 или 302, получен {response.status_code}"

    # Если это перенаправление (302), проверяем URL
    if response.status_code == 302:
        assert "location" in response.headers, "Заголовок Location отсутствует в ответе"
        assert "/login" in response.headers["location"], f"Ожидался URL с /login, получен {response.headers['location']}"
        print(f"Перенаправление на: {response.headers['location']}")
    else:
        print("Перенаправление не требуется, страница доступна напрямую")


# Тест для успешной авторизации
def test_login_success():
    # Данные для авторизации
    form_data = {
        "username": "Daniil",
        "password": "1234"
    }

    # Отправляем POST-запрос на /login
    response = client.post("/login", data=form_data, allow_redirects=False)

    # Проверяем статус-код (перенаправление)
    assert response.status_code == status.HTTP_301_MOVED_PERMANENTLY, f"Ожидался статус-код 301, получен {response.status_code}"

    # Проверяем заголовок Location для перенаправления
    assert response.headers[
               "location"] == "/show_data", f"Ожидалось перенаправление на /show_data, получено {response.headers['location']}"

    print("Успешная авторизация:")

# Тест для неудачной авторизации
def test_login_failure():
    # Неверные данные для авторизации
    form_data = {
        "username": "admin",
        "password": "wrongpassword"
    }

    # Отправляем POST-запрос на /login
    response = client.post("/login", data=form_data, allow_redirects=False)

    # Проверяем статус-код
    assert response.status_code == 401, f"Ожидался статус-код 401, получен {response.status_code}"

    print("Неудачная авторизация:")

