import pytest
from fastapi.testclient import TestClient
from fastapi import status
from main import app
import os
import requests

client = TestClient(app)

# URL веб-формы для отправки файла
UPLOAD_URL = "http://example.com/upload"  # Замените на реальный URL

# Путь к тестовому видеофайлу
TEST_VIDEO_PATH = "test_video/test.mp4"  # Убедитесь, что файл существует

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

# def test_upload_video():
#     # Проверка наличия тестового файла
#     assert os.path.exists(TEST_VIDEO_PATH), f"Файл {TEST_VIDEO_PATH} не найден"
#
#     # Открываем файл для отправки
#     with open(TEST_VIDEO_PATH, "rb") as video_file:
#         # Создаем словарь с файлом для отправки
#         files = {"file": (os.path.basename(TEST_VIDEO_PATH), video_file, "video.mp4")}
#
#         # Отправляем POST-запрос с файлом
#         response = requests.post("http://127.0.0.1:8080/fetch_data_local", files=files, allow_redirects=False)
#
#     # Проверка статус-кода ответа (перенаправление)
#     assert response.status_code == 301, f"Ожидался статус-код 303, получен {response.status_code}"
#
#     # Получаем URL для перенаправления
#     redirect_url = response.headers["Location"]
#     print(f"Перенаправление на: {redirect_url}")
#
#     # Переходим по URL перенаправления
#     redirect_response = requests.get(redirect_url)
#     assert redirect_response.status_code == 200, f"Ожидался статус-код 200, получен {redirect_response.status_code}"
#
#     print(f"Файл успешно загружен")
