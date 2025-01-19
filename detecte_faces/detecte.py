import cv2 as cv
import matplotlib.pyplot as plt

# Класс по детектированию лиц на изображении
class CascadeHaara():
    def __init__(self, path_classifier):
        # Загрузка классификатора и создание каскадного объекта для распознавания лиц (указан путь к модели в папке)
        self.face_cascade = cv.CascadeClassifier(path_classifier)
        self.__image = None

    def load_image(self, path_image):
        # Чтение изображения
        image = cv.imread(path_image)
        # Конвертация изображения в градации серого
        self.__image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        grayscale_image = cv.cvtColor(self.__image, cv.COLOR_RGB2GRAY)

        # Детектирование лиц на изображении с помощью предобученной модели
        detected_faces = self.face_cascade.detectMultiScale(grayscale_image)

        # Добавление зеленых квадратов по контуру задетектированных лиц
        for (column, row, width, height) in detected_faces:
            cv.rectangle(
                self.__image,
                (column, row),
                (column + width, row + height),
                (0, 255, 0),
                2
            )

    def return_result(self):
        plt.figure(figsize=(10, 10))
        plt.title(f"Количество задетектированных лиц")
        plt.imshow(self.__image)
        plt.show()
        return self.__image

