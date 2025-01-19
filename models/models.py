import re

from pydantic import BaseModel, Field, field_validator


class VideoModel(BaseModel):
    name: str = Field(..., max_length=50, description='Имя загружаемого видео')

    @field_validator
    def file_must_be_mp4(cls, values):
        filename = values.get('name')
        # Проверка файла на формат mp4
        match = re.fullmatch(".mp4", filename)
        if not match:
            raise ValueError('Прошу ввести файл в формате mp4')
        return values
