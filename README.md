# Проект по созданию веб приложения по детектированию лиц на видео
Веб приложение имеет старничку авторизации, форму для загрузки видео 
и таблицу с результатами (с сылками для скачивания видео с задетектированный лицами)

# Запуск веб приложения
Шаг 1: Клонирование репозитория

```sh
git init
git clone https://github.com/DaniilShd/detecte_faces
```
Шаг 2: Установка зависимостей

Создайте и активируйте виртуальное окружение:
```sh
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

Установите зависимости:

```sh
pip install -r requirements.txt
```

Шаг 3: Запуск приложения

```sh
cd app
python main.py
```

