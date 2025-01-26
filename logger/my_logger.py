from loguru import logger


# Запись логов в файл с ротацией (создание новых файлов при достижении определенного размера)
logger.add("../tmp/app.log", rotation="500 KB")

