import re

from pydantic import BaseModel, Field, model_validator
from fastapi import FastAPI, Request, UploadFile, File, Form
from logger.my_logger import logger



class VideoModel(BaseModel):
    file: UploadFile = File(...)
    # name: str = Form(...)
    check_filename: bool = Form(...)


    # def __init__(
    #     self,
    #     file: UploadFile,
    #     name: str = Form(),
    #     check_filename = False
    # ):
    #     super().__init__(name=name, file=file, check_filename=check_filename)

    # @model_validator(mode="after")
    # def validate(self):
    #     if self.check_filename:
    #         pattern = re.compile('.*\.mp4')
    #         if not pattern.search(self.file.filename):
    #             raise ValueError('Необходимо загрузить файл в формате mp4')
    #         return self






# class VideoModel(BaseModel):
#     name: str = Field(..., max_length=50, description='Имя загружаемого видео')
#     # file: UploadFile = File(...)
#
#     @field_validator('name')
#     def file_must_be_mp4(cls, values):
#         filename = values.get('name')
#         logger.info(f"name file - {filename}")
#         # Проверка файла на формат mp4
#         match = re.fullmatch(".mp4", filename)
#         if not match:
#             raise ValueError('Прошу загрузить файл в формате mp4')
#         return values
#
#
# class PdfModel(models.Model):
#     pdf = models.FileField(upload_to=customer_directory_path, null=True, blank=True)
#
#     def clean(self):
#         pattern = re.compile('.*\.xlsm$')
#
#         if not pattern.search(self.pdf):
#             raise ValidationError(_('Only .xlsm files are accepted'))





# Класс пользователя
# class User(BaseModel):
#     name: str
#     age: int
#     email: str
#     department: str
#
#     # Кастомная валидация для поля age
#     @field_validator('age')
#     def validate_age(cls, v):
#         if isinstance(v, str):
#             # Если это строка, пытаемся преобразовать ее в целое число
#             try:
#                 v = int(v)
#             except ValueError:
#                 raise ValueError('age must be a valid integer')
#         # Проверка для пустой строки
#         if v == "":
#             raise ValueError('age cannot be an empty string')
#         return v
#
#     class Config:
#         strict = True  # Включение строгой валидации типов
