# Проект по созданию веб приложения по детектированию лиц на видео
Веб приложение имеет старничку авторизации, форму для загрузки видео 
и таблицу с результатами (с сылками для скачивания видео с задетектированный лицами)

# Запуск телеграм бота
Шаг 1: Клонирование репозитория

```sh
git init
git clone https://github.com/DaniilShd/hakaton_bot
```
Шаг 2: Установка зависимостей

Создайте и активируйте виртуальное окружение:
```sh
cd hakaton_bot
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

